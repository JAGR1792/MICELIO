# Generated from gramatica/Micelio.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .MicelioParser import MicelioParser
else:
    from MicelioParser import MicelioParser

# This class defines a complete generic visitor for a parse tree produced by MicelioParser.

class MicelioVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MicelioParser#program.
    def visitProgram(self, ctx:MicelioParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#statement.
    def visitStatement(self, ctx:MicelioParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#simple_stmt.
    def visitSimple_stmt(self, ctx:MicelioParser.Simple_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#compound_stmt.
    def visitCompound_stmt(self, ctx:MicelioParser.Compound_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#var_decl.
    def visitVar_decl(self, ctx:MicelioParser.Var_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#const_decl.
    def visitConst_decl(self, ctx:MicelioParser.Const_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#assignment.
    def visitAssignment(self, ctx:MicelioParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#return_stmt.
    def visitReturn_stmt(self, ctx:MicelioParser.Return_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#break_stmt.
    def visitBreak_stmt(self, ctx:MicelioParser.Break_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#continue_stmt.
    def visitContinue_stmt(self, ctx:MicelioParser.Continue_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#import_stmt.
    def visitImport_stmt(self, ctx:MicelioParser.Import_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#leer_stmt.
    def visitLeer_stmt(self, ctx:MicelioParser.Leer_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#imp_stmt.
    def visitImp_stmt(self, ctx:MicelioParser.Imp_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#if_stmt.
    def visitIf_stmt(self, ctx:MicelioParser.If_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#switch_stmt.
    def visitSwitch_stmt(self, ctx:MicelioParser.Switch_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#caseClause.
    def visitCaseClause(self, ctx:MicelioParser.CaseClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#defaultClause.
    def visitDefaultClause(self, ctx:MicelioParser.DefaultClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#while_stmt.
    def visitWhile_stmt(self, ctx:MicelioParser.While_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#for_stmt.
    def visitFor_stmt(self, ctx:MicelioParser.For_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#func_def.
    def visitFunc_def(self, ctx:MicelioParser.Func_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#param_list.
    def visitParam_list(self, ctx:MicelioParser.Param_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#paramNormal.
    def visitParamNormal(self, ctx:MicelioParser.ParamNormalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#paramArgs.
    def visitParamArgs(self, ctx:MicelioParser.ParamArgsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#paramKwargs.
    def visitParamKwargs(self, ctx:MicelioParser.ParamKwargsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#block.
    def visitBlock(self, ctx:MicelioParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#mulDivMod.
    def visitMulDivMod(self, ctx:MicelioParser.MulDivModContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#memberAccess.
    def visitMemberAccess(self, ctx:MicelioParser.MemberAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#pipeExpr.
    def visitPipeExpr(self, ctx:MicelioParser.PipeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#comparison.
    def visitComparison(self, ctx:MicelioParser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#inExpr.
    def visitInExpr(self, ctx:MicelioParser.InExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#orExpr.
    def visitOrExpr(self, ctx:MicelioParser.OrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#addSub.
    def visitAddSub(self, ctx:MicelioParser.AddSubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#anonFuncExpr.
    def visitAnonFuncExpr(self, ctx:MicelioParser.AnonFuncExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#parenExpr.
    def visitParenExpr(self, ctx:MicelioParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#indexExpr.
    def visitIndexExpr(self, ctx:MicelioParser.IndexExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#postIncDec.
    def visitPostIncDec(self, ctx:MicelioParser.PostIncDecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#notExpr.
    def visitNotExpr(self, ctx:MicelioParser.NotExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#literalExpr.
    def visitLiteralExpr(self, ctx:MicelioParser.LiteralExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#unaryMinus.
    def visitUnaryMinus(self, ctx:MicelioParser.UnaryMinusContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#dictExpr.
    def visitDictExpr(self, ctx:MicelioParser.DictExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#mapLiteral.
    def visitMapLiteral(self, ctx:MicelioParser.MapLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#powExpr.
    def visitPowExpr(self, ctx:MicelioParser.PowExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#callExpr.
    def visitCallExpr(self, ctx:MicelioParser.CallExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#listExpr.
    def visitListExpr(self, ctx:MicelioParser.ListExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#setExpr.
    def visitSetExpr(self, ctx:MicelioParser.SetExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#preIncDec.
    def visitPreIncDec(self, ctx:MicelioParser.PreIncDecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#idExpr.
    def visitIdExpr(self, ctx:MicelioParser.IdExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#matrizExpr.
    def visitMatrizExpr(self, ctx:MicelioParser.MatrizExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#andExpr.
    def visitAndExpr(self, ctx:MicelioParser.AndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#keyValue.
    def visitKeyValue(self, ctx:MicelioParser.KeyValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#exprList.
    def visitExprList(self, ctx:MicelioParser.ExprListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#literal.
    def visitLiteral(self, ctx:MicelioParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MicelioParser#sep.
    def visitSep(self, ctx:MicelioParser.SepContext):
        return self.visitChildren(ctx)



del MicelioParser