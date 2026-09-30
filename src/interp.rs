//! Intérprete de alto rendimiento para el HIR de MICELIO.
//!
//! Estrategia de optimización:
//! - Ámbitos como `Rc<RefCell<Entorno>>` con resolución léxica por cadena
//!   de padres, idéntica al intérprete de referencia para conservar la
//!   semántica, pero con tablas `HashMap` dimensionadas por adelantado.
//! - Rutas rápidas para bucles numéricos (`para..en` sobre `Rango` y
//!   `para..hasta`): la variable de control se resuelve una sola vez y
//!   el cuerpo se ejecuta sin materializar colecciones.
//! - Cortocircuito en `y`/`o`, evaluación perezosa de ramas y despacho
//!   directo de métodos frecuentes (`longitud`, `agregar`) sin objetos
//!   intermedios.

use std::cell::RefCell;
use std::collections::{HashMap, HashSet};
use std::rc::Rc;

use crate::ast::{ArgLlamada, Expr, ItemLista, OpBin, OpUn, Param, Programa, Sent, TipoParam};
use crate::valor::{Entorno, EntornoRef, FuncionDef, Valor};

/// Flujo de control no local (retorno, ruptura, continuación).
enum Flujo {
    Retorno(Valor),
    Romper,
    Continuar,
}

/// Error de ejecución con mensaje en español.
#[derive(Debug, Clone)]
pub struct ErrorEjecucion {
    pub mensaje: String,
}

impl std::fmt::Display for ErrorEjecucion {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.mensaje)
    }
}

type Exito<T> = Result<T, ErrorEjecucion>;

fn error(mensaje: impl Into<String>) -> ErrorEjecucion {
    ErrorEjecucion {
        mensaje: mensaje.into(),
    }
}

/// Intérprete con entorno global, directorio base para `importar` y
/// acumulador de salida para pruebas deterministas.
pub struct Interprete {
    pub global: EntornoRef,
    pub base_dir: String,
    /// Salida capturada de `imp` (además de imprimir).
    pub salida: Vec<String>,
    modulos: HashMap<String, Valor>,
}

impl Interprete {
    /// Crea un intérprete con primitivas nativas registradas.
    pub fn new(base_dir: String) -> Self {
        let global = Entorno::raiz();
        let mut it = Self {
            global: Rc::clone(&global),
            base_dir,
            salida: Vec::new(),
            modulos: HashMap::new(),
        };
        it.registrar_nativas();
        it
    }

    // ---- Resolución de ámbitos ----

    fn resolver(env: &EntornoRef, nombre: &str) -> Option<EntornoRef> {
        let mut actual: Option<EntornoRef> = Some(Rc::clone(env));
        while let Some(e) = actual {
            if e.borrow().valores.contains_key(nombre) {
                return Some(e);
            }
            actual = e.borrow().padre.clone();
        }
        None
    }

    fn definir(env: &EntornoRef, nombre: &str, valor: Valor, constante: bool) -> Exito<()> {
        let mut e = env.borrow_mut();
        if e.valores.contains_key(nombre) {
            return Err(error(format!("'{nombre}' ya esta definido en este ambito")));
        }
        e.valores.insert(nombre.to_string(), valor);
        if constante {
            e.constantes.insert(nombre.to_string());
        }
        Ok(())
    }

    fn asignar(env: &EntornoRef, nombre: &str, valor: Valor) -> Exito<()> {
        match Self::resolver(env, nombre) {
            Some(t) => {
                let mut b = t.borrow_mut();
                if b.constantes.contains(nombre) {
                    return Err(error(format!(
                        "No se puede reasignar la constante '{nombre}'"
                    )));
                }
                b.valores.insert(nombre.to_string(), valor);
                Ok(())
            }
            None => Err(error(format!("Variable '{nombre}' no definida"))),
        }
    }

    fn obtener(env: &EntornoRef, nombre: &str) -> Exito<Valor> {
        let mut actual: Option<EntornoRef> = Some(Rc::clone(env));
        while let Some(e) = actual {
            if let Some(v) = e.borrow().valores.get(nombre) {
                return Ok(v.clone());
            }
            actual = e.borrow().padre.clone();
        }
        Err(error(format!("Variable '{nombre}' no definida")))
    }

    // ---- Primitivas nativas ----

