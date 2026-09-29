//! Analizador sintáctico por descenso recursivo.
//!
//! Produce el HIR definido en `crate::ast` a partir de los tokens del
//! analizador léxico. La precedencia de operadores replica `Micelio.g4`:
//! `|>` < `o` < `y` < `in` < comparación < `+ -` < `* / % .*` < `**`
//! (asociativo a derecha) < unarios < postfijos.
//!
//! Los separadores (`;` y saltos de línea) se aceptan como `sep*` en todos
//! los puntos donde la gramática los permite. Los errores se reportan en
//! español con la posición en bytes para diagnósticos pedagógicos.

use crate::ast::{ArgLlamada, Expr, ItemLista, OpBin, OpUn, Param, Programa, Sent, TipoParam};
use crate::lexer::{Token, TokenAnotado};

/// Error sintáctico con posición para mensajes en español.
#[derive(Debug, Clone)]
pub struct ErrorSintaxis {
    pub mensaje: String,
    pub posicion: u32,
}

/// Analizador con cursor sobre el vector de tokens.
pub struct Parser {
    toks: Vec<TokenAnotado>,
    pos: usize,
}

impl Parser {
    /// Crea un analizador sobre tokens ya producidos por el lexer.
    pub fn new(toks: Vec<TokenAnotado>) -> Self {
        Self { toks, pos: 0 }
    }

    fn peek(&self) -> &Token {
        &self
            .toks
            .get(self.pos)
            .map(|t| &t.token)
            .unwrap_or(&Token::Fin)
    }

    fn peek2(&self) -> &Token {
        &self
            .toks
            .get(self.pos + 1)
            .map(|t| &t.token)
            .unwrap_or(&Token::Fin)
    }

    fn posicion(&self) -> u32 {
        self.toks.get(self.pos).map(|t| t.span.inicio).unwrap_or(0)
    }

    fn avanzar(&mut self) -> Token {
        let t = self
            .toks
            .get(self.pos)
            .map(|t| t.token.clone())
            .unwrap_or(Token::Fin);
        if self.pos < self.toks.len() {
            self.pos += 1;
        }
        t
    }

    fn es_sep(t: &Token) -> bool {
        matches!(t, Token::NuevaLinea | Token::PuntoComa)
    }

    /// Omite cero o más separadores.
    fn omitir_sep(&mut self) {
        while Self::es_sep(self.peek()) {
            self.pos += 1;
        }
    }

    fn error<T>(&self, mensaje: impl Into<String>) -> Result<T, ErrorSintaxis> {
        Err(ErrorSintaxis {
            mensaje: mensaje.into(),
            posicion: self.posicion(),
        })
    }

    /// Texto canónico de un token cuando actúa como nombre (identificadores
    /// y palabras reservadas en posición de `ident` según la gramática).
    fn texto_nombre(t: &Token) -> Option<String> {
        match t {
            Token::Ident(s) => Some(s.clone()),
            Token::Var => Some("var".to_string()),
            Token::Const => Some("const".to_string()),
            Token::Funcion => Some("funcion".to_string()),
            Token::Matriz => Some("matriz".to_string()),
            Token::Regresa => Some("regresa".to_string()),
            Token::Si => Some("si".to_string()),
            Token::SinoSi => Some("sino_si".to_string()),
            Token::Sino => Some("sino".to_string()),
            Token::Segun => Some("segun".to_string()),
            Token::Caso => Some("caso".to_string()),
            Token::Defecto => Some("defecto".to_string()),
            Token::Para => Some("para".to_string()),
            Token::Hasta => Some("hasta".to_string()),
            Token::Inc => Some("inc".to_string()),
            Token::En => Some("en".to_string()),
            Token::Mientras => Some("mientras".to_string()),
            Token::Romper => Some("romper".to_string()),
            Token::Continuar => Some("continuar".to_string()),
            Token::Leer => Some("leer".to_string()),
            Token::Imp => Some("imp".to_string()),
            Token::Importar => Some("importar".to_string()),
            Token::Como => Some("como".to_string()),
            Token::Set => Some("set".to_string()),
            Token::Dict => Some("dict".to_string()),
            Token::Y => Some("y".to_string()),
            Token::O => Some("o".to_string()),
            Token::No => Some("no".to_string()),
            Token::In => Some("in".to_string()),
            Token::Nulo => Some("nulo".to_string()),
            _ => None,
        }
    }

