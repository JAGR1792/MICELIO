//! Punto de entrada del binario `micesito`.
//!
//! Funciones:
//! - Ejecución de programas `.mice` con el intérprete nativo de alto
//!   rendimiento (`micesito programa.mice`).
//! - Banco de pruebas de la vuelta §4.6 del ROADMAP (`--bench`).
//! - Demostración del analizador léxico sin ANTLR (`--lexer`).
//!
//! La medición de rendimiento utiliza calentamiento previo, barreras
//! `black_box` contra el plegado de constantes y selección del mejor
//! tiempo entre varias pasadas para reducir el ruido del sistema.

use std::hint::black_box;
use std::time::Instant;

mod ast;
mod interp;
mod lexer;
mod parser;
mod valor;

/// Suma el intervalo semiabierto `[inicio, fin)` mediante un iterador perezoso.
///
/// Equivalente nativo del programa MICELIO:
///
/// ```text
/// var total = 0
/// para i en rango(inicio, fin) { total = total + i }
/// ```
///
/// A diferencia de `rango()` en `builtins.mice`, no materializa ninguna
/// lista. Con `opt-level=3`, LLVM lo reduce a la secuencia mínima de sumas.
#[inline(never)]
fn vuelta_nativa(inicio: i64, fin: i64) -> i64 {
    let mut total: i64 = 0;
    for i in inicio..fin {
        total = total.wrapping_add(black_box(i));
    }
    total
}

/// Mide el mejor tiempo de `vuelta_nativa` entre cinco ejecuciones.
fn medir_vuelta(inicio: i64, fin: i64) -> (i64, f64) {
    let mut mejor = f64::MAX;
    let mut resultado = 0;
    for _ in 0..5 {
        let a = black_box(inicio);
        let b = black_box(fin);
        let t0 = Instant::now();
        resultado = vuelta_nativa(a, b);
        black_box(resultado);
        let ms = t0.elapsed().as_secs_f64() * 1000.0;
        if ms < mejor {
            mejor = ms;
        }
    }
    (resultado, mejor)
}

/// Ejecuta el banco de pruebas de rendimiento.
fn bench() {
    println!("MICELIO-rs, vuelta §4.6 | release -O3 + LTO + codegen-units=1");
    demo_lexer();
    let _ = vuelta_nativa(1, 1000);
    for (a, b) in [(1, 10_000), (1, 1_000_000), (1, 10_000_000)] {
        let (r, ms) = medir_vuelta(a, b);
        println!("rango({a},{b}) -> total={r} en {ms:.3}ms");
    }
    println!("\nNota: rango(a,b) es un intervalo perezoso, sin lista intermedia.");
}

/// Tokeniza el programa de la vuelta y reporta el coste del análisis léxico.
fn demo_lexer() {
    let fuente = "var total = 0\npara i en rango(1, 10000) {\n total = total + i\n}\nimp total\n";
    let t0 = Instant::now();
    match lexer::tokenizar(fuente) {
        Ok(tokens) => {
            let us = t0.elapsed().as_micros();
            println!(
                "[lexer] tokens={} en {}µs (una pasada, sin expresiones regulares)",
                tokens.len(),
                us
            );
        }
        Err(e) => eprintln!("[lexer] error en posición {}: {}", e.posicion, e.mensaje),
    }
}

/// Ejecuta un archivo `.mice` y propaga el código de salida.
fn ejecutar_archivo(ruta: &str) -> i32 {
    let base = dir_de(ruta);
    let mut it = interp::Interprete::new(base);
    match it.ejecutar_archivo(ruta) {
        Ok(_) => 0,
        Err(e) => {
            eprintln!("Error de ejecución: {e}");
            1
        }
    }
}

fn dir_de(ruta: &str) -> String {
    match ruta.rfind('/') {
        Some(i) => ruta[..i].to_string(),
        None => ".".to_string(),
    }
}

fn ayuda() {
    println!("Uso: micesito [opciones] [programa.mice]");
    println!("  programa.mice   Ejecuta un programa MICELIO");
    println!("  --bench         Banco de pruebas de la vuelta §4.6");
    println!("  --lexer         Demostración del analizador léxico");
    println!("  --help, -h      Esta ayuda");
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() == 1 {
        bench();
        return;
    }
    match args[1].as_str() {
        "--bench" => bench(),
        "--lexer" => demo_lexer(),
        "--help" | "-h" => ayuda(),
        ruta => std::process::exit(ejecutar_archivo(ruta)),
    }
}
