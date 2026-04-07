# Generated from gramatica/Micelio.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .MicelioParser import MicelioParser
else:
    from MicelioParser import MicelioParser

# This class defines a complete listener for a parse tree produced by MicelioParser.
class MicelioListener(ParseTreeListener):

    # Enter a parse tree produced by MicelioParser#program.
    def enterProgram(self, ctx:MicelioParser.ProgramContext):
        pass

    # Exit a parse tree produced by MicelioParser#program.
    def exitProgram(self, ctx:MicelioParser.ProgramContext):
        pass


    # Enter a parse tree produced by MicelioParser#statement.
    def enterStatement(self, ctx:MicelioParser.StatementContext):
        pass

    # Exit a parse tree produced by MicelioParser#statement.
    def exitStatement(self, ctx:MicelioParser.StatementContext):
        pass


    # Enter a parse tree produced by MicelioParser#simple_stmt.
    def enterSimple_stmt(self, ctx:MicelioParser.Simple_stmtContext):
        pass

    # Exit a parse tree produced by MicelioParser#simple_stmt.
    def exitSimple_stmt(self, ctx:MicelioParser.Simple_stmtContext):
        pass


    # Enter a parse tree produced by MicelioParser#compound_stmt.
    def enterCompound_stmt(self, ctx:MicelioParser.Compound_stmtContext):
        pass

    # Exit a parse tree produced by MicelioParser#compound_stmt.
    def exitCompound_stmt(self, ctx:MicelioParser.Compound_stmtContext):
        pass


    # Enter a parse tree produced by MicelioParser#var_decl.
    def enterVar_decl(self, ctx:MicelioParser.Var_declContext):
        pass

    # Exit a parse tree produced by MicelioParser#var_decl.
    def exitVar_decl(self, ctx:MicelioParser.Var_declContext):
        pass


    # Enter a parse tree produced by MicelioParser#const_decl.
    def enterConst_decl(self, ctx:MicelioParser.Const_declContext):
        pass

    # Exit a parse tree produced by MicelioParser#const_decl.
    def exitConst_decl(self, ctx:MicelioParser.Const_declContext):
        pass


    # Enter a parse tree produced by MicelioParser#assignment.
    def enterAssignment(self, ctx:MicelioParser.AssignmentContext):
        pass

    # Exit a parse tree produced by MicelioParser#assignment.
    def exitAssignment(self, ctx:MicelioParser.AssignmentContext):
        pass


    # Enter a parse tree produced by MicelioParser#return_stmt.
    def enterReturn_stmt(self, ctx:MicelioParser.Return_stmtContext):
        pass

    # Exit a parse tree produced by MicelioParser#return_stmt.
    def exitReturn_stmt(self, ctx:MicelioParser.Return_stmtContext):
        pass


    # Enter a parse tree produced by MicelioParser#break_stmt.
    def enterBreak_stmt(self, ctx:MicelioParser.Break_stmtContext):
        pass

    # Exit a parse tree produced by MicelioParser#break_stmt.
    def exitBreak_stmt(self, ctx:MicelioParser.Break_stmtContext):
        pass


    # Enter a parse tree produced by MicelioParser#continue_stmt.
    def enterContinue_stmt(self, ctx:MicelioParser.Continue_stmtContext):
        pass

    # Exit a parse tree produced by MicelioParser#continue_stmt.
    def exitContinue_stmt(self, ctx:MicelioParser.Continue_stmtContext):
        pass


    # Enter a parse tree produced by MicelioParser#import_stmt.
    def enterImport_stmt(self, ctx:MicelioParser.Import_stmtContext):
        pass

    # Exit a parse tree produced by MicelioParser#import_stmt.
    def exitImport_stmt(self, ctx:MicelioParser.Import_stmtContext):
        pass


    # Enter a parse tree produced by MicelioParser#leer_stmt.
    def enterLeer_stmt(self, ctx:MicelioParser.Leer_stmtContext):
        pass

    # Exit a parse tree produced by MicelioParser#leer_stmt.
    def exitLeer_stmt(self, ctx:MicelioParser.Leer_stmtContext):
        pass


    # Enter a parse tree produced by MicelioParser#imp_stmt.
    def enterImp_stmt(self, ctx:MicelioParser.Imp_stmtContext):
        pass

    # Exit a parse tree produced by MicelioParser#imp_stmt.
    def exitImp_stmt(self, ctx:MicelioParser.Imp_stmtContext):
        pass


    # Enter a parse tree produced by MicelioParser#if_stmt.
    def enterIf_stmt(self, ctx:MicelioParser.If_stmtContext):
        pass

    # Exit a parse tree produced by MicelioParser#if_stmt.
    def exitIf_stmt(self, ctx:MicelioParser.If_stmtContext):
        pass


    # Enter a parse tree produced by MicelioParser#switch_stmt.
    def enterSwitch_stmt(self, ctx:MicelioParser.Switch_stmtContext):
        pass

    # Exit a parse tree produced by MicelioParser#switch_stmt.
    def exitSwitch_stmt(self, ctx:MicelioParser.Switch_stmtContext):
        pass


    # Enter a parse tree produced by MicelioParser#caseClause.
    def enterCaseClause(self, ctx:MicelioParser.CaseClauseContext):
        pass

    # Exit a parse tree produced by MicelioParser#caseClause.
    def exitCaseClause(self, ctx:MicelioParser.CaseClauseContext):
        pass


    # Enter a parse tree produced by MicelioParser#defaultClause.
    def enterDefaultClause(self, ctx:MicelioParser.DefaultClauseContext):
        pass

    # Exit a parse tree produced by MicelioParser#defaultClause.
    def exitDefaultClause(self, ctx:MicelioParser.DefaultClauseContext):
        pass


    # Enter a parse tree produced by MicelioParser#while_stmt.
    def enterWhile_stmt(self, ctx:MicelioParser.While_stmtContext):
        pass

    # Exit a parse tree produced by MicelioParser#while_stmt.
    def exitWhile_stmt(self, ctx:MicelioParser.While_stmtContext):
        pass


    # Enter a parse tree produced by MicelioParser#for_stmt.
    def enterFor_stmt(self, ctx:MicelioParser.For_stmtContext):
        pass

    # Exit a parse tree produced by MicelioParser#for_stmt.
    def exitFor_stmt(self, ctx:MicelioParser.For_stmtContext):
        pass


    # Enter a parse tree produced by MicelioParser#func_def.
    def enterFunc_def(self, ctx:MicelioParser.Func_defContext):
        pass

    # Exit a parse tree produced by MicelioParser#func_def.
    def exitFunc_def(self, ctx:MicelioParser.Func_defContext):
        pass


    # Enter a parse tree produced by MicelioParser#param_list.
    def enterParam_list(self, ctx:MicelioParser.Param_listContext):
        pass

    # Exit a parse tree produced by MicelioParser#param_list.
    def exitParam_list(self, ctx:MicelioParser.Param_listContext):
        pass


    # Enter a parse tree produced by MicelioParser#paramNormal.
    def enterParamNormal(self, ctx:MicelioParser.ParamNormalContext):
        pass

    # Exit a parse tree produced by MicelioParser#paramNormal.
    def exitParamNormal(self, ctx:MicelioParser.ParamNormalContext):
        pass


    # Enter a parse tree produced by MicelioParser#paramArgs.
    def enterParamArgs(self, ctx:MicelioParser.ParamArgsContext):
        pass

    # Exit a parse tree produced by MicelioParser#paramArgs.
    def exitParamArgs(self, ctx:MicelioParser.ParamArgsContext):
        pass


    # Enter a parse tree produced by MicelioParser#paramKwargs.
    def enterParamKwargs(self, ctx:MicelioParser.ParamKwargsContext):
        pass

    # Exit a parse tree produced by MicelioParser#paramKwargs.
    def exitParamKwargs(self, ctx:MicelioParser.ParamKwargsContext):
        pass


    # Enter a parse tree produced by MicelioParser#block.
    def enterBlock(self, ctx:MicelioParser.BlockContext):
        pass

    # Exit a parse tree produced by MicelioParser#block.
    def exitBlock(self, ctx:MicelioParser.BlockContext):
        pass


    # Enter a parse tree produced by MicelioParser#mulDivMod.
    def enterMulDivMod(self, ctx:MicelioParser.MulDivModContext):
        pass

    # Exit a parse tree produced by MicelioParser#mulDivMod.
    def exitMulDivMod(self, ctx:MicelioParser.MulDivModContext):
        pass


    # Enter a parse tree produced by MicelioParser#memberAccess.
    def enterMemberAccess(self, ctx:MicelioParser.MemberAccessContext):
        pass

    # Exit a parse tree produced by MicelioParser#memberAccess.
    def exitMemberAccess(self, ctx:MicelioParser.MemberAccessContext):
        pass


    # Enter a parse tree produced by MicelioParser#pipeExpr.
    def enterPipeExpr(self, ctx:MicelioParser.PipeExprContext):
        pass

    # Exit a parse tree produced by MicelioParser#pipeExpr.
    def exitPipeExpr(self, ctx:MicelioParser.PipeExprContext):
        pass


    # Enter a parse tree produced by MicelioParser#comparison.
    def enterComparison(self, ctx:MicelioParser.ComparisonContext):
        pass

    # Exit a parse tree produced by MicelioParser#comparison.
    def exitComparison(self, ctx:MicelioParser.ComparisonContext):
        pass


    # Enter a parse tree produced by MicelioParser#inExpr.
    def enterInExpr(self, ctx:MicelioParser.InExprContext):
        pass

    # Exit a parse tree produced by MicelioParser#inExpr.
    def exitInExpr(self, ctx:MicelioParser.InExprContext):
        pass


    # Enter a parse tree produced by MicelioParser#orExpr.
    def enterOrExpr(self, ctx:MicelioParser.OrExprContext):
        pass

    # Exit a parse tree produced by MicelioParser#orExpr.
    def exitOrExpr(self, ctx:MicelioParser.OrExprContext):
        pass


    # Enter a parse tree produced by MicelioParser#addSub.
    def enterAddSub(self, ctx:MicelioParser.AddSubContext):
        pass

    # Exit a parse tree produced by MicelioParser#addSub.
    def exitAddSub(self, ctx:MicelioParser.AddSubContext):
        pass


    # Enter a parse tree produced by MicelioParser#anonFuncExpr.
    def enterAnonFuncExpr(self, ctx:MicelioParser.AnonFuncExprContext):
        pass

    # Exit a parse tree produced by MicelioParser#anonFuncExpr.
    def exitAnonFuncExpr(self, ctx:MicelioParser.AnonFuncExprContext):
        pass


    # Enter a parse tree produced by MicelioParser#parenExpr.
    def enterParenExpr(self, ctx:MicelioParser.ParenExprContext):
        pass

    # Exit a parse tree produced by MicelioParser#parenExpr.
    def exitParenExpr(self, ctx:MicelioParser.ParenExprContext):
        pass


    # Enter a parse tree produced by MicelioParser#indexExpr.
    def enterIndexExpr(self, ctx:MicelioParser.IndexExprContext):
        pass

    # Exit a parse tree produced by MicelioParser#indexExpr.
    def exitIndexExpr(self, ctx:MicelioParser.IndexExprContext):
        pass


    # Enter a parse tree produced by MicelioParser#postIncDec.
    def enterPostIncDec(self, ctx:MicelioParser.PostIncDecContext):
        pass

    # Exit a parse tree produced by MicelioParser#postIncDec.
    def exitPostIncDec(self, ctx:MicelioParser.PostIncDecContext):
        pass


    # Enter a parse tree produced by MicelioParser#notExpr.
    def enterNotExpr(self, ctx:MicelioParser.NotExprContext):
        pass

    # Exit a parse tree produced by MicelioParser#notExpr.
    def exitNotExpr(self, ctx:MicelioParser.NotExprContext):
        pass


    # Enter a parse tree produced by MicelioParser#literalExpr.
    def enterLiteralExpr(self, ctx:MicelioParser.LiteralExprContext):
        pass

    # Exit a parse tree produced by MicelioParser#literalExpr.
    def exitLiteralExpr(self, ctx:MicelioParser.LiteralExprContext):
        pass


    # Enter a parse tree produced by MicelioParser#unaryMinus.
    def enterUnaryMinus(self, ctx:MicelioParser.UnaryMinusContext):
        pass

    # Exit a parse tree produced by MicelioParser#unaryMinus.
    def exitUnaryMinus(self, ctx:MicelioParser.UnaryMinusContext):
        pass


    # Enter a parse tree produced by MicelioParser#dictExpr.
    def enterDictExpr(self, ctx:MicelioParser.DictExprContext):
        pass

    # Exit a parse tree produced by MicelioParser#dictExpr.
    def exitDictExpr(self, ctx:MicelioParser.DictExprContext):
        pass


    # Enter a parse tree produced by MicelioParser#mapLiteral.
    def enterMapLiteral(self, ctx:MicelioParser.MapLiteralContext):
        pass

    # Exit a parse tree produced by MicelioParser#mapLiteral.
    def exitMapLiteral(self, ctx:MicelioParser.MapLiteralContext):
        pass


    # Enter a parse tree produced by MicelioParser#powExpr.
    def enterPowExpr(self, ctx:MicelioParser.PowExprContext):
        pass

    # Exit a parse tree produced by MicelioParser#powExpr.
    def exitPowExpr(self, ctx:MicelioParser.PowExprContext):
        pass


    # Enter a parse tree produced by MicelioParser#callExpr.
    def enterCallExpr(self, ctx:MicelioParser.CallExprContext):
        pass

    # Exit a parse tree produced by MicelioParser#callExpr.
    def exitCallExpr(self, ctx:MicelioParser.CallExprContext):
        pass


    # Enter a parse tree produced by MicelioParser#listExpr.
    def enterListExpr(self, ctx:MicelioParser.ListExprContext):
        pass

    # Exit a parse tree produced by MicelioParser#listExpr.
    def exitListExpr(self, ctx:MicelioParser.ListExprContext):
        pass


    # Enter a parse tree produced by MicelioParser#setExpr.
    def enterSetExpr(self, ctx:MicelioParser.SetExprContext):
        pass

    # Exit a parse tree produced by MicelioParser#setExpr.
    def exitSetExpr(self, ctx:MicelioParser.SetExprContext):
        pass


    # Enter a parse tree produced by MicelioParser#preIncDec.
    def enterPreIncDec(self, ctx:MicelioParser.PreIncDecContext):
        pass

    # Exit a parse tree produced by MicelioParser#preIncDec.
    def exitPreIncDec(self, ctx:MicelioParser.PreIncDecContext):
        pass


    # Enter a parse tree produced by MicelioParser#idExpr.
    def enterIdExpr(self, ctx:MicelioParser.IdExprContext):
        pass

    # Exit a parse tree produced by MicelioParser#idExpr.
    def exitIdExpr(self, ctx:MicelioParser.IdExprContext):
        pass


    # Enter a parse tree produced by MicelioParser#matrizExpr.
    def enterMatrizExpr(self, ctx:MicelioParser.MatrizExprContext):
        pass

    # Exit a parse tree produced by MicelioParser#matrizExpr.
    def exitMatrizExpr(self, ctx:MicelioParser.MatrizExprContext):
        pass


    # Enter a parse tree produced by MicelioParser#andExpr.
    def enterAndExpr(self, ctx:MicelioParser.AndExprContext):
        pass

    # Exit a parse tree produced by MicelioParser#andExpr.
    def exitAndExpr(self, ctx:MicelioParser.AndExprContext):
        pass


    # Enter a parse tree produced by MicelioParser#keyValue.
    def enterKeyValue(self, ctx:MicelioParser.KeyValueContext):
        pass

    # Exit a parse tree produced by MicelioParser#keyValue.
    def exitKeyValue(self, ctx:MicelioParser.KeyValueContext):
        pass


    # Enter a parse tree produced by MicelioParser#exprList.
    def enterExprList(self, ctx:MicelioParser.ExprListContext):
        pass

    # Exit a parse tree produced by MicelioParser#exprList.
    def exitExprList(self, ctx:MicelioParser.ExprListContext):
        pass


    # Enter a parse tree produced by MicelioParser#literal.
    def enterLiteral(self, ctx:MicelioParser.LiteralContext):
        pass

    # Exit a parse tree produced by MicelioParser#literal.
    def exitLiteral(self, ctx:MicelioParser.LiteralContext):
        pass


    # Enter a parse tree produced by MicelioParser#sep.
    def enterSep(self, ctx:MicelioParser.SepContext):
        pass

    # Exit a parse tree produced by MicelioParser#sep.
    def exitSep(self, ctx:MicelioParser.SepContext):
        pass



del MicelioParser