    /// Punto de entrada: `program : sep* (statement sep*)* EOF`.
    pub fn programa(mut self) -> Result<Programa, ErrorSintaxis> {
        self.omitir_sep();
        let mut sents = Vec::new();
        while !matches!(self.peek(), Token::Fin) {
            sents.push(self.sentencia()?);
            self.omitir_sep();
        }
        Ok(Programa { sentencias: sents })
    }

    fn sentencia(&mut self) -> Result<Sent, ErrorSintaxis> {
        match self.peek() {
            Token::Si => self.si(),
            Token::Segun => self.segun(),
            Token::Mientras => self.mientras(),
            Token::Para => self.para(),
            Token::Funcion => self.def_funcion_nombrada(),
            Token::LlaveIzq => Ok(Sent::Bloque(self.bloque()?)),
            _ => self.simple(),
        }
    }

    fn simple(&mut self) -> Result<Sent, ErrorSintaxis> {
        match self.peek() {
            Token::Var => self.decl_var(),
            Token::Const => self.decl_const(),
            Token::Regresa => self.retorna(),
            Token::Romper => {
                self.avanzar();
                Ok(Sent::Romper)
            }
            Token::Continuar => {
                self.avanzar();
                Ok(Sent::Continuar)
            }
            Token::Importar => self.importar(),
            Token::Leer => self.leer(),
            Token::Imp => self.imp(),
            _ => {
                // Distingue asignación `ID ('[' expr ']')* '=' expr`
                // de una expresión general mediante inspección limitada.
                if self.es_asignacion() {
                    self.asignacion()
                } else {
                    Ok(Sent::Expr(self.expr_pipe()?))
                }
            }
        }
    }

    /// Inspección sin consumo para detectar `assign_target '='`.
    fn es_asignacion(&self) -> bool {
        let mut i = self.pos;
        let t0 = self.toks.get(i).map(|t| &t.token);
        // El objetivo debe comenzar con un nombre.
        if t0.is_none_or(|t| Self::texto_nombre(t).is_none()) {
            return false;
        }
        // `verdadero/falso/nulo` y literales no son objetivos válidos.
        if matches!(
            t0,
            Some(Token::Verdadero) | Some(Token::Falso) | Some(Token::Nulo)
        ) {
            return false;
        }
        i += 1;
        // Índices `[expr]` encadenados. Se realiza un balanceo simple de
        // corchetes sin validar el interior.
        loop {
            let a = self.toks.get(i).map(|t| &t.token);
            if matches!(a, Some(Token::CorcheteIzq)) {
                let mut prof = 0;
                while i < self.toks.len() {
                    match &self.toks[i].token {
                        Token::CorcheteIzq => prof += 1,
                        Token::CorcheteDer => {
                            prof -= 1;
                            if prof == 0 {
                                i += 1;
                                break;
                            }
                        }
                        Token::Fin => return false,
                        _ => {}
                    }
                    i += 1;
                }
                continue;
            }
            break;
        }
        matches!(self.toks.get(i).map(|t| &t.token), Some(Token::Asignacion))
    }

    fn decl_var(&mut self) -> Result<Sent, ErrorSintaxis> {
        self.avanzar(); // var
        let mut nombres = Vec::new();
        loop {
            match self.avanzar() {
                Token::Ident(s) => nombres.push(s),
                t => {
                    let nombre = Self::texto_nombre(&t);
                    if let Some(n) = nombre {
                        // Las palabras reservadas no son declarables como variables.
                        return self.error(format!("Nombre de variable inválido: '{n}'"));
                    }
                    return self.error("Se esperaba un nombre tras 'var'");
                }
            }
            if matches!(self.peek(), Token::Coma) {
                self.avanzar();
            } else {
                break;
            }
        }
        let mut valores = Vec::new();
        if matches!(self.peek(), Token::Asignacion) {
            self.avanzar();
            loop {
                valores.push(self.expr_pipe()?);
                if matches!(self.peek(), Token::Coma) {
                    self.avanzar();
                } else {
                    break;
                }
            }
        }
        Ok(Sent::DeclVar { nombres, valores })
    }

