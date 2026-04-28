from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import reduce as py_reduce
import json
import mimetypes
import os
import shutil
import subprocess
import sys
import tempfile
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Callable
from urllib.parse import parse_qs, urlparse


class MicelioRuntimeError(Exception):
    pass


class ReturnFlow(Exception):
    def __init__(self, value: Any):
        super().__init__()
        self.value = value


class BreakFlow(Exception):
    pass


class ContinueFlow(Exception):
    pass


class Environment:
    def __init__(self, parent: "Environment | None" = None):
        self.parent = parent
        self.values: dict[str, Any] = {}
        self.constants: set[str] = set()

    def define(self, name: str, value: Any, is_const: bool = False) -> None:
        if name in self.values:
            raise MicelioRuntimeError(f"'{name}' ya esta definido en este ambito")
        self.values[name] = value
        if is_const:
            self.constants.add(name)

    def get(self, name: str) -> Any:
        env: Environment | None = self
        while env is not None:
            if name in env.values:
                return env.values[name]
            env = env.parent
        raise MicelioRuntimeError(f"Variable '{name}' no definida")

    def assign(self, name: str, value: Any) -> None:
        env: Environment | None = self
        while env is not None:
            if name in env.values:
                if name in env.constants:
                    raise MicelioRuntimeError(f"No se puede reasignar la constante '{name}'")
                env.values[name] = value
                return
            env = env.parent
        raise MicelioRuntimeError(f"Variable '{name}' no definida")


@dataclass
class FunctionValue:
    """
    Representa una función definida en Micelio.
    Soporta parámetros normales, *args (variádicos) y **kwargs (nombrados).
    """
    name: str | None
    params: list[str]              # Parámetros normales
    args_param: str | None         # Nombre del parámetro *args (None si no existe)
    kwargs_param: str | None       # Nombre del parámetro **kwargs (None si no existe)
    body_ctx: Any                  # Contexto ANTLR del cuerpo
    closure: Environment           # Entorno de cierre

    def call(self, args: list[Any], kwargs: dict[str, Any], 
             call_eval: Callable[[Any, Environment], Any]) -> Any:
        """
        Ejecuta la función con los argumentos dados.
        
        - args: argumentos posicionales
        - kwargs: argumentos nombrados (diccionario)
        - call_eval: función para evaluar el cuerpo en un entorno
        """
        # Crear entorno local
        local_env = Environment(self.closure)
        
        # Asignar parámetros normales
        for i, param in enumerate(self.params):
            if i < len(args):
                local_env.define(param, args[i])
            else:
                fname = self.name or "función anónima"
                raise MicelioRuntimeError(
                    f"{fname} esperaba {len(self.params)} argumento(s), recibió {len(args)}"
                )
        
        # Empaquetar argumentos extras en *args
        if self.args_param:
            extra_args = args[len(self.params):]
            local_env.define(self.args_param, extra_args)
        elif len(args) > len(self.params):
            fname = self.name or "función anónima"
            raise MicelioRuntimeError(
                f"{fname} no acepta más de {len(self.params)} argumento(s)"
            )
        
        # Empaquetar argumentos nombrados en **kwargs
        if self.kwargs_param:
            local_env.define(self.kwargs_param, kwargs)
        elif kwargs:
            fname = self.name or "función anónima"
            kwargs_str = ", ".join(kwargs.keys())
            raise MicelioRuntimeError(
                f"{fname} no acepta argumentos nombrados: {kwargs_str}"
            )
        
        # Ejecutar el cuerpo en el entorno local
        try:
            return call_eval(self.body_ctx, local_env)
        except ReturnFlow as ret:
            return ret.value


class BoundMethod:
    def __init__(self, obj: Any, name: str):
        self.obj = obj
        self.name = name

    def __call__(self, *args: Any) -> Any:
        if isinstance(self.obj, list):
            if self.name == "agregar":
                if len(args) != 1:
                    raise MicelioRuntimeError("agregar() requiere 1 argumento")
                self.obj.append(args[0])
                return None
            if self.name == "extender":
                if len(args) != 1:
                    raise MicelioRuntimeError("extender() requiere 1 argumento")
                if not isinstance(args[0], list):
                    raise MicelioRuntimeError("extender() requiere una lista")
                self.obj.extend(args[0])
                return None
            if self.name == "quitar":
                if len(args) != 1:
                    raise MicelioRuntimeError("quitar() requiere 1 argumento")
                self.obj.remove(args[0])
                return None
            if self.name == "insertar":
                if len(args) != 2:
                    raise MicelioRuntimeError("insertar() requiere 2 argumentos")
                self.obj.insert(int(args[0]), args[1])
                return None
            if self.name == "longitud":
                if args:
                    raise MicelioRuntimeError("longitud() no recibe argumentos")
                return len(self.obj)

        if isinstance(self.obj, set):
            if self.name == "agregar":
                if len(args) != 1:
                    raise MicelioRuntimeError("agregar() requiere 1 argumento")
                self.obj.add(args[0])
                return None
            if self.name == "quitar":
                if len(args) != 1:
                    raise MicelioRuntimeError("quitar() requiere 1 argumento")
                self.obj.discard(args[0])
                return None

        if isinstance(self.obj, dict):
            if self.name == "claves":
                if args:
                    raise MicelioRuntimeError("claves() no recibe argumentos")
                return list(self.obj.keys())
            if self.name == "valores":
                if args:
                    raise MicelioRuntimeError("valores() no recibe argumentos")
                return list(self.obj.values())
            if self.name == "items":
                if args:
                    raise MicelioRuntimeError("items() no recibe argumentos")
                return list(self.obj.items())

        if isinstance(self.obj, str):
            if self.name == "longitud":
                if args:
                    raise MicelioRuntimeError("longitud() no recibe argumentos")
                return len(self.obj)
            if self.name in ("separar", "split"):
                if len(args) > 1:
                    raise MicelioRuntimeError("separar() recibe 0 o 1 argumento")
                if len(args) == 0:
                    return self.obj.split()
                return self.obj.split(str(args[0]))

        raise MicelioRuntimeError(f"Metodo '{self.name}' no soportado para {type(self.obj).__name__}")


def to_number(value: Any, base: int = 10) -> float:
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        txt = value.strip().lower()
        if txt.startswith("0b"):
            return float(int(txt, 2))
        if txt.startswith("0o"):
            return float(int(txt, 8))
        if txt.startswith("0x"):
            return float(int(txt, 16))
        return float(int(txt, base)) if base != 10 else float(txt)
    raise MicelioRuntimeError(f"No se puede convertir {type(value).__name__} a numero")


def int_to_base(n: int, base: int, uppercase: bool = False) -> str:
    if not (2 <= base <= 36):
        raise MicelioRuntimeError("La base debe estar entre 2 y 36")
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    if uppercase:
        digits = digits.upper()
    if n == 0:
        return "0"
    neg = n < 0
    n = abs(n)
    out = []
    while n > 0:
        out.append(digits[n % base])
        n //= base
    rep = "".join(reversed(out))
    return f"-{rep}" if neg else rep


def to_text(value: Any, base: int = 10, mayusculas: bool = False) -> str:
    if isinstance(value, bool):
        return "verdadero" if value else "falso"
    if value is None:
        return "nulo"
    if isinstance(value, (int, float)) and base != 10:
        return int_to_base(int(value), int(base), uppercase=bool(mayusculas))
    return str(value)


def to_bool(value: Any) -> bool:
    return bool(value)


def to_int(value: Any, base: int = 10) -> int:
    return int(to_number(value, base=base))


