//! Motor de gráficos para MICELIO basado en el crate `image`.
//!
//! Proporciona las primitivas `__grafico_*` que `stdlib/grafico.mice`
//! invoca. El estado se mantiene en un `Mutex<Option<EstadoGrafico>>`
//! global para ser accesible desde las funciones nativas.
//!
//! Diseño:
//! - Un único gráfico activo a la vez (coherente con el intérprete de
//!   referencia que usa un estado global `_PLOT_STATE`).
//! - Coordenadas del usuario se transforman a píxeles mediante los límites
//!   establecidos en `__grafico_reset`.
//! - El texto se renderiza con un bitmap mínimo (5x7) para no depender
//!   de fuentes TrueType del sistema.
#![allow(dead_code)]

use crate::valor::Valor;
use image::{ImageBuffer, Rgb, RgbImage};
use std::sync::Mutex;

/// Estado del gráfico activo.
pub struct EstadoGrafico {
    pub ancho: u32,
    pub alto: u32,
    pub margen: u32,
    pub img: RgbImage,
    pub xmin: f64,
    pub xmax: f64,
    pub ymin: f64,
    pub ymax: f64,
    pub titulo: String,
    pub xlabel: String,
    pub ylabel: String,
    pub color_linea: (u8, u8, u8),
}

static ESTADO: Mutex<Option<EstadoGrafico>> = Mutex::new(None);

pub fn con_estado<F, R>(f: F) -> R
where
    F: FnOnce(&mut EstadoGrafico) -> R,
{
    let mut g = ESTADO.lock().unwrap();
    let e = g.as_mut().expect("No hay gráfico activo");
    f(e)
}

/// Transforma coordenada X del usuario a píxel.
pub fn a_px(e: &EstadoGrafico, x: f64) -> i32 {
    let area = (e.ancho - 2 * e.margen) as f64;
    let t = (x - e.xmin) / (e.xmax - e.xmin);
    e.margen as i32 + (t * area) as i32
}

/// Transforma coordenada Y del usuario a píxel (invertida).
pub fn a_py(e: &EstadoGrafico, y: f64) -> i32 {
    let area = (e.alto - 2 * e.margen) as f64;
    let t = (y - e.ymin) / (e.ymax - e.ymin);
    (e.alto as i32 - e.margen as i32) - (t * area) as i32
}

pub fn color(r: i64, g: i64, b: i64) -> Rgb<u8> {
    Rgb([
        r.clamp(0, 255) as u8,
        g.clamp(0, 255) as u8,
        b.clamp(0, 255) as u8,
    ])
}

pub fn poner_pixel(img: &mut RgbImage, x: i32, y: i32, c: Rgb<u8>) {
    if x >= 0 && y >= 0 && (x as u32) < img.width() && (y as u32) < img.height() {
        img.put_pixel(x as u32, y as u32, c);
    }
}

pub fn linea_bresenham(
    img: &mut RgbImage,
    x0: i32,
    y0: i32,
    x1: i32,
    y1: i32,
    c: Rgb<u8>,
    grosor: i32,
) {
    let dx = (x1 - x0).abs();
    let dy = (y1 - y0).abs();
    let sx = if x0 < x1 { 1 } else { -1 };
    let sy = if y0 < y1 { 1 } else { -1 };
    let mut err = dx - dy;
    let mut x = x0;
    let mut y = y0;
    loop {
        for gy in -grosor..=grosor {
            for gx in -grosor..=grosor {
                poner_pixel(img, x + gx, y + gy, c);
            }
        }
        if x == x1 && y == y1 {
            break;
        }
        let e2 = 2 * err;
        if e2 > -dy {
            err -= dy;
            x += sx;
        }
        if e2 < dx {
            err += dx;
            y += sy;
        }
    }
}