    fn decl_const(&mut self) -> Result<Sent, ErrorSintaxis> {
        self.avanzar(); // const
        let nombre = match self.avanzar() {
            Token::Ident(s) => s,
            _ => return self.error("Se esperaba un nombre tras 'const'"),
        };
        if !matches!(self.avanzar(), Token::Asignacion) {
            return self.error("Se esperaba '=' en declaración const");
        }
        Ok(Sent::DeclConst {
            nombre,
            valor: self.expr_pipe()?,
        })
    }

    fn asignacion(&mut self) -> Result<Sent, ErrorSintaxis> {
        let base = match self.avanzar() {
            Token::Ident(s) => s,
            t => match Self::texto_nombre(&t) {
                Some(n) => n,
                None => return self.error("Objetivo de asignación inválido"),
            },
        };
        let mut indices = Vec::new();
        while matches!(self.peek(), Token::CorcheteIzq) {
            self.avanzar();
            self.omitir_sep();
            indices.push(self.expr_pipe()?);
            self.omitir_sep();
            if !matches!(self.avanzar(), Token::CorcheteDer) {
                return self.error("Se esperaba ']'");
            }
        }
        if !matches!(self.avanzar(), Token::Asignacion) {
            return self.error("Se esperaba '='");
        }
        Ok(Sent::Asign {
            base,
            indices,
            valor: self.expr_pipe()?,
        })
    }

    fn retorna(&mut self) -> Result<Sent, ErrorSintaxis> {
        self.avanzar();
        // `regresa` sin valor si sigue un separador, cierre o fin.
        match self.peek() {
            Token::NuevaLinea | Token::PuntoComa | Token::LlaveDer | Token::Fin => {
                Ok(Sent::Retorna(None))
            }
            _ => Ok(Sent::Retorna(Some(self.expr_pipe()?))),
        }
    }

    fn importar(&mut self) -> Result<Sent, ErrorSintaxis> {
        self.avanzar();
        let ruta = match self.avanzar() {
            Token::Texto(s) => s,
            _ => return self.error("importar requiere una ruta entre comillas"),
        };
        let alias = if matches!(self.peek(), Token::Como) {
            self.avanzar();
            match self.avanzar() {
                Token::Ident(s) => Some(s),
                _ => return self.error("Se esperaba un alias tras 'como'"),
            }
        } else {
            None
        };
        Ok(Sent::Importar { ruta, alias })
    }

    fn leer(&mut self) -> Result<Sent, ErrorSintaxis> {
        self.avanzar();
        let nombre = match self.avanzar() {
            Token::Ident(s) => s,
            _ => return self.error("leer requiere un nombre de variable"),
        };
        Ok(Sent::Leer { nombre })
    }

    fn imp(&mut self) -> Result<Sent, ErrorSintaxis> {
        self.avanzar();
        Ok(Sent::Imp(self.expr_pipe()?))
    }

    fn si(&mut self) -> Result<Sent, ErrorSintaxis> {
        self.avanzar(); // si
        self.esperar(Token::ParenIzq, "si requiere '('")?;
        let cond = self.expr_pipe()?;
        self.esperar(Token::ParenDer, "si requiere ')'")?;
        self.omitir_sep();
        let entonces = self.bloque()?;
        let mut sino_si = Vec::new();
        loop {
            self.omitir_sep();
            if !matches!(self.peek(), Token::SinoSi) {
                break;
            }
            self.avanzar();
            self.omitir_sep();
            self.esperar(Token::ParenIzq, "sino_si requiere '('")?;
            let c = self.expr_pipe()?;
            self.esperar(Token::ParenDer, "sino_si requiere ')'")?;
            self.omitir_sep();
            sino_si.push((c, self.bloque()?));
        }
        self.omitir_sep();
        let sino_ = if matches!(self.peek(), Token::Sino) {
            self.avanzar();
            self.omitir_sep();
            Some(self.bloque()?)
        } else {
            None
        };
        Ok(Sent::Si {
            cond,
            entonces,
            sino_si,
            sino_,
        })
    }

