from __future__ import annotations

import ast
import os

from antlr4 import CommonTokenStream, InputStream
from antlr4 import ParserRuleContext

from MicelioLexer import MicelioLexer
from MicelioParser import MicelioParser
from MicelioVisitor import MicelioVisitor
from runtime import (
    BoundMethod,
    BreakFlow,
    ContinueFlow,
    Environment,
    FunctionValue,
    MicelioRuntimeError,
    ReturnFlow,
    elementwise_mul,
    make_builtins,
    matrix_mul,
    micelio_repr,
    module_table,
)


class EvalVisitor(MicelioVisitor):
    def __init__(self, base_dir: str | None = None):
        super().__init__()
        self.global_env = Environment()
        self.env = self.global_env
        self.modules = module_table()
        self.current_dir = os.path.abspath(base_dir or os.getcwd())
        self.loaded_modules: dict[str, dict[str, object]] = {}
        builtins = make_builtins()

        def _map(fn, iterable):
            return [self._call_callable(fn, [x]) for x in iterable]

        def _filter(fn, iterable):
            return [x for x in iterable if self._call_callable(fn, [x])]

        def _reduce(fn, iterable, initial):
            acc = initial
            for x in iterable:
                acc = self._call_callable(fn, [acc, x])
            return acc

        builtins["map"] = _map
        builtins["filter"] = _filter
        builtins["reduce"] = _reduce

        if "lista" in self.modules:
            self.modules["lista"]["map"] = _map
            self.modules["lista"]["filter"] = _filter
            self.modules["lista"]["reduce"] = _reduce

        for name, fn in builtins.items():
            self.global_env.define(name, fn)

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

    def _assign_or_define(self, name: str, value):
        try:
            self.env.assign(name, value)
        except MicelioRuntimeError:
            self.env.define(name, value)

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
            return fn.call(args, self._eval_in_env)
        return fn(*args)

    def _decode_string_literal(self, raw: str) -> str:
        try:
            value = ast.literal_eval(raw)
        except (SyntaxError, ValueError):
            return raw[1:-1]
        return value if isinstance(value, str) else str(value)

    def visitProgram(self, ctx: MicelioParser.ProgramContext):
        result = None
        for child in ctx.children:
            if isinstance(child, MicelioParser.StatementContext):
                result = self.visit(child)
        return result

    def visitStatement(self, ctx: MicelioParser.StatementContext):
        return self.visitChildren(ctx)

    def visitVar_decl(self, ctx: MicelioParser.Var_declContext):
        names = [ident.getText() for ident in ctx.ID()]
        expr_nodes = ctx.expr()

        if not expr_nodes:
            for name in names:
                self.env.define(name, None)
            return None

        if len(expr_nodes) == 1:
            value = self.visit(expr_nodes[0])
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
        name = ctx.ID().getText()
        value = self.visit(ctx.expr())
        self.env.assign(name, value)
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

                saved_dir = self.current_dir
                self.current_dir = os.path.dirname(full_path)
                before = set(self.global_env.values.keys())
                try:
                    self._execute_source(code)
                finally:
                    self.current_dir = saved_dir

                exported = {
                    name: value
                    for name, value in self.global_env.values.items()
                    if name not in before and not name.startswith("_")
                }
                module = exported
                self.loaded_modules[full_path] = module

        alias = ctx.ID().getText() if ctx.ID() else module_name
        self.env.define(alias, module)
        return module

    def visitLeer_stmt(self, ctx: MicelioParser.Leer_stmtContext):
        name = ctx.ID().getText()
        raw = input()
        value = raw
        try:
            value = float(raw) if '.' in raw else int(raw)
        except ValueError:
            low = raw.strip().lower()
            if low == 'verdadero':
                value = True
            elif low == 'falso':
                value = False
            elif low == 'nulo':
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
        while self.visit(ctx.expr()):
            try:
                result = self.visit(ctx.block())
            except ContinueFlow:
                continue
            except BreakFlow:
                break
        return result

    def visitFor_stmt(self, ctx: MicelioParser.For_stmtContext):
        var_name = ctx.ID().getText()
        result = None

        if ctx.EN() is not None:
            iterable = self.visit(ctx.expr(0))
            if not isinstance(iterable, (list, tuple, set, str, dict)):
                raise MicelioRuntimeError("para ... en requiere un iterable")
            for value in iterable:
                self._assign_or_define(var_name, value)
                try:
                    result = self.visit(ctx.block())
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

        def condition(cur):
            return cur <= end if step > 0 else cur >= end

        current = start
        while condition(current):
            self.env.assign(var_name, current)
            try:
                result = self.visit(ctx.block())
            except ContinueFlow:
                pass
            except BreakFlow:
                break
            current = current + step
        return result

    def visitFunc_def(self, ctx: MicelioParser.Func_defContext):
        name = ctx.ID().getText()
        params = [p.getText() for p in (ctx.param_list().ID() if ctx.param_list() else [])]
        fn = FunctionValue(name=name, params=params, body_ctx=ctx.block(), closure=self.env)
        self.env.define(name, fn)
        return fn

    def visitBlock(self, ctx: MicelioParser.BlockContext):
        local = Environment(self.env)
        result = None
        saved = self.env
        self.env = local
        try:
            for st in ctx.statement():
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
        return self.env.get(ctx.ID().getText())

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
        params = [p.getText() for p in (ctx.param_list().ID() if ctx.param_list() else [])]
        return FunctionValue(name=None, params=params, body_ctx=ctx.block(), closure=self.env)

    def visitIndexExpr(self, ctx: MicelioParser.IndexExprContext):
        container = self.visit(ctx.expr(0))
        index = self.visit(ctx.expr(1))
        return container[index]

    def visitCallExpr(self, ctx: MicelioParser.CallExprContext):
        callee = self.visit(ctx.expr())
        args = []
        if ctx.exprList() is not None:
            args = [self.visit(e) for e in ctx.exprList().expr()]
        return self._call_callable(callee, args)

    def _inc_dec(self, expr_ctx, delta: int, post: bool):
        if not isinstance(expr_ctx, MicelioParser.IdExprContext):
            raise MicelioRuntimeError("++/-- solo funciona con variables")
        name = expr_ctx.ID().getText()
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

        if isinstance(right_ctx, MicelioParser.CallExprContext):
            callee = self.visit(right_ctx.expr())
            args = []
            if right_ctx.exprList() is not None:
                args = [self.visit(e) for e in right_ctx.exprList().expr()]
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
