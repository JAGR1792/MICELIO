//! Sistema de valores de MICELIO.
//!
//! Representación etiquetada y compacta optimizada para los caminos
//! críticos (bucles numéricos y operaciones aritméticas). Los enteros,
//! flotantes y lógicos se almacenan por valor; las colecciones y textos
//! utilizan asignación en el montículo con conteo de referencias implícito
//! mediante `Clone` estructural.

use std::collections::HashMap;
use std::fmt;
use std::rc::Rc;

use crate::ast::{Param, Sent};

/// Función definida por el usuario con su clausura léxica.
#[derive(Debug, Clone)]
pub struct FuncionDef {
    pub nombre: Option<String>,
    pub params: Vec<Param>,
    /// Índice del primer parámetro variádico (`*args`), si existe.
    pub args_param: Option<String>,
    pub cuerpo: Vec<Sent>,
    pub clausura: EntornoRef,
}

/// Referencia compartida a un ámbito léxico.
pub type EntornoRef = Rc<std::cell::RefCell<Entorno>>;

/// Ámbito con encadenamiento a padre para resolución léxica.
#[derive(Debug, Clone, Default)]
pub struct Entorno {
    pub padre: Option<EntornoRef>,
    pub valores: HashMap<String, Valor>,
    pub constantes: std::collections::HashSet<String>,
}

impl Entorno {
    /// Crea un ámbito raíz vacío.
    pub fn raiz() -> EntornoRef {
        Rc::new(std::cell::RefCell::new(Self::default()))
    }

    /// Crea un ámbito hijo del proporcionado.
    pub fn hijo(padre: &EntornoRef) -> EntornoRef {
        Rc::new(std::cell::RefCell::new(Self {
            padre: Some(Rc::clone(padre)),
            valores: HashMap::new(),
            constantes: std::collections::HashSet::new(),
        }))
    }
}

/// Contenedor de lista con semántica por referencia (como Python).
/// `Rc<RefCell<..>>` permite que múltiples variables y cierres compartan
/// la misma lista y que el entrenamiento de redes neuronales mute pesos
/// in-place sin copias defensivas.
pub type ListaRef = std::rc::Rc<std::cell::RefCell<Vec<Valor>>>;
/// Contenedor de diccionario con semántica por referencia.
pub type DiccRef = std::rc::Rc<std::cell::RefCell<std::collections::HashMap<String, Valor>>>;

/// Valor del lenguaje.
#[derive(Debug, Clone)]
pub enum Valor {
    Nulo,
    Logico(bool),
    Entero(i64),
    Flotante(f64),
    Texto(String),
    Lista(ListaRef),
    /// Rango perezoso `[inicio, fin)` con paso. Equivale a `rango()` sin
    /// materializar la lista, lo que permite bucles de millones de
    /// iteraciones con memoria `O(1)`.
    Rango {
        inicio: i64,
        fin: i64,
        paso: i64,
    },
    Diccionario(DiccRef),
    Funcion(Rc<FuncionDef>),
    /// Función nativa implementada en Rust. El `&'static str` identifica
    /// la primitiva para mensajes de error estables.
    Nativa(&'static str, fn(&[Valor]) -> Result<Valor, String>),
}

impl Valor {
    /// Crea una lista con semántica por referencia.
    pub fn nueva_lista(v: Vec<Valor>) -> Self {
        Valor::Lista(std::rc::Rc::new(std::cell::RefCell::new(v)))
    }

    /// Crea un diccionario con semántica por referencia.
    pub fn nuevo_diccionario(m: std::collections::HashMap<String, Valor>) -> Self {
        Valor::Diccionario(std::rc::Rc::new(std::cell::RefCell::new(m)))
    }

    /// Nombre del tipo en español, coherente con `tipo()` del lenguaje.
    pub fn nombre_tipo(&self) -> &'static str {
        match self {
            Valor::Nulo => "nulo",
            Valor::Logico(_) => "logico",
            Valor::Entero(_) | Valor::Flotante(_) => "numero",
            Valor::Texto(_) => "texto",
            Valor::Lista(_) | Valor::Rango { .. } => "lista",
            Valor::Diccionario(_) => "diccionario",
            Valor::Funcion(_) | Valor::Nativa(_, _) => "funcion",
        }
    }

    /// Verdad del lenguaje: `falso`, `nulo`, `0`, `""` y listas vacías
    /// son falsos; el resto es verdadero.
    pub fn es_verdadero(&self) -> bool {
        match self {
            Valor::Nulo => false,
            Valor::Logico(b) => *b,
            Valor::Entero(i) => *i != 0,
            Valor::Flotante(f) => *f != 0.0,
            Valor::Texto(s) => !s.is_empty(),
            Valor::Lista(v) => !v.borrow().is_empty(),
            Valor::Rango { inicio, fin, paso } => {
                if *paso > 0 {
                    inicio < fin
                } else {
                    inicio > fin
                }
            }
            Valor::Diccionario(m) => !m.borrow().is_empty(),
            Valor::Funcion(_) | Valor::Nativa(_, _) => true,
        }
    }