    fn segun(&mut self) -> Result<Sent, ErrorSintaxis> {
        self.avanzar();
        self.esperar(Token::ParenIzq, "segun requiere '('")?;
        let expr = self.expr_pipe()?;
        self.esperar(Token::ParenDer, "segun requiere ')'")?;
        self.omitir_sep();
        self.esperar(Token::LlaveIzq, "segun requiere '{'")?;
        self.omitir_sep();
        let mut casos = Vec::new();
        let mut defecto = None;
        loop {
            self.omitir_sep();
            match self.peek() {
                Token::Caso => {
                    self.avanzar();
                    let v = self.expr_pipe()?;
                    self.esperar(Token::DosPuntos, "caso requiere ':'")?;
                    self.omitir_sep();
                    let mut cuerpo = Vec::new();
                    while !matches!(
                        self.peek(),
                        Token::Caso | Token::Defecto | Token::LlaveDer | Token::Fin
                    ) {
                        cuerpo.push(self.sentencia()?);
                        self.omitir_sep();
                    }
                    casos.push((v, cuerpo));
                }
                Token::Defecto => {
                    self.avanzar();
                    self.esperar(Token::DosPuntos, "defecto requiere ':'")?;
                    self.omitir_sep();
                    let mut cuerpo = Vec::new();
                    while !matches!(self.peek(), Token::LlaveDer | Token::Fin) {
                        cuerpo.push(self.sentencia()?);
                        self.omitir_sep();
                    }
                    defecto = Some(cuerpo);
                }
                Token::LlaveDer => {
                    self.avanzar();
                    break;
                }
                Token::Fin => return self.error("Bloque segun sin cerrar"),
                _ => return self.error("Se esperaba 'caso', 'defecto' o '}'"),
            }
        }
        Ok(Sent::Segun {
            expr,
            casos,
            defecto,
        })
    }

    fn mientras(&mut self) -> Result<Sent, ErrorSintaxis> {
        self.avanzar();
        self.esperar(Token::ParenIzq, "mientras requiere '('")?;
        let cond = self.expr_pipe()?;
        self.esperar(Token::ParenDer, "mientras requiere ')'")?;
        self.omitir_sep();
        Ok(Sent::Mientras {
            cond,
            cuerpo: self.bloque()?,
        })
    }

    fn para(&mut self) -> Result<Sent, ErrorSintaxis> {
        self.avanzar(); // para
        let var = match self.avanzar() {
            Token::Ident(s) => s,
            _ => return self.error("para requiere una variable"),
        };
        match self.peek() {
            Token::En => {
                self.avanzar();
                let iterable = self.expr_pipe()?;
                self.omitir_sep();
                Ok(Sent::ParaEn {
                    var,
                    iterable,
                    cuerpo: self.bloque()?,
                })
            }
            Token::Asignacion => {
                self.avanzar();
                let inicio = self.expr_pipe()?;
                if !matches!(self.peek(), Token::Hasta) {
                    return self.error("para clásico requiere 'hasta'");
                }
                self.avanzar();
                let fin = self.expr_pipe()?;
                let paso = if matches!(self.peek(), Token::Inc) {
                    self.avanzar();
                    Some(self.expr_pipe()?)
                } else {
                    None
                };
                self.omitir_sep();
                Ok(Sent::ParaHasta {
                    var,
                    inicio,
                    fin,
                    paso,
                    cuerpo: self.bloque()?,
                })
            }
            _ => self.error("para requiere 'en' o '='"),
        }
    }

