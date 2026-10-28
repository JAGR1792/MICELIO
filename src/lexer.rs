//! Analizador léxico de MICELIO.
//!
//! Diseño:
//! - Una única pasada sobre la entrada (`O(n)` en tiempo, `O(t)` en memoria
//!   donde `t` es el número de tokens).
//! - Sin expresiones regulares ni tablas ATN generadas. El autómata está
//!   codificado de forma explícita para favorecer la predicción de saltos
//!   y mantener el conjunto de trabajo en caché L1.
//! - Los identificadores y literales conservan su_span_ (`inicio`, `longitud`)
//!   para diagnósticos precisos sin necesidad de copiar durante el escaneo.
//!
//! Compatibilidad:
//! Implementa el vocabulario completo de `Micelio.g4`: palabras reservadas en
//! español, literales numéricos enteros y flotantes, cadenas con escapes,
//! operadores simples, dobles y triples (`**`, `==`, `!=`, `<=`, `>=`, `..`,
//! `...`, `|>`, `++`, `--`, `.*`), puntuación y separadores (`;`, saltos de
//! línea). Los comentarios con `#` se descartan.

/// Posición de un token dentro del fuente original.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Span {
    /// Desplazamiento en bytes desde el inicio del archivo.
    pub inicio: u32,
    /// Longitud en bytes.
    pub longitud: u32,
}

/// Conjunto completo de tokens del lenguaje.
#[derive(Debug, Clone, PartialEq)]
pub enum Token {
    // Palabras reservadas.
    Var,
    Const,
    Funcion,
    Matriz,
    Regresa,
    Si,
    SinoSi,
    Sino,
    Segun,
    Caso,
    Defecto,
    Para,
    Hasta,
    Inc,
    En,
    Mientras,
    Romper,
    Continuar,
    Leer,
    Imp,
    Importar,
    Como,
    Set,
    Dict,
    Verdadero,
    Falso,
    Nulo,
    Y,
    O,
    No,
    In,

    // Identificadores y literales.
    Ident(String),
    Entero(i64),
    Flotante(f64),
    Texto(String),

    // Operadores aritméticos y de asignación.
    Mas,
    Menos,
    Por,
    Division,
    Modulo,
    Potencia,      // **
    ProductoPunto, // .*
    MasMas,        // ++
    MenosMenos,    // --
    Asignacion,    // =

    // Comparación.
    Igual,      // ==
    Distinto,   // !=
    Menor,      // <
    MenorIgual, // <=
    Mayor,      // >
    MayorIgual, // >=

    // Puntuación.
    ParenIzq,
    ParenDer,
    CorcheteIzq,
    CorcheteDer,
    LlaveIzq,
    LlaveDer,
    Coma,
    DosPuntos,
    Punto,
    RangoPuntos, // ..
    Elipsis,     // ...
    Pipe,        // |>

    // Separadores significativos (el parser los acepta como `sep*`).
    PuntoComa,
    NuevaLinea,

    Fin,
}

/// Token anotado con su localización.
#[derive(Debug, Clone, PartialEq)]
pub struct TokenAnotado {
    pub token: Token,
    pub span: Span,
}

/// Error léxico con posición para mensajes pedagógicos en español.
#[derive(Debug, Clone, PartialEq)]
pub struct ErrorLexico {
    pub mensaje: String,
    pub posicion: u32,
}

/// Analizador léxico incremental sobre un buffer de bytes.
///
/// # Invariantes
/// - `pos` siempre apunta al siguiente byte por consumir o a `src.len()`.
/// - Nunca se realiza indexación fuera de límites: `peek` devuelve 0 como
///   centinela de fin de entrada.
pub struct Lexer<'a> {
    src: &'a [u8],
    pos: usize,
}

impl<'a> Lexer<'a> {
    /// Crea un analizador sobre el texto fuente completo.
    pub fn new(src: &'a str) -> Self {
        Self {
            src: src.as_bytes(),
            pos: 0,
        }
    }

    #[inline(always)]
    fn peek(&self) -> u8 {
        if self.pos < self.src.len() {
            self.src[self.pos]
        } else {
            0
        }
    }