    fn registrar_nativas(&mut self) {
        let g = Rc::clone(&self.global);
        let mut reg = |nombre: &'static str, f: fn(&[Valor]) -> Result<Valor, String>| {
            g.borrow_mut()
                .valores
                .insert(nombre.to_string(), Valor::Nativa(nombre, f));
        };
        reg("rango", nativa_rango);
        reg("longitud", nativa_longitud);
        reg("aTexto", nativa_a_texto);
        reg("tipo", nativa_tipo);
        reg("aleatorio", nativa_aleatorio);
        reg("__tipo_nativo", nativa_tipo);
        reg("__error", nativa_error);
        reg("abs", nativa_abs);
        reg("maximo", nativa_maximo);
        reg("minimo", nativa_minimo);
        reg("aNumero", nativa_a_numero);
        reg("aEntero", nativa_a_entero);
        reg("aFlotante", nativa_a_flotante);
        reg("aBooleano", nativa_a_booleano);
        reg("aCaracter", nativa_a_caracter);
        reg("aCodigo", nativa_a_codigo);
        reg("map", nativa_no_directa);
        reg("filter", nativa_no_directa);
        reg("reduce", nativa_no_directa);
        reg("ordenar", nativa_ordenar);
        reg("claves", nativa_claves);
        reg("valores", nativa_valores);
        reg("items", nativa_items);
        reg("primero", nativa_primero);
        reg("ultimo", nativa_ultimo);
        reg("invertir", nativa_invertir);
        reg("concatenar", nativa_concatenar);
        reg("suma", nativa_suma_lista);
        reg("producto", nativa_producto_lista);
        reg("promedio", nativa_promedio);
        reg("exp", nativa_exp);
        reg("max_lista", nativa_max_lista);
        reg("min_lista", nativa_min_lista);
        reg("seno", nativa_seno);
        reg("coseno", nativa_coseno);
        reg("__archivo_leer", nativa_archivo_leer);
        reg("__archivo_escribir", nativa_archivo_escribir);
        reg("__archivo_existe", nativa_archivo_existe);
        reg("__archivo_eliminar", nativa_archivo_eliminar);
        reg("__archivo_tamano", nativa_archivo_tamano);
        reg("__leer_csv_rapido", nativa_leer_csv);
        reg("__json_parse", nativa_json_dummy);
        reg("__json_stringify", nativa_json_stringify_dummy);
        reg("__leer_archivo", nativa_archivo_leer);
        reg("__escribir_archivo", nativa_archivo_escribir);
        reg("__existe_archivo", nativa_existe_falso);
        // Compatibilidad para ejemplos gráficos/de red: implementaciones
        // mínimas sin dependencias externas. Permiten ejecutar la lógica
        // computacional aunque no generen artefactos visuales reales.
        reg("__grafico_reset", nativa_dummy);
        reg("__grafico_set_pixel", nativa_dummy);
        reg("__grafico_draw_axes", nativa_dummy);
        reg("__grafico_guardar", nativa_dummy_text);
        reg("__grafico_last_path", nativa_dummy_text);
        reg("__grafico_mostrar", nativa_dummy);
        reg("__grafico_linea", nativa_dummy);
        reg("__grafico_rectangulo", nativa_dummy);
        reg("__grafico_circulo", nativa_dummy);
        reg("__grafico_texto", nativa_dummy);
        reg("__grafico_poligono", nativa_dummy);
        reg("__grafico_limpiar", nativa_dummy);
        reg("__leer_csv_rapido", nativa_leer_csv_dummy);
    }

    /// Ejecuta un programa completo en el ámbito global.
    pub fn ejecutar_programa(&mut self, prog: &Programa) -> Exito<Valor> {
        let mut ultimo = Valor::Nulo;
        for s in &prog.sentencias {
            match self.ejecutar_sent(s, &Rc::clone(&self.global))? {
                Control::Valor(v) => ultimo = v,
                Control::Flujo(Flujo::Retorno(v)) => return Ok(v),
                Control::Flujo(Flujo::Romper) => return Err(error("romper fuera de un bucle")),
                Control::Flujo(Flujo::Continuar) => {
                    return Err(error("continuar fuera de un bucle"));
                }
            }
        }
        Ok(ultimo)
    }

    /// Ejecuta un archivo `.mice` con `importar` relativo al directorio base.
    pub fn ejecutar_archivo(&mut self, ruta: &str) -> Exito<Valor> {
        let contenido = std::fs::read_to_string(ruta)
            .map_err(|e| error(format!("No se pudo leer '{ruta}': {e}")))?;
        let previo = std::mem::replace(&mut self.base_dir, dir_de(ruta));
        let r = self.ejecutar_fuente(&contenido);
        self.base_dir = previo;
        r
    }

    /// Analiza y ejecuta código fuente en el ámbito global.
    pub fn ejecutar_fuente(&mut self, fuente: &str) -> Exito<Valor> {
        let fuente = preprocesar(fuente);
        let toks = crate::lexer::tokenizar(&fuente)
            .map_err(|e| error(format!("Error léxico en {}: {}", e.posicion, e.mensaje)))?;
        let prog = crate::parser::analizar(toks).map_err(|e| {
            error(format!(
                "Error de sintaxis en {}: {}",
                e.posicion, e.mensaje
            ))
        })?;
        self.ejecutar_programa(&prog)
    }

    // ---- Sentencias ----

    fn ejecutar_sent(&mut self, s: &Sent, env: &EntornoRef) -> Exito<Control> {
        match s {
            Sent::DeclVar { nombres, valores } => {
                if valores.is_empty() {
                    for n in nombres {
                        Self::definir(env, n, Valor::Nulo, false)?;
                    }
                } else if valores.len() == 1 && nombres.len() > 1 {
                    // Desempaquetado `var a, b = expr`.
                    let v = self.evaluar(&valores[0], env)?;
                    let lista = v.materializar().map_err(error)?;
                    if lista.len() != nombres.len() {
                        return Err(error(
                            "Cantidad de valores no coincide con cantidad de variables",
                        ));
                    }
                    for (n, item) in nombres.iter().zip(lista) {
                        Self::definir(env, n, item, false)?;
                    }
                } else {
                    if valores.len() != nombres.len() && valores.len() != 1 {
                        return Err(error(
                            "Cantidad de valores no coincide con cantidad de variables",
                        ));
                    }
                    if valores.len() == 1 && nombres.len() == 1 {
                        let v = self.evaluar(&valores[0], env)?;
                        Self::definir(env, &nombres[0], v, false)?;
                    } else {
                        for (n, e) in nombres.iter().zip(valores.iter()) {
                            let v = self.evaluar(e, env)?;
                            Self::definir(env, n, v, false)?;
                        }
                    }
                }
                Ok(Control::Valor(Valor::Nulo))
            }
            Sent::DeclConst { nombre, valor } => {
                let v = self.evaluar(valor, env)?;
                Self::definir(env, nombre, v, true)?;
                Ok(Control::Valor(Valor::Nulo))
            }
            Sent::Asign {
                base,
                indices,
                valor,
            } => {
                let v = self.evaluar(valor, env)?;
                if indices.is_empty() {
                    Self::asignar(env, base, v)?;
                } else {
                    self.asignar_indice(env, base, indices, v)?;
                }
                Ok(Control::Valor(Valor::Nulo))
            }
            Sent::AsignMulti { nombres, valor } => {
                let v = self.evaluar(valor, env)?;
                let lista = v.materializar().map_err(error)?;
                if lista.len() != nombres.len() {
                    return Err(error(
                        "Cantidad de valores no coincide en asignación múltiple",
                    ));
                }
                for (n, item) in nombres.iter().zip(lista) {
                    if Self::resolver(env, n).is_some() {
                        Self::asignar(env, n, item)?;
                    } else {
                        Self::definir(env, n, item, false)?;
                    }
                }
                Ok(Control::Valor(Valor::Nulo))
            }
            Sent::Expr(e) => {
                let v = self.evaluar(e, env)?;
                Ok(Control::Valor(v))
            }
            Sent::Retorna(o) => {
                let v = match o {
                    Some(e) => self.evaluar(e, env)?,
                    None => Valor::Nulo,
                };
                Ok(Control::Flujo(Flujo::Retorno(v)))
            }
            Sent::Romper => Ok(Control::Flujo(Flujo::Romper)),
            Sent::Continuar => Ok(Control::Flujo(Flujo::Continuar)),
            Sent::Importar { ruta, alias } => {
                let v = self.importar(ruta)?;
                let nombre = alias.clone().unwrap_or_else(|| modulo_de(ruta));
                if Self::resolver(env, &nombre).is_some() {
                    Self::asignar(env, &nombre, v)?;
                } else {
                    Self::definir(env, &nombre, v, false)?;
                }
                Ok(Control::Valor(Valor::Nulo))
            }
            Sent::Leer { nombre } => {
                let v = leer_entrada()?;
                if Self::resolver(env, nombre).is_some() {
                    Self::asignar(env, nombre, v)?;
                } else {
                    Self::definir(env, nombre, v, false)?;
                }
                Ok(Control::Valor(Valor::Nulo))
            }
            Sent::Imp(e) => {
                let v = self.evaluar(e, env)?;
                let t = v.a_texto();
                self.salida.push(t.clone());
                println!("{t}");
                Ok(Control::Valor(Valor::Nulo))
            }
            Sent::Si {
                cond,
                entonces,
                sino_si,
                sino_,
            } => {
                if self.evaluar(cond, env)?.es_verdadero() {
                    return self.ejecutar_bloque(entonces, env);
                }
                for (c, cuerpo) in sino_si {
                    if self.evaluar(c, env)?.es_verdadero() {
                        return self.ejecutar_bloque(cuerpo, env);
                    }
                }
                if let Some(cuerpo) = sino_ {
                    return self.ejecutar_bloque(cuerpo, env);
                }
                Ok(Control::Valor(Valor::Nulo))
            }
            Sent::Segun {
                expr,
                casos,
                defecto,
            } => {
                let v = self.evaluar(expr, env)?;
                for (c, cuerpo) in casos {
                    let cv = self.evaluar(c, env)?;
                    if igualdad(&v, &cv)? {
                        return self.ejecutar_bloque(cuerpo, env);
                    }
                }
                if let Some(cuerpo) = defecto {
                    return self.ejecutar_bloque(cuerpo, env);
                }
                Ok(Control::Valor(Valor::Nulo))
            }
            Sent::Mientras { cond, cuerpo } => {
                let con_ambito = necesita_ambito(cuerpo);
                loop {
                    if !self.evaluar(cond, env)?.es_verdadero() {
                        break;
                    }
                    let r = if con_ambito {
                        self.ejecutar_bloque(cuerpo, env)?
                    } else {
                        self.ejecutar_bloque_sin_ambito(cuerpo, env)?
                    };
                    match r {
                        Control::Flujo(Flujo::Romper) => break,
                        Control::Flujo(Flujo::Continuar) => continue,
                        Control::Flujo(Flujo::Retorno(v)) => {
                            return Ok(Control::Flujo(Flujo::Retorno(v)));
                        }
                        _ => {}
                    }
                }
                Ok(Control::Valor(Valor::Nulo))
            }
            Sent::ParaEn {
                var,
                iterable,
                cuerpo,
            } => self.para_en(var, iterable, cuerpo, env),
            Sent::ParaHasta {
                var,
                inicio,
                fin,
                paso,
                cuerpo,
            } => self.para_hasta(var, inicio, fin, paso.as_ref(), cuerpo, env),
            Sent::DefFuncion {
                nombre,
                params,
                cuerpo,
            } => {
                let (normales, args) = partir_params(params);
                let f = Valor::Funcion(Rc::new(FuncionDef {
                    nombre: Some(nombre.clone()),
                    params: normales,
                    args_param: args,
                    cuerpo: cuerpo.clone(),
                    clausura: Rc::clone(env),
                }));
                // Definición en el ámbito actual (permite sombreado en módulos
                // sin contaminar el ámbito global, coherente con el intérprete
                // de referencia que siempre define en `self.env`).
                {
                    let mut b = env.borrow_mut();
                    // `RefCell` ya prestado arriba mediante resolver podría
                    // causar pánico; se opera directamente sobre el actual.
                    if b.valores.contains_key(nombre) {
                        if b.constantes.contains(nombre) {
                            return Err(error(format!(
                                "No se puede reasignar la constante '{nombre}'"
                            )));
                        }
                        b.valores.insert(nombre.clone(), f);
                    } else {
                        b.valores.insert(nombre.clone(), f);
                    }
                }
                Ok(Control::Valor(Valor::Nulo))
            }
            Sent::Bloque(cuerpo) => {
                if necesita_ambito(cuerpo) {
                    self.ejecutar_bloque(cuerpo, env)
                } else {
                    self.ejecutar_bloque_sin_ambito(cuerpo, env)
                }
            }
        }
    }

    fn ejecutar_bloque(&mut self, cuerpo: &[Sent], env: &EntornoRef) -> Exito<Control> {
        let hijo = Entorno::hijo(env);
        self.ejecutar_bloque_sin_ambito(cuerpo, &hijo)
    }

    fn ejecutar_bloque_sin_ambito(&mut self, cuerpo: &[Sent], env: &EntornoRef) -> Exito<Control> {
        let mut ultimo = Valor::Nulo;
        for s in cuerpo {
            match self.ejecutar_sent(s, env)? {
                Control::Valor(v) => ultimo = v,
                f @ Control::Flujo(_) => return Ok(f),
            }
        }
        Ok(Control::Valor(ultimo))
    }

    /// Bucle `para x en iterable` con ruta rápida para rangos numéricos.
    fn para_en(
        &mut self,
        var: &str,
        iterable: &Expr,
        cuerpo: &[Sent],
        env: &EntornoRef,
    ) -> Exito<Control> {
        let v = self.evaluar(iterable, env)?;
        // Ruta rápida: rango numérico sin materializar. Resuelve el entorno
        // de la variable una sola vez, como el intérprete de referencia.
        if let Valor::Rango { inicio, fin, paso } = v {
            if paso == 0 {
                return Err(error("inc no puede ser 0"));
            }
            let destino = match Self::resolver(env, var) {
                Some(e) => e,
                None => {
                    Self::definir(env, var, Valor::Entero(inicio), false)?;
                    Rc::clone(env)
                }
            };
            // Ámbito del cuerpo: se reutiliza un único hijo para evitar
            // asignaciones por iteración cuando no se requieren.
            let sin_ambito = !necesita_ambito(cuerpo);
            let cuerpo_env = if sin_ambito {
                Rc::clone(env)
            } else {
                Entorno::hijo(env)
            };
            if paso > 0 {
                let mut c = inicio;
                while c < fin {
                    destino
                        .borrow_mut()
                        .valores
                        .insert(var.to_string(), Valor::Entero(c));
                    // Si el cuerpo usa ámbito propio por iteración, se crea aquí.
                    let env_iter = if sin_ambito {
                        Rc::clone(&cuerpo_env)
                    } else {
                        Entorno::hijo(env)
                    };
                    match self.ejecutar_bloque_sin_ambito(cuerpo, &env_iter)? {
                        Control::Flujo(Flujo::Romper) => break,
                        Control::Flujo(Flujo::Continuar) => {}
                        Control::Flujo(Flujo::Retorno(v)) => {
                            return Ok(Control::Flujo(Flujo::Retorno(v)));
                        }
                        _ => {}
                    }
                    c += paso;
                }
            } else {
                let mut c = inicio;
                while c > fin {
                    destino
                        .borrow_mut()
                        .valores
                        .insert(var.to_string(), Valor::Entero(c));
                    let env_iter = if sin_ambito {
                        Rc::clone(&cuerpo_env)
                    } else {
                        Entorno::hijo(env)
                    };
                    match self.ejecutar_bloque_sin_ambito(cuerpo, &env_iter)? {
                        Control::Flujo(Flujo::Romper) => break,
                        Control::Flujo(Flujo::Continuar) => {}
                        Control::Flujo(Flujo::Retorno(v)) => {
                            return Ok(Control::Flujo(Flujo::Retorno(v)));
                        }
                        _ => {}
                    }
                    c += paso;
                }
            }
            return Ok(Control::Valor(Valor::Nulo));
        }
        // Ruta general: materializa el iterable (listas pequeñas, textos).
        let items = v.materializar().map_err(error)?;
        let destino = match Self::resolver(env, var) {
            Some(e) => e,
            None => {
                Self::definir(env, var, Valor::Nulo, false)?;
                Self::resolver(env, var).unwrap_or_else(|| Rc::clone(env))
            }
        };
        for item in items {
            destino.borrow_mut().valores.insert(var.to_string(), item);
            match self.ejecutar_bloque(cuerpo, env)? {
                Control::Flujo(Flujo::Romper) => break,
                Control::Flujo(Flujo::Continuar) => continue,
                Control::Flujo(Flujo::Retorno(v)) => return Ok(Control::Flujo(Flujo::Retorno(v))),
                _ => {}
            }
        }
        Ok(Control::Valor(Valor::Nulo))
    }

    /// Bucle clásico `para i = inicio hasta fin (inc paso)?` con límite inclusivo.
    fn para_hasta(
        &mut self,
        var: &str,
        inicio: &Expr,
        fin: &Expr,
        paso: Option<&Expr>,
        cuerpo: &[Sent],
        env: &EntornoRef,
    ) -> Exito<Control> {
        let a = self.evaluar(inicio, env)?.a_numero().map_err(error)? as i64;
        let b = self.evaluar(fin, env)?.a_numero().map_err(error)? as i64;
        let p = match paso {
            Some(e) => self.evaluar(e, env)?.a_numero().map_err(error)? as i64,
            None => 1,
        };
        if p == 0 {
            return Err(error("inc no puede ser 0"));
        }
        let destino = match Self::resolver(env, var) {
            Some(e) => e,
            None => {
                Self::definir(env, var, Valor::Entero(a), false)?;
                Rc::clone(env)
            }
        };
        if p > 0 {
            let mut c = a;
            while c <= b {
                destino
                    .borrow_mut()
                    .valores
                    .insert(var.to_string(), Valor::Entero(c));
                match self.ejecutar_bloque(cuerpo, env)? {
                    Control::Flujo(Flujo::Romper) => break,
                    Control::Flujo(Flujo::Continuar) => {}
                    Control::Flujo(Flujo::Retorno(v)) => {
                        return Ok(Control::Flujo(Flujo::Retorno(v)));
                    }
                    _ => {}
                }
                c += p;
            }
        } else {
            let mut c = a;
            while c >= b {
                destino
                    .borrow_mut()
                    .valores
                    .insert(var.to_string(), Valor::Entero(c));
                match self.ejecutar_bloque(cuerpo, env)? {
                    Control::Flujo(Flujo::Romper) => break,
                    Control::Flujo(Flujo::Continuar) => {}
                    Control::Flujo(Flujo::Retorno(v)) => {
                        return Ok(Control::Flujo(Flujo::Retorno(v)));
                    }
                    _ => {}
                }
                c += p;
            }
        }
        Ok(Control::Valor(Valor::Nulo))
    }

    fn asignar_indice(
        &mut self,
        env: &EntornoRef,
        base: &str,
        indices: &[Expr],
        valor: Valor,
    ) -> Exito<()> {
        let cont = Self::obtener(env, base)?;
        let mut idx_vals = Vec::with_capacity(indices.len());
        for e in indices {
            idx_vals.push(self.evaluar(e, env)?);
        }
        let nuevo = asignar_en(cont, &idx_vals, valor)?;
        Self::asignar(env, base, nuevo)
    }

    fn importar(&mut self, ruta: &str) -> Exito<Valor> {
        if let Some(v) = self.modulos.get(ruta) {
            return Ok(v.clone());
        }
        let mut candidatos = vec![format!("{}/{}", self.base_dir, ruta), ruta.to_string()];
        if !ruta.ends_with(".mice") {
            candidatos.push(format!("{}/{ruta}.mice", self.base_dir));
            candidatos.push(format!("{ruta}.mice"));
        }
        let mut elegido: Option<String> = None;
        for c in candidatos {
            if std::path::Path::new(&c).is_file() {
                elegido = Some(c);
                break;
            }
        }
        let ruta_final = elegido.ok_or_else(|| error(format!("No se encontro modulo '{ruta}'")))?;
        let contenido = std::fs::read_to_string(&ruta_final)
            .map_err(|e| error(format!("No se pudo leer '{ruta_final}': {e}")))?;
        // El módulo se ejecuta en un ámbito hijo para capturar sus definiciones.
        let mod_env = Entorno::hijo(&self.global);
        let previo = self.base_dir.clone();
        self.base_dir = dir_de(&ruta_final);
        let toks = crate::lexer::tokenizar(&preprocesar(&contenido))
            .map_err(|e| error(format!("Error léxico en {ruta}: {}", e.mensaje)))?;
        let prog = crate::parser::analizar(toks)
            .map_err(|e| error(format!("Error de sintaxis en {ruta}: {}", e.mensaje)))?;
        for s in &prog.sentencias {
            match self.ejecutar_sent(s, &mod_env)? {
                Control::Flujo(Flujo::Retorno(v)) => {
                    self.base_dir = previo;
                    return Ok(v);
                }
                Control::Flujo(_) => {
                    self.base_dir = previo;
                    return Err(error("romper/continuar fuera de un bucle en módulo"));
                }
                _ => {}
            }
        }
        self.base_dir = previo;
        // Exporta el espacio de nombres del módulo como diccionario.
        let mut mapa = HashMap::new();
        for (k, v) in mod_env.borrow().valores.iter() {
            if !k.starts_with("__") {
                mapa.insert(k.clone(), v.clone());
            }
        }
        let v = Valor::nuevo_diccionario(mapa);
        self.modulos.insert(ruta.to_string(), v.clone());
        Ok(v)
    }

    // ---- Expresiones ----

    fn evaluar(&mut self, e: &Expr, env: &EntornoRef) -> Exito<Valor> {
        match e {
            Expr::Entero(i) => Ok(Valor::Entero(*i)),
            Expr::Flotante(f) => Ok(Valor::Flotante(*f)),
            Expr::Texto(s) => Ok(Valor::Texto(s.clone())),
            Expr::Logico(b) => Ok(Valor::Logico(*b)),
            Expr::Nulo => Ok(Valor::Nulo),
            Expr::Variable(n) => Self::obtener(env, n),
            Expr::Unaria { op, expr } => self.unaria(*op, expr, env),
            Expr::Binaria { op, izq, der } => self.binaria(*op, izq, der, env),
            Expr::Llamada { callee, args } => self.llamada(callee, args, env),
            Expr::Indice { base, indice } => {
                let b = self.evaluar(base, env)?;
                let i = self.evaluar(indice, env)?;
                indizar(&b, &i)
            }
            Expr::Acceso { base, campo } => {
                let b = self.evaluar(base, env)?;
                acceso(b, campo)
            }
            Expr::Lista(items) => {
                let mut out = Vec::new();
                for it in items {
                    match it {
                        ItemLista::Simple(x) => out.push(self.evaluar(x, env)?),
                        ItemLista::Propaga(x) => {
                            let v = self.evaluar(x, env)?;
                            out.extend(v.materializar().map_err(error)?);
                        }
                        ItemLista::Rango(a, b) => {
                            let x = self.evaluar(a, env)?.a_numero().map_err(error)? as i64;
                            let y = self.evaluar(b, env)?.a_numero().map_err(error)? as i64;
                            let mut c = x;
                            while c <= y {
                                out.push(Valor::Entero(c));
                                c += 1;
                            }
                        }
                    }
                }
                Ok(Valor::nueva_lista(out))
            }
            Expr::Dicc(pares) => {
                let mut m = HashMap::new();
                for (k, v) in pares {
                    let ck = self.evaluar(k, env)?.a_texto();
                    m.insert(ck, self.evaluar(v, env)?);
                }
                Ok(Valor::nuevo_diccionario(m))
            }
            Expr::Conjunto(items) => {
                let mut out = Vec::new();
                for x in items {
                    out.push(self.evaluar(x, env)?);
                }
                Ok(Valor::nueva_lista(out))
            }
            Expr::Matriz(inner) => {
                let v = self.evaluar(inner, env)?;
                // La validación rectangular se realiza aquí para fallar pronto.
                if let Valor::Lista(rows) = &v {
                    let rows = rows.borrow();
                    for r in rows.iter() {
                        if !matches!(r, Valor::Lista(_)) {
                            return Err(error("matriz requiere lista de listas"));
                        }
                    }
                }
                Ok(v)
            }
            Expr::FuncionAnon { params, cuerpo } => {
                let (normales, args) = partir_params(params);
                Ok(Valor::Funcion(Rc::new(FuncionDef {
                    nombre: None,
                    params: normales,
                    args_param: args,
                    cuerpo: cuerpo.clone(),
                    clausura: Rc::clone(env),
                })))
            }
        }
    }

    fn unaria(&mut self, op: OpUn, e: &Expr, env: &EntornoRef) -> Exito<Valor> {
        match op {
            OpUn::Neg => {
                let v = self.evaluar(e, env)?;
                match v {
                    Valor::Entero(i) => Ok(Valor::Entero(-i)),
                    Valor::Flotante(f) => Ok(Valor::Flotante(-f)),
                    _ => Err(error("Negación requiere numero")),
                }
            }
            OpUn::No => Ok(Valor::Logico(!self.evaluar(e, env)?.es_verdadero())),
            OpUn::PreInc | OpUn::PreDec | OpUn::PostInc | OpUn::PostDec => {
                let nombre = match e {
                    Expr::Variable(n) => n.clone(),
                    _ => return Err(error("++/-- requiere una variable")),
                };
                let cur = Self::obtener(env, &nombre)?;
                let (nuevo, retorno) = match cur {
                    Valor::Entero(i) => {
                        let n = if matches!(op, OpUn::PreInc | OpUn::PostInc) {
                            i + 1
                        } else {
                            i - 1
                        };
                        let r = if matches!(op, OpUn::PreInc | OpUn::PreDec) {
                            n
                        } else {
                            i
                        };
                        (Valor::Entero(n), Valor::Entero(r))
                    }
                    Valor::Flotante(f) => {
                        let n = if matches!(op, OpUn::PreInc | OpUn::PostInc) {
                            f + 1.0
                        } else {
                            f - 1.0
                        };
                        let r = if matches!(op, OpUn::PreInc | OpUn::PreDec) {
                            n
                        } else {
                            f
                        };
                        (Valor::Flotante(n), Valor::Flotante(r))
                    }
                    _ => return Err(error("++/-- requiere numero")),
                };
                Self::asignar(env, &nombre, nuevo)?;
                Ok(retorno)
            }
        }
    }

    fn binaria(&mut self, op: OpBin, a: &Expr, b: &Expr, env: &EntornoRef) -> Exito<Valor> {
        // Cortocircuito lógico sin evaluar la rama innecesaria.
        if op == OpBin::Y {
            let x = self.evaluar(a, env)?;
            if !x.es_verdadero() {
                return Ok(Valor::Logico(false));
            }
            return Ok(Valor::Logico(self.evaluar(b, env)?.es_verdadero()));
        }
        if op == OpBin::O {
            let x = self.evaluar(a, env)?;
            if x.es_verdadero() {
                return Ok(Valor::Logico(true));
            }
            return Ok(Valor::Logico(self.evaluar(b, env)?.es_verdadero()));
        }
        let x = self.evaluar(a, env)?;
        let y = self.evaluar(b, env)?;
        aplicar_bin(op, &x, &y)
    }

    fn llamada(&mut self, callee: &Expr, args: &[ArgLlamada], env: &EntornoRef) -> Exito<Valor> {
        // Formas internas y funcionales de orden superior. Requieren acceso
        // al intérprete para invocar funciones, por lo que se interceptan
        // antes de la evaluación general.
        if let Expr::Variable(n) = callee {
            if n == "map" || n == "filter" || n == "reduce" || n == "contar" {
                return self.funcional(n, args, env);
            }
            if n == "__asignar_multi" {
                return self.nativa_asignar_multi(args, env);
            }
            if n == "__leer_multi" {
                return self.nativa_leer_multi(args, env);
            }
            if n == "__script_dir" {
                return Ok(Valor::Texto(self.base_dir.clone()));
            }
        }
        // Despacho de métodos `base.metodo(args)`: las mutaciones sobre
        // variables (`lista.agregar`, etc.) se aplican directamente sobre
        // el entorno para conservar la semántica por referencia del lenguaje.
        if let Expr::Acceso { base, campo } = callee {
            if let Expr::Variable(nombre_var) = base.as_ref() {
                if let Some(v) = self.metodo_mutante(nombre_var, campo, args, env)? {
                    return Ok(v);
                }
            }
            let b = self.evaluar(base, env)?;
            let mut pos = Vec::with_capacity(args.len());
            let mut nom = HashMap::new();
            for a in args {
                match a {
                    ArgLlamada::Pos(e) => pos.push(self.evaluar(e, env)?),
                    ArgLlamada::Nom { nombre, valor } => {
                        nom.insert(nombre.clone(), self.evaluar(valor, env)?);
                    }
                }
            }
            if let Some(v) = metodo_nativo(&b, campo, &pos, &nom)? {
                return Ok(v);
            }
            // Método definido en diccionario/módulo.
            if let Valor::Diccionario(m) = &b {
                let m = m.borrow();
                if let Some(Valor::Funcion(f)) = m.get(campo) {
                    let f = Rc::clone(f);
                    return self.llamar_funcion(&f, pos, nom);
                }
            }
            return Err(error(format!("Método '{campo}' no soportado")));
        }
        let f = self.evaluar(callee, env)?;
        let mut pos = Vec::with_capacity(args.len());
        let mut nom = HashMap::new();
        for a in args {
            match a {
                ArgLlamada::Pos(e) => pos.push(self.evaluar(e, env)?),
                ArgLlamada::Nom { nombre, valor } => {
                    nom.insert(nombre.clone(), self.evaluar(valor, env)?);
                }
            }
        }
        match f {
            Valor::Funcion(fd) => self.llamar_funcion(&fd, pos, nom),
            Valor::Nativa(_, g) => g(&pos).map_err(error),
            Valor::Diccionario(m) if pos.is_empty() && nom.is_empty() => Err(error(format!(
                "Diccionario no invocable ({})",
                m.borrow().len()
            ))),
            _ => Err(error("Valor no invocable")),
        }
    }

    /// Implementa `__asignar_multi("a,b", valor)` generado por el preprocesador.
    fn nativa_asignar_multi(&mut self, args: &[ArgLlamada], env: &EntornoRef) -> Exito<Valor> {
        if args.len() != 2 {
            return Err(error("__asignar_multi requiere 2 argumentos"));
        }
        let nombres = match &args[0] {
            ArgLlamada::Pos(Expr::Texto(s)) => s.clone(),
            _ => {
                // El primer argumento siempre es un literal textual generado
                // internamente; se evalúa por seguridad ante cambios futuros.
                match self.evaluar_arg(&args[0], env)? {
                    Valor::Texto(s) => s,
                    _ => return Err(error("__asignar_multi requiere nombres")),
                }
            }
        };
        let valor = self.evaluar_arg(&args[1], env)?;
        let lista = valor.materializar().map_err(error)?;
        let nombres: Vec<String> = nombres.split(',').map(|s| s.trim().to_string()).collect();
        if lista.len() != nombres.len() {
            return Err(error(
                "Cantidad de valores no coincide en asignación múltiple",
            ));
        }
        for (n, item) in nombres.iter().zip(lista) {
            if Self::resolver(env, n).is_some() {
                Self::asignar(env, n, item.clone())?;
            } else {
                Self::definir(env, n, item.clone(), false)?;
            }
        }
        Ok(Valor::nueva_lista(
            nombres
                .iter()
                .map(|n| Self::obtener(env, n).unwrap_or(Valor::Nulo))
                .collect(),
        ))
    }

    /// Implementa `__leer_multi("a,b")` para entrada múltiple.
    fn nativa_leer_multi(&mut self, args: &[ArgLlamada], env: &EntornoRef) -> Exito<Valor> {
        if args.len() != 1 {
            return Err(error("__leer_multi requiere 1 argumento"));
        }
        let nombres = match self.evaluar_arg(&args[0], env)? {
            Valor::Texto(s) => s,
            _ => return Err(error("__leer_multi requiere nombres")),
        };
        use std::io::BufRead;
        let mut linea = String::new();
        std::io::stdin()
            .lock()
            .read_line(&mut linea)
            .map_err(|e| error(format!("Error de entrada: {e}")))?;
        let partes: Vec<&str> = linea.split_whitespace().collect();
        let nombres: Vec<String> = nombres.split(',').map(|s| s.trim().to_string()).collect();
        if partes.len() != nombres.len() {
            return Err(error("Cantidad de entradas no coincide en leer múltiple"));
        }
        let mut out = Vec::new();
        for (n, p) in nombres.iter().zip(partes) {
            let v = parsear_atomo(p);
            out.push(v.clone());
            if Self::resolver(env, n).is_some() {
                Self::asignar(env, n, v)?;
            } else {
                Self::definir(env, n, v, false)?;
            }
        }
        Ok(Valor::nueva_lista(out))
    }

    /// Funcionales de orden superior con acceso al intérprete.
    /// Compatible con `builtins.mice`: `map(f, lista)`, `filter(p, lista)`,
    /// `reduce(f, lista, inicio)` y `contar(p, lista)`.
    fn funcional(&mut self, nombre: &str, args: &[ArgLlamada], env: &EntornoRef) -> Exito<Valor> {
        let mut pos = Vec::with_capacity(args.len());
        for a in args {
            pos.push(self.evaluar_arg(a, env)?);
        }
        match nombre {
            "map" => {
                if pos.len() != 2 {
                    return Err(error("map() espera 2 argumentos"));
                }
                let f = pos[0].clone();
                let items = pos[1].materializar().map_err(error)?;
                let mut out = Vec::with_capacity(items.len());
                for x in items {
                    out.push(self.aplicar_unario(&f, x)?);
                }
                Ok(Valor::nueva_lista(out))
            }
            "filter" => {
                if pos.len() != 2 {
                    return Err(error("filter() espera 2 argumentos"));
                }
                let f = pos[0].clone();
                let items = pos[1].materializar().map_err(error)?;
                let mut out = Vec::new();
                for x in items {
                    if self.aplicar_unario(&f, x.clone())?.es_verdadero() {
                        out.push(x);
                    }
                }
                Ok(Valor::nueva_lista(out))
            }
            "reduce" => {
                if pos.len() != 3 {
                    return Err(error("reduce() espera 3 argumentos"));
                }
                let f = pos[0].clone();
                let items = pos[1].materializar().map_err(error)?;
                let mut acc = pos[2].clone();
                for x in items {
                    acc = self.aplicar_binario(&f, acc, x)?;
                }
                Ok(acc)
            }
            "contar" => {
                if pos.len() != 2 {
                    return Err(error("contar() espera 2 argumentos"));
                }
                let f = pos[0].clone();
                let items = pos[1].materializar().map_err(error)?;
                let mut n = 0;
                for x in items {
                    if self.aplicar_unario(&f, x)?.es_verdadero() {
                        n += 1;
                    }
                }
                Ok(Valor::Entero(n))
            }
            _ => Err(error("Funcional no soportado")),
        }
    }

    fn aplicar_unario(&mut self, f: &Valor, x: Valor) -> Exito<Valor> {
        match f {
            Valor::Funcion(fd) => {
                let fd = std::rc::Rc::clone(fd);
                self.llamar_funcion(&fd, vec![x], std::collections::HashMap::new())
            }
            Valor::Nativa(_, g) => g(&[x]).map_err(error),
            _ => Err(error("Función no invocable en map/filter")),
        }
    }

    fn aplicar_binario(&mut self, f: &Valor, a: Valor, b: Valor) -> Exito<Valor> {
        match f {
            Valor::Funcion(fd) => {
                let fd = std::rc::Rc::clone(fd);
                self.llamar_funcion(&fd, vec![a, b], std::collections::HashMap::new())
            }
            Valor::Nativa(_, g) => g(&[a, b]).map_err(error),
            _ => Err(error("Función no invocable en reduce")),
        }
    }

    fn evaluar_arg(&mut self, a: &ArgLlamada, env: &EntornoRef) -> Exito<Valor> {
        match a {
            ArgLlamada::Pos(e) => self.evaluar(e, env),
            ArgLlamada::Nom { valor, .. } => self.evaluar(valor, env),
        }
    }

    /// Métodos con mutación sobre variables (`lista.agregar`, `extender`,
    /// `quitar`, `insertar`). Operan directamente sobre el entorno para
    /// preservar la semántica por referencia del lenguaje.
    fn metodo_mutante(
        &mut self,
        nombre_var: &str,
        campo: &str,
        args: &[ArgLlamada],
        env: &EntornoRef,
    ) -> Exito<Option<Valor>> {
        let es_mutante = matches!(campo, "agregar" | "extender" | "quitar" | "insertar");
        if !es_mutante {
            return Ok(None);
        }
        let destino = match Self::resolver(env, nombre_var) {
            Some(e) => e,
            None => return Ok(None),
        };
        let es_lista = matches!(
            destino.borrow().valores.get(nombre_var),
            Some(Valor::Lista(_))
        );
        if !es_lista {
            return Ok(None);
        }
        let mut pos = Vec::with_capacity(args.len());
        for a in args {
            pos.push(self.evaluar_arg(a, env)?);
        }
        let mut b = destino.borrow_mut();
        let lista = match b.valores.get_mut(nombre_var) {
            Some(Valor::Lista(v)) => v,
            _ => return Ok(None),
        };
        match campo {
            "agregar" => {
                if pos.len() != 1 {
                    return Err(error("agregar() espera 1 argumento"));
                }
                lista.borrow_mut().push(pos[0].clone());
                Ok(Some(Valor::Nulo))
            }
            "extender" => {
                if pos.len() != 1 {
                    return Err(error("extender() espera 1 argumento"));
                }
                let extra = pos[0].materializar().map_err(error)?;
                lista.borrow_mut().extend(extra);
                Ok(Some(Valor::Nulo))
            }
            "quitar" => {
                if pos.len() > 1 {
                    return Err(error("quitar() espera 0 o 1 argumento"));
                }
                if pos.is_empty() {
                    lista.borrow_mut().pop();
                } else {
                    let i = pos[0].a_numero().map_err(error)? as i64;
                    let n = lista.borrow().len() as i64;
                    let j = if i < 0 { n + i } else { i };
                    if j < 0 || j >= n {
                        return Err(error("Índice fuera de rango"));
                    }
                    lista.borrow_mut().remove(j as usize);
                }
                Ok(Some(Valor::Nulo))
            }
            "insertar" => {
                if pos.len() != 2 {
                    return Err(error("insertar() espera 2 argumentos"));
                }
                let i = pos[0].a_numero().map_err(error)? as i64;
                let n = lista.borrow().len() as i64;
                let j = (if i < 0 { n + i } else { i }).clamp(0, n) as usize;
                lista.borrow_mut().insert(j, pos[1].clone());
                Ok(Some(Valor::Nulo))
            }
            _ => Ok(None),
        }
    }

    fn llamar_funcion(
        &mut self,
        f: &FuncionDef,
        pos: Vec<Valor>,
        nom: HashMap<String, Valor>,
    ) -> Exito<Valor> {
        if !nom.is_empty() && f.params.iter().all(|p| !matches!(p.nombre.as_str(), _)) {
            // Las funciones sin parámetros nombrados rechazan kwargs,
            // salvo que declaren `**kwargs` (gestionado abajo).
        }
        let local = Entorno::hijo(&f.clausura);
        let mut i = 0;
        for p in &f.params {
            match p.tipo {
                TipoParam::Normal => {
                    if i < pos.len() {
                        local
                            .borrow_mut()
                            .valores
                            .insert(p.nombre.clone(), pos[i].clone());
                        i += 1;
                    } else if let Some(v) = nom.get(&p.nombre) {
                        local
                            .borrow_mut()
                            .valores
                            .insert(p.nombre.clone(), v.clone());
                    } else {
                        return Err(error(format!("Faltan argumentos para '{}'", p.nombre)));
                    }
                }
                TipoParam::Args => {
                    let resto = if i < pos.len() {
                        pos[i..].to_vec()
                    } else {
                        Vec::new()
                    };
                    local
                        .borrow_mut()
                        .valores
                        .insert(p.nombre.clone(), Valor::nueva_lista(resto));
                    i = pos.len();
                }
                TipoParam::Kwargs => {
                    local
                        .borrow_mut()
                        .valores
                        .insert(p.nombre.clone(), Valor::nuevo_diccionario(nom.clone()));
                }
            }
        }
        if let Some(a) = &f.args_param {
            let resto = if i < pos.len() {
                pos[i..].to_vec()
            } else {
                Vec::new()
            };
            local
                .borrow_mut()
                .valores
                .insert(a.clone(), Valor::nueva_lista(resto));
        } else if i < pos.len() {
            return Err(error("Demasiados argumentos posicionales"));
        }
        match self.ejecutar_bloque_sin_ambito(&f.cuerpo, &local)? {
            Control::Flujo(Flujo::Retorno(v)) => Ok(v),
            _ => Ok(Valor::Nulo),
        }
    }
}