pub fn circulo_impl(img: &mut RgbImage, cx: i32, cy: i32, r: i32, c: Rgb<u8>, relleno: bool) {
    if r <= 0 {
        poner_pixel(img, cx, cy, c);
        return;
    }
    if relleno {
        for y in -r..=r {
            for x in -r..=r {
                if x * x + y * y <= r * r {
                    poner_pixel(img, cx + x, cy + y, c);
                }
            }
        }
    } else {
        // Algoritmo de punto medio.
        let mut x = r;
        let mut y = 0;
        let mut err = 0;
        while x >= y {
            poner_pixel(img, cx + x, cy + y, c);
            poner_pixel(img, cx + y, cy + x, c);
            poner_pixel(img, cx - y, cy + x, c);
            poner_pixel(img, cx - x, cy + y, c);
            poner_pixel(img, cx - x, cy - y, c);
            poner_pixel(img, cx - y, cy - x, c);
            poner_pixel(img, cx + y, cy - x, c);
            poner_pixel(img, cx + x, cy - y, c);
            y += 1;
            if err <= 0 {
                err += 2 * y + 1;
            } else {
                x -= 1;
                err -= 2 * x + 1;
            }
        }
    }
}

pub fn rectangulo_impl(
    img: &mut RgbImage,
    x: i32,
    y: i32,
    w: i32,
    h: i32,
    c: Rgb<u8>,
    relleno: bool,
) {
    if relleno {
        for yy in y..y + h {
            for xx in x..x + w {
                poner_pixel(img, xx, yy, c);
            }
        }
    } else {
        for xx in x..x + w {
            poner_pixel(img, xx, y, c);
            poner_pixel(img, xx, y + h - 1, c);
        }
        for yy in y..y + h {
            poner_pixel(img, x, yy, c);
            poner_pixel(img, x + w - 1, yy, c);
        }
    }
}

// Bitmap 5x7 para texto básico.
const FONT_5X7: &str = "\
  #  \
 # # \
#   #\
#   #\
#####\
#   #\
#   #\
     \
  #  \
 # # \
#   #\
#   #\
#####\
#   #\
#   #\
";

pub fn dibujar_texto(img: &mut RgbImage, x: i32, y: i32, texto: &str, c: Rgb<u8>, escala: i32) {
    // Renderizado mínimo: cada carácter es un bloque 6x8 con glifo simplificado.
    // Se usa un patrón genérico para mantener el binario autocontenido.
    let mut cx = x;
    for ch in texto.chars() {
        // Glifo básico: dibuja el carácter como un rectángulo pequeño
        // con el código ASCII para distinguir caracteres.
        let code = ch as i32;
        // Patrón simple basado en el código del carácter.
        for dy in 0..7 {
            for dx in 0..5 {
                let bit = (code >> (dy * 5 + dx)) & 1;
                if bit == 1 || (dx == 2 && dy == 3) {
                    for sy in 0..escala {
                        for sx in 0..escala {
                            poner_pixel(img, cx + dx * escala + sx, y + dy * escala + sy, c);
                        }
                    }
                }
            }
        }
        cx += 6 * escala;
    }
}

// ---- Primitivas nativas expuestas a Micelio ----

pub fn reset(args: &[crate::valor::Valor]) -> Result<crate::valor::Valor, String> {
    use crate::valor::Valor;
    if args.len() < 3 {
        return Err("__grafico_reset requiere ancho, alto, margen".to_string());
    }
    let ancho = args[0].a_numero()? as u32;
    let alto = args[1].a_numero()? as u32;
    let margen = args[2].a_numero()? as u32;
    let img = ImageBuffer::from_pixel(ancho, alto, Rgb([255, 255, 255]));
    let mut g = ESTADO.lock().unwrap();
    eprintln!("[reset] setting state ancho={} alto={}", ancho, alto);
    *g = Some(EstadoGrafico {
        ancho,
        alto,
        margen,
        img,
        xmin: 0.0,
        xmax: 1.0,
        ymin: 0.0,
        ymax: 1.0,
        titulo: String::new(),
        xlabel: String::new(),
        ylabel: String::new(),
        color_linea: (0, 0, 0),
    });
    Ok(Valor::Nulo)
}