    fn lista_params(&mut self) -> Result<Vec<Param>, ErrorSintaxis> {
        let mut out = Vec::new();
        if matches!(self.peek(), Token::ParenDer) {
            return Ok(out);
        }
        loop {
            self.omitir_sep();
            if matches!(self.peek(), Token::Por) {
                self.avanzar(); // *args
                match self.avanzar() {
                    Token::Ident(s) => out.push(Param {
                        nombre: s,
                        tipo: TipoParam::Args,
                    }),
                    _ => return self.error("Se esperaba nombre tras '*'"),
                }
            } else if matches!(self.peek(), Token::Potencia) {
                self.avanzar(); // **kwargs
                match self.avanzar() {
                    Token::Ident(s) => out.push(Param {
                        nombre: s,
                        tipo: TipoParam::Kwargs,
                    }),
                    _ => return self.error("Se esperaba nombre tras '**'"),
                }
            } else {
                match self.avanzar() {
                    Token::Ident(s) => out.push(Param {
                        nombre: s,
                        tipo: TipoParam::Normal,
                    }),
                    _ => return self.error("Parámetro inválido"),
                }
            }
            self.omitir_sep();
            if matches!(self.peek(), Token::Coma) {
                self.avanzar();
            } else {
                break;
            }
        }
        Ok(out)
    }

    fn def_funcion_nombrada(&mut self) -> Result<Sent, ErrorSintaxis> {
        self.avanzar();
        let nombre = match self.avanzar() {
            Token::Ident(s) => s,
            _ => return self.error("funcion requiere un nombre"),
        };
        self.esperar(Token::ParenIzq, "funcion requiere '('")?;
        let params = self.lista_params()?;
        self.esperar(Token::ParenDer, "funcion requiere ')'")?;
        self.omitir_sep();
        Ok(Sent::DefFuncion {
            nombre,
            params,
            cuerpo: self.bloque()?,
        })
    }

    fn bloque(&mut self) -> Result<Vec<Sent>, ErrorSintaxis> {
        self.esperar(Token::LlaveIzq, "se esperaba '{'")?;
        self.omitir_sep();
        let mut out = Vec::new();
        while !matches!(self.peek(), Token::LlaveDer | Token::Fin) {
            out.push(self.sentencia()?);
            self.omitir_sep();
        }
        self.esperar(Token::LlaveDer, "se esperaba '}'")?;
        Ok(out)
    }

    fn esperar(&mut self, esperado: Token, mensaje: &str) -> Result<(), ErrorSintaxis> {
        // Comparación por discriminante para ignorar el contenido asociado.
        if std::mem::discriminant(self.peek()) == std::mem::discriminant(&esperado) {
            self.avanzar();
            Ok(())
        } else {
            self.error(mensaje)
        }
    }

    // ---- Expresiones (precedencia ascendente) ----

    fn expr_pipe(&mut self) -> Result<Expr, ErrorSintaxis> {
        let mut izq = self.expr_o()?;
        loop {
            // `sep*` alrededor de `|>` según la gramática.
            let save = self.pos;
            self.omitir_sep();
            if !matches!(self.peek(), Token::Pipe) {
                self.pos = save;
                break;
            }
            self.avanzar();
            self.omitir_sep();
            let der = self.expr_o()?;
            // Semántica compatible con el intérprete de referencia:
            // `a |> f` es `f(a)`; `a |> f(b)` es `f(b, a)` (el valor
            // canalizado ocupa la segunda posición cuando ya hay argumentos).
            izq = match der {
                Expr::Llamada { callee, mut args } => {
                    if args.is_empty() {
                        args.push(ArgLlamada::Pos(izq));
                    } else {
                        args.insert(1, ArgLlamada::Pos(izq));
                    }
                    Expr::Llamada { callee, args }
                }
                f => Expr::Llamada {
                    callee: Box::new(f),
                    args: vec![ArgLlamada::Pos(izq)],
                },
            };
        }
        Ok(izq)
    }

    fn expr_o(&mut self) -> Result<Expr, ErrorSintaxis> {
        let mut izq = self.expr_y()?;
        while matches!(self.peek(), Token::O) {
            self.avanzar();
            let der = self.expr_y()?;
            izq = Expr::Binaria {
                op: OpBin::O,
                izq: Box::new(izq),
                der: Box::new(der),
            };
        }
        Ok(izq)
    }

    fn expr_y(&mut self) -> Result<Expr, ErrorSintaxis> {
        let mut izq = self.expr_in()?;
        while matches!(self.peek(), Token::Y) {
            self.avanzar();
            let der = self.expr_in()?;
            izq = Expr::Binaria {
                op: OpBin::Y,
                izq: Box::new(izq),
                der: Box::new(der),
            };
        }
        Ok(izq)
    }