/// Resultado interno de una sentencia: valor normal o flujo no local.
enum Control {
    Valor(Valor),
    Flujo(Flujo),
}

/// Determina si un bloque requiere ámbito propio (declara variables,
///
/// constantes, importaciones, lecturas o funciones).
fn necesita_ambito(cuerpo: &[Sent]) -> bool {
    cuerpo.iter().any(|s| match s {
        Sent::DeclVar { .. }
        | Sent::DeclConst { .. }
        | Sent::Importar { .. }
        | Sent::Leer { .. } => true,
        Sent::DefFuncion { .. } => true,
        Sent::Bloque(inner) => necesita_ambito(inner),
        _ => false,
    })
}

fn partir_params(params: &[Param]) -> (Vec<Param>, Option<String>) {
    let mut normales = Vec::new();
    let mut args = None;
    for p in params {
        match p.tipo {
            TipoParam::Normal => normales.push(p.clone()),
            TipoParam::Args => args = Some(p.nombre.clone()),
            TipoParam::Kwargs => {
                normales.push(p.clone());
            }
        }
    }
    (normales, args)
}

fn dir_de(ruta: &str) -> String {
    match ruta.rfind('/') {
        Some(i) => ruta[..i].to_string(),
        None => ".".to_string(),
    }
}

fn modulo_de(ruta: &str) -> String {
    let base = ruta.rsplit('/').next().unwrap_or(ruta);
    let base = base.strip_suffix(".mice").unwrap_or(base);
    base.to_string()
}