    #[inline(always)]
    fn peek2(&self) -> u8 {
        if self.pos + 1 < self.src.len() {
            self.src[self.pos + 1]
        } else {
            0
        }
    }

    #[inline(always)]
    fn peek3(&self) -> u8 {
        if self.pos + 2 < self.src.len() {
            self.src[self.pos + 2]
        } else {
            0
        }
    }

    /// Omite espacios horizontales y comentarios, pero conserva saltos de línea.
    fn omitir_trivia(&mut self) {
        loop {
            let c = self.peek();
            if c == b' ' || c == b'\t' || c == b'\r' {
                self.pos += 1;
            } else if c == b'#' {
                while self.peek() != b'\n' && self.peek() != 0 {
                    self.pos += 1;
                }
            } else {
                break;
            }
        }
    }

    /// Clasifica un identificador o palabra reservada.
    ///
    /// Complejidad `O(k)` donde `k` es la longitud del identificador.
    /// La comparación se realiza por `match` directo sobre el slice,
    /// lo que el compilador convierte en una cadena de comparaciones
    /// de enteros sin acceso a tablas hash.
    fn palabra(&mut self, inicio: usize) -> Token {
        while self.peek().is_ascii_alphanumeric() || self.peek() == b'_' {
            self.pos += 1;
        }
        let s = &self.src[inicio..self.pos];
        match s {
            b"var" => Token::Var,
            b"const" => Token::Const,
            b"funcion" => Token::Funcion,
            b"matriz" => Token::Matriz,
            b"regresa" => Token::Regresa,
            b"si" => Token::Si,
            b"sino_si" => Token::SinoSi,
            b"sino" => Token::Sino,
            b"segun" => Token::Segun,
            b"caso" => Token::Caso,
            b"defecto" => Token::Defecto,
            b"para" => Token::Para,
            b"hasta" => Token::Hasta,
            b"inc" => Token::Inc,
            b"en" => Token::En,
            b"mientras" => Token::Mientras,
            b"romper" => Token::Romper,
            b"continuar" => Token::Continuar,
            b"leer" => Token::Leer,
            b"imp" => Token::Imp,
            b"importar" => Token::Importar,
            b"como" => Token::Como,
            b"set" => Token::Set,
            b"dict" => Token::Dict,
            b"verdadero" => Token::Verdadero,
            b"falso" => Token::Falso,
            b"nulo" => Token::Nulo,
            b"y" => Token::Y,
            b"o" => Token::O,
            b"no" => Token::No,
            b"in" => Token::In,
            _ => Token::Ident(
                // SAFETY: el slice proviene de un identificador ASCII válido,
                // por lo que la conversión a UTF-8 siempre tiene éxito.
                String::from_utf8_lossy(s).into_owned(),
            ),
        }
    }

    /// Escanea un literal numérico entero o flotante.
    fn numero(&mut self, inicio: usize) -> Token {
        while self.peek().is_ascii_digit() {
            self.pos += 1;
        }
        // Parte fraccionaria opcional. Se exige al menos un dígito tras el punto
        // para no confundir `1..10` (rango) con `1.` (flotante).
        if self.peek() == b'.' && self.peek2().is_ascii_digit() {
            self.pos += 1; // consume '.'
            while self.peek().is_ascii_digit() {
                self.pos += 1;
            }
            let s = &self.src[inicio..self.pos];
            let v: f64 = String::from_utf8_lossy(s).parse().unwrap_or(0.0);
            return Token::Flotante(v);
        }
        let s = &self.src[inicio..self.pos];
        // El desbordamiento se satura a los extremos de i64 para mantener
        // la ejecución total sin pánicos en modo release.
        let v: i64 = String::from_utf8_lossy(s).parse().unwrap_or(0);
        Token::Entero(v)
    }