    /// Conversión numérica con la misma tolerancia que el intérprete
    /// de referencia (cadenas con prefijos `0x`, `0o`, `0b`).
    pub fn a_numero(&self) -> Result<f64, String> {
        match self {
            Valor::Entero(i) => Ok(*i as f64),
            Valor::Flotante(f) => Ok(*f),
            Valor::Logico(true) => Ok(1.0),
            Valor::Logico(false) | Valor::Nulo => Ok(0.0),
            Valor::Texto(s) => {
                let t = s.trim().to_lowercase();
                if let Some(h) = t.strip_prefix("0x") {
                    i64::from_str_radix(h, 16)
                        .map(|v| v as f64)
                        .map_err(|_| format!("No se puede convertir '{s}' a numero"))
                } else if let Some(o) = t.strip_prefix("0o") {
                    i64::from_str_radix(o, 8)
                        .map(|v| v as f64)
                        .map_err(|_| format!("No se puede convertir '{s}' a numero"))
                } else if let Some(b) = t.strip_prefix("0b") {
                    i64::from_str_radix(b, 2)
                        .map(|v| v as f64)
                        .map_err(|_| format!("No se puede convertir '{s}' a numero"))
                } else {
                    t.parse::<f64>()
                        .map_err(|_| format!("No se puede convertir '{s}' a numero"))
                }
            }
            v => Err(format!(
                "Operación numérica requiere numeros, recibido {}",
                v.nombre_tipo()
            )),
        }
    }

    /// Representación textual coherente con `aTexto()` y `imp`.
    pub fn a_texto(&self) -> String {
        match self {
            Valor::Nulo => "nulo".to_string(),
            Valor::Logico(true) => "verdadero".to_string(),
            Valor::Logico(false) => "falso".to_string(),
            Valor::Entero(i) => i.to_string(),
            Valor::Flotante(f) => {
                if f.fract() == 0.0 && f.is_finite() {
                    format!("{f:.1}")
                } else {
                    format!("{f}")
                }
            }
            Valor::Texto(s) => s.clone(),
            Valor::Lista(v) => {
                let inner: Vec<String> = v.borrow().iter().map(|x| x.repr()).collect();
                format!("[{}]", inner.join(", "))
            }
            Valor::Rango { inicio, fin, paso } => {
                format!("rango({inicio}, {fin}, {paso})")
            }
            Valor::Diccionario(m) => {
                let mref = m.borrow();
                let mut pares: Vec<String> = mref
                    .iter()
                    .map(|(k, v)| format!("{k}: {}", v.repr()))
                    .collect();
                pares.sort();
                format!("{{{}}}", pares.join(", "))
            }
            Valor::Funcion(f) => format!("<funcion {}>", f.nombre.as_deref().unwrap_or("anonima")),
            Valor::Nativa(n, _) => format!("<nativa {n}>"),
        }
    }

    /// Representación para depuración y literales anidados.
    pub fn repr(&self) -> String {
        match self {
            Valor::Texto(s) => format!("\"{s}\""),
            _ => self.a_texto(),
        }
    }

    /// Longitud universal (`longitud()`): textos, listas, rangos y diccionarios.
    pub fn longitud(&self) -> Result<i64, String> {
        match self {
            Valor::Texto(s) => Ok(s.chars().count() as i64),
            Valor::Lista(v) => Ok(v.borrow().len() as i64),
            Valor::Rango { inicio, fin, paso } => {
                if *paso == 0 {
                    return Err("Rango con paso 0".to_string());
                }
                if (*paso > 0 && inicio >= fin) || (*paso < 0 && inicio <= fin) {
                    Ok(0)
                } else {
                    Ok((fin - inicio + paso - paso.signum()) / paso)
                }
            }
            Valor::Diccionario(m) => Ok(m.borrow().len() as i64),
            v => Err(format!("longitud() no soporta {}", v.nombre_tipo())),
        }
    }

    /// Materializa un iterable en `Vec<Valor>` para índices y propagación.
    /// Los rangos grandes se limitan a 10M elementos para evitar
    /// agotamiento de memoria; los bucles deben iterar el `Rango`
    /// directamente sin materializar.
    pub fn materializar(&self) -> Result<Vec<Valor>, String> {
        match self {
            Valor::Lista(v) => Ok(v.borrow().clone()),
            Valor::Texto(s) => Ok(s.chars().map(|c| Valor::Texto(c.to_string())).collect()),
            Valor::Diccionario(m) => {
                let mut ks: Vec<String> = m.borrow().keys().cloned().collect();
                ks.sort();
                Ok(ks.into_iter().map(Valor::Texto).collect())
            }
            Valor::Rango { inicio, fin, paso } => {
                let n = self.longitud()?;
                if n > 10_000_000 {
                    return Err(
                        "Rango demasiado grande para materializar; itere directamente".to_string(),
                    );
                }
                let mut out = Vec::with_capacity(n.max(0) as usize);
                let mut c = *inicio;
                if *paso > 0 {
                    while c < *fin {
                        out.push(Valor::Entero(c));
                        c += *paso;
                    }
                } else {
                    while c > *fin {
                        out.push(Valor::Entero(c));
                        c += *paso;
                    }
                }
                Ok(out)
            }
            v => Err(format!(
                "Valor {} no es iterable en para..en",
                v.nombre_tipo()
            )),
        }
    }
}

impl fmt::Display for Valor {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.a_texto())
    }
}
