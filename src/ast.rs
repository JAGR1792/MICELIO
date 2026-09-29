//! Árbol de sintaxis abstracta (HIR) de MICELIO.
//!
//! El AST es la representación intermedia entre el analizador sintáctico
//! y el intérprete. Se diseña para minimizar la indirección en los caminos
//! críticos: los nodos frecuentes (`Expr::Variable`, `Expr::Literal`) son
//! compactos y las listas de sentencias se almacenan en `Vec` contiguos
//! para favorecer la localidad de caché durante la ejecución.

/// Programa completo: secuencia de sentencias de nivel superior.
#[derive(Debug, Clone)]
pub struct Programa {
    pub sentencias: Vec<Sent>,
}

/// Sentencia del lenguaje. Corresponde a `statement` en `Micelio.g4`.
#[derive(Debug, Clone)]
pub enum Sent {
    /// `var a, b = 1, 2`. `valores` puede estar vacío (declaración sin inicializar).
    DeclVar {
        nombres: Vec<String>,
        valores: Vec<Expr>,
    },
    /// `const X = expr`.
    DeclConst {
        nombre: String,
        valor: Expr,
    },
    /// `objetivo = expr`, donde el objetivo admite indexación encadenada.
    Asign {
        base: String,
        indices: Vec<Expr>,
        valor: Expr,
    },
    /// Asignación múltiple `__asignar_multi("a,b", expr)` (forma desazucarada).
    AsignMulti {
        nombres: Vec<String>,
        valor: Expr,
    },
    /// Sentencia de expresión (llamadas, operaciones con efectos).
    Expr(Expr),
    /// `regresa expr?`.
    Retorna(Option<Expr>),
    Romper,
    Continuar,
    /// `importar "ruta" como alias`.
    Importar {
        ruta: String,
        alias: Option<String>,
    },
    /// `leer x`.
    Leer {
        nombre: String,
    },
    /// `imp expr`.
    Imp(Expr),
    /// `si (cond) { } sino_si ... sino ...`.
    Si {
        cond: Expr,
        entonces: Vec<Sent>,
        sino_si: Vec<(Expr, Vec<Sent>)>,
        sino_: Option<Vec<Sent>>,
    },
    /// `segun (expr) { caso ...: defecto: ... }`.
    Segun {
        expr: Expr,
        casos: Vec<(Expr, Vec<Sent>)>,
        defecto: Option<Vec<Sent>>,
    },
    /// `mientras (cond) { }`.
    Mientras {
        cond: Expr,
        cuerpo: Vec<Sent>,
    },
    /// `para x en iterable { }`.
    ParaEn {
        var: String,
        iterable: Expr,
        cuerpo: Vec<Sent>,
    },
    /// `para i = inicio hasta fin (inc paso)? { }`. El límite es inclusivo,
    /// coherente con el intérprete de referencia.
    ParaHasta {
        var: String,
        inicio: Expr,
        fin: Expr,
        paso: Option<Expr>,
        cuerpo: Vec<Sent>,
    },
    /// `funcion nombre(params) { }`.
    DefFuncion {
        nombre: String,
        params: Vec<Param>,
        cuerpo: Vec<Sent>,
    },
    /// Bloque `{ ... }` con ámbito propio si declara variables.
    Bloque(Vec<Sent>),
}

/// Parámetro formal. Soporta `x`, `*args` y `**kwargs`.
#[derive(Debug, Clone)]
pub struct Param {
    pub nombre: String,
    pub tipo: TipoParam,
}

/// Clasificación del parámetro según su prefijo sintáctico.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TipoParam {
    Normal,
    Args,
    Kwargs,
}

/// Expresión del lenguaje. Corresponde a `expr` en `Micelio.g4`.
#[derive(Debug, Clone)]
pub enum Expr {
    Entero(i64),
    Flotante(f64),
    Texto(String),
    Logico(bool),
    Nulo,
    Variable(String),
    Unaria {
        op: OpUn,
        expr: Box<Expr>,
    },
    Binaria {
        op: OpBin,
        izq: Box<Expr>,
        der: Box<Expr>,
    },
    /// `f(args, nombre=valor)`.
    Llamada {
        callee: Box<Expr>,
        args: Vec<ArgLlamada>,
    },
    /// `base[indice]`.
    Indice {
        base: Box<Expr>,
        indice: Box<Expr>,
    },
    /// `base.miembro`. La llamada a método se representa como
    /// `Llamada { callee: Acceso, .. }`.
    Acceso {
        base: Box<Expr>,
        campo: String,
    },
    Lista(Vec<ItemLista>),
    /// `dict(k:v, ...)` o `{k:v, ...}`.
    Dicc(Vec<(Expr, Expr)>),
    /// `set(a, b)` evaluado como lista con semántica de conjunto en
    /// operaciones de pertenencia.
    Conjunto(Vec<Expr>),
    /// `matriz(expr)`.
    Matriz(Box<Expr>),
    /// `funcion (params) { }` anónima.
    FuncionAnon {
        params: Vec<Param>,
        cuerpo: Vec<Sent>,
    },
}

/// Elemento de lista: simple, propagación (`...x`) o rango (`a..b`).
#[derive(Debug, Clone)]
pub enum ItemLista {
    Simple(Expr),
    Propaga(Expr),
    Rango(Expr, Expr),
}

/// Argumento de llamada: posicional o nombrado.
#[derive(Debug, Clone)]
pub enum ArgLlamada {
    Pos(Expr),
    Nom { nombre: String, valor: Expr },
}

/// Operador binario.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum OpBin {
    Suma,
    Resta,
    Mul,
    Div,
    Mod,
    Pot,
    ProdPunto,
    Igual,
    Distinto,
    Menor,
    MenorIgual,
    Mayor,
    MayorIgual,
    Y,
    O,
    In,
    Pipe,
}

/// Operador unario, incluidos pre/post incremento.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum OpUn {
    Neg,
    No,
    PreInc,
    PreDec,
    PostInc,
    PostDec,
}