    fn expr_in(&mut self) -> Result<Expr, ErrorSintaxis> {
        let mut izq = self.comparacion()?;
        while matches!(self.peek(), Token::In) {
            self.avanzar();
            let der = self.comparacion()?;
            izq = Expr::Binaria {
                op: OpBin::In,
                izq: Box::new(izq),
                der: Box::new(der),
            };
        }
        Ok(izq)
    }

    fn comparacion(&mut self) -> Result<Expr, ErrorSintaxis> {
        let mut izq = self.suma()?;
        loop {
            let op = match self.peek() {
                Token::Igual => OpBin::Igual,
                Token::Distinto => OpBin::Distinto,
                Token::Menor => OpBin::Menor,
                Token::MenorIgual => OpBin::MenorIgual,
                Token::Mayor => OpBin::Mayor,
                Token::MayorIgual => OpBin::MayorIgual,
                _ => break,
            };
            self.avanzar();
            let der = self.suma()?;
            izq = Expr::Binaria {
                op,
                izq: Box::new(izq),
                der: Box::new(der),
            };
        }
        Ok(izq)
    }

    fn suma(&mut self) -> Result<Expr, ErrorSintaxis> {
        let mut izq = self.mul()?;
        loop {
            let op = match self.peek() {
                Token::Mas => OpBin::Suma,
                Token::Menos => OpBin::Resta,
                _ => break,
            };
            self.avanzar();
            let der = self.mul()?;
            izq = Expr::Binaria {
                op,
                izq: Box::new(izq),
                der: Box::new(der),
            };
        }
        Ok(izq)
    }

    fn mul(&mut self) -> Result<Expr, ErrorSintaxis> {
        let mut izq = self.pot()?;
        loop {
            let op = match self.peek() {
                Token::Por => OpBin::Mul,
                Token::Division => OpBin::Div,
                Token::Modulo => OpBin::Mod,
                Token::ProductoPunto => OpBin::ProdPunto,
                _ => break,
            };
            self.avanzar();
            let der = self.pot()?;
            izq = Expr::Binaria {
                op,
                izq: Box::new(izq),
                der: Box::new(der),
            };
        }
        Ok(izq)
    }

    /// Potencia asociativa a derecha: `2 ** 3 ** 2 = 2 ** (3 ** 2)`.
    fn pot(&mut self) -> Result<Expr, ErrorSintaxis> {
        let base = self.unario()?;
        if matches!(self.peek(), Token::Potencia) {
            self.avanzar();
            let exp = self.pot()?;
            return Ok(Expr::Binaria {
                op: OpBin::Pot,
                izq: Box::new(base),
                der: Box::new(exp),
            });
        }
        Ok(base)
    }

    fn unario(&mut self) -> Result<Expr, ErrorSintaxis> {
        match self.peek() {
            Token::Menos => {
                self.avanzar();
                Ok(Expr::Unaria {
                    op: OpUn::Neg,
                    expr: Box::new(self.unario()?),
                })
            }
            Token::No => {
                self.avanzar();
                Ok(Expr::Unaria {
                    op: OpUn::No,
                    expr: Box::new(self.unario()?),
                })
            }
            Token::MasMas => {
                self.avanzar();
                Ok(Expr::Unaria {
                    op: OpUn::PreInc,
                    expr: Box::new(self.unario()?),
                })
            }
            Token::MenosMenos => {
                self.avanzar();
                Ok(Expr::Unaria {
                    op: OpUn::PreDec,
                    expr: Box::new(self.unario()?),
                })
            }
            _ => self.postfijo(),
        }
    }

