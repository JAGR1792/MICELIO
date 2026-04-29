// Generated from gramatica/Micelio.g4 by ANTLR 4.13.2
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link MicelioParser}.
 */
public interface MicelioListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link MicelioParser#program}.
	 * @param ctx the parse tree
	 */
	void enterProgram(MicelioParser.ProgramContext ctx);
	/**
	 * Exit a parse tree produced by {@link MicelioParser#program}.
	 * @param ctx the parse tree
	 */
	void exitProgram(MicelioParser.ProgramContext ctx);
	/**
	 * Enter a parse tree produced by {@link MicelioParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterStatement(MicelioParser.StatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link MicelioParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitStatement(MicelioParser.StatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link MicelioParser#simple_stmt}.
	 * @param ctx the parse tree
	 */
	void enterSimple_stmt(MicelioParser.Simple_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MicelioParser#simple_stmt}.
	 * @param ctx the parse tree
	 */
	void exitSimple_stmt(MicelioParser.Simple_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link MicelioParser#compound_stmt}.
	 * @param ctx the parse tree
	 */
	void enterCompound_stmt(MicelioParser.Compound_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MicelioParser#compound_stmt}.
	 * @param ctx the parse tree
	 */
	void exitCompound_stmt(MicelioParser.Compound_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link MicelioParser#var_decl}.
	 * @param ctx the parse tree
	 */
	void enterVar_decl(MicelioParser.Var_declContext ctx);
	/**
	 * Exit a parse tree produced by {@link MicelioParser#var_decl}.
	 * @param ctx the parse tree
	 */
	void exitVar_decl(MicelioParser.Var_declContext ctx);
	/**
	 * Enter a parse tree produced by {@link MicelioParser#const_decl}.
	 * @param ctx the parse tree
	 */
	void enterConst_decl(MicelioParser.Const_declContext ctx);
	/**
	 * Exit a parse tree produced by {@link MicelioParser#const_decl}.
	 * @param ctx the parse tree
	 */
	void exitConst_decl(MicelioParser.Const_declContext ctx);
	/**
	 * Enter a parse tree produced by {@link MicelioParser#assignment}.
	 * @param ctx the parse tree
	 */
	void enterAssignment(MicelioParser.AssignmentContext ctx);
	/**
	 * Exit a parse tree produced by {@link MicelioParser#assignment}.
	 * @param ctx the parse tree
	 */
	void exitAssignment(MicelioParser.AssignmentContext ctx);
	/**
	 * Enter a parse tree produced by {@link MicelioParser#return_stmt}.
	 * @param ctx the parse tree
	 */
	void enterReturn_stmt(MicelioParser.Return_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MicelioParser#return_stmt}.
	 * @param ctx the parse tree
	 */
	void exitReturn_stmt(MicelioParser.Return_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link MicelioParser#break_stmt}.
	 * @param ctx the parse tree
	 */
	void enterBreak_stmt(MicelioParser.Break_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MicelioParser#break_stmt}.
	 * @param ctx the parse tree
	 */
	void exitBreak_stmt(MicelioParser.Break_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link MicelioParser#continue_stmt}.
	 * @param ctx the parse tree
	 */
	void enterContinue_stmt(MicelioParser.Continue_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MicelioParser#continue_stmt}.
	 * @param ctx the parse tree
	 */
	void exitContinue_stmt(MicelioParser.Continue_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link MicelioParser#import_stmt}.
	 * @param ctx the parse tree
	 */
	void enterImport_stmt(MicelioParser.Import_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MicelioParser#import_stmt}.
	 * @param ctx the parse tree
	 */
	void exitImport_stmt(MicelioParser.Import_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link MicelioParser#leer_stmt}.
	 * @param ctx the parse tree
	 */
	void enterLeer_stmt(MicelioParser.Leer_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MicelioParser#leer_stmt}.
	 * @param ctx the parse tree
	 */
	void exitLeer_stmt(MicelioParser.Leer_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link MicelioParser#imp_stmt}.
	 * @param ctx the parse tree
	 */
	void enterImp_stmt(MicelioParser.Imp_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MicelioParser#imp_stmt}.
	 * @param ctx the parse tree
	 */
	void exitImp_stmt(MicelioParser.Imp_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link MicelioParser#if_stmt}.
	 * @param ctx the parse tree
	 */
	void enterIf_stmt(MicelioParser.If_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MicelioParser#if_stmt}.
	 * @param ctx the parse tree
	 */
	void exitIf_stmt(MicelioParser.If_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link MicelioParser#switch_stmt}.
	 * @param ctx the parse tree
	 */
	void enterSwitch_stmt(MicelioParser.Switch_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MicelioParser#switch_stmt}.
	 * @param ctx the parse tree
	 */
	void exitSwitch_stmt(MicelioParser.Switch_stmtContext ctx);
	/**
	 * Enter a parse tree produced by the {@code caseClause}
	 * labeled alternative in {@link MicelioParser#case_block}.
	 * @param ctx the parse tree
	 */
	void enterCaseClause(MicelioParser.CaseClauseContext ctx);
	/**
	 * Exit a parse tree produced by the {@code caseClause}
	 * labeled alternative in {@link MicelioParser#case_block}.
	 * @param ctx the parse tree
	 */
	void exitCaseClause(MicelioParser.CaseClauseContext ctx);
	/**
	 * Enter a parse tree produced by the {@code defaultClause}
	 * labeled alternative in {@link MicelioParser#case_block}.
	 * @param ctx the parse tree
	 */
	void enterDefaultClause(MicelioParser.DefaultClauseContext ctx);
	/**
	 * Exit a parse tree produced by the {@code defaultClause}
	 * labeled alternative in {@link MicelioParser#case_block}.
	 * @param ctx the parse tree
	 */
	void exitDefaultClause(MicelioParser.DefaultClauseContext ctx);
	/**
	 * Enter a parse tree produced by {@link MicelioParser#while_stmt}.
	 * @param ctx the parse tree
	 */
	void enterWhile_stmt(MicelioParser.While_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MicelioParser#while_stmt}.
	 * @param ctx the parse tree
	 */
	void exitWhile_stmt(MicelioParser.While_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link MicelioParser#for_stmt}.
	 * @param ctx the parse tree
	 */
	void enterFor_stmt(MicelioParser.For_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link MicelioParser#for_stmt}.
	 * @param ctx the parse tree
	 */
	void exitFor_stmt(MicelioParser.For_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link MicelioParser#func_def}.
	 * @param ctx the parse tree
	 */
	void enterFunc_def(MicelioParser.Func_defContext ctx);
	/**
	 * Exit a parse tree produced by {@link MicelioParser#func_def}.
	 * @param ctx the parse tree
	 */
	void exitFunc_def(MicelioParser.Func_defContext ctx);
	/**
	 * Enter a parse tree produced by {@link MicelioParser#param_list}.
	 * @param ctx the parse tree
	 */
	void enterParam_list(MicelioParser.Param_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link MicelioParser#param_list}.
	 * @param ctx the parse tree
	 */
	void exitParam_list(MicelioParser.Param_listContext ctx);
	/**
	 * Enter a parse tree produced by the {@code paramNormal}
	 * labeled alternative in {@link MicelioParser#param_item}.
	 * @param ctx the parse tree
	 */
	void enterParamNormal(MicelioParser.ParamNormalContext ctx);
	/**
	 * Exit a parse tree produced by the {@code paramNormal}
	 * labeled alternative in {@link MicelioParser#param_item}.
	 * @param ctx the parse tree
	 */
	void exitParamNormal(MicelioParser.ParamNormalContext ctx);
	/**
	 * Enter a parse tree produced by the {@code paramArgs}
	 * labeled alternative in {@link MicelioParser#param_item}.
	 * @param ctx the parse tree
	 */
	void enterParamArgs(MicelioParser.ParamArgsContext ctx);
	/**
	 * Exit a parse tree produced by the {@code paramArgs}
	 * labeled alternative in {@link MicelioParser#param_item}.
	 * @param ctx the parse tree
	 */
	void exitParamArgs(MicelioParser.ParamArgsContext ctx);
	/**
	 * Enter a parse tree produced by the {@code paramKwargs}
	 * labeled alternative in {@link MicelioParser#param_item}.
	 * @param ctx the parse tree
	 */
	void enterParamKwargs(MicelioParser.ParamKwargsContext ctx);
	/**
	 * Exit a parse tree produced by the {@code paramKwargs}
	 * labeled alternative in {@link MicelioParser#param_item}.
	 * @param ctx the parse tree
	 */
	void exitParamKwargs(MicelioParser.ParamKwargsContext ctx);
	/**
	 * Enter a parse tree produced by {@link MicelioParser#block}.
	 * @param ctx the parse tree
	 */
	void enterBlock(MicelioParser.BlockContext ctx);
	/**
	 * Exit a parse tree produced by {@link MicelioParser#block}.
	 * @param ctx the parse tree
	 */
	void exitBlock(MicelioParser.BlockContext ctx);
	/**
	 * Enter a parse tree produced by the {@code mulDivMod}
	 * labeled alternative in {@link MicelioParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterMulDivMod(MicelioParser.MulDivModContext ctx);
	/**
	 * Exit a parse tree produced by the {@code mulDivMod}
	 * labeled alternative in {@link MicelioParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitMulDivMod(MicelioParser.MulDivModContext ctx);
	/**
	 * Enter a parse tree produced by the {@code postfixRoot}
	 * labeled alternative in {@link MicelioParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterPostfixRoot(MicelioParser.PostfixRootContext ctx);
	/**
	 * Exit a parse tree produced by the {@code postfixRoot}
	 * labeled alternative in {@link MicelioParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitPostfixRoot(MicelioParser.PostfixRootContext ctx);
	/**
	 * Enter a parse tree produced by the {@code pipeExpr}
	 * labeled alternative in {@link MicelioParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterPipeExpr(MicelioParser.PipeExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code pipeExpr}
	 * labeled alternative in {@link MicelioParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitPipeExpr(MicelioParser.PipeExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code comparison}
	 * labeled alternative in {@link MicelioParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterComparison(MicelioParser.ComparisonContext ctx);
	/**
	 * Exit a parse tree produced by the {@code comparison}
	 * labeled alternative in {@link MicelioParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitComparison(MicelioParser.ComparisonContext ctx);
	/**
	 * Enter a parse tree produced by the {@code inExpr}
	 * labeled alternative in {@link MicelioParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterInExpr(MicelioParser.InExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code inExpr}
	 * labeled alternative in {@link MicelioParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitInExpr(MicelioParser.InExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code orExpr}
	 * labeled alternative in {@link MicelioParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterOrExpr(MicelioParser.OrExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code orExpr}
	 * labeled alternative in {@link MicelioParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitOrExpr(MicelioParser.OrExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code addSub}
	 * labeled alternative in {@link MicelioParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterAddSub(MicelioParser.AddSubContext ctx);
	/**
	 * Exit a parse tree produced by the {@code addSub}
	 * labeled alternative in {@link MicelioParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitAddSub(MicelioParser.AddSubContext ctx);
	/**
	 * Enter a parse tree produced by the {@code postIncDec}
	 * labeled alternative in {@link MicelioParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterPostIncDec(MicelioParser.PostIncDecContext ctx);
	/**
	 * Exit a parse tree produced by the {@code postIncDec}
	 * labeled alternative in {@link MicelioParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitPostIncDec(MicelioParser.PostIncDecContext ctx);
	/**
	 * Enter a parse tree produced by the {@code notExpr}
	 * labeled alternative in {@link MicelioParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterNotExpr(MicelioParser.NotExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code notExpr}
	 * labeled alternative in {@link MicelioParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitNotExpr(MicelioParser.NotExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code unaryMinus}
	 * labeled alternative in {@link MicelioParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterUnaryMinus(MicelioParser.UnaryMinusContext ctx);
	/**
	 * Exit a parse tree produced by the {@code unaryMinus}
	 * labeled alternative in {@link MicelioParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitUnaryMinus(MicelioParser.UnaryMinusContext ctx);
	/**
	 * Enter a parse tree produced by the {@code powExpr}
	 * labeled alternative in {@link MicelioParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterPowExpr(MicelioParser.PowExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code powExpr}
	 * labeled alternative in {@link MicelioParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitPowExpr(MicelioParser.PowExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code preIncDec}
	 * labeled alternative in {@link MicelioParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterPreIncDec(MicelioParser.PreIncDecContext ctx);
	/**
	 * Exit a parse tree produced by the {@code preIncDec}
	 * labeled alternative in {@link MicelioParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitPreIncDec(MicelioParser.PreIncDecContext ctx);
	/**
	 * Enter a parse tree produced by the {@code andExpr}
	 * labeled alternative in {@link MicelioParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterAndExpr(MicelioParser.AndExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code andExpr}
	 * labeled alternative in {@link MicelioParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitAndExpr(MicelioParser.AndExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code postfixExprNode}
	 * labeled alternative in {@link MicelioParser#postfixExpr}.
	 * @param ctx the parse tree
	 */
	void enterPostfixExprNode(MicelioParser.PostfixExprNodeContext ctx);
	/**
	 * Exit a parse tree produced by the {@code postfixExprNode}
	 * labeled alternative in {@link MicelioParser#postfixExpr}.
	 * @param ctx the parse tree
	 */
	void exitPostfixExprNode(MicelioParser.PostfixExprNodeContext ctx);
	/**
	 * Enter a parse tree produced by the {@code literalExpr}
	 * labeled alternative in {@link MicelioParser#primary}.
	 * @param ctx the parse tree
	 */
	void enterLiteralExpr(MicelioParser.LiteralExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code literalExpr}
	 * labeled alternative in {@link MicelioParser#primary}.
	 * @param ctx the parse tree
	 */
	void exitLiteralExpr(MicelioParser.LiteralExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code idExpr}
	 * labeled alternative in {@link MicelioParser#primary}.
	 * @param ctx the parse tree
	 */
	void enterIdExpr(MicelioParser.IdExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code idExpr}
	 * labeled alternative in {@link MicelioParser#primary}.
	 * @param ctx the parse tree
	 */
	void exitIdExpr(MicelioParser.IdExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code parenExpr}
	 * labeled alternative in {@link MicelioParser#primary}.
	 * @param ctx the parse tree
	 */
	void enterParenExpr(MicelioParser.ParenExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code parenExpr}
	 * labeled alternative in {@link MicelioParser#primary}.
	 * @param ctx the parse tree
	 */
	void exitParenExpr(MicelioParser.ParenExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code listExpr}
	 * labeled alternative in {@link MicelioParser#primary}.
	 * @param ctx the parse tree
	 */
	void enterListExpr(MicelioParser.ListExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code listExpr}
	 * labeled alternative in {@link MicelioParser#primary}.
	 * @param ctx the parse tree
	 */
	void exitListExpr(MicelioParser.ListExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code setExpr}
	 * labeled alternative in {@link MicelioParser#primary}.
	 * @param ctx the parse tree
	 */
	void enterSetExpr(MicelioParser.SetExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code setExpr}
	 * labeled alternative in {@link MicelioParser#primary}.
	 * @param ctx the parse tree
	 */
	void exitSetExpr(MicelioParser.SetExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code dictExpr}
	 * labeled alternative in {@link MicelioParser#primary}.
	 * @param ctx the parse tree
	 */
	void enterDictExpr(MicelioParser.DictExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code dictExpr}
	 * labeled alternative in {@link MicelioParser#primary}.
	 * @param ctx the parse tree
	 */
	void exitDictExpr(MicelioParser.DictExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code mapLiteral}
	 * labeled alternative in {@link MicelioParser#primary}.
	 * @param ctx the parse tree
	 */
	void enterMapLiteral(MicelioParser.MapLiteralContext ctx);
	/**
	 * Exit a parse tree produced by the {@code mapLiteral}
	 * labeled alternative in {@link MicelioParser#primary}.
	 * @param ctx the parse tree
	 */
	void exitMapLiteral(MicelioParser.MapLiteralContext ctx);
	/**
	 * Enter a parse tree produced by the {@code anonFuncExpr}
	 * labeled alternative in {@link MicelioParser#primary}.
	 * @param ctx the parse tree
	 */
	void enterAnonFuncExpr(MicelioParser.AnonFuncExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code anonFuncExpr}
	 * labeled alternative in {@link MicelioParser#primary}.
	 * @param ctx the parse tree
	 */
	void exitAnonFuncExpr(MicelioParser.AnonFuncExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code matrizExpr}
	 * labeled alternative in {@link MicelioParser#primary}.
	 * @param ctx the parse tree
	 */
	void enterMatrizExpr(MicelioParser.MatrizExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code matrizExpr}
	 * labeled alternative in {@link MicelioParser#primary}.
	 * @param ctx the parse tree
	 */
	void exitMatrizExpr(MicelioParser.MatrizExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code indexSuffix}
	 * labeled alternative in {@link MicelioParser#postfixSuffix}.
	 * @param ctx the parse tree
	 */
	void enterIndexSuffix(MicelioParser.IndexSuffixContext ctx);
	/**
	 * Exit a parse tree produced by the {@code indexSuffix}
	 * labeled alternative in {@link MicelioParser#postfixSuffix}.
	 * @param ctx the parse tree
	 */
	void exitIndexSuffix(MicelioParser.IndexSuffixContext ctx);
	/**
	 * Enter a parse tree produced by the {@code callSuffix}
	 * labeled alternative in {@link MicelioParser#postfixSuffix}.
	 * @param ctx the parse tree
	 */
	void enterCallSuffix(MicelioParser.CallSuffixContext ctx);
	/**
	 * Exit a parse tree produced by the {@code callSuffix}
	 * labeled alternative in {@link MicelioParser#postfixSuffix}.
	 * @param ctx the parse tree
	 */
	void exitCallSuffix(MicelioParser.CallSuffixContext ctx);
	/**
	 * Enter a parse tree produced by the {@code memberSuffix}
	 * labeled alternative in {@link MicelioParser#postfixSuffix}.
	 * @param ctx the parse tree
	 */
	void enterMemberSuffix(MicelioParser.MemberSuffixContext ctx);
	/**
	 * Exit a parse tree produced by the {@code memberSuffix}
	 * labeled alternative in {@link MicelioParser#postfixSuffix}.
	 * @param ctx the parse tree
	 */
	void exitMemberSuffix(MicelioParser.MemberSuffixContext ctx);
	/**
	 * Enter a parse tree produced by {@link MicelioParser#keyValue}.
	 * @param ctx the parse tree
	 */
	void enterKeyValue(MicelioParser.KeyValueContext ctx);
	/**
	 * Exit a parse tree produced by {@link MicelioParser#keyValue}.
	 * @param ctx the parse tree
	 */
	void exitKeyValue(MicelioParser.KeyValueContext ctx);
	/**
	 * Enter a parse tree produced by {@link MicelioParser#exprList}.
	 * @param ctx the parse tree
	 */
	void enterExprList(MicelioParser.ExprListContext ctx);
	/**
	 * Exit a parse tree produced by {@link MicelioParser#exprList}.
	 * @param ctx the parse tree
	 */
	void exitExprList(MicelioParser.ExprListContext ctx);
	/**
	 * Enter a parse tree produced by {@link MicelioParser#literal}.
	 * @param ctx the parse tree
	 */
	void enterLiteral(MicelioParser.LiteralContext ctx);
	/**
	 * Exit a parse tree produced by {@link MicelioParser#literal}.
	 * @param ctx the parse tree
	 */
	void exitLiteral(MicelioParser.LiteralContext ctx);
	/**
	 * Enter a parse tree produced by {@link MicelioParser#sep}.
	 * @param ctx the parse tree
	 */
	void enterSep(MicelioParser.SepContext ctx);
	/**
	 * Exit a parse tree produced by {@link MicelioParser#sep}.
	 * @param ctx the parse tree
	 */
	void exitSep(MicelioParser.SepContext ctx);
}