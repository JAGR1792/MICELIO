//! Punto de entrada del binario `micesito`.
//!
//! Responsabilidades:
//! - Exponer la interfaz de línea de comandos para ejecutar el banco de
//!   pruebas de rendimiento de la vuelta (§4.6 del ROADMAP).
//! - Demostrar el analizador léxico sin ANTLR sobre un programa representativo.
//!
//! El diseño prioriza la reproducibilidad de las mediciones: calentamiento
//! previo, uso de `black_box` para evitar el plegado de constantes y selección
//! del mejor tiempo entre varias pasadas.

use std::hint::black_box;
use std::time::Instant;

mod lexer;

// Módulo de transición hacia la implementación completa del lenguaje.
// Se permite código sin uso temporalmente hasta la integración del
// analizador sintáctico y el intérprete en los próximos commits.
#[allow(dead_code)]
mod ast;

/// Suma el intervalo semiabierto `[inicio, fin)` mediante un iterador perezoso.
///
/// Esta función es el equivalente nativo del programa MICELIO:
///
/// ```text
/// var total = 0
/// para i en rango(inicio, fin) { total = total + i }
/// ```
///
/// A diferencia de `rango()` en `builtins.mice`, que materializa una lista,
/// aquí no se realiza ninguna asignación en el montículo. Con `opt-level=3`,
/// LLVM reduce el bucle a la secuencia mínima de sumas, idéntica a la de C.
///
/// Se utiliza `wrapping_add` para definir el desbordamiento como aritmética
/// modular, coherente con la semántica de enteros de 64 bits del lenguaje.
#[inline(never)]
fn vuelta_nativa(inicio: i64, fin: i64) -> i64 {
    let mut total: i64 = 0;
    for i in inicio..fin {
        total = total.wrapping_add(black_box(i));
    }
    total
}

/// Mide el mejor tiempo de `vuelta_nativa` entre cinco ejecuciones.
///
/// El calentamiento previo y la selección del mínimo reducen el ruido por
/// frecuencia dinámica y planificación del sistema operativo.
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

/// Tokeniza el programa de la vuelta y reporta el número de tokens y el tiempo.
///
/// Cualquier error léxico se informa por salida estándar de errores sin
/// interrumpir el resto del banco de pruebas.
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
        Err(e) => {
            eprintln!("[lexer] error en posición {}: {}", e.posicion, e.mensaje);
        }
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() > 1 && args[1] == "--lexer" {
        demo_lexer();
        return;
    }

    println!("MICELIO-rs, vuelta §4.6 | release -O3 + LTO + codegen-units=1");
    demo_lexer();

    // Calentamiento para estabilizar la frecuencia del procesador.
    let _ = vuelta_nativa(1, 1000);

    let casos = [(1, 10_000), (1, 1_000_000), (1, 10_000_000)];
    for (a, b) in casos {
        let (r, ms) = medir_vuelta(a, b);
        println!("rango({a},{b}) -> total={r} en {ms:.3}ms");
    }

    println!("\nNota: rango(a,b) es un intervalo perezoso, sin lista intermedia.");
}