    fn postfijo(&mut self) -> Result<Expr, ErrorSintaxis> {
        let mut e = self.primario()?;
        loop {
            match self.peek() {
                Token::CorcheteIzq => {
                    self.avanzar();
                    self.omitir_sep();
                    let idx = self.expr_pipe()?;
                    self.omitir_sep();
                    if !matches!(self.avanzar(), Token::CorcheteDer) {
                        return self.error("Se esperaba ']'");
                    }
                    e = Expr::Indice {
                        base: Box::new(e),
                        indice: Box::new(idx),
                    };
                }
                Token::Punto => {
                    self.avanzar();
                    let campo = match self.avanzar() {
                        Token::Ident(s) => s,
                        t => match Self::texto_nombre(&t) {
                            Some(n) => n,
                            None => return self.error("Se esperaba un miembro tras '.'"),
                        },
                    };
                    e = Expr::Acceso {
                        base: Box::new(e),
                        campo,
                    };
                }
                Token::ParenIzq => {
                    self.avanzar();
                    let args = self.args_llamada()?;
                    if !matches!(self.avanzar(), Token::ParenDer) {
                        return self.error("Se esperaba ')'");
                    }
                    e = Expr::Llamada {
                        callee: Box::new(e),
                        args,
                    };
                }
                Token::MasMas => {
                    self.avanzar();
                    e = Expr::Unaria {
                        op: OpUn::PostInc,
                        expr: Box::new(e),
                    };
                }
                Token::MenosMenos => {
                    self.avanzar();
                    e = Expr::Unaria {
                        op: OpUn::PostDec,
                        expr: Box::new(e),
                    };
                }
                _ => break,
            }
        }
        Ok(e)
    }

    fn args_llamada(&mut self) -> Result<Vec<ArgLlamada>, ErrorSintaxis> {
        let mut out = Vec::new();
        self.omitir_sep();
        if matches!(self.peek(), Token::ParenDer) {
            return Ok(out);
        }
        loop {
            self.omitir_sep();
            // Argumento nombrado `nombre = expr` (una sola `=`).
            if Self::texto_nombre(self.peek()).is_some()
                && matches!(self.peek2(), Token::Asignacion)
            {
                let nombre = Self::texto_nombre(&self.avanzar()).unwrap_or_default();
                self.avanzar(); // =
                out.push(ArgLlamada::Nom {
                    nombre,
                    valor: self.expr_pipe()?,
                });
            } else {
                out.push(ArgLlamada::Pos(self.expr_pipe()?));
            }
            self.omitir_sep();
            if matches!(self.peek(), Token::Coma) {
                self.avanzar();
            } else {
                break;
            }
        }
        Ok(out)
    }

    fn primario(&mut self) -> Result<Expr, ErrorSintaxis> {
        match self.avanzar() {
            Token::Entero(i) => Ok(Expr::Entero(i)),
            Token::Flotante(f) => Ok(Expr::Flotante(f)),
            Token::Texto(s) => Ok(Expr::Texto(s)),
            Token::Verdadero => Ok(Expr::Logico(true)),
            Token::Falso => Ok(Expr::Logico(false)),
            Token::Nulo => Ok(Expr::Nulo),
            Token::Ident(s) => Ok(Expr::Variable(s)),
            Token::ParenIzq => {
                self.omitir_sep();
                let e = self.expr_pipe()?;
                self.omitir_sep();
                if !matches!(self.avanzar(), Token::ParenDer) {
                    return self.error("Se esperaba ')'");
                }
                Ok(e)
            }
            Token::CorcheteIzq => self.lista(),
            Token::Set => self.set_o_dict_con_nombre(true),
            Token::Dict => self.set_o_dict_con_nombre(false),
            Token::LlaveIzq => self.mapa(),
            Token::Funcion => self.funcion_anonima(),
            Token::Matriz => {
                if !matches!(self.avanzar(), Token::ParenIzq) {
                    return self.error("matriz requiere '('");
                }
                self.omitir_sep();
                let e = self.expr_pipe()?;
                self.omitir_sep();
                if !matches!(self.avanzar(), Token::ParenDer) {
                    return self.error("matriz requiere ')'");
                }
                Ok(Expr::Matriz(Box::new(e)))
            }
            t => self.error(format!("Expresión inesperada: {t:?}")),
        }
    }