def to_float(value: Any, base: int = 10) -> float:
    return float(to_number(value, base=base))


def to_char(value: Any) -> str:
    code = int(to_number(value))
    try:
        return chr(code)
    except ValueError as exc:
        raise MicelioRuntimeError("aCaracter() requiere un codigo Unicode valido") from exc


def to_code(value: Any) -> int:
    txt = str(value)
    if len(txt) != 1:
        raise MicelioRuntimeError("aCodigo() requiere exactamente un caracter")
    return ord(txt)


def to_base_with_digits(n: int, digits: str) -> str:
    if len(digits) < 2:
        raise MicelioRuntimeError("aBaseConDigitos() requiere al menos 2 digitos")
    if len(set(digits)) != len(digits):
        raise MicelioRuntimeError("aBaseConDigitos() requiere digitos unicos")
    base = len(digits)
    if n == 0:
        return digits[0]
    neg = n < 0
    n = abs(n)
    out = []
    while n > 0:
        out.append(digits[n % base])
        n //= base
    rep = "".join(reversed(out))
    return f"-{rep}" if neg else rep


def to_base_complement(n: int, base: int, bits: int, uppercase: bool = False) -> str:
    if bits <= 0:
        raise MicelioRuntimeError("aBaseComplemento() requiere bits > 0")
    min_val = -(2 ** (bits - 1))
    max_val = 2 ** (bits - 1) - 1
    if n < min_val or n > max_val:
        raise MicelioRuntimeError(
            "aBaseComplemento(): numero fuera de rango para el ancho de bits dado"
        )
    unsigned = n if n >= 0 else (2 ** bits + n)
    if base == 2:
        return format(unsigned, f"0{bits}b")
    return int_to_base(unsigned, base, uppercase=uppercase)


def to_base_fraction(number: Any, base: int, precision: int, uppercase: bool = False) -> str:
    if not (2 <= base <= 36):
        raise MicelioRuntimeError("aBaseFraccion(): la base debe estar entre 2 y 36")
    if precision < 0:
        raise MicelioRuntimeError("aBaseFraccion(): precision debe ser >= 0")

    num = to_number(number)
    neg = num < 0
    frac_num = Fraction(str(abs(num)))
    int_part = int(frac_num)
    frac_part = frac_num - int_part

    int_txt = int_to_base(int_part, base, uppercase=uppercase)
    if precision == 0:
        return f"-{int_txt}" if neg else int_txt
    if frac_part == 0:
        return f"-{int_txt}" if neg else int_txt

    symbols = "0123456789abcdefghijklmnopqrstuvwxyz"
    if uppercase:
        symbols = symbols.upper()

    out_frac: list[str] = []
    for _ in range(precision):
        frac_part *= base
        digit = int(frac_part)
        out_frac.append(symbols[digit])
        frac_part -= digit
        if frac_part == 0:
            break

    rep = int_txt + "." + "".join(out_frac)
    return f"-{rep}" if neg else rep


def matrix_mul(a: list[list[Any]], b: list[list[Any]]) -> list[list[float]]:
    if not a or not b:
        return []
    a_cols = len(a[0])
    b_rows = len(b)
    if a_cols != b_rows:
        raise MicelioRuntimeError("Dimensiones invalidas para multiplicacion matricial")
    b_cols = len(b[0])
    out = []
    for i in range(len(a)):
        row = []
        for j in range(b_cols):
            total = 0.0
            for k in range(a_cols):
                total += float(a[i][k]) * float(b[k][j])
            row.append(total)
        out.append(row)
    return out




def elementwise_mul(left: Any, right: Any) -> Any:
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        return left * right
    if isinstance(left, list) and isinstance(right, list):
        if len(left) != len(right):
            raise MicelioRuntimeError("Producto elemento a elemento requiere mismo tamano")
        return [elementwise_mul(l, r) for l, r in zip(left, right)]
    raise MicelioRuntimeError("Operacion .*, tipos no compatibles")


_PLOT_STATE = {
    "width": 800,
    "height": 500,
    "margin": 48,
    "pixels": [],
    "last_path": None,
}

_GUI_STYLE_STATE = {
    "theme": "ocean",
}


def _gtk_apply_theme(theme_name: str) -> bool:
    try:
        import gi

        gi.require_version("Gtk", "3.0")
        from gi.repository import Gdk, Gtk
    except Exception:
        return False

    palette = {
        "ocean": {
            "bg": "#0f172a",
            "surface": "#1e293b",
            "text": "#e2e8f0",
            "muted": "#93c5fd",
            "accent": "#22d3ee",
            "accent_text": "#06202a",
        },
        "forest": {
            "bg": "#0f1f17",
            "surface": "#1b4332",
            "text": "#e8f5e9",
            "muted": "#95d5b2",
            "accent": "#74c69d",
            "accent_text": "#0b1a13",
        },
        "sunset": {
            "bg": "#2b1a17",
            "surface": "#4a2c2a",
            "text": "#fff1e6",
            "muted": "#ffcab0",
            "accent": "#ff8c42",
            "accent_text": "#2b1303",
        },
        "mono": {
            "bg": "#1a1a1a",
            "surface": "#262626",
            "text": "#f4f4f5",
            "muted": "#d4d4d8",
            "accent": "#a1a1aa",
            "accent_text": "#18181b",
        },
    }

    theme = str(theme_name).strip().lower()
    if theme not in palette:
        theme = "ocean"

    p = palette[theme]
    css = f"""
    window {{
        background-color: {p['bg']};
        color: {p['text']};
    }}
    label {{
        color: {p['text']};
    }}
    frame {{
        border-color: {p['muted']};
    }}
    entry, textview text, textview {{
        background-color: {p['surface']};
        color: {p['text']};
        caret-color: {p['accent']};
    }}
    button {{
        background: {p['accent']};
        color: {p['accent_text']};
        border-radius: 8px;
        border: 1px solid {p['muted']};
        padding: 6px 10px;
    }}
    button:hover {{
        background: {p['muted']};
    }}
    """

    provider = Gtk.CssProvider()
    try:
        provider.load_from_data(css.encode("utf-8"))
        screen = Gdk.Screen.get_default()
        if screen is None:
            return False
        Gtk.StyleContext.add_provider_for_screen(
            screen,
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )
        return True
    except Exception:
        return False


def _gui_set_theme(name: Any) -> str:
    allowed = {"ocean", "forest", "sunset", "mono"}
    theme = str(name).strip().lower()
    if theme not in allowed:
        theme = "ocean"
    _GUI_STYLE_STATE["theme"] = theme
    return theme


def _gui_get_theme() -> str:
    return _GUI_STYLE_STATE["theme"]


def _gui_list_themes() -> list[str]:
    return ["ocean", "forest", "sunset", "mono"]


def _plot_reset(width: Any, height: Any, margin: Any) -> list[int]:
    w = int(to_number(width))
    h = int(to_number(height))
    m = int(to_number(margin))
    if w <= 0 or h <= 0:
        raise MicelioRuntimeError("Tamano de lienzo invalido")
    if m < 0 or m >= w // 2 or m >= h // 2:
        raise MicelioRuntimeError("Margen invalido para el tamano del lienzo")

    _PLOT_STATE["width"] = w
    _PLOT_STATE["height"] = h
    _PLOT_STATE["margin"] = m
    _PLOT_STATE["pixels"] = [
        [[255, 255, 255] for _ in range(w)]
        for _ in range(h)
    ]
    _PLOT_STATE["last_path"] = None
    return [w, h, m]