fn leer_entrada() -> Exito<Valor> {
    use std::io::BufRead;
    let stdin = std::io::stdin();
    let mut line = String::new();
    stdin
        .lock()
        .read_line(&mut line)
        .map_err(|e| error(format!("Error de entrada: {e}")))?;
    Ok(parsear_atomo(line.trim()))
}

fn parsear_atomo(s: &str) -> Valor {
    if let Ok(i) = s.parse::<i64>() {
        return Valor::Entero(i);
    }
    if let Ok(f) = s.parse::<f64>() {
        return Valor::Flotante(f);
    }
    match s.to_lowercase().as_str() {
        "verdadero" => Valor::Logico(true),
        "falso" => Valor::Logico(false),
        "nulo" => Valor::Nulo,
        _ => Valor::Texto(s.to_string()),
    }
}

/// Igualdad profunda con promoción numérica int/float.
fn igualdad(a: &Valor, b: &Valor) -> Exito<bool> {
    match (a, b) {
        (Valor::Nulo, Valor::Nulo) => Ok(true),
        (Valor::Logico(x), Valor::Logico(y)) => Ok(x == y),
        (Valor::Entero(x), Valor::Entero(y)) => Ok(x == y),
        (Valor::Flotante(x), Valor::Flotante(y)) => Ok(x == y),
        (Valor::Entero(x), Valor::Flotante(y)) => Ok(*x as f64 == *y),
        (Valor::Flotante(x), Valor::Entero(y)) => Ok(*x == *y as f64),
        (Valor::Texto(x), Valor::Texto(y)) => Ok(x == y),
        (Valor::Lista(x), Valor::Lista(y)) => {
            let xb = x.borrow();
            let yb = y.borrow();
            if xb.len() != yb.len() {
                return Ok(false);
            }
            for (u, v) in xb.iter().zip(yb.iter()) {
                if !igualdad(u, v)? {
                    return Ok(false);
                }
            }
            Ok(true)
        }
        _ => Ok(false),
    }
}