pub fn set_pixel(args: &[crate::valor::Valor]) -> Result<crate::valor::Valor, String> {
    use crate::valor::Valor;
    if args.len() < 5 {
        return Err("__grafico_set_pixel requiere x, y, r, g, b".to_string());
    }
    let x = args[0].a_numero()? as i32;
    let y = args[1].a_numero()? as i32;
    let r = args[2].a_numero()? as i64;
    let g = args[3].a_numero()? as i64;
    let b = args[4].a_numero()? as i64;
    con_estado(|e| {
        poner_pixel(&mut e.img, x, y, color(r, g, b));
    });
    Ok(Valor::Nulo)
}

pub fn linea(args: &[crate::valor::Valor]) -> Result<crate::valor::Valor, String> {
    use crate::valor::Valor;
    if args.len() < 8 {
        return Err("__grafico_linea requiere x0, y0, x1, y1, r, g, b, grosor".to_string());
    }
    let x0 = args[0].a_numero()? as i32;
    let y0 = args[1].a_numero()? as i32;
    let x1 = args[2].a_numero()? as i32;
    let y1 = args[3].a_numero()? as i32;
    let r = args[4].a_numero()? as i64;
    let g = args[5].a_numero()? as i64;
    let b = args[6].a_numero()? as i64;
    let grosor = args[7].a_numero()? as i32;
    con_estado(|e| {
        linea_bresenham(&mut e.img, x0, y0, x1, y1, color(r, g, b), grosor);
    });
    Ok(Valor::Nulo)
}

pub fn rectangulo(args: &[crate::valor::Valor]) -> Result<crate::valor::Valor, String> {
    use crate::valor::Valor;
    if args.len() < 8 {
        return Err("__grafico_rectangulo requiere x, y, w, h, r, g, b, relleno".to_string());
    }
    let x = args[0].a_numero()? as i32;
    let y = args[1].a_numero()? as i32;
    let w = args[2].a_numero()? as i32;
    let h = args[3].a_numero()? as i32;
    let r = args[4].a_numero()? as i64;
    let g = args[5].a_numero()? as i64;
    let b = args[6].a_numero()? as i64;
    let relleno = args[7].es_verdadero();
    con_estado(|e| {
        rectangulo_impl(&mut e.img, x, y, w, h, color(r, g, b), relleno);
    });
    Ok(Valor::Nulo)
}

pub fn circulo(args: &[crate::valor::Valor]) -> Result<crate::valor::Valor, String> {
    use crate::valor::Valor;
    if args.len() < 7 {
        return Err("__grafico_circulo requiere cx, cy, radio, r, g, b, relleno".to_string());
    }
    let cx = args[0].a_numero()? as i32;
    let cy = args[1].a_numero()? as i32;
    let radio = args[2].a_numero()? as i32;
    let r = args[3].a_numero()? as i64;
    let g = args[4].a_numero()? as i64;
    let b = args[5].a_numero()? as i64;
    let relleno = args[6].es_verdadero();
    con_estado(|e| {
        circulo_impl(&mut e.img, cx, cy, radio, color(r, g, b), relleno);
    });
    Ok(Valor::Nulo)
}

pub fn texto(args: &[crate::valor::Valor]) -> Result<crate::valor::Valor, String> {
    use crate::valor::Valor;
    if args.len() < 7 {
        return Err("__grafico_texto requiere x, y, texto, r, g, b, tam".to_string());
    }
    let x = args[0].a_numero()? as i32;
    let y = args[1].a_numero()? as i32;
    let txt = args[2].a_texto();
    let r = args[3].a_numero()? as i64;
    let g = args[4].a_numero()? as i64;
    let b = args[5].a_numero()? as i64;
    let tam = args[6].a_numero()? as i32;
    con_estado(|e| {
        dibujar_texto(&mut e.img, x, y, &txt, color(r, g, b), tam.max(1));
    });
    Ok(Valor::Nulo)
}