def _plot_set_pixel(x: Any, y: Any, r: Any, g: Any, b: Any) -> None:
    if not _PLOT_STATE["pixels"]:
        _plot_reset(800, 500, 48)

    px = int(to_number(x))
    py = int(to_number(y))
    rr = max(0, min(255, int(to_number(r))))
    gg = max(0, min(255, int(to_number(g))))
    bb = max(0, min(255, int(to_number(b))))

    w = _PLOT_STATE["width"]
    h = _PLOT_STATE["height"]
    if 0 <= px < w and 0 <= py < h:
        _PLOT_STATE["pixels"][py][px][0] = rr
        _PLOT_STATE["pixels"][py][px][1] = gg
        _PLOT_STATE["pixels"][py][px][2] = bb


def _plot_draw_axes() -> None:
    if not _PLOT_STATE["pixels"]:
        _plot_reset(800, 500, 48)

    left = _PLOT_STATE["margin"]
    right = _PLOT_STATE["width"] - _PLOT_STATE["margin"]
    top = _PLOT_STATE["margin"]
    bottom = _PLOT_STATE["height"] - _PLOT_STATE["margin"]

    for x in range(left, right + 1):
        _plot_set_pixel(x, bottom, 80, 80, 80)
    for y in range(top, bottom + 1):
        _plot_set_pixel(left, y, 80, 80, 80)


def _plot_guardar(path: Any, title: Any, xlabel: Any, ylabel: Any) -> str:
    if not _PLOT_STATE["pixels"]:
        _plot_reset(800, 500, 48)

    raw_path = str(path)
    out_path = raw_path
    if raw_path.lower().endswith(".png"):
        out_path = raw_path[:-4] + ".ppm"

    # Keep generated images organized under a dedicated folder
    # when the user provides only a filename.
    if os.path.dirname(out_path) == "":
        out_path = os.path.join("graficos", out_path)

    folder = os.path.dirname(out_path)
    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("P3\n")
        f.write(f"# {str(title)} | x:{str(xlabel)} y:{str(ylabel)}\n")
        f.write(f"{_PLOT_STATE['width']} {_PLOT_STATE['height']}\n255\n")
        for row in _PLOT_STATE["pixels"]:
            line = []
            for rr, gg, bb in row:
                line.append(f"{rr} {gg} {bb}")
            f.write(" ".join(line) + "\n")

    _PLOT_STATE["last_path"] = out_path
    return out_path


def _plot_last_path() -> str | None:
    return _PLOT_STATE["last_path"]


def _gtk_show_image_window(image_path: str, title: str, allow_save: bool) -> bool:
    try:
        import gi

        gi.require_version("Gtk", "3.0")
        gi.require_version("GdkPixbuf", "2.0")
        from gi.repository import GdkPixbuf, Gtk
    except Exception:
        return False

    try:
        original = GdkPixbuf.Pixbuf.new_from_file(image_path)
    except Exception:
        return False

    window = Gtk.Window(title=title)
    window.set_default_size(980, 720)
    _gtk_apply_theme(_GUI_STYLE_STATE["theme"])

    root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    root.set_border_width(8)
    window.add(root)

    view_state: dict[str, Any] = {
        "scale": 1.0,
        "fit_mode": False,
    }

    image = Gtk.Image.new_from_pixbuf(original)
    scroll = Gtk.ScrolledWindow()
    scroll.add(image)
    root.pack_start(scroll, True, True, 0)

    controls = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    root.pack_start(controls, False, False, 0)

    status = Gtk.Label(label="")
    status.set_xalign(0.0)
    root.pack_start(status, False, False, 0)

    def _set_status(extra: str = ""):
        base = (
            f"{original.get_width()}x{original.get_height()} px | "
            f"zoom {int(view_state['scale'] * 100)}%"
        )
        status.set_text(base if extra == "" else f"{base} | {extra}")

    def _apply_scale(new_scale: float):
        clamped = max(0.10, min(8.0, float(new_scale)))
        view_state["scale"] = clamped
        w = max(1, int(original.get_width() * clamped))
        h = max(1, int(original.get_height() * clamped))
        scaled = original.scale_simple(w, h, GdkPixbuf.InterpType.BILINEAR)
        if scaled is not None:
            image.set_from_pixbuf(scaled)
        _set_status()

    def _fit_to_window(*_args):
        alloc_w = scroll.get_allocated_width()
        alloc_h = scroll.get_allocated_height()
        if alloc_w <= 4 or alloc_h <= 4:
            return
        scale_w = alloc_w / max(1, original.get_width())
        scale_h = alloc_h / max(1, original.get_height())
        _apply_scale(min(scale_w, scale_h))

    def _on_zoom_in(_btn):
        view_state["fit_mode"] = False
        _apply_scale(view_state["scale"] * 1.25)

    def _on_zoom_out(_btn):
        view_state["fit_mode"] = False
        _apply_scale(view_state["scale"] / 1.25)

    def _on_zoom_reset(_btn):
        view_state["fit_mode"] = False
        _apply_scale(1.0)

    def _on_zoom_fit(_btn):
        view_state["fit_mode"] = True
        _fit_to_window()

    def _on_size_allocate(_widget, _alloc):
        if view_state["fit_mode"]:
            _fit_to_window()

    def _show_msg(msg: str):
        dlg = Gtk.MessageDialog(
            transient_for=window,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Micelio",
        )
        dlg.format_secondary_text(msg)
        dlg.run()
        dlg.destroy()

    def _on_save_clicked(_btn):
        chooser = Gtk.FileChooserDialog(
            title="Guardar grafico",
            parent=window,
            action=Gtk.FileChooserAction.SAVE,
        )
        chooser.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_SAVE,
            Gtk.ResponseType.OK,
        )
        chooser.set_do_overwrite_confirmation(True)
        chooser.set_current_name(os.path.basename(image_path))

        resp = chooser.run()
        target = chooser.get_filename() if resp == Gtk.ResponseType.OK else None
        chooser.destroy()
        if not target:
            return

        try:
            if target.lower().endswith(".png"):
                convert_bin = shutil.which("convert") or shutil.which("magick")
                if convert_bin is None:
                    _show_msg("No se encontro ImageMagick (convert/magick) para exportar PNG.")
                    return
                cmd = [convert_bin, image_path, target]
                if os.path.basename(convert_bin) == "magick":
                    cmd = [convert_bin, "convert", image_path, target]
                subprocess.run(cmd, check=True)
            else:
                shutil.copyfile(image_path, target)
            _show_msg(f"Guardado en:\n{target}")
            _set_status("guardado")
        except Exception as exc:
            _show_msg(f"No se pudo guardar: {exc}")

    btn_zoom_in = Gtk.Button(label="+")
    btn_zoom_in.connect("clicked", _on_zoom_in)
    controls.pack_start(btn_zoom_in, False, False, 0)

    btn_zoom_out = Gtk.Button(label="-")
    btn_zoom_out.connect("clicked", _on_zoom_out)
    controls.pack_start(btn_zoom_out, False, False, 0)

    btn_zoom_fit = Gtk.Button(label="Ajustar")
    btn_zoom_fit.connect("clicked", _on_zoom_fit)
    controls.pack_start(btn_zoom_fit, False, False, 0)

    btn_zoom_reset = Gtk.Button(label="1:1")
    btn_zoom_reset.connect("clicked", _on_zoom_reset)
    controls.pack_start(btn_zoom_reset, False, False, 0)

    if allow_save:
        btn_save = Gtk.Button(label="Guardar como...")
        btn_save.connect("clicked", _on_save_clicked)
        controls.pack_start(btn_save, False, False, 0)

    btn_close = Gtk.Button(label="Cerrar")
    btn_close.connect("clicked", lambda _btn: window.destroy())
    controls.pack_end(btn_close, False, False, 0)

    scroll.connect("size-allocate", _on_size_allocate)
    _set_status()

    window.connect("destroy", lambda *_: Gtk.main_quit())
    window.show_all()
    Gtk.main()
    return True