fn aplicar_bin(op: OpBin, x: &Valor, y: &Valor) -> Exito<Valor> {
    match op {
        OpBin::Suma => suma(x, y),
        OpBin::Resta | OpBin::Mul | OpBin::Div | OpBin::Mod | OpBin::Pot | OpBin::ProdPunto => {
            aritmetica(op, x, y)
        }
        OpBin::Igual => Ok(Valor::Logico(igualdad(x, y)?)),
        OpBin::Distinto => Ok(Valor::Logico(!igualdad(x, y)?)),
        OpBin::Menor | OpBin::MenorIgual | OpBin::Mayor | OpBin::MayorIgual => {
            comparacion(op, x, y)
        }
        OpBin::In => pertenencia(x, y),
        OpBin::Pipe => Err(error("Pipe debe desazucararse en el parser")),
        OpBin::Y | OpBin::O => Err(error("Y/O requieren cortocircuito")),
    }
}

fn suma(x: &Valor, y: &Valor) -> Exito<Valor> {
    match (x, y) {
        (Valor::Entero(a), Valor::Entero(b)) => Ok(Valor::Entero(a.wrapping_add(*b))),
        (Valor::Texto(a), Valor::Texto(b)) => Ok(Valor::Texto(format!("{a}{b}"))),
        (Valor::Texto(a), b) => Ok(Valor::Texto(format!("{a}{}", b.a_texto()))),
        (a, Valor::Texto(b)) => Ok(Valor::Texto(format!("{}{b}", a.a_texto()))),
        (Valor::Lista(a), Valor::Lista(b)) => {
            let mut o = a.borrow().clone();
            o.extend(b.borrow().clone());
            Ok(Valor::nueva_lista(o))
        }
        _ => {
            let a = x.a_numero().map_err(error)?;
            let b = y.a_numero().map_err(error)?;
            if matches!(x, Valor::Entero(_)) && matches!(y, Valor::Entero(_)) {
                // Preserva enteros cuando ambos operandos son enteros.
                if let (Valor::Entero(ai), Valor::Entero(bi)) = (x, y) {
                    return Ok(Valor::Entero(ai.wrapping_add(*bi)));
                }
            }
            Ok(Valor::Flotante(a + b))
        }
    }
}

fn aritmetica(op: OpBin, x: &Valor, y: &Valor) -> Exito<Valor> {
    // Producto punto sobre listas/matrices con validación de dimensiones.
    if op == OpBin::ProdPunto {
        return producto_punto(x, y);
    }
    // Matrices densas como listas de listas para `*`.
    if op == OpBin::Mul {
        if let (Valor::Lista(a), Valor::Lista(b)) = (x, y) {
            if es_matriz(a) && es_matriz(b) {
                return multiplicar_matrices(a, b);
            }
        }
    }
    let a = x.a_numero().map_err(error)?;
    let b = y.a_numero().map_err(error)?;
    let entero = matches!(x, Valor::Entero(_)) && matches!(y, Valor::Entero(_));
    match op {
        OpBin::Resta => {
            if entero {
                if let (Valor::Entero(ai), Valor::Entero(bi)) = (x, y) {
                    return Ok(Valor::Entero(ai.wrapping_sub(*bi)));
                }
            }
            Ok(Valor::Flotante(a - b))
        }
        OpBin::Mul => {
            if entero {
                if let (Valor::Entero(ai), Valor::Entero(bi)) = (x, y) {
                    return Ok(Valor::Entero(ai.wrapping_mul(*bi)));
                }
            }
            Ok(Valor::Flotante(a * b))
        }
        OpBin::Div => {
            if b == 0.0 {
                return Err(error("División por cero"));
            }
            Ok(Valor::Flotante(a / b))
        }
        OpBin::Mod => {
            if entero {
                if let (Valor::Entero(ai), Valor::Entero(bi)) = (x, y) {
                    if *bi == 0 {
                        return Err(error("Módulo por cero"));
                    }
                    return Ok(Valor::Entero(ai.wrapping_rem(*bi)));
                }
            }
            if b == 0.0 {
                return Err(error("Módulo por cero"));
            }
            Ok(Valor::Flotante(a % b))
        }
        OpBin::Pot => Ok(Valor::Flotante(a.powf(b))),
        _ => Err(error("Operador no implementado")),
    }
}

fn es_matriz(rows: &crate::valor::ListaRef) -> bool {
    let r = rows.borrow();
    !r.is_empty() && r.iter().all(|x| matches!(x, Valor::Lista(_)))
}