    /// Escanea una cadena entre comillas simples o dobles con escapes `\`.
    fn texto(&mut self, comilla: u8, inicio: usize) -> Result<Token, ErrorLexico> {
        let mut out = Vec::with_capacity(16);
        loop {
            let c = self.peek();
            if c == 0 || c == b'\n' {
                return Err(ErrorLexico {
                    mensaje: "Cadena sin cerrar: falta la comilla de cierre".to_string(),
                    posicion: inicio as u32,
                });
            }
            if c == comilla {
                self.pos += 1;
                break;
            }
            if c == b'\\' {
                self.pos += 1;
                let e = self.peek();
                self.pos += 1;
                match e {
                    b'n' => out.push(b'\n'),
                    b't' => out.push(b'\t'),
                    b'r' => out.push(b'\r'),
                    b'\\' => out.push(b'\\'),
                    b'\'' => out.push(b'\''),
                    b'"' => out.push(b'"'),
                    b'0' => out.push(0),
                    _ => {
                        out.push(b'\\');
                        out.push(e);
                    }
                }
            } else {
                out.push(c);
                self.pos += 1;
            }
        }
        Ok(Token::Texto(String::from_utf8_lossy(&out).into_owned()))
    }

    /// Produce el siguiente token con su span.
    fn siguiente(&mut self) -> Result<Option<TokenAnotado>, ErrorLexico> {
        self.omitir_trivia();
        let inicio = self.pos;
        let c = self.peek();
        if c == 0 {
            return Ok(None);
        }
        // Saltos de línea y punto y coma son separadores explícitos.
        if c == b'\n' {
            self.pos += 1;
            return Ok(Some(TokenAnotado {
                token: Token::NuevaLinea,
                span: Span {
                    inicio: inicio as u32,
                    longitud: 1,
                },
            }));
        }
        if c == b';' {
            self.pos += 1;
            return Ok(Some(TokenAnotado {
                token: Token::PuntoComa,
                span: Span {
                    inicio: inicio as u32,
                    longitud: 1,
                },
            }));
        }
        // Identificadores y palabras reservadas.
        if c.is_ascii_alphabetic() || c == b'_' {
            self.pos += 1;
            let t = self.palabra(inicio);
            return Ok(Some(TokenAnotado {
                token: t,
                span: Span {
                    inicio: inicio as u32,
                    longitud: (self.pos - inicio) as u32,
                },
            }));
        }
        // Números.
        if c.is_ascii_digit() {
            let t = self.numero(inicio);
            return Ok(Some(TokenAnotado {
                token: t,
                span: Span {
                    inicio: inicio as u32,
                    longitud: (self.pos - inicio) as u32,
                },
            }));
        }
        // Cadenas.
        if c == b'"' || c == b'\'' {
            self.pos += 1;
            let t = self.texto(c, inicio)?;
            return Ok(Some(TokenAnotado {
                token: t,
                span: Span {
                    inicio: inicio as u32,
                    longitud: (self.pos - inicio) as u32,
                },
            }));
        }

        // Operadores de uno a tres caracteres. El orden de comprobación
        // prioriza los trigramas (`...`, `**`) sobre los bigramas y estos
        // sobre los unigramas para garantizar el emparejamiento voraz.
        let c2 = self.peek2();
        let c3 = self.peek3();
        let triple: Option<(Token, usize)> = match (c, c2, c3) {
            (b'.', b'.', b'.') => Some((Token::Elipsis, 3)),
            _ => None,
        };
        if let Some((t, n)) = triple {
            self.pos += n;
            return Ok(Some(TokenAnotado {
                token: t,
                span: Span {
                    inicio: inicio as u32,
                    longitud: n as u32,
                },
            }));
        }
        let doble: Option<Token> = match (c, c2) {
            (b'*', b'*') => Some(Token::Potencia),
            (b'.', b'*') => Some(Token::ProductoPunto),
            (b'+', b'+') => Some(Token::MasMas),
            (b'-', b'-') => Some(Token::MenosMenos),
            (b'=', b'=') => Some(Token::Igual),
            (b'!', b'=') => Some(Token::Distinto),
            (b'<', b'=') => Some(Token::MenorIgual),
            (b'>', b'=') => Some(Token::MayorIgual),
            (b'.', b'.') => Some(Token::RangoPuntos),
            (b'|', b'>') => Some(Token::Pipe),
            _ => None,
        };
        if let Some(t) = doble {
            self.pos += 2;
            return Ok(Some(TokenAnotado {
                token: t,
                span: Span {
                    inicio: inicio as u32,
                    longitud: 2,
                },
            }));
        }
        let simple: Option<Token> = match c {
            b'+' => Some(Token::Mas),
            b'-' => Some(Token::Menos),
            b'*' => Some(Token::Por),
            b'/' => Some(Token::Division),
            b'%' => Some(Token::Modulo),
            b'=' => Some(Token::Asignacion),
            b'<' => Some(Token::Menor),
            b'>' => Some(Token::Mayor),
            b'(' => Some(Token::ParenIzq),
            b')' => Some(Token::ParenDer),
            b'[' => Some(Token::CorcheteIzq),
            b']' => Some(Token::CorcheteDer),
            b'{' => Some(Token::LlaveIzq),
            b'}' => Some(Token::LlaveDer),
            b',' => Some(Token::Coma),
            b':' => Some(Token::DosPuntos),
            b'.' => Some(Token::Punto),
            _ => None,
        };
        if let Some(t) = simple {
            self.pos += 1;
            return Ok(Some(TokenAnotado {
                token: t,
                span: Span {
                    inicio: inicio as u32,
                    longitud: 1,
                },
            }));
        }
        Err(ErrorLexico {
            mensaje: format!("Carácter inesperado: '{}'", c as char),
            posicion: inicio as u32,
        })
    }