def _plot_mostrar(path: Any, title: Any, xlabel: Any, ylabel: Any) -> str:
    out_path = _plot_last_path()
    if out_path is None:
        # Preview path goes to temp dir so `mostrar()` does not clutter cwd.
        temp_dir = os.path.join(tempfile.gettempdir(), "micelio_plots")
        os.makedirs(temp_dir, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(prefix="preview_", suffix=".ppm", dir=temp_dir)
        os.close(fd)
        out_path = _plot_guardar(tmp_path, title, xlabel, ylabel)

    if _gtk_show_image_window(out_path, "Micelio Plot", allow_save=True):
        return out_path

    # Headless fallback to external viewer.
    opened = False
    try:
        if os.name == "nt":
            os.startfile(out_path)  # type: ignore[attr-defined]
            opened = True
        elif sys.platform == "darwin":
            subprocess.Popen(
                ["open", out_path],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True,
                start_new_session=True,
            )
            opened = True
        else:
            viewer = shutil.which("xdg-open")
            if viewer is not None:
                subprocess.Popen(
                    [viewer, out_path],
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    close_fds=True,
                    start_new_session=True,
                )
                opened = True
    except Exception:
        pass

    if opened:
        _gui_alert(
            "Se abrio la vista previa con el visor del sistema.\\n"
            f"Ruta: {out_path}",
            "Micelio Plot",
        )

    return out_path


def _gui_alert(message: Any, title: Any = "Micelio") -> None:
    zenity = shutil.which("zenity")
    if zenity is not None:
        try:
            subprocess.run([zenity, "--info", "--title", str(title), "--text", str(message)], check=False)
            return None
        except Exception:
            pass

    print(str(message))
    return None


def _gui_confirm(message: Any, title: Any = "Micelio") -> bool:
    zenity = shutil.which("zenity")
    if zenity is not None:
        try:
            proc = subprocess.run(
                [zenity, "--question", "--title", str(title), "--text", str(message)],
                check=False,
            )
            return proc.returncode == 0
        except Exception:
            pass

    try:
        ans = input(f"{title}: {message} [s/N] ").strip().lower()
        return ans in {"s", "si", "y", "yes"}
    except Exception:
        return False


def _gui_input(prompt: Any, default: Any = "", title: Any = "Micelio") -> Any:
    zenity = shutil.which("zenity")
    if zenity is not None:
        try:
            proc = subprocess.run(
                [
                    zenity,
                    "--entry",
                    "--title",
                    str(title),
                    "--text",
                    str(prompt),
                    "--entry-text",
                    str(default),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            if proc.returncode == 0:
                return proc.stdout.rstrip("\n")
            return None
        except Exception:
            pass

    try:
        val = input(f"{title}: {prompt} ")
        return val if val != "" else str(default)
    except Exception:
        return None


def _gui_open_file(title: Any = "Abrir archivo") -> Any:
    zenity = shutil.which("zenity")
    if zenity is not None:
        try:
            proc = subprocess.run(
                [zenity, "--file-selection", "--title", str(title)],
                check=False,
                capture_output=True,
                text=True,
            )
            if proc.returncode == 0:
                out = proc.stdout.rstrip("\n")
                return out if out else None
            return None
        except Exception:
            pass

    return None


def _gui_save_file(title: Any = "Guardar archivo", initial_name: Any = "") -> Any:
    zenity = shutil.which("zenity")
    if zenity is not None:
        try:
            proc = subprocess.run(
                [
                    zenity,
                    "--file-selection",
                    "--save",
                    "--confirm-overwrite",
                    "--title",
                    str(title),
                    "--filename",
                    str(initial_name) if str(initial_name) != "" else "salida.ppm",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            if proc.returncode == 0:
                out = proc.stdout.rstrip("\n")
                return out if out else None
            return None
        except Exception:
            pass

    return None


def _gui_show_image(path: Any, title: Any = "Micelio GUI") -> Any:
    image_path = str(path)
    if not os.path.isfile(image_path):
        return None

    if _gtk_show_image_window(image_path, str(title), allow_save=False):
        return image_path

    try:
        if os.name == "nt":
            os.startfile(image_path)  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.Popen(["open", image_path])
        else:
            viewer = shutil.which("xdg-open")
            if viewer is not None:
                subprocess.Popen([viewer, image_path])
    except Exception:
        pass
    return image_path


def _gui_file_copy(src: Any, dst: Any) -> bool:
    source = str(src)
    target = str(dst)
    if not os.path.isfile(source):
        return False
    folder = os.path.dirname(target)
    if folder:
        os.makedirs(folder, exist_ok=True)
    shutil.copyfile(source, target)
    return True


def _gui_calc_window(
    title: Any = "Micelio Calculadora",
    width: Any = 420,
    height: Any = 620,
    fixed_size: Any = True,
) -> bool:
    try:
        import gi

        gi.require_version("Gtk", "3.0")
        from gi.repository import Gtk
    except Exception:
        _gui_alert(
            "No se encontro GTK (PyGObject). Se usara el modo GUI por dialogos.",
            str(title),
        )
        return False

    try:
        import math as py_math
    except Exception:
        return False

    win_w = max(320, int(to_number(width)))
    win_h = max(440, int(to_number(height)))
    is_fixed = bool(fixed_size)

    window = Gtk.Window(title=str(title))
    window.set_default_size(win_w, win_h)
    if is_fixed:
        window.set_resizable(False)
    _gtk_apply_theme(_GUI_STYLE_STATE["theme"])

    root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    root.set_border_width(12)
    window.add(root)

    header = Gtk.Label(label="Calculadora UX")
    header.set_xalign(0.0)
    root.pack_start(header, False, False, 0)

    subtitle = Gtk.Label(label="Operaciones rapidas con historial y errores visibles")
    subtitle.set_xalign(0.0)
    root.pack_start(subtitle, False, False, 0)

    grid = Gtk.Grid()
    grid.set_column_spacing(8)
    grid.set_row_spacing(8)
    root.pack_start(grid, False, False, 0)

    lbl_a = Gtk.Label(label="A")
    lbl_a.set_xalign(0.0)
    ent_a = Gtk.Entry()
    ent_a.set_text("10")
    ent_a.set_hexpand(True)

    lbl_b = Gtk.Label(label="B")
    lbl_b.set_xalign(0.0)
    ent_b = Gtk.Entry()
    ent_b.set_text("5")
    ent_b.set_hexpand(True)

    grid.attach(lbl_a, 0, 0, 1, 1)
    grid.attach(ent_a, 1, 0, 3, 1)
    grid.attach(lbl_b, 0, 1, 1, 1)
    grid.attach(ent_b, 1, 1, 3, 1)

    result_frame = Gtk.Frame(label="Resultado")
    result_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
    result_box.set_border_width(8)
    result_frame.add(result_box)
    root.pack_start(result_frame, False, False, 0)

    result_label = Gtk.Label(label="Listo")
    result_label.set_xalign(0.0)
    result_box.pack_start(result_label, False, False, 0)

    history_frame = Gtk.Frame(label="Historial")
    history_scroll = Gtk.ScrolledWindow()
    history_scroll.set_vexpand(True)
    history_frame.add(history_scroll)
    root.pack_start(history_frame, True, True, 0)

    history_view = Gtk.TextView()
    history_view.set_editable(False)
    history_view.set_cursor_visible(False)
    history_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
    history_buffer = history_view.get_buffer()
    history_scroll.add(history_view)

    actions = Gtk.Grid()
    actions.set_column_spacing(8)
    actions.set_row_spacing(8)
    root.pack_start(actions, False, False, 0)

    def _append_history(text: str):
        end = history_buffer.get_end_iter()
        history_buffer.insert(end, text + "\n")

    def _read_number(entry: Any, name: str) -> float | None:
        raw = entry.get_text().strip()
        if raw == "":
            result_label.set_text(f"Error: falta valor en {name}")
            return None
        try:
            return float(raw)
        except Exception:
            result_label.set_text(f"Error: {name} no es numero")
            return None

    def _binary(op_name: str, fn: Callable[[float, float], float | None]):
        a_val = _read_number(ent_a, "A")
        b_val = _read_number(ent_b, "B")
        if a_val is None or b_val is None:
            return

        out = fn(a_val, b_val)
        if out is None:
            return
        result_label.set_text(f"{op_name}: {out}")
        _append_history(f"{op_name}({a_val}, {b_val}) = {out}")

    def _unary(op_name: str, fn: Callable[[float], float | None]):
        x_val = _read_number(ent_a, "A")
        if x_val is None:
            return

        out = fn(x_val)
        if out is None:
            return
        result_label.set_text(f"{op_name}: {out}")
        _append_history(f"{op_name}({x_val}) = {out}")

    buttons: list[tuple[str, Callable[[Any], None], int, int]] = [
        ("+", lambda _b: _binary("sumar", lambda a, b: a + b), 0, 0),
        ("-", lambda _b: _binary("restar", lambda a, b: a - b), 1, 0),
        ("*", lambda _b: _binary("multiplicar", lambda a, b: a * b), 2, 0),
        (
            "/",
            lambda _b: _binary(
                "dividir",
                lambda a, b: None
                if b == 0 and result_label.set_text("Error: division entre 0") is None
                else a / b,
            ),
            3,
            0,
        ),
        ("pow", lambda _b: _binary("potencia", lambda a, b: py_math.pow(a, b)), 0, 1),
        (
            "raiz",
            lambda _b: _unary(
                "raiz",
                lambda x: None
                if x < 0 and result_label.set_text("Error: raiz de negativo") is None
                else py_math.sqrt(x),
            ),
            1,
            1,
        ),
        ("sin", lambda _b: _unary("seno", lambda x: py_math.sin(x)), 2, 1),
        ("cos", lambda _b: _unary("coseno", lambda x: py_math.cos(x)), 3, 1),
        ("tan", lambda _b: _unary("tangente", lambda x: py_math.tan(x)), 0, 2),
    ]

    for label, handler, col, row in buttons:
        btn = Gtk.Button(label=label)
        btn.set_hexpand(True)
        btn.connect("clicked", handler)
        actions.attach(btn, col, row, 1, 1)

    btn_clear = Gtk.Button(label="Limpiar")

    def _clear(_btn):
        ent_a.set_text("")
        ent_b.set_text("")
        result_label.set_text("Listo")

    btn_clear.connect("clicked", _clear)
    actions.attach(btn_clear, 1, 2, 1, 1)

    btn_clear_history = Gtk.Button(label="Limpiar historial")

    def _clear_history(_btn):
        history_buffer.set_text("")

    btn_clear_history.connect("clicked", _clear_history)
    actions.attach(btn_clear_history, 2, 2, 1, 1)

    btn_close = Gtk.Button(label="Cerrar")
    btn_close.connect("clicked", lambda _btn: window.destroy())
    actions.attach(btn_close, 3, 2, 1, 1)

    window.connect("destroy", lambda *_: Gtk.main_quit())
    window.show_all()
    Gtk.main()
    return True


def _flask_disponible() -> bool:
    try:
        import flask  # noqa: F401

        return True
    except Exception:
        return False


def _flask_demo(
    host: Any = "127.0.0.1",
    port: Any = 5000,
    title: Any = "Micelio Flask",
    message: Any = "Hola desde Micelio",
) -> Any:
    try:
        from flask import Flask
    except Exception:
        return None

    app = Flask("micelio_demo")
    page_title = str(title)
    page_message = str(message)

    @app.get("/")
    def index():
        return (
            "<!doctype html><html><head><meta charset='utf-8'>"
            f"<title>{page_title}</title>"
            "<style>body{font-family:ui-sans-serif,system-ui;margin:2rem;max-width:760px;}"
            "h1{margin-bottom:.25rem;} .card{padding:1rem;border:1px solid #ddd;border-radius:10px;}"
            "code{background:#f5f5f5;padding:.2rem .4rem;border-radius:6px;}</style></head><body>"
            f"<h1>{page_title}</h1><p>{page_message}</p>"
            "<div class='card'><strong>API:</strong> <code>/api/ping</code></div>"
            "</body></html>"
        )

    @app.get("/api/ping")
    def ping():
        return {"ok": True, "framework": "flask", "runtime": "micelio"}

    host_s = str(host)
    port_i = int(to_number(port))
    app.run(host=host_s, port=port_i, debug=False)
    return f"http://{host_s}:{port_i}"


def _flask_generar_demo(path: Any = "micelio_flask_demo", app_name: Any = "app") -> bool:
    target = str(path).strip()
    if target == "":
        target = "micelio_flask_demo"
    os.makedirs(target, exist_ok=True)

    module_name = str(app_name).strip()
    if module_name == "":
        module_name = "app"

    app_py = os.path.join(target, f"{module_name}.py")
    readme = os.path.join(target, "README.md")
    reqs = os.path.join(target, "requirements.txt")

    code = (
        "from flask import Flask\n\n"
        "app = Flask(__name__)\n\n"
        "@app.get('/')\n"
        "def index():\n"
        "    return {'ok': True, 'msg': 'Hola desde plantilla Flask para Micelio'}\n\n"
        "if __name__ == '__main__':\n"
        "    app.run(host='127.0.0.1', port=5000, debug=True)\n"
    )
    with open(app_py, "w", encoding="utf-8") as f:
        f.write(code)

    with open(reqs, "w", encoding="utf-8") as f:
        f.write("flask>=3.0\n")

    with open(readme, "w", encoding="utf-8") as f:
        f.write(
            "# Flask Demo para Micelio\n\n"
            "## Instalacion\n"
            "```bash\n"
            "python3 -m venv .venv\n"
            "source .venv/bin/activate\n"
            "pip install -r requirements.txt\n"
            "python app.py\n"
            "```\n"
        )

    return True


def _hifa_crear(nombre: Any = "hifa_app") -> dict[str, Any]:
    return {
        "framework": "hifa",
        "name": str(nombre),
        "routes": {},
        "static_dir": None,
        "template_dir": None,
        "not_found": None,
    }


def _hifa_estaticos(app: Any, carpeta: Any) -> Any:
    if not isinstance(app, dict):
        return app
    app["static_dir"] = str(carpeta)
    return app


def _hifa_plantillas(app: Any, carpeta: Any) -> Any:
    if not isinstance(app, dict):
        return app
    app["template_dir"] = str(carpeta)
    return app


def _hifa_ruta_texto(
    app: Any,
    method: Any,
    path: Any,
    body: Any,
    content_type: Any = "text/html; charset=utf-8",
    status: Any = 200,
) -> Any:
    if not isinstance(app, dict):
        return app
    routes = app.setdefault("routes", {})
    key = f"{str(method).upper()} {str(path)}"
    routes[key] = {
        "type": "text",
        "body": str(body),
        "content_type": str(content_type),
        "status": int(to_number(status)),
    }
    return app


def _hifa_ruta_json(
    app: Any,
    method: Any,
    path: Any,
    data: Any,
    status: Any = 200,
) -> Any:
    if not isinstance(app, dict):
        return app
    routes = app.setdefault("routes", {})
    key = f"{str(method).upper()} {str(path)}"
    routes[key] = {
        "type": "json",
        "data": data,
        "status": int(to_number(status)),
    }
    return app


def _hifa_ruta_template(
    app: Any,
    method: Any,
    path: Any,
    template_name: Any,
    context: Any = None,
    status: Any = 200,
) -> Any:
    if not isinstance(app, dict):
        return app
    routes = app.setdefault("routes", {})
    key = f"{str(method).upper()} {str(path)}"
    ctx = context if isinstance(context, dict) else {}
    routes[key] = {
        "type": "template",
        "template": str(template_name),
        "context": ctx,
        "status": int(to_number(status)),
    }
    return app


def _hifa_ruta_archivo(
    app: Any,
    method: Any,
    path: Any,
    file_path: Any,
    content_type: Any = "",
    status: Any = 200,
) -> Any:
    if not isinstance(app, dict):
        return app
    routes = app.setdefault("routes", {})
    key = f"{str(method).upper()} {str(path)}"
    routes[key] = {
        "type": "file",
        "file": str(file_path),
        "content_type": str(content_type),
        "status": int(to_number(status)),
    }
    return app


def _hifa_ruta_redirect(
    app: Any,
    method: Any,
    path: Any,
    target: Any,
    status: Any = 302,
) -> Any:
    if not isinstance(app, dict):
        return app
    routes = app.setdefault("routes", {})
    key = f"{str(method).upper()} {str(path)}"
    routes[key] = {
        "type": "redirect",
        "target": str(target),
        "status": int(to_number(status)),
    }
    return app


def _hifa_not_found_text(app: Any, body: Any, content_type: Any = "text/html; charset=utf-8") -> Any:
    if not isinstance(app, dict):
        return app
    app["not_found"] = {
        "type": "text",
        "body": str(body),
        "content_type": str(content_type),
        "status": 404,
    }
    return app


def _hifa_not_found_json(app: Any, data: Any) -> Any:
    if not isinstance(app, dict):
        return app
    app["not_found"] = {
        "type": "json",
        "data": data,
        "status": 404,
    }
    return app


def _hifa_listar_rutas(app: Any) -> list[str]:
    if not isinstance(app, dict):
        return []
    routes = app.get("routes", {})
    if not isinstance(routes, dict):
        return []
    return sorted(list(routes.keys()))


def _hifa_render_template(template_text: str, context: dict[str, Any]) -> str:
    out = template_text
    for k, v in context.items():
        out = out.replace("{{" + str(k) + "}}", str(v))
    return out


def _hifa_iniciar(app: Any, host: Any = "127.0.0.1", port: Any = 8080, auto_open: Any = False) -> Any:
    if not isinstance(app, dict):
        raise MicelioRuntimeError("hifa.iniciar() requiere un objeto app valido")

    routes = app.get("routes", {})
    static_dir = app.get("static_dir")
    template_dir = app.get("template_dir")
    not_found = app.get("not_found")
    host_s = str(host)
    port_i = int(to_number(port))
    should_open = bool(auto_open)

    class HifaHandler(BaseHTTPRequestHandler):
        def _send_bytes(self, status_code: int, payload: bytes, content_type: str):
            self.send_response(status_code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def _send_text(self, status_code: int, text: str, content_type: str):
            self._send_bytes(status_code, text.encode("utf-8"), content_type)

        def _read_body(self) -> bytes:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0:
                return b""
            return self.rfile.read(length)

        def _serve_static(self, path_only: str) -> bool:
            if not static_dir:
                return False
            if not path_only.startswith("/static/"):
                return False

            rel = path_only[len("/static/") :]
            if rel == "":
                return False

            base = os.path.abspath(str(static_dir))
            candidate = os.path.abspath(os.path.join(base, rel))
            if not candidate.startswith(base):
                return False
            if not os.path.isfile(candidate):
                return False

            with open(candidate, "rb") as f:
                blob = f.read()
            guessed = mimetypes.guess_type(candidate)[0] or "application/octet-stream"
            self._send_bytes(int(HTTPStatus.OK), blob, guessed)
            return True

        def _handle(self):
            parsed = urlparse(self.path)
            path_only = parsed.path
            key = f"{self.command.upper()} {path_only}"
            route = routes.get(key)

            if route is None and self._serve_static(path_only):
                return

            if route is None:
                nf = not_found
                if isinstance(nf, dict):
                    nf_kind = nf.get("type")
                    nf_status = int(nf.get("status", 404))
                    if nf_kind == "text":
                        nf_ct = str(nf.get("content_type", "text/html; charset=utf-8"))
                        self._send_text(nf_status, str(nf.get("body", "404 Not Found")), nf_ct)
                        return
                    if nf_kind == "json":
                        self._send_text(
                            nf_status,
                            json.dumps(nf.get("data", {}), ensure_ascii=False),
                            "application/json; charset=utf-8",
                        )
                        return

                msg = {
                    "ok": False,
                    "framework": "hifa",
                    "error": "ruta no encontrada",
                    "path": path_only,
                    "method": self.command.upper(),
                }
                self._send_text(404, json.dumps(msg, ensure_ascii=False), "application/json; charset=utf-8")
                return

            kind = route.get("type")
            code = int(route.get("status", 200))

            if kind == "text":
                ct = str(route.get("content_type", "text/plain; charset=utf-8"))
                self._send_text(code, str(route.get("body", "")), ct)
                return

            if kind == "json":
                payload = route.get("data", {})
                self._send_text(code, json.dumps(payload, ensure_ascii=False), "application/json; charset=utf-8")
                return

            if kind == "template":
                if not template_dir:
                    self._send_text(500, "Template dir no configurado", "text/plain; charset=utf-8")
                    return
                tpl_path = os.path.join(str(template_dir), str(route.get("template", "")))
                if not os.path.isfile(tpl_path):
                    self._send_text(404, "Template no encontrado", "text/plain; charset=utf-8")
                    return
                with open(tpl_path, "r", encoding="utf-8") as f:
                    tpl_text = f.read()

                ctx = route.get("context", {})
                if not isinstance(ctx, dict):
                    ctx = {}
                ctx.setdefault("path", path_only)
                ctx.setdefault("query", parse_qs(parsed.query))
                body = self._read_body()
                ctx.setdefault("body", body.decode("utf-8", errors="replace"))
                rendered = _hifa_render_template(tpl_text, ctx)
                self._send_text(code, rendered, "text/html; charset=utf-8")
                return

            if kind == "file":
                file_path = str(route.get("file", ""))
                if not os.path.isfile(file_path):
                    self._send_text(404, "Archivo no encontrado", "text/plain; charset=utf-8")
                    return
                with open(file_path, "rb") as f:
                    blob = f.read()
                ct = str(route.get("content_type", "")).strip()
                if ct == "":
                    ct = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
                self._send_bytes(code, blob, ct)
                return

            if kind == "redirect":
                target = str(route.get("target", "/"))
                self.send_response(code)
                self.send_header("Location", target)
                self.send_header("Content-Length", "0")
                self.end_headers()
                return

            self._send_text(500, "Ruta invalida", "text/plain; charset=utf-8")

        def do_GET(self):
            self._handle()

        def do_POST(self):
            self._handle()

        def do_PUT(self):
            self._handle()

        def do_DELETE(self):
            self._handle()

        def log_message(self, fmt: str, *args: Any):
            print(f"[hifa] {self.address_string()} - {fmt % args}")

    server = ThreadingHTTPServer((host_s, port_i), HifaHandler)
    print(f"Hifa corriendo en http://{host_s}:{port_i}")
    if should_open:
        try:
            webbrowser.open(f"http://{host_s}:{port_i}")
        except Exception:
            pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return f"http://{host_s}:{port_i}"


def _hifa_generar_demo(path: Any = "hifa_demo") -> bool:
    target = str(path).strip() or "hifa_demo"
    os.makedirs(target, exist_ok=True)

    templates_dir = os.path.join(target, "templates")
    static_dir = os.path.join(target, "static")
    os.makedirs(templates_dir, exist_ok=True)
    os.makedirs(static_dir, exist_ok=True)

    html = (
        "<!doctype html>\n"
        "<html lang='es'>\n"
        "<head>\n"
        "  <meta charset='utf-8' />\n"
        "  <meta name='viewport' content='width=device-width, initial-scale=1' />\n"
        "  <title>{{title}}</title>\n"
        "  <link rel='stylesheet' href='/static/styles.css' />\n"
        "</head>\n"
        "<body>\n"
        "  <main class='card'>\n"
        "    <h1>{{title}}</h1>\n"
        "    <p>{{message}}</p>\n"
        "    <button id='ping'>Probar API</button>\n"
        "    <pre id='out'></pre>\n"
        "  </main>\n"
        "  <script src='/static/app.js'></script>\n"
        "</body>\n"
        "</html>\n"
    )
    css = (
        ":root{--bg:#0f172a;--card:#111827;--ink:#e5e7eb;--accent:#22d3ee;}\n"
        "body{margin:0;font-family:ui-sans-serif,system-ui;background:radial-gradient(circle at top,#1f2937,#0f172a);color:var(--ink);}\n"
        ".card{max-width:680px;margin:8vh auto;padding:24px;border:1px solid #334155;border-radius:14px;background:rgba(17,24,39,.86);}\n"
        "button{padding:10px 14px;border-radius:10px;border:0;background:var(--accent);color:#06202a;font-weight:700;cursor:pointer;}\n"
        "pre{margin-top:14px;background:#020617;padding:10px;border-radius:8px;overflow:auto;}\n"
    )
    js = (
        "document.getElementById('ping').addEventListener('click', async () => {\n"
        "  const res = await fetch('/api/ping');\n"
        "  const data = await res.json();\n"
        "  document.getElementById('out').textContent = JSON.stringify(data, null, 2);\n"
        "});\n"
    )
    app_mice = (
        "importar \"../modulos_std/hifa.mice\" como hifa\n\n"
        "var app = hifa.crear(\"mi_hifa\")\n"
        "hifa.plantillas(app, \"templates\")\n"
        "hifa.estaticos(app, \"static\")\n\n"
        "hifa.get_template(app, \"/\", \"index.html\", {\"title\": \"Hifa\", \"message\": \"Framework web rapido en Micelio\"})\n"
        "hifa.get_json(app, \"/api/ping\", {\"ok\": verdadero, \"framework\": \"hifa\"})\n\n"
        "hifa.iniciar(app, \"127.0.0.1\", 8080)\n"
    )

    with open(os.path.join(templates_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    with open(os.path.join(static_dir, "styles.css"), "w", encoding="utf-8") as f:
        f.write(css)
    with open(os.path.join(static_dir, "app.js"), "w", encoding="utf-8") as f:
        f.write(js)
    with open(os.path.join(target, "app_hifa.mice"), "w", encoding="utf-8") as f:
        f.write(app_mice)

    return True


def make_primitives() -> dict[str, Any]:
    """
    Crea el conjunto mínimo de primitivas de sistema que requieren Python.
    Estas son funciones especiales (prefijadas con __) que no pueden expresarse
    fácilmente en Micelio porque requieren acceso directo al OS o librerías Python.
    
    El resto de funciones globales (map, filter, tipo, longitud, etc.)
    se definen en modulos_std/builtins.mice y se cargan al iniciar el intérprete.
    """
    import math as _pymath
    import random as _pyrandom
    
    def _a_numero(valor: Any) -> float:
        """Convierte un valor a número. Se llama desde builtins.mice."""
        return to_number(valor)
    
    def _a_texto(valor: Any) -> str:
        """Convierte un valor a texto. Se llama desde builtins.mice."""
        return to_text(valor)
    
    def _tipo_nativo(x: Any) -> str:
        """Obtiene el tipo nativo Python de un valor."""
        tipo_map = {
            bool: "booleano",
            int: "numero",
            float: "numero",
            str: "texto",
            list: "lista",
            dict: "diccionario",
            set: "conjunto",
            type(None): "nulo",
        }
        return tipo_map.get(type(x), type(x).__name__)
    
    def _ordenar_nativo(lst: Any) -> list[Any]:
        """Ordena una lista usando el algoritmo nativo de Python (Timsort)."""
        if isinstance(lst, list):
            try:
                return sorted(lst)
            except TypeError:
                raise MicelioRuntimeError("No se pueden comparar los elementos de la lista")
        return list(sorted(lst))
    
    def _aleatorio() -> float:
        """Genera un número aleatorio entre 0 y 1."""
        return _pyrandom.random()
    
    def _exp_nativo(x: Any) -> float:
        """Calcula e^x (exponencial). Usado por módulo ML."""
        return _pymath.exp(float(to_number(x)))
    
    def _error(mensaje: Any) -> None:
        """Lanza una excepción con el mensaje dado."""
        raise MicelioRuntimeError(str(mensaje))
    
    # Funciones de archivos
    def _archivo_leer(ruta: Any) -> str:
        """Lee el contenido completo de un archivo de texto."""
        try:
            with open(str(ruta), 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise MicelioRuntimeError(f"Archivo no encontrado: {ruta}")
        except Exception as e:
            raise MicelioRuntimeError(f"Error leyendo archivo: {e}")
    
    def _archivo_escribir(ruta: Any, contenido: Any) -> None:
        """Escribe contenido en un archivo (sobrescribe si existe)."""
        try:
            with open(str(ruta), 'w', encoding='utf-8') as f:
                f.write(str(contenido))
        except Exception as e:
            raise MicelioRuntimeError(f"Error escribiendo archivo: {e}")
    
    def _archivo_anexar(ruta: Any, contenido: Any) -> None:
        """Añade contenido al final de un archivo."""
        try:
            with open(str(ruta), 'a', encoding='utf-8') as f:
                f.write(str(contenido))
        except Exception as e:
            raise MicelioRuntimeError(f"Error anexando archivo: {e}")
    
    def _archivo_existe(ruta: Any) -> bool:
        """Verifica si un archivo existe."""
        return os.path.isfile(str(ruta))
    
    def _archivo_eliminar(ruta: Any) -> None:
        """Elimina un archivo."""
        try:
            os.remove(str(ruta))
        except Exception as e:
            raise MicelioRuntimeError(f"Error eliminando archivo: {e}")
    
    def _directorio_existe(ruta: Any) -> bool:
        """Verifica si un directorio existe."""
        return os.path.isdir(str(ruta))
    
    def _directorio_crear(ruta: Any) -> None:
        """Crea un directorio."""
        try:
            os.makedirs(str(ruta), exist_ok=True)
        except Exception as e:
            raise MicelioRuntimeError(f"Error creando directorio: {e}")
    
    return {
        # Conversiones base (requieren lógica Python compleja)
        '__a_numero': _a_numero,
        '__a_texto': _a_texto,
        '__tipo_nativo': _tipo_nativo,
        '__ordenar_nativo': _ordenar_nativo,
        
        # Números aleatorios
        '__aleatorio': _aleatorio,
        
        # Funciones matemáticas
        '__exp_nativo': _exp_nativo,
        
        # Manejo de errores
        '__error': _error,
        
        # Operaciones de archivos
        '__archivo_leer': _archivo_leer,
        '__archivo_escribir': _archivo_escribir,
        '__archivo_anexar': _archivo_anexar,
        '__archivo_existe': _archivo_existe,
        '__archivo_eliminar': _archivo_eliminar,
        '__directorio_existe': _directorio_existe,
        '__directorio_crear': _directorio_crear,
    }


def make_builtins() -> dict[str, Any]:
    def _map(fn: Callable[..., Any], iterable: Any) -> Any:
        if not isinstance(iterable, list):
            return fn(iterable)
        return [fn(x) for x in iterable]

    def _filter(fn: Callable[..., Any], iterable: list[Any]) -> list[Any]:
        return [x for x in iterable if fn(x)]

    def _reduce(fn: Callable[..., Any], iterable: list[Any], initial: Any) -> Any:
        return py_reduce(fn, iterable, initial)

    def _ordenar(iterable: Any) -> list[Any]:
        if not isinstance(iterable, list):
            raise MicelioRuntimeError("ordenar() requiere una lista")
        try:
            return sorted(iterable)
        except TypeError as exc:
            raise MicelioRuntimeError(
                "ordenar() requiere elementos comparables entre si"
            ) from exc

    def _a_binario(n: Any) -> str:
        return int_to_base(int(to_number(n)), 2)

    def _a_octal(n: Any) -> str:
        return int_to_base(int(to_number(n)), 8)

    def _a_hexadecimal(n: Any) -> str:
        return int_to_base(int(to_number(n)), 16)

    def _a_base(n: Any, base: Any) -> str:
        return int_to_base(int(to_number(n)), int(to_number(base)))

    def _desde_base(texto: Any, base: Any) -> float:
        return float(int(str(texto), int(to_number(base))))

    def _a_base_complemento(n: Any, base: Any, bits: Any) -> str:
        return to_base_complement(
            int(to_number(n)),
            int(to_number(base)),
            int(to_number(bits)),
        )

    def _a_base_fraccion(numero: Any, base: Any, precision: Any) -> str:
        return to_base_fraction(
            numero,
            int(to_number(base)),
            int(to_number(precision)),
        )

    def _a_base_con_digitos(numero: Any, digitos: Any) -> str:
        return to_base_with_digits(int(to_number(numero)), str(digitos))

    return {
        "map": _map,
        "filter": _filter,
        "reduce": _reduce,
        "ordenar": _ordenar,
        "longitud": lambda x: len(x),
        "aNumero": to_number,
        "aEntero": to_int,
        "aFlotante": to_float,
        "aTexto": to_text,
        "aBooleano": to_bool,
        "aCaracter": to_char,
        "aCodigo": to_code,
        "aBinario": _a_binario,
        "aOctal": _a_octal,
        "aHexadecimal": _a_hexadecimal,
        "aBase": _a_base,
        "aBaseComplemento": _a_base_complemento,
        "aBasecomplemento": _a_base_complemento,
        "aBaseFraccion": _a_base_fraccion,
        "aBasefraccion": _a_base_fraccion,
        "aBaseConDigitos": _a_base_con_digitos,
        "aBaseCondigitos": _a_base_con_digitos,
        "desdeBinario": lambda txt: _desde_base(txt, 2),
        "desdeOctal": lambda txt: _desde_base(txt, 8),
        "desdeHexadecimal": lambda txt: _desde_base(txt, 16),
        "desdeBase": _desde_base,
        "__grafico_reset": _plot_reset,
        "__grafico_set_pixel": _plot_set_pixel,
        "__grafico_draw_axes": _plot_draw_axes,
        "__grafico_guardar": _plot_guardar,
        "__grafico_last_path": _plot_last_path,
        "__grafico_mostrar": _plot_mostrar,
        "__gui_alert": _gui_alert,
        "__gui_confirm": _gui_confirm,
        "__gui_input": _gui_input,
        "__gui_open_file": _gui_open_file,
        "__gui_save_file": _gui_save_file,
        "__gui_show_image": _gui_show_image,
        "__gui_file_copy": _gui_file_copy,
        "__gui_calc_window": _gui_calc_window,
        "__gui_set_theme": _gui_set_theme,
        "__gui_get_theme": _gui_get_theme,
        "__gui_list_themes": _gui_list_themes,
        "__flask_disponible": _flask_disponible,
        "__flask_demo": _flask_demo,
        "__flask_generar_demo": _flask_generar_demo,
        "__hifa_crear": _hifa_crear,
        "__hifa_estaticos": _hifa_estaticos,
        "__hifa_plantillas": _hifa_plantillas,
        "__hifa_ruta_texto": _hifa_ruta_texto,
        "__hifa_ruta_json": _hifa_ruta_json,
        "__hifa_ruta_template": _hifa_ruta_template,
        "__hifa_ruta_archivo": _hifa_ruta_archivo,
        "__hifa_ruta_redirect": _hifa_ruta_redirect,
        "__hifa_not_found_text": _hifa_not_found_text,
        "__hifa_not_found_json": _hifa_not_found_json,
        "__hifa_listar_rutas": _hifa_listar_rutas,
        "__hifa_iniciar": _hifa_iniciar,
        "__hifa_generar_demo": _hifa_generar_demo,
    }


def module_table() -> dict[str, dict[str, Any]]:
    builtins = make_builtins()
    return {
        "convert": {
            "aNumero": builtins["aNumero"],
            "aEntero": builtins["aEntero"],
            "aFlotante": builtins["aFlotante"],
            "aTexto": builtins["aTexto"],
            "aBooleano": builtins["aBooleano"],
            "aCaracter": builtins["aCaracter"],
            "aCodigo": builtins["aCodigo"],
            "aBinario": builtins["aBinario"],
            "aOctal": builtins["aOctal"],
            "aHexadecimal": builtins["aHexadecimal"],
            "aBase": builtins["aBase"],
            "aBaseComplemento": builtins["aBaseComplemento"],
            "aBaseFraccion": builtins["aBaseFraccion"],
            "aBaseConDigitos": builtins["aBaseConDigitos"],
            "desdeBinario": builtins["desdeBinario"],
            "desdeOctal": builtins["desdeOctal"],
            "desdeHexadecimal": builtins["desdeHexadecimal"],
            "desdeBase": builtins["desdeBase"],
        },
        "lista": {
            "map": builtins["map"],
            "filter": builtins["filter"],
            "reduce": builtins["reduce"],
            "ordenar": builtins["ordenar"],
        },
    }


def micelio_repr(value: Any) -> str:
    if value is True:
        return "verdadero"
    if value is False:
        return "falso"
    if value is None:
        return "nulo"
    if isinstance(value, list):
        return "[" + ", ".join(micelio_repr(v) for v in value) + "]"
    if isinstance(value, set):
        return "{" + ", ".join(sorted(micelio_repr(v) for v in value)) + "}"
    if isinstance(value, dict):
        items = [f"{micelio_repr(k)}: {micelio_repr(v)}" for k, v in value.items()]
        return "{" + ", ".join(items) + "}"
    if isinstance(value, str):
        escaped = (
            value.replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\n", "\\n")
            .replace("\t", "\\t")
        )
        return f'"{escaped}"'
    return str(value)