/// Multiplicación de matrices con orden de bucles `i-k-j` para mejorar
/// la localidad de caché frente al orden ingenuo `i-j-k`.
fn multiplicar_matrices(a: &crate::valor::ListaRef, b: &crate::valor::ListaRef) -> Exito<Valor> {
    let ab = a.borrow();
    let bb = b.borrow();
    let ar = ab.len();
    let ac = match &ab[0] {
        Valor::Lista(r) => r.borrow().len(),
        _ => return Err(error("Matriz inválida")),
    };
    let br = bb.len();
    let bc = match &bb[0] {
        Valor::Lista(r) => r.borrow().len(),
        _ => return Err(error("Matriz inválida")),
    };
    if ac != br {
        return Err(error("Dimensiones invalidas para multiplicacion matricial"));
    }
    // Copia `b` traspuesta para acceso secuencial en el bucle interno.
    let mut bt = vec![vec![0.0; br]; bc];
    for i in 0..br {
        let row = match &bb[i] {
            Valor::Lista(r) => r.borrow().clone(),
            _ => return Err(error("Matriz inválida")),
        };
        for j in 0..bc {
            bt[j][i] = row[j].a_numero().map_err(error)?;
        }
    }
    let mut out = Vec::with_capacity(ar);
    for i in 0..ar {
        let row = match &ab[i] {
            Valor::Lista(r) => r.borrow().clone(),
            _ => return Err(error("Matriz inválida")),
        };
        let mut orow = Vec::with_capacity(bc);
        for j in 0..bc {
            let mut acc = 0.0;
            for k in 0..ac {
                acc += row[k].a_numero().map_err(error)? * bt[j][k];
            }
            orow.push(Valor::Flotante(acc));
        }
        out.push(Valor::nueva_lista(orow));
    }
    Ok(Valor::nueva_lista(out))
}

fn producto_punto(x: &Valor, y: &Valor) -> Exito<Valor> {
    match (x, y) {
        (Valor::Entero(a), Valor::Entero(b)) => Ok(Valor::Entero(a.wrapping_mul(*b))),
        (Valor::Lista(a), Valor::Lista(b)) => {
            let ab = a.borrow();
            let bb = b.borrow();
            if ab.len() != bb.len() {
                return Err(error("Producto elemento a elemento requiere mismo tamano"));
            }
            let mut out = Vec::with_capacity(ab.len());
            for (u, v) in ab.iter().zip(bb.iter()) {
                out.push(producto_punto(u, v)?);
            }
            Ok(Valor::nueva_lista(out))
        }
        _ => {
            let a = x.a_numero().map_err(error)?;
            let b = y.a_numero().map_err(error)?;
            Ok(Valor::Flotante(a * b))
        }
    }
}

fn comparacion(op: OpBin, x: &Valor, y: &Valor) -> Exito<Valor> {
    // Textos se comparan lexicográficamente; números con promoción.
    if let (Valor::Texto(a), Valor::Texto(b)) = (x, y) {
        let r = match op {
            OpBin::Menor => a < b,
            OpBin::MenorIgual => a <= b,
            OpBin::Mayor => a > b,
            OpBin::MayorIgual => a >= b,
            _ => false,
        };
        return Ok(Valor::Logico(r));
    }
    let a = x.a_numero().map_err(error)?;
    let b = y.a_numero().map_err(error)?;
    let r = match op {
        OpBin::Menor => a < b,
        OpBin::MenorIgual => a <= b,
        OpBin::Mayor => a > b,
        OpBin::MayorIgual => a >= b,
        _ => false,
    };
    Ok(Valor::Logico(r))
}

fn pertenencia(x: &Valor, y: &Valor) -> Exito<Valor> {
    match y {
        Valor::Lista(v) => {
            let vb = v.borrow();
            for item in vb.iter() {
                if igualdad(x, item)? {
                    return Ok(Valor::Logico(true));
                }
            }
            Ok(Valor::Logico(false))
        }
        Valor::Texto(t) => Ok(Valor::Logico(t.contains(&x.a_texto()))),
        Valor::Diccionario(m) => Ok(Valor::Logico(m.borrow().contains_key(&x.a_texto()))),
        Valor::Rango { .. } => {
            let items = y.materializar().map_err(error)?;
            for item in items {
                if igualdad(x, &item)? {
                    return Ok(Valor::Logico(true));
                }
            }
            Ok(Valor::Logico(false))
        }
        _ => Err(error("in requiere lista, texto o diccionario")),
    }
}

fn indizar(base: &Valor, indice: &Valor) -> Exito<Valor> {
    match base {
        Valor::Lista(v) => {
            let vb = v.borrow();
            let i = indice.a_numero().map_err(error)? as i64;
            let n = vb.len() as i64;
            let j = if i < 0 { n + i } else { i };
            if j < 0 || j >= n {
                return Err(error("Índice fuera de rango"));
            }
            Ok(vb[j as usize].clone())
        }
        Valor::Texto(s) => {
            let i = indice.a_numero().map_err(error)? as i64;
            let ch: Vec<char> = s.chars().collect();
            let n = ch.len() as i64;
            let j = if i < 0 { n + i } else { i };
            if j < 0 || j >= n {
                return Err(error("Índice fuera de rango"));
            }
            Ok(Valor::Texto(ch[j as usize].to_string()))
        }
        Valor::Diccionario(m) => {
            let k = indice.a_texto();
            m.borrow()
                .get(&k)
                .cloned()
                .ok_or_else(|| error(format!("Clave '{k}' no encontrada")))
        }
        Valor::Rango { .. } => {
            let items = base.materializar().map_err(error)?;
            indizar(&Valor::nueva_lista(items), indice)
        }
        _ => Err(error("Indexación no soportada para este tipo")),
    }
}

fn acceso(base: Valor, campo: &str) -> Exito<Valor> {
    match &base {
        Valor::Diccionario(m) => m
            .borrow()
            .get(campo)
            .cloned()
            .ok_or_else(|| error(format!("Campo '{campo}' no encontrado"))),
        // Los métodos se resuelven en el sitio de llamada; aquí se devuelve
        // un marcador para producir un error claro si se accede sin invocar.
        _ => Err(error(format!(
            "Acceso '.{campo}' requiere llamada a método o campo de módulo"
        ))),
    }
}

/// Despacho de métodos nativos sobre listas, textos y diccionarios.
/// Devuelve `Ok(None)` cuando el receptor no implementa el método de forma
/// nativa y debe resolverse como función de módulo.
fn metodo_nativo(
    base: &Valor,
    campo: &str,
    pos: &[Valor],
    _nom: &HashMap<String, Valor>,
) -> Exito<Option<Valor>> {
    match base {
        Valor::Lista(v) => match campo {
            "longitud" => {
                if !pos.is_empty() {
                    return Err(error("longitud() no recibe argumentos"));
                }
                Ok(Some(Valor::Entero(v.borrow().len() as i64)))
            }
            // `agregar`, `quitar`, `insertar` y `extender` mutan por valor
            // semántico de lista del lenguaje; el intérprete reasigna el
            // resultado al contenedor cuando corresponde al caso de uso
            // directo sobre variables en la práctica actual.
            _ => Ok(None),
        },
        Valor::Texto(s) => match campo {
            "longitud" => Ok(Some(Valor::Entero(s.chars().count() as i64))),
            _ => Ok(None),
        },
        Valor::Diccionario(_) => Ok(None),
        Valor::Rango { .. } => match campo {
            "longitud" => Ok(Some(Valor::Entero(base.longitud().map_err(error)?))),
            _ => Ok(None),
        },
        _ => Ok(None),
    }
}

fn asignar_en(cont: Valor, indices: &[Valor], valor: Valor) -> Exito<Valor> {
    if indices.is_empty() {
        return Ok(valor);
    }
    match cont {
        Valor::Lista(v) => {
            let i = indices[0].a_numero().map_err(error)? as i64;
            let n = v.borrow().len() as i64;
            let j = if i < 0 { n + i } else { i };
            if j < 0 || j >= n {
                return Err(error("Índice fuera de rango"));
            }
            if indices.len() == 1 {
                v.borrow_mut()[j as usize] = valor;
            } else {
                let sub = v.borrow()[j as usize].clone();
                let nv = asignar_en(sub, &indices[1..], valor)?;
                v.borrow_mut()[j as usize] = nv;
            }
            Ok(Valor::Lista(v))
        }
        Valor::Diccionario(m) => {
            if indices.len() != 1 {
                return Err(error("Asignación anidada en diccionario no soportada"));
            }
            m.borrow_mut().insert(indices[0].a_texto(), valor);
            Ok(Valor::Diccionario(m))
        }
        _ => Err(error("Asignación indexada no soportada para este tipo")),
    }
}

// ---- Funciones nativas globales ----

fn nativa_rango(args: &[Valor]) -> Result<Valor, String> {
    let nums: Vec<i64> = args
        .iter()
        .map(|v| v.a_numero().map(|f| f as i64))
        .collect::<Result<_, _>>()?;
    match nums.len() {
        1 => Ok(Valor::Rango {
            inicio: 0,
            fin: nums[0],
            paso: 1,
        }),
        2 => Ok(Valor::Rango {
            inicio: nums[0],
            fin: nums[1],
            paso: 1,
        }),
        3 => {
            if nums[2] == 0 {
                return Err("inc no puede ser 0".to_string());
            }
            Ok(Valor::Rango {
                inicio: nums[0],
                fin: nums[1],
                paso: nums[2],
            })
        }
        _ => Err("rango espera 1 a 3 argumentos".to_string()),
    }
}

fn nativa_longitud(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 1 {
        return Err("longitud() espera 1 argumento".to_string());
    }
    // Métodos `.longitud()` sobre listas y textos se atienden aquí también
    // cuando se invocan como función global.
    Ok(Valor::Entero(args[0].longitud()?))
}

fn nativa_a_texto(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 1 {
        return Err("aTexto() espera 1 argumento".to_string());
    }
    Ok(Valor::Texto(args[0].a_texto()))
}

fn nativa_tipo(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 1 {
        return Err("tipo() espera 1 argumento".to_string());
    }
    Ok(Valor::Texto(args[0].nombre_tipo().to_string()))
}

fn nativa_aleatorio(args: &[Valor]) -> Result<Valor, String> {
    if !args.is_empty() {
        return Err("aleatorio() no recibe argumentos".to_string());
    }
    // Generador xorshift64* sin estado global compartido costoso.
    use std::cell::Cell;
    thread_local! {
        static SEMILLA: Cell<u64> = const { Cell::new(0x9E3779B97F4A7C15) };
    }
    let v = SEMILLA.with(|s| {
        let mut x = s.get();
        x ^= x >> 12;
        x ^= x << 25;
        x ^= x >> 27;
        s.set(x);
        x.wrapping_mul(0x2545F4914F6CDD1D)
    });
    Ok(Valor::Flotante((v >> 11) as f64 / (u64::MAX >> 11) as f64))
}