    fn lista(&mut self) -> Result<Expr, ErrorSintaxis> {
        let mut items = Vec::new();
        self.omitir_sep();
        if matches!(self.peek(), Token::CorcheteDer) {
            self.avanzar();
            return Ok(Expr::Lista(items));
        }
        loop {
            self.omitir_sep();
            if matches!(self.peek(), Token::Elipsis) {
                self.avanzar();
                items.push(ItemLista::Propaga(self.expr_pipe()?));
            } else {
                let a = self.expr_pipe()?;
                if matches!(self.peek(), Token::RangoPuntos) {
                    self.avanzar();
                    items.push(ItemLista::Rango(a, self.expr_pipe()?));
                } else {
                    items.push(ItemLista::Simple(a));
                }
            }
            self.omitir_sep();
            if matches!(self.peek(), Token::Coma) {
                self.avanzar();
            } else {
                break;
            }
        }
        self.omitir_sep();
        if !matches!(self.avanzar(), Token::CorcheteDer) {
            return self.error("Se esperaba ']'");
        }
        Ok(Expr::Lista(items))
    }

    fn set_o_dict_con_nombre(&mut self, es_set: bool) -> Result<Expr, ErrorSintaxis> {
        if !matches!(self.avanzar(), Token::ParenIzq) {
            return self.error("Se esperaba '('");
        }
        self.omitir_sep();
        let mut args = Vec::new();
        if !matches!(self.peek(), Token::ParenDer) {
            loop {
                self.omitir_sep();
                args.push(self.expr_pipe()?);
                self.omitir_sep();
                if matches!(self.peek(), Token::Coma) {
                    self.avanzar();
                } else {
                    break;
                }
            }
        }
        if !matches!(self.avanzar(), Token::ParenDer) {
            return self.error("Se esperaba ')'");
        }
        if es_set {
            Ok(Expr::Conjunto(args))
        } else {
            // `dict(a, b)` sin claves se evalúa como lista; la forma con
            // claves utiliza `dict(clave: valor)`, que el parser general
            // trata como llamada y el intérprete resuelve por nombre.
            Ok(Expr::Conjunto(args))
        }
    }

    fn mapa(&mut self) -> Result<Expr, ErrorSintaxis> {
        let mut pares = Vec::new();
        self.omitir_sep();
        if matches!(self.peek(), Token::LlaveDer) {
            self.avanzar();
            return Ok(Expr::Dicc(pares));
        }
        loop {
            self.omitir_sep();
            let k = self.expr_pipe()?;
            self.omitir_sep();
            if !matches!(self.avanzar(), Token::DosPuntos) {
                return self.error("Mapa requiere 'clave: valor'");
            }
            let v = self.expr_pipe()?;
            pares.push((k, v));
            self.omitir_sep();
            if matches!(self.peek(), Token::Coma) {
                self.avanzar();
            } else {
                break;
            }
        }
        self.omitir_sep();
        if !matches!(self.avanzar(), Token::LlaveDer) {
            return self.error("Se esperaba '}'");
        }
        Ok(Expr::Dicc(pares))
    }

    fn funcion_anonima(&mut self) -> Result<Expr, ErrorSintaxis> {
        if !matches!(self.avanzar(), Token::ParenIzq) {
            return self.error("funcion anónima requiere '('");
        }
        let params = self.lista_params()?;
        if !matches!(self.avanzar(), Token::ParenDer) {
            return self.error("funcion anónima requiere ')'");
        }
        self.omitir_sep();
        Ok(Expr::FuncionAnon {
            params,
            cuerpo: self.bloque()?,
        })
    }
}

/// Analiza un programa completo a partir de tokens.
pub fn analizar(toks: Vec<TokenAnotado>) -> Result<Programa, ErrorSintaxis> {
    Parser::new(toks).programa()
}

#[cfg(test)]
mod pruebas {
    use super::*;
    use crate::lexer::tokenizar;

    fn parse(src: &str) -> Programa {
        let toks = tokenizar(src).expect("lex");
        analizar(toks).expect("parse")
    }

    #[test]
    fn vuelta_parse() {
        let p = parse("var total = 0\npara i en rango(1, 10) { total = total + i }\nimp total\n");
        assert_eq!(p.sentencias.len(), 3);
    }

    #[test]
    fn precedencia_potencia() {
        let p = parse("var x = 2 ** 3 ** 2\n");
        assert_eq!(p.sentencias.len(), 1);
    }
}