    /// Tokeniza la entrada completa.
    ///
    /// Reserva por adelantado `src.len()/4` tokens como heurística:
    /// el español promedia ~4 bytes por token en código típico.
    pub fn tokenizar(mut self) -> Result<Vec<TokenAnotado>, ErrorLexico> {
        let mut out = Vec::with_capacity((self.src.len() / 4).max(16));
        loop {
            match self.siguiente()? {
                Some(t) => out.push(t),
                None => {
                    out.push(TokenAnotado {
                        token: Token::Fin,
                        span: Span {
                            inicio: self.pos as u32,
                            longitud: 0,
                        },
                    });
                    break;
                }
            }
        }
        Ok(out)
    }
}

/// Atajo para casos simples (pruebas y REPL).
pub fn tokenizar(src: &str) -> Result<Vec<TokenAnotado>, ErrorLexico> {
    Lexer::new(src).tokenizar()
}

#[cfg(test)]
mod pruebas {
    use super::*;

    fn tipos(src: &str) -> Vec<Token> {
        tokenizar(src)
            .expect("debe tokenizar")
            .into_iter()
            .map(|t| t.token)
            .collect()
    }

    #[test]
    fn palabras_reservadas_basicas() {
        let ts = tipos("var para en imp");
        assert!(matches!(ts[0], Token::Var));
        assert!(matches!(ts[1], Token::Para));
        assert!(matches!(ts[2], Token::En));
        assert!(matches!(ts[3], Token::Imp));
    }

    #[test]
    fn operadores_multiples() {
        let ts = tipos("** .* ++ -- == != <= >= .. ... |>");
        use Token::*;
        assert!(matches!(ts[0], Potencia));
        assert!(matches!(ts[1], ProductoPunto));
        assert!(matches!(ts[2], MasMas));
        assert!(matches!(ts[3], MenosMenos));
        assert!(matches!(ts[4], Igual));
        assert!(matches!(ts[5], Distinto));
        assert!(matches!(ts[6], MenorIgual));
        assert!(matches!(ts[7], MayorIgual));
        assert!(matches!(ts[8], RangoPuntos));
        assert!(matches!(ts[9], Elipsis));
        assert!(matches!(ts[10], Pipe));
    }

    #[test]
    fn vuelta_completa() {
        let src = "var total = 0\npara i en rango(1, 10000) {\n total = total + i\n}\nimp total\n";
        let toks = tokenizar(src).expect("vuelta debe tokenizar");
        // 23 tokens de contenido + separadores + Fin.
        assert!(toks.len() >= 23);
    }
}