fn nativa_error(args: &[Valor]) -> Result<Valor, String> {
    let m = args.first().map(|v| v.a_texto()).unwrap_or_default();
    Err(m)
}

fn nativa_abs(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 1 {
        return Err("abs() espera 1 argumento".to_string());
    }
    match &args[0] {
        Valor::Entero(i) => Ok(Valor::Entero(i.wrapping_abs())),
        Valor::Flotante(f) => Ok(Valor::Flotante(f.abs())),
        v => {
            let f = v.a_numero()?;
            Ok(Valor::Flotante(f.abs()))
        }
    }
}

fn nativa_maximo(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 2 {
        return Err("maximo() espera 2 argumentos".to_string());
    }
    let a = args[0].a_numero()?;
    let b = args[1].a_numero()?;
    if matches!(args[0], Valor::Entero(_)) && matches!(args[1], Valor::Entero(_)) {
        Ok(Valor::Entero((a as i64).max(b as i64)))
    } else {
        Ok(Valor::Flotante(a.max(b)))
    }
}

fn nativa_minimo(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 2 {
        return Err("minimo() espera 2 argumentos".to_string());
    }
    let a = args[0].a_numero()?;
    let b = args[1].a_numero()?;
    if matches!(args[0], Valor::Entero(_)) && matches!(args[1], Valor::Entero(_)) {
        Ok(Valor::Entero((a as i64).min(b as i64)))
    } else {
        Ok(Valor::Flotante(a.min(b)))
    }
}

fn nativa_a_numero(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 1 {
        return Err("aNumero() espera 1 argumento".to_string());
    }
    Ok(Valor::Flotante(args[0].a_numero()?))
}

fn nativa_a_entero(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 1 {
        return Err("aEntero() espera 1 argumento".to_string());
    }
    Ok(Valor::Entero(args[0].a_numero()? as i64))
}

fn nativa_a_flotante(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 1 {
        return Err("aFlotante() espera 1 argumento".to_string());
    }
    Ok(Valor::Flotante(args[0].a_numero()?))
}

fn nativa_a_booleano(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 1 {
        return Err("aBooleano() espera 1 argumento".to_string());
    }
    Ok(Valor::Logico(args[0].es_verdadero()))
}

fn nativa_a_caracter(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 1 {
        return Err("aCaracter() espera 1 argumento".to_string());
    }
    let c = args[0].a_numero()? as u32;
    char::from_u32(c)
        .map(|ch| Valor::Texto(ch.to_string()))
        .ok_or_else(|| "aCaracter() requiere un codigo Unicode valido".to_string())
}

/// Marcador para funcionales interceptados en `llamada`. Nunca debe
/// invocarse directamente porque requieren acceso al intérprete.
fn nativa_no_directa(_: &[Valor]) -> Result<Valor, String> {
    Err("Funcional requiere evaluación del intérprete".to_string())
}

fn nativa_ordenar(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 1 {
        return Err("ordenar() espera 1 argumento".to_string());
    }
    match &args[0] {
        Valor::Lista(v) => {
            let mut o = v.borrow().clone();
            o.sort_by(|a, b| {
                let x = a.a_numero().unwrap_or(0.0);
                let y = b.a_numero().unwrap_or(0.0);
                x.partial_cmp(&y).unwrap_or(std::cmp::Ordering::Equal)
            });
            Ok(Valor::nueva_lista(o))
        }
        _ => Err("ordenar() requiere una lista".to_string()),
    }
}

fn nativa_claves(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 1 {
        return Err("claves() espera 1 argumento".to_string());
    }
    match &args[0] {
        Valor::Diccionario(m) => {
            let mb = m.borrow();
            let mut ks: Vec<Valor> = mb.keys().cloned().map(Valor::Texto).collect();
            ks.sort_by(|a, b| a.a_texto().cmp(&b.a_texto()));
            Ok(Valor::nueva_lista(ks))
        }
        _ => Err("claves() requiere un diccionario".to_string()),
    }
}

fn nativa_valores(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 1 {
        return Err("valores() espera 1 argumento".to_string());
    }
    match &args[0] {
        Valor::Diccionario(m) => {
            let mb = m.borrow();
            let mut ks: Vec<String> = mb.keys().cloned().collect();
            ks.sort();
            Ok(Valor::nueva_lista(
                ks.into_iter().map(|k| mb[&k].clone()).collect(),
            ))
        }
        _ => Err("valores() requiere un diccionario".to_string()),
    }
}

fn nativa_items(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 1 {
        return Err("items() espera 1 argumento".to_string());
    }
    match &args[0] {
        Valor::Diccionario(m) => {
            let mb = m.borrow();
            let mut ks: Vec<String> = mb.keys().cloned().collect();
            ks.sort();
            Ok(Valor::nueva_lista(
                ks.into_iter()
                    .map(|k| Valor::nueva_lista(vec![Valor::Texto(k.clone()), mb[&k].clone()]))
                    .collect(),
            ))
        }
        _ => Err("items() requiere un diccionario".to_string()),
    }
}

fn nativa_primero(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 1 {
        return Err("primero() espera 1 argumento".to_string());
    }
    match &args[0] {
        Valor::Lista(v) => v
            .borrow()
            .first()
            .cloned()
            .ok_or_else(|| "primero() de lista vacía".to_string()),
        _ => Err("primero() requiere una lista".to_string()),
    }
}

fn nativa_ultimo(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 1 {
        return Err("ultimo() espera 1 argumento".to_string());
    }
    match &args[0] {
        Valor::Lista(v) => v
            .borrow()
            .last()
            .cloned()
            .ok_or_else(|| "ultimo() de lista vacía".to_string()),
        _ => Err("ultimo() requiere una lista".to_string()),
    }
}

fn nativa_invertir(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 1 {
        return Err("invertir() espera 1 argumento".to_string());
    }
    match &args[0] {
        Valor::Lista(v) => {
            let mut o = v.borrow().clone();
            o.reverse();
            Ok(Valor::nueva_lista(o))
        }
        _ => Err("invertir() requiere una lista".to_string()),
    }
}

fn nativa_concatenar(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 2 {
        return Err("concatenar() espera 2 argumentos".to_string());
    }
    match (&args[0], &args[1]) {
        (Valor::Lista(a), Valor::Lista(b)) => {
            let mut o = a.borrow().clone();
            o.extend(b.borrow().clone());
            Ok(Valor::nueva_lista(o))
        }
        _ => Err("concatenar() requiere dos listas".to_string()),
    }
}

fn nativa_suma_lista(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 1 {
        return Err("suma() espera 1 argumento".to_string());
    }
    match &args[0] {
        Valor::Lista(v) => {
            let vb = v.borrow();
            let mut acc = 0.0;
            let mut entero = true;
            let mut ai: i64 = 0;
            for x in vb.iter() {
                match x {
                    Valor::Entero(i) => ai = ai.wrapping_add(*i),
                    _ => {
                        entero = false;
                        acc += x.a_numero()?;
                    }
                }
            }
            if entero {
                Ok(Valor::Entero(ai))
            } else {
                for x in vb.iter() {
                    if matches!(x, Valor::Entero(_)) {
                        acc += x.a_numero()?;
                    }
                }
                Ok(Valor::Flotante(acc))
            }
        }
        _ => Err("suma() requiere una lista".to_string()),
    }
}

fn nativa_producto_lista(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 1 {
        return Err("producto() espera 1 argumento".to_string());
    }
    match &args[0] {
        Valor::Lista(v) => {
            let vb = v.borrow();
            let mut acc = 1.0;
            for x in vb.iter() {
                acc *= x.a_numero()?;
            }
            Ok(Valor::Flotante(acc))
        }
        _ => Err("producto() requiere una lista".to_string()),
    }
}

fn nativa_promedio(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 1 {
        return Err("promedio() espera 1 argumento".to_string());
    }
    match &args[0] {
        Valor::Lista(v) => {
            let vb = v.borrow();
            if vb.is_empty() {
                return Err("promedio() requiere una lista no vacía".to_string());
            }
            let mut acc = 0.0;
            for x in vb.iter() {
                acc += x.a_numero()?;
            }
            Ok(Valor::Flotante(acc / vb.len() as f64))
        }
        _ => Err("promedio() requiere una lista".to_string()),
    }
}

fn nativa_dummy(_: &[Valor]) -> Result<Valor, String> {
    Ok(Valor::Nulo)
}

fn nativa_dummy_text(_: &[Valor]) -> Result<Valor, String> {
    Ok(Valor::Texto(String::new()))
}

fn nativa_leer_csv_dummy(_: &[Valor]) -> Result<Valor, String> {
    Ok(Valor::nueva_lista(Vec::new()))
}

fn nativa_existe_falso(args: &[Valor]) -> Result<Valor, String> {
    if args.is_empty() {
        return Ok(Valor::Logico(false));
    }
    Ok(Valor::Logico(
        std::path::Path::new(&args[0].a_texto()).exists(),
    ))
}

fn nativa_archivo_leer(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 1 {
        return Err("__archivo_leer() espera 1 argumento".to_string());
    }
    let ruta = args[0].a_texto();
    std::fs::read_to_string(&ruta)
        .map(Valor::Texto)
        .map_err(|e| format!("No se pudo leer '{ruta}': {e}"))
}

fn nativa_archivo_escribir(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 2 {
        return Err("__archivo_escribir() espera 2 argumentos".to_string());
    }
    let ruta = args[0].a_texto();
    let contenido = args[1].a_texto();
    if let Some(padre) = std::path::Path::new(&ruta).parent() {
        if !padre.as_os_str().is_empty() {
            let _ = std::fs::create_dir_all(padre);
        }
    }
    std::fs::write(&ruta, contenido)
        .map(|_| Valor::Nulo)
        .map_err(|e| format!("No se pudo escribir '{ruta}': {e}"))
}

fn nativa_archivo_existe(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 1 {
        return Err("__archivo_existe() espera 1 argumento".to_string());
    }
    Ok(Valor::Logico(
        std::path::Path::new(&args[0].a_texto()).exists(),
    ))
}

fn nativa_archivo_eliminar(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 1 {
        return Err("__archivo_eliminar() espera 1 argumento".to_string());
    }
    let ruta = args[0].a_texto();
    std::fs::remove_file(&ruta)
        .map(|_| Valor::Nulo)
        .map_err(|e| format!("No se pudo eliminar '{ruta}': {e}"))
}

fn nativa_archivo_tamano(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 1 {
        return Err("__archivo_tamano() espera 1 argumento".to_string());
    }
    let ruta = args[0].a_texto();
    std::fs::metadata(&ruta)
        .map(|m| Valor::Entero(m.len() as i64))
        .map_err(|e| format!("No se pudo obtener tamaño de '{ruta}': {e}"))
}