pub fn poligono(args: &[crate::valor::Valor]) -> Result<crate::valor::Valor, String> {
    use crate::valor::Valor;
    // Acepta una lista de puntos [x,y] y colores. Implementación simplificada:
    // dibuja líneas entre puntos consecutivos.
    if args.is_empty() {
        return Ok(Valor::Nulo);
    }
    // Primer arg: lista de puntos. Resto: r, g, b, relleno.
    let pts = args[0].materializar()?;
    let r = args
        .get(1)
        .map(|v| v.a_numero().unwrap_or(0.0) as i64)
        .unwrap_or(0);
    let g = args
        .get(2)
        .map(|v| v.a_numero().unwrap_or(0.0) as i64)
        .unwrap_or(0);
    let b = args
        .get(3)
        .map(|v| v.a_numero().unwrap_or(0.0) as i64)
        .unwrap_or(0);
    let mut puntos: Vec<(i32, i32)> = Vec::new();
    for p in pts {
        if let Valor::Lista(pair) = p {
            let pb = pair.borrow();
            if pb.len() >= 2 {
                puntos.push((
                    pb[0].a_numero().unwrap_or(0.0) as i32,
                    pb[1].a_numero().unwrap_or(0.0) as i32,
                ));
            }
        }
    }
    con_estado(|e| {
        for w in puntos.windows(2) {
            linea_bresenham(
                &mut e.img,
                w[0].0,
                w[0].1,
                w[1].0,
                w[1].1,
                color(r, g, b),
                1,
            );
        }
        if puntos.len() > 2 {
            let first = puntos[0];
            let last = puntos[puntos.len() - 1];
            linea_bresenham(
                &mut e.img,
                last.0,
                last.1,
                first.0,
                first.1,
                color(r, g, b),
                1,
            );
        }
    });
    Ok(Valor::Nulo)
}

pub fn guardar(args: &[crate::valor::Valor]) -> Result<crate::valor::Valor, String> {
    use crate::valor::Valor;
    if args.is_empty() {
        return Err("__grafico_guardar requiere path".to_string());
    }
    let path = args[0].a_texto();
    // Actualiza título/etiquetas si se proporcionan.
    if args.len() >= 2 {
        let t = args[1].a_texto();
        con_estado(|e| e.titulo = t);
    }
    if args.len() >= 3 {
        let x = args[2].a_texto();
        con_estado(|e| e.xlabel = x);
    }
    if args.len() >= 4 {
        let y = args[3].a_texto();
        con_estado(|e| e.ylabel = y);
    }
    // Transforma coordenadas del usuario a píxeles para ejes.
    con_estado(|e| {
        // Dibuja ejes simples.
        let left = e.margen as i32;
        let right = e.ancho as i32 - e.margen as i32;
        let top = e.margen as i32;
        let bottom = e.alto as i32 - e.margen as i32;
        linea_bresenham(&mut e.img, left, bottom, right, bottom, Rgb([0, 0, 0]), 2);
        linea_bresenham(&mut e.img, left, top, left, bottom, Rgb([0, 0, 0]), 2);
    });
    // Guarda.
    let img = {
        let g = ESTADO.lock().unwrap();
        g.as_ref().map(|e| e.img.clone())
    };
    if let Some(img) = img {
        if let Some(parent) = std::path::Path::new(&path).parent() {
            if !parent.as_os_str().is_empty() {
                let _ = std::fs::create_dir_all(parent);
            }
        }
        img.save(&path)
            .map_err(|e| format!("No se pudo guardar '{path}': {e}"))?;
    }
    Ok(Valor::Texto(path))
}

pub fn mostrar(args: &[crate::valor::Valor]) -> Result<crate::valor::Valor, String> {
    // En modo nativo, mostrar equivale a guardar y reportar la ruta.
    guardar(args)
}

pub fn limpiar(_: &[crate::valor::Valor]) -> Result<crate::valor::Valor, String> {
    con_estado(|e| {
        e.img = ImageBuffer::from_pixel(e.ancho, e.alto, Rgb([255, 255, 255]));
    });
    Ok(Valor::Nulo)
}

pub fn draw_axes(_args: &[crate::valor::Valor]) -> Result<crate::valor::Valor, String> {
    Ok(Valor::Nulo)
}
