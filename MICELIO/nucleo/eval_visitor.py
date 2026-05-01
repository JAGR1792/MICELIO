from __future__ import annotations

import ast
import os

from antlr4 import CommonTokenStream, InputStream
from antlr4 import ParserRuleContext

from generado.gramatica.MicelioLexer import MicelioLexer
from generado.gramatica.MicelioParser import MicelioParser
from generado.gramatica.MicelioVisitor import MicelioVisitor
from nucleo.runtime import (
    BoundMethod,
    BreakFlow,
    ContinueFlow,
    Environment,
    FunctionValue,
    MicelioRuntimeError,
    ReturnFlow,
    elementwise_mul,
    make_builtins,
    make_primitives,
    matrix_mul,
    micelio_repr,
    module_table,
)
from errores.pedagogicos import pipeline_assignment_warning


class EvalVisitor(MicelioVisitor):
    def __init__(self, base_dir: str | None = None):
        super().__init__()
        self.global_env = Environment()
        self.env = self.global_env
        self._id_env_cache: dict[int, Environment] = {}
        self._assign_env_cache: dict[int, Environment] = {}
        self.modules = module_table()
        self.current_dir = os.path.abspath(base_dir or os.getcwd())
        self.loaded_modules: dict[str, dict[str, object]] = {}

        # ─── 1. Inyectar primitivas Python (funciones __*)
        # Estas son las operaciones de bajo nivel que requieren Python
        primitives = make_primitives()
        for name, fn in primitives.items():
            self.global_env.define(name, fn)
        
        # ─── 2. Definir funciones especiales que requieren acceso a self
        
        def _parse_input_atom(raw: str):
            """Convierte string de entrada a número o booleano si aplica"""
            value = raw
            try:
                value = float(raw) if "." in raw else int(raw)
            except ValueError:
                low = raw.strip().lower()
                if low == "verdadero":
                    value = True
                elif low == "falso":
                    value = False
                elif low == "nulo":
                    value = None
            return value

        def _ensure_unpack_values(values, count: int):
            """Verifica que el desempaquetado tenga la cantidad correcta"""
            if not isinstance(values, (list, tuple)):
                raise MicelioRuntimeError(
                    "Desempaquetado requiere lista o tupla"
                )
            if len(values) != count:
                raise MicelioRuntimeError(
                    "Cantidad de valores no coincide con cantidad de variables en desempaquetado"
                )
            return values

        def _asignar_multi(names_csv, values):
            """Asigna múltiples variables a la vez (para a, b = ...)"""
            names = [n.strip() for n in str(names_csv).split(",") if n.strip()]
            unpacked = _ensure_unpack_values(values, len(names))
            for name, item in zip(names, unpacked):
                self.env.assign(name, item)
            return unpacked

        def _leer_multi(names_csv):
            """Lee múltiples valores de entrada (para leer a, b)"""
            names = [n.strip() for n in str(names_csv).split(",") if n.strip()]
            raw = input()
            parts = raw.split()
            if len(parts) != len(names):
                raise MicelioRuntimeError(
                    "Cantidad de entradas no coincide con variables en leer múltiple"
                )
            parsed = [_parse_input_atom(p) for p in parts]
            for name, item in zip(names, parsed):
                self._assign_or_define(name, item)
            return parsed
        
        # Registrar las funciones especiales
        self.global_env.define("__asignar_multi", _asignar_multi)
        self.global_env.define("__leer_multi", _leer_multi)
        self.global_env.define("__script_dir", lambda: self.current_dir)
        
        # ─── 3. Cargar el archivo builtins.mice que define las funciones globales
        self._cargar_builtins_micelio()
    
    def _cargar_builtins_micelio(self):
        """
        Carga automáticamente el archivo modulos_std/builtins.mice
        que contiene la definición de todas las funciones globales
        (map, filter, reduce, tipo, longitud, etc.) en Micelio puro.
        """
        # Resolver ruta al archivo builtins.mice
        ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta = os.path.normpath(os.path.join(ruta_base, 'modulos_std', 'builtins.mice'))
        
        if not os.path.isfile(ruta):
            # No es crítico si no existe, pero advertir
            import warnings
            warnings.warn(f'modulos_std/builtins.mice no encontrado en {ruta}')
            return
        
        # Leer el código del archivo
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                codigo = f.read()
        except Exception as e:
            raise MicelioRuntimeError(f'Error leyendo builtins.mice: {e}') from e
        
        # Guardar directorio actual y cambiarlo para imports relativos
        saved_dir = self.current_dir
        self.current_dir = os.path.dirname(ruta)
        
        try:
            # Ejecutar el código en el entorno global
            self._ejecutar_codigo_fuente(codigo)
        except Exception as e:
            raise MicelioRuntimeError(f'Error cargando builtins.mice: {e}') from e
        finally:
            # Restaurar directorio
            self.current_dir = saved_dir
    
    def _ejecutar_codigo_fuente(self, codigo: str):
        """
        Ejecuta código fuente Micelio en el entorno actual.
        Se usa internamente para cargar builtins.mice.
        """
        lexer = MicelioLexer(InputStream(codigo))
        tokens = CommonTokenStream(lexer)
        parser = MicelioParser(tokens)
        tree = parser.program()
        self.visit(tree)

    def _execute_source(self, code: str):
        lexer = MicelioLexer(InputStream(code))
        tokens = CommonTokenStream(lexer)
        parser = MicelioParser(tokens)
        tree = parser.program()
        return self.visit(tree)

    def _resolve_module_path(self, raw_path: str) -> str:
        requested = raw_path
        candidates = []

        if os.path.isabs(requested):
            candidates.append(requested)
        else:
            candidates.append(os.path.join(self.current_dir, requested))
            candidates.append(os.path.join(self.current_dir, "modulos_std", requested))

        expanded = []
        for cand in candidates:
            expanded.append(cand)
            if not cand.endswith(".mice"):
                expanded.append(cand + ".mice")

        for cand in expanded:
            if os.path.isfile(cand):
                return os.path.abspath(cand)

        raise MicelioRuntimeError(f"No se encontro modulo '{raw_path}'")

    def _eval_in_env(self, node: ParserRuleContext, env: Environment):
        saved = self.env
        self.env = env
        try:
            return self.visit(node)
        finally:
            self.env = saved

    def _resolve_env_for_name(self, name: str) -> Environment | None:
        env = self.env
        while env is not None:
            if name in env.values:
                return env
            env = env.parent
        return None

    def _is_env_visible(self, candidate: Environment | None) -> bool:
        env = self.env
        while env is not None:
            if env is candidate:
                return True
            env = env.parent
        return False

    def _assign_or_define(self, name: str, value):
        target_env = self._resolve_env_for_name(name)
        if target_env is None:
            self.env.define(name, value)
            return
        if name in target_env.constants:
            raise MicelioRuntimeError(f"No se puede reasignar la constante '{name}'")
        target_env.values[name] = value

    def _ensure_number(self, value, op: str):
        if not isinstance(value, (int, float)):
            raise MicelioRuntimeError(f"Operacion {op} requiere numeros")

    def _is_numeric_matrix(self, value) -> bool:
        if not isinstance(value, list) or not value:
            return False
        if not all(isinstance(row, list) and row for row in value):
            return False
        cols = len(value[0])
        if cols == 0:
            return False
        for row in value:
            if len(row) != cols:
                return False
            if not all(isinstance(cell, (int, float)) for cell in row):
                return False
        return True

    def _matrix_add_sub(self, left, right, is_add: bool):
        if len(left) != len(right) or len(left[0]) != len(right[0]):
            raise MicelioRuntimeError("Dimensiones invalidas para suma/resta matricial")
        out = []
        for row_l, row_r in zip(left, right):
            row = []
            for a, b in zip(row_l, row_r):
                row.append(a + b if is_add else a - b)
            out.append(row)
        return out

    def _resolve_callable(self, value):
        if isinstance(value, BoundMethod):
            return value
        if isinstance(value, FunctionValue):
            return value
        if callable(value):
            return value
        raise MicelioRuntimeError(f"'{value}' no es invocable")

    def _call_callable(self, callee, args):
        fn = self._resolve_callable(callee)
        if isinstance(fn, FunctionValue):
            # Pasar args, kwargs vacío, y la función para evaluar
            return fn.call(args, {}, self._eval_in_env)
        return fn(*args)

    def _decode_string_literal(self, raw: str) -> str:
        try:
            value = ast.literal_eval(raw)
        except (SyntaxError, ValueError):
            return raw[1:-1]
        return value if isinstance(value, str) else str(value)

    def _block_needs_scope(self, block_ctx: MicelioParser.BlockContext) -> bool:
        for st in block_ctx.statement():
            simple = st.simple_stmt()
            if simple is not None:
                if simple.var_decl() is not None:
                    return True
                if simple.const_decl() is not None:
                    return True
                if simple.import_stmt() is not None:
                    return True
                if simple.leer_stmt() is not None:
                    return True

            compound = st.compound_stmt()
            if compound is not None and compound.func_def() is not None:
                return True

        return False

    def _exec_block_body_no_scope(self, block_ctx: MicelioParser.BlockContext):
        result = None
        for st in block_ctx.statement():
            result = self.visit(st)
        return result

    def visitProgram(self, ctx: MicelioParser.ProgramContext):
        result = None
        for st in ctx.statement():
            result = self.visit(st)
        return result

    def visitStatement(self, ctx: MicelioParser.StatementContext):
        simple = ctx.simple_stmt()
        if simple and simple.expr():
            expr_ctx = simple.expr()
            value = self.visit(expr_ctx)
            if isinstance(expr_ctx, MicelioParser.PipeExprContext):
                line = expr_ctx.start.line if getattr(expr_ctx, "start", None) else "?"
                print(pipeline_assignment_warning(line))
            return value
        if simple is not None:
            return self.visit(simple)

        compound = ctx.compound_stmt()
        if compound is not None:
            return self.visit(compound)

        return None

    def visitSimple_stmt(self, ctx: MicelioParser.Simple_stmtContext):
        var_decl = ctx.var_decl()
        if var_decl is not None:
            return self.visit(var_decl)

        const_decl = ctx.const_decl()
        if const_decl is not None:
            return self.visit(const_decl)

        assignment = ctx.assignment()
        if assignment is not None:
            return self.visit(assignment)

        return_stmt = ctx.return_stmt()
        if return_stmt is not None:
            return self.visit(return_stmt)

        break_stmt = ctx.break_stmt()
        if break_stmt is not None:
            return self.visit(break_stmt)

        continue_stmt = ctx.continue_stmt()
        if continue_stmt is not None:
            return self.visit(continue_stmt)

        import_stmt = ctx.import_stmt()
        if import_stmt is not None:
            return self.visit(import_stmt)

        leer_stmt = ctx.leer_stmt()
        if leer_stmt is not None:
            return self.visit(leer_stmt)

        imp_stmt = ctx.imp_stmt()
        if imp_stmt is not None:
            return self.visit(imp_stmt)

        expr = ctx.expr()
        if expr is not None:
            return self.visit(expr)

        return None

    def visitCompound_stmt(self, ctx: MicelioParser.Compound_stmtContext):
        if_stmt = ctx.if_stmt()
        if if_stmt is not None:
            return self.visit(if_stmt)

        switch_stmt = ctx.switch_stmt()
        if switch_stmt is not None:
            return self.visit(switch_stmt)

        while_stmt = ctx.while_stmt()
        if while_stmt is not None:
            return self.visit(while_stmt)

        for_stmt = ctx.for_stmt()
        if for_stmt is not None:
            return self.visit(for_stmt)

        func_def = ctx.func_def()
        if func_def is not None:
            return self.visit(func_def)

        block = ctx.block()
        if block is not None:
            return self.visit(block)

        return None

    def visitVar_decl(self, ctx: MicelioParser.Var_declContext):
        names = [ident.getText() for ident in ctx.ID()]
        expr_nodes = ctx.expr()

        if not expr_nodes:
            for name in names:
                self.env.define(name, None)
            return None

        if len(expr_nodes) == 1:
            value = self.visit(expr_nodes[0])

          
            if len(names) > 1:
                if not isinstance(value, (list, tuple)):
                    raise MicelioRuntimeError(
                        "Desempaquetado requiere lista o tupla en declaracion multiple"
                    )
                if len(value) != len(names):
                    raise MicelioRuntimeError(
                        "Cantidad de valores no coincide con cantidad de variables en desempaquetado"
                    )
                for name, item in zip(names, value):
                    self.env.define(name, item)
                return value

            for name in names:
                self.env.define(name, value)
            return value

        if len(expr_nodes) != len(names):
            raise MicelioRuntimeError(
                "Cantidad de valores no coincide con cantidad de variables en declaracion"
            )

        last = None
        for name, node in zip(names, expr_nodes):
            last = self.visit(node)
            self.env.define(name, last)
        return last

    def visitConst_decl(self, ctx: MicelioParser.Const_declContext):
        name = ctx.ID().getText()
        value = self.visit(ctx.expr())
        self.env.define(name, value, is_const=True)
        return value

    def visitAssignment(self, ctx: MicelioParser.AssignmentContext):
        target = ctx.assign_target()
        name = target.ID().getText()
        value = self.visit(ctx.expr())
        indexes = [self.visit(expr_ctx) for expr_ctx in target.expr()]
        cache_key = id(ctx)
        target_env = self._assign_env_cache.get(cache_key)
        if (
            target_env is None
            or not self._is_env_visible(target_env)
            or name not in target_env.values
        ):
            target_env = self._resolve_env_for_name(name)
            if target_env is None:
                raise MicelioRuntimeError(f"Variable '{name}' no definida")
            self._assign_env_cache[cache_key] = target_env

        if indexes:
            container = target_env.values[name]
            try:
                for index in indexes[:-1]:
                    container = container[index]
                container[indexes[-1]] = value
            except Exception as exc:
                raise MicelioRuntimeError(
                    f"No se pudo asignar a '{name}' en el indice {indexes!r}: {exc}"
                ) from exc
            return value

        if name in target_env.constants:
            raise MicelioRuntimeError(f"No se puede reasignar la constante '{name}'")
        target_env.values[name] = value
        return value

    def visitReturn_stmt(self, ctx: MicelioParser.Return_stmtContext):
        value = self.visit(ctx.expr()) if ctx.expr() else None
        raise ReturnFlow(value)

    def visitBreak_stmt(self, ctx: MicelioParser.Break_stmtContext):
        raise BreakFlow()

    def visitContinue_stmt(self, ctx: MicelioParser.Continue_stmtContext):
        raise ContinueFlow()

    def visitImport_stmt(self, ctx: MicelioParser.Import_stmtContext):
        raw = ctx.STRING().getText()
        path = self._decode_string_literal(raw)
        module_name = os.path.splitext(os.path.basename(path))[0]

        module = self.modules.get(module_name)
        if module is None:
            full_path = self._resolve_module_path(path)
            if full_path in self.loaded_modules:
                module = self.loaded_modules[full_path]
            else:
                with open(full_path, "r", encoding="utf-8") as f:
                    code = f.read()

                # Evaluar el modulo en un entorno aislado para evitar colisiones
                # con nombres globales (ej: abs/exp en builtins y math).
                module_env = Environment(self.global_env)
                saved_env = self.env
                saved_dir = self.current_dir
                self.env = module_env
                self.current_dir = os.path.dirname(full_path)
                try:
                    self._execute_source(code)
                finally:
                    self.env = saved_env
                    self.current_dir = saved_dir

                module = {
                    name: value
                    for name, value in module_env.values.items()
                    if not name.startswith("_")
                }
                self.loaded_modules[full_path] = module

        alias = ctx.ID().getText() if ctx.ID() else module_name
        self.env.define(alias, module)
        return module

    def visitLeer_stmt(self, ctx: MicelioParser.Leer_stmtContext):
        name = ctx.ID().getText()
        raw = input()
        value = raw
        try:
            value = float(raw) if "." in raw else int(raw)
        except ValueError:
            low = raw.strip().lower()
            if low == "verdadero":
                value = True
            elif low == "falso":
                value = False
            elif low == "nulo":
                value = None
        self._assign_or_define(name, value)
        return value

    def visitImp_stmt(self, ctx: MicelioParser.Imp_stmtContext):
        value = self.visit(ctx.expr())
        print(micelio_repr(value))
        return value

    def visitIf_stmt(self, ctx: MicelioParser.If_stmtContext):
        cond = self.visit(ctx.expr())
        if cond:
            return self.visit(ctx.block(0))
        if ctx.block(1):
            return self.visit(ctx.block(1))
        return None

    def visitSwitch_stmt(self, ctx: MicelioParser.Switch_stmtContext):
        target = self.visit(ctx.expr())
        matched = False
        for case_ctx in ctx.case_block():
            if isinstance(case_ctx, MicelioParser.CaseClauseContext):
                if matched or self.visit(case_ctx.expr()) == target:
                    matched = True
                    try:
                        result = None
                        for st in case_ctx.statement():
                            result = self.visit(st)
                    except BreakFlow:
                        return None
            else:
                if not matched:
                    result = None
                    for st in case_ctx.statement():
                        result = self.visit(st)
                    return result
        return None

    def visitWhile_stmt(self, ctx: MicelioParser.While_stmtContext):
        result = None
        cond_ctx = ctx.expr()
        block_ctx = ctx.block()
        needs_scope = self._block_needs_scope(block_ctx)
        while self.visit(cond_ctx):
            try:
                if needs_scope:
                    result = self.visit(block_ctx)
                else:
                    result = self._exec_block_body_no_scope(block_ctx)
            except ContinueFlow:
                continue
            except BreakFlow:
                break
        return result

    def visitFor_stmt(self, ctx: MicelioParser.For_stmtContext):
        var_name = ctx.ID().getText()
        result = None
        block_ctx = ctx.block()
        needs_scope = self._block_needs_scope(block_ctx)

        if ctx.EN() is not None:
            iterable = self.visit(ctx.expr(0))
            if not isinstance(iterable, (list, tuple, set, str, dict)):
                raise MicelioRuntimeError("para ... en requiere un iterable")
            target_env = self._resolve_env_for_name(var_name)
            if target_env is None:
                self.env.define(var_name, None)
                target_env = self.env
            if var_name in target_env.constants:
                raise MicelioRuntimeError(f"No se puede reasignar la constante '{var_name}'")
            for value in iterable:
                target_env.values[var_name] = value
                try:
                    if needs_scope:
                        result = self.visit(block_ctx)
                    else:
                        result = self._exec_block_body_no_scope(block_ctx)
                except ContinueFlow:
                    continue
                except BreakFlow:
                    break
            return result

        start = self.visit(ctx.expr(0))
        end = self.visit(ctx.expr(1))
        step = self.visit(ctx.expr(2)) if ctx.expr(2) else 1

        if step == 0:
            raise MicelioRuntimeError("inc no puede ser 0")

        self._assign_or_define(var_name, start)

        # Resuelve una vez donde la variable del bucle vive para evitar asignaciones recursivas
        # En cada iteracion de bucles finitos
        target_env = self.env
        while target_env is not None and var_name not in target_env.values:
            target_env = target_env.parent
        if target_env is None:
            target_env = self.env

        current = start
        if step > 0:
            while current <= end:
                target_env.values[var_name] = current
                try:
                    if needs_scope:
                        result = self.visit(block_ctx)
                    else:
                        result = self._exec_block_body_no_scope(block_ctx)
                except ContinueFlow:
                    pass
                except BreakFlow:
                    break
                current += step
        else:
            while current >= end:
                target_env.values[var_name] = current
                try:
                    if needs_scope:
                        result = self.visit(block_ctx)
                    else:
                        result = self._exec_block_body_no_scope(block_ctx)
                except ContinueFlow:
                    pass
                except BreakFlow:
                    break
                current += step
        return result

    def visitFunc_def(self, ctx: MicelioParser.Func_defContext):
        """
        Procesa la definición de una función.
        Soporta parámetros normales, *args (variádicos) y **kwargs (nombrados).
        
        Ejemplo: funcion foo(a, b, *args, **kwargs) { ... }
        """
        name = ctx.ID().getText()
        params = []
        args_param = None
        kwargs_param = None
        
        # Extraer parámetros de la lista
        if ctx.param_list():
            # Con la nueva gramática, param_list tiene param_item(s)
            try:
                param_items = ctx.param_list().param_item()
                if param_items is not None:
                    # Si es una única región/elemento (referente a la memoria), param_item() devuelve un solo elemento
                    if not isinstance(param_items, list):
                        param_items = [param_items]
                    
                    for item in param_items:
                        # Verificar qué tipo de parámetro es
                        if item.getChildCount() == 1:
                            # Parámetro normal: solo ID
                            params.append(item.ID().getText())
                        elif item.getChildCount() == 2:
                            # *args o **kwargs: operador + ID
                            op_token = item.getChild(0).getSymbol()
                            id_text = item.ID().getText()
                            
                            if op_token.text == '*':
                                args_param = id_text
                            elif op_token.text == '**':
                                kwargs_param = id_text
            except Exception:
                # Fallback para compatibilidad con versión anterior
                # Si param_list solo tiene IDs (sin el nuevo formato)
                old_ids = ctx.param_list().ID()
                if old_ids:
                    if isinstance(old_ids, list):
                        params = [p.getText() for p in old_ids]
                    else:
                        params = [old_ids.getText()]
        
        # Crear el objeto FunctionValue con los parámetros procesados
        fn = FunctionValue(
            name=name,
            params=params,
            args_param=args_param,
            kwargs_param=kwargs_param,
            body_ctx=ctx.block(),
            closure=self.env
        )
        self.env.define(name, fn)
        return fn

    def visitBlock(self, ctx: MicelioParser.BlockContext):
        local = Environment(self.env)
        result = None
        saved = self.env
        self.env = local
        try:
            statements = ctx.statement()
            for st in statements:
                result = self.visit(st)
            return result
        finally:
            self.env = saved

    def visitLiteralExpr(self, ctx: MicelioParser.LiteralExprContext):
        lit = ctx.literal()
        if lit.NUMBER():
            txt = lit.NUMBER().getText()
            return float(txt) if '.' in txt else int(txt)
        if lit.BOOL():
            return lit.BOOL().getText() == 'verdadero'
        if lit.NULL():
            return None
        if lit.STRING():
            raw = lit.STRING().getText()
            return self._decode_string_literal(raw)
        return None

    def visitIdExpr(self, ctx: MicelioParser.IdExprContext):
        name = ctx.ID().getText()
        cache_key = id(ctx)
        target_env = self._id_env_cache.get(cache_key)
        if (
            target_env is None
            or not self._is_env_visible(target_env)
            or name not in target_env.values
        ):
            target_env = self._resolve_env_for_name(name)
            if target_env is None:
                raise MicelioRuntimeError(f"Variable '{name}' no definida")
            self._id_env_cache[cache_key] = target_env
        return target_env.values[name]

    def visitParenExpr(self, ctx: MicelioParser.ParenExprContext):
        return self.visit(ctx.expr())

    def visitListExpr(self, ctx: MicelioParser.ListExprContext):
        return [self.visit(e) for e in ctx.expr()]

    def visitSetExpr(self, ctx: MicelioParser.SetExprContext):
        return set(self.visit(e) for e in ctx.expr())

    def visitDictExpr(self, ctx: MicelioParser.DictExprContext):
        out = {}
        for kv in ctx.keyValue():
            out[self.visit(kv.expr(0))] = self.visit(kv.expr(1))
        return out

    def visitMapLiteral(self, ctx: MicelioParser.MapLiteralContext):
        out = {}
        for kv in ctx.keyValue():
            out[self.visit(kv.expr(0))] = self.visit(kv.expr(1))
        return out

    def visitAnonFuncExpr(self, ctx: MicelioParser.AnonFuncExprContext):
        params: list[str] = []
        args_param = None
        kwargs_param = None

        if ctx.param_list() is not None:
            for param_item in ctx.param_list().param_item():
                if isinstance(param_item, MicelioParser.ParamNormalContext):
                    params.append(param_item.ID().getText())
                elif isinstance(param_item, MicelioParser.ParamArgsContext):
                    args_param = param_item.ID().getText()
                elif isinstance(param_item, MicelioParser.ParamKwargsContext):
                    kwargs_param = param_item.ID().getText()

        return FunctionValue(
            name=None,
            params=params,
            args_param=args_param,
            kwargs_param=kwargs_param,
            body_ctx=ctx.block(),
            closure=self.env,
        )

    def _apply_postfix_suffix(self, value, suffix_ctx):
        if isinstance(suffix_ctx, MicelioParser.IndexSuffixContext):
            index = self.visit(suffix_ctx.expr())
            return value[index]

        if isinstance(suffix_ctx, MicelioParser.CallSuffixContext):
            args = []
            if suffix_ctx.exprList() is not None:
                args = [self.visit(e) for e in suffix_ctx.exprList().expr()]
            return self._call_callable(value, args)

        if isinstance(suffix_ctx, MicelioParser.MemberSuffixContext):
            member = suffix_ctx.ID().getText()
            if isinstance(value, dict) and member in value:
                return value[member]
            return BoundMethod(value, member)

        return value

    def _evaluate_postfix_expr(self, ctx: MicelioParser.PostfixExprNodeContext):
        value = self.visit(ctx.primary())
        suffixes = list(ctx.postfixSuffix())
        if not suffixes:
            return value

        for suffix_ctx in suffixes:
            value = self._apply_postfix_suffix(value, suffix_ctx)
        return value

    def visitPostfixRoot(self, ctx: MicelioParser.PostfixRootContext):
        return self._evaluate_postfix_expr(ctx.postfixExpr())

    def visitPostfixExprNode(self, ctx: MicelioParser.PostfixExprNodeContext):
        return self._evaluate_postfix_expr(ctx)

    def _inc_dec(self, expr_ctx, delta: int, post: bool):
        # Unwrap the expression to find the ID
        # expr_ctx could be a PostfixRootContext -> PostfixExprNodeContext -> primary (IdExprContext)
        id_expr = None
        
        # If it's a PostfixRootContext, get the postfixExpr
        if isinstance(expr_ctx, MicelioParser.PostfixRootContext):
            postfix_expr = expr_ctx.postfixExpr()
            if isinstance(postfix_expr, MicelioParser.PostfixExprNodeContext):
                # Check if it has no suffixes
                if postfix_expr.getChildCount() == 1:  # Only the primary
                    primary = postfix_expr.primary()
                    if isinstance(primary, MicelioParser.IdExprContext):
                        id_expr = primary
        # If it's already an IdExprContext
        elif isinstance(expr_ctx, MicelioParser.IdExprContext):
            id_expr = expr_ctx
        # If it's a PostfixExprNodeContext with no suffixes
        elif isinstance(expr_ctx, MicelioParser.PostfixExprNodeContext):
            if expr_ctx.getChildCount() == 1:
                primary = expr_ctx.primary()
                if isinstance(primary, MicelioParser.IdExprContext):
                    id_expr = primary
        
        if id_expr is None:
            raise MicelioRuntimeError("++/-- solo funciona con variables")
        
        name = id_expr.ID().getText()
        cur = self.env.get(name)
        self._ensure_number(cur, "++/--")
        new_val = cur + delta
        self.env.assign(name, new_val)
        return cur if post else new_val

    def visitPreIncDec(self, ctx: MicelioParser.PreIncDecContext):
        delta = 1 if ctx.op.text == '++' else -1
        return self._inc_dec(ctx.expr(), delta, post=False)

    def visitPostIncDec(self, ctx: MicelioParser.PostIncDecContext):
        delta = 1 if ctx.op.text == '++' else -1
        return self._inc_dec(ctx.expr(), delta, post=True)

    def visitUnaryMinus(self, ctx: MicelioParser.UnaryMinusContext):
        value = self.visit(ctx.expr())
        self._ensure_number(value, "-")
        return -value

    def visitNotExpr(self, ctx: MicelioParser.NotExprContext):
        return not self.visit(ctx.expr())

    def visitMulDivMod(self, ctx: MicelioParser.MulDivModContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.op.text

        if op == '.*':
            return elementwise_mul(left, right)

        if op == '*':
            if isinstance(left, list) and left and isinstance(left[0], list) and isinstance(right, list) and right and isinstance(right[0], list):
                return matrix_mul(left, right)
            return left * right

        self._ensure_number(left, op)
        self._ensure_number(right, op)
        if op == '/':
            if right == 0:
                raise MicelioRuntimeError("Division por cero")
            return left / right
        if op == '%':
            if right == 0:
                raise MicelioRuntimeError("Modulo por cero")
            return left % right
        return None

    def visitAddSub(self, ctx: MicelioParser.AddSubContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))

        if self._is_numeric_matrix(left) and self._is_numeric_matrix(right):
            return self._matrix_add_sub(left, right, ctx.op.text == '+')

        if ctx.op.text == '+':
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        return left - right

    def visitPowExpr(self, ctx: MicelioParser.PowExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        self._ensure_number(left, '**')
        self._ensure_number(right, '**')
        return left ** right

    def visitComparison(self, ctx: MicelioParser.ComparisonContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.op.text
        if op == '==':
            return left == right
        if op == '!=':
            return left != right
        if op == '<':
            return left < right
        if op == '<=':
            return left <= right
        if op == '>':
            return left > right
        if op == '>=':
            return left >= right
        return None

    def visitAndExpr(self, ctx: MicelioParser.AndExprContext):
        left = self.visit(ctx.expr(0))
        if not left:
            return False
        return bool(self.visit(ctx.expr(1)))

    def visitOrExpr(self, ctx: MicelioParser.OrExprContext):
        left = self.visit(ctx.expr(0))
        if left:
            return True
        return bool(self.visit(ctx.expr(1)))

    def visitInExpr(self, ctx: MicelioParser.InExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        return left in right

    def visitPipeExpr(self, ctx: MicelioParser.PipeExprContext):
        left_value = self.visit(ctx.expr(0))
        right_ctx = ctx.expr(1)

        postfix_root = right_ctx if isinstance(right_ctx, MicelioParser.PostfixRootContext) else None
        postfix_expr = postfix_root.postfixExpr() if postfix_root is not None else None

        if isinstance(postfix_expr, MicelioParser.PostfixExprNodeContext):
            suffixes = list(postfix_expr.postfixSuffix())
            if suffixes and isinstance(suffixes[-1], MicelioParser.CallSuffixContext):
                callee = self.visit(postfix_expr.primary())
                for suffix_ctx in suffixes[:-1]:
                    callee = self._apply_postfix_suffix(callee, suffix_ctx)

                call_suffix = suffixes[-1]
                args = []
                if call_suffix.exprList() is not None:
                    args = [self.visit(e) for e in call_suffix.exprList().expr()]
                if not args:
                    return self._call_callable(callee, [left_value])
                pipe_args = [args[0], left_value] + args[1:]
                return self._call_callable(callee, pipe_args)

        callee = self.visit(right_ctx)
        return self._call_callable(callee, [left_value])

    def visitMemberAccess(self, ctx: MicelioParser.MemberAccessContext):
        obj = self.visit(ctx.expr())
        member = ctx.ID().getText()

        if isinstance(obj, dict) and member in obj:
            return obj[member]

        return BoundMethod(obj, member)