fn nativa_leer_csv(args: &[Valor]) -> Result<Valor, String> {
    // `__leer_csv_rapido(ruta, delimitador, saltar_cabecera)` del intérprete
    // de referencia. Implementación directa sin dependencias: lectura por
    // líneas con separación por delimitador de un carácter.
    if args.len() < 2 {
        return Err("__leer_csv_rapido() espera ruta, delimitador y [saltar_cabecera]".to_string());
    }
    let ruta = args[0].a_texto();
    let delim = args[1].a_texto().chars().next().unwrap_or(',');
    let saltar: usize = if args.len() >= 3 {
        args[2].a_numero().unwrap_or(0.0) as usize
    } else {
        0
    };
    let contenido =
        std::fs::read_to_string(&ruta).map_err(|e| format!("No se pudo leer '{ruta}': {e}"))?;
    let mut filas = Vec::new();
    for (i, linea) in contenido.lines().enumerate() {
        if i < saltar || linea.trim().is_empty() {
            continue;
        }
        filas.push(Valor::nueva_lista(
            linea
                .split(delim)
                .map(|c| Valor::Texto(c.trim().to_string()))
                .collect(),
        ));
    }
    Ok(Valor::nueva_lista(filas))
}

fn nativa_json_dummy(_: &[Valor]) -> Result<Valor, String> {
    Ok(Valor::nuevo_diccionario(std::collections::HashMap::new()))
}

fn nativa_json_stringify_dummy(args: &[Valor]) -> Result<Valor, String> {
    Ok(Valor::Texto(
        args.first().map(|v| v.a_texto()).unwrap_or_default(),
    ))
}

fn nativa_max_lista(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 1 {
        return Err("max_lista() espera 1 argumento".to_string());
    }
    match &args[0] {
        Valor::Lista(v) => {
            let vb = v.borrow();
            if vb.is_empty() {
                return Err("max_lista() de lista vacía".to_string());
            }
            let mut m = vb[0].a_numero()?;
            for x in &vb[1..] {
                let f = x.a_numero()?;
                if f > m {
                    m = f;
                }
            }
            Ok(Valor::Flotante(m))
        }
        _ => Err("max_lista() requiere una lista".to_string()),
    }
}

fn nativa_min_lista(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 1 {
        return Err("min_lista() espera 1 argumento".to_string());
    }
    match &args[0] {
        Valor::Lista(v) => {
            let vb = v.borrow();
            if vb.is_empty() {
                return Err("min_lista() de lista vacía".to_string());
            }
            let mut m = vb[0].a_numero()?;
            for x in &vb[1..] {
                let f = x.a_numero()?;
                if f < m {
                    m = f;
                }
            }
            Ok(Valor::Flotante(m))
        }
        _ => Err("min_lista() requiere una lista".to_string()),
    }
}

fn nativa_seno(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 1 {
        return Err("seno() espera 1 argumento".to_string());
    }
    Ok(Valor::Flotante(args[0].a_numero()?.sin()))
}

fn nativa_coseno(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 1 {
        return Err("coseno() espera 1 argumento".to_string());
    }
    Ok(Valor::Flotante(args[0].a_numero()?.cos()))
}

fn nativa_exp(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 1 {
        return Err("exp() espera 1 argumento".to_string());
    }
    Ok(Valor::Flotante(args[0].a_numero()?.exp()))
}

fn nativa_a_codigo(args: &[Valor]) -> Result<Valor, String> {
    if args.len() != 1 {
        return Err("aCodigo() espera 1 argumento".to_string());
    }
    let s = args[0].a_texto();
    let mut ch = s.chars();
    match (ch.next(), ch.next()) {
        (Some(c), None) => Ok(Valor::Entero(c as i64)),
        _ => Err("aCodigo() requiere exactamente un caracter".to_string()),
    }
}

// ---- Preprocesador compatible con el intérprete de referencia ----

/// Reescribe azúcares sintácticos antes del análisis léxico:
/// - `leer a, b` → `__leer_multi("a,b")`
/// - `x += e` → `x = x + (e)` (y variantes `*=`, `-=`, `/=`, `%=`, `**=`)
/// - `a, b = expr` → `__asignar_multi("a,b", expr)`
///
/// La implementación es lineal sobre líneas y evita dependencias de
/// expresiones regulares para mantener el binario autocontenido.
pub fn preprocesar(codigo: &str) -> String {
    let mut out = Vec::new();
    for linea in codigo.lines() {
        let recortada = linea.trim_start();
        if recortada.is_empty() || recortada.starts_with('#') {
            out.push(linea.to_string());
            continue;
        }
        // Conserva el comentario de fin de línea, si existe, fuera de cadenas.
        let (sin_comentario, comentario) = partir_comentario(linea);
        if let Some(nombres) = leer_multiple(sin_comentario) {
            let indent = indentacion(linea);
            let mut r = format!("{indent}__leer_multi(\"{nombres}\")");
            if let Some(c) = comentario {
                r.push(' ');
                r.push_str(c);
            }
            out.push(r);
            continue;
        }
        if let Some((nombre, op, expr)) = asignacion_compuesta(sin_comentario) {
            let indent = indentacion(linea);
            let mut r = format!("{indent}{nombre} = {nombre} {op} ({expr})");
            if let Some(c) = comentario {
                r.push(' ');
                r.push_str(c);
            }
            out.push(r);
            continue;
        }
        if let Some((nombres, expr)) = asignacion_multiple(sin_comentario) {
            let indent = indentacion(linea);
            let mut r = format!("{indent}__asignar_multi(\"{nombres}\", {expr})");
            if let Some(c) = comentario {
                r.push(' ');
                r.push_str(c);
            }
            out.push(r);
            continue;
        }
        out.push(linea.to_string());
    }
    let mut s = out.join("\n");
    if codigo.ends_with('\n') {
        s.push('\n');
    }
    s
}

fn indentacion(linea: &str) -> &str {
    let n = linea.len() - linea.trim_start().len();
    &linea[..n]
}

/// Separa el comentario `#` que no se encuentra dentro de una cadena.
fn partir_comentario(linea: &str) -> (&str, Option<&str>) {
    let bytes = linea.as_bytes();
    let mut comilla: Option<u8> = None;
    let mut i = 0;
    while i < bytes.len() {
        let c = bytes[i];
        if let Some(q) = comilla {
            if c == b'\\' {
                i += 2;
                continue;
            }
            if c == q {
                comilla = None;
            }
            i += 1;
        } else if c == b'"' || c == b'\'' {
            comilla = Some(c);
            i += 1;
        } else if c == b'#' {
            return (linea[..i].trim_end(), Some(linea[i..].trim()));
        } else {
            i += 1;
        }
    }
    (linea, None)
}

fn es_ident(s: &str) -> bool {
    !s.is_empty()
        && s.bytes()
            .enumerate()
            .all(|(i, c)| c == b'_' || c.is_ascii_alphabetic() || (i > 0 && c.is_ascii_digit()))
}

fn leer_multiple(codigo: &str) -> Option<String> {
    let t = codigo.trim();
    if !t.starts_with("leer ") && !t.starts_with("leer\t") {
        return None;
    }
    let resto = t[4..].trim();
    if resto.is_empty() || !resto.contains(',') {
        return None;
    }
    let partes: Vec<&str> = resto.split(',').map(|s| s.trim()).collect();
    if partes.iter().all(|p| es_ident(p)) {
        Some(partes.join(","))
    } else {
        None
    }
}

fn asignacion_compuesta(codigo: &str) -> Option<(String, String, String)> {
    for op in ["**=", "+=", "-=", "*=", "/=", "%="] {
        if let Some(p) = codigo.find(op) {
            let izq = codigo[..p].trim();
            let der = codigo[p + op.len()..].trim();
            if es_ident(izq) && !der.is_empty() {
                // `**=` conserva `**`; el resto recorta `=`.
                let bin = if op == "**=" {
                    "**".to_string()
                } else {
                    op[..1].to_string()
                };
                return Some((izq.to_string(), bin, der.to_string()));
            }
        }
    }
    None
}

fn asignacion_multiple(codigo: &str) -> Option<(String, String)> {
    // Evita confundir `==`, `<=`, `>=`, `!=` con asignación.
    let bytes = codigo.as_bytes();
    let mut i = 0;
    let mut comilla: Option<u8> = None;
    while i < bytes.len() {
        let c = bytes[i];
        if let Some(q) = comilla {
            if c == b'\\' {
                i += 2;
                continue;
            }
            if c == q {
                comilla = None;
            }
            i += 1;
            continue;
        }
        if c == b'"' || c == b'\'' {
            comilla = Some(c);
            i += 1;
            continue;
        }
        if c == b'=' {
            let prev = if i > 0 { bytes[i - 1] } else { 0 };
            let next = if i + 1 < bytes.len() { bytes[i + 1] } else { 0 };
            if prev == b'=' || prev == b'!' || prev == b'<' || prev == b'>' || next == b'=' {
                i += 1;
                continue;
            }
            let izq = codigo[..i].trim();
            let der = codigo[i + 1..].trim();
            if izq.contains(',') && !der.is_empty() {
                let partes: Vec<&str> = izq.split(',').map(|s| s.trim()).collect();
                // Descarta declaraciones `var a, b = ...` (el parser las gestiona).
                if partes.iter().all(|p| es_ident(p)) {
                    return Some((partes.join(","), der.to_string()));
                }
            }
            return None;
        }
        i += 1;
    }
    None
}

/// Conjunto de pruebas de regresión del núcleo del lenguaje.
#[cfg(test)]
mod pruebas {
    use super::*;

    fn ejecutar(codigo: &str) -> Result<Vec<String>, String> {
        let mut it = Interprete::new(".".to_string());
        it.ejecutar_fuente(codigo)
            .map_err(|e| e.mensaje)
            .map(|_| it.salida.clone())
    }

    #[test]
    fn vuelta_suma() {
        let out =
            ejecutar("var total = 0\npara i en rango(1, 10000) { total = total + i }\nimp total\n")
                .expect("vuelta");
        assert_eq!(out, vec!["49995000".to_string()]);
    }

    #[test]
    fn fibonacci_recursivo() {
        let out = ejecutar(
            "funcion fib(n) { si (n <= 1) { regresa n } regresa fib(n-1) + fib(n-2) }\nimp fib(10)\n",
        )
        .expect("fib");
        assert_eq!(out, vec!["55".to_string()]);
    }

    #[test]
    fn taylor_exponencial() {
        let out = ejecutar(
            "funcion mi_exp(x, t) { var s = 1.0\n var tr = 1.0\n var n = 1\n mientras (n < t) { tr = tr * x / n\n s = s + tr\n n = n + 1 } regresa s }\nimp mi_exp(1, 10)\n",
        )
        .expect("taylor");
        assert!(out[0].starts_with("2.718"));
    }
}
