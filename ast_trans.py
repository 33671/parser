from lark import Transformer, v_args
import lark
from tokens import TokenType,NodeType,AstNode,Token
from typing import Optional, List, Union

@v_args(inline=True)  # 使转换器方法接收解包后的子节点参数
class AstTransformer(Transformer):

    def program(self, *statements):
        return AstNode(NodeType.PROGRAM, children=list(statements))

    def declaration(self, type_, name, value=None):

        return AstNode(NodeType.DECLARATION,var_type=type_, var_name=name, right=value)

    def assignment(self, name, value):
        return AstNode(NodeType.ASSIGNMENT, var_name=name, right=value)


    def assign_expr(self, name, value=None):
        return AstNode(NodeType.ASSIGN_EXPR, var_name=name, right=value)

    def for_init_clause(self, clause=None):
        return AstNode(NodeType.FOR_INIT_CLAUSE, init_clause=clause)

    def for_cond_expr(self, name):
        return AstNode(NodeType.FOR_COND_EXPR, cond_expr=name)

    def assign_expr_for_update(self, name):
        return AstNode(NodeType.ASSIGN_EXPR_FOR_UPDATE, left=name)
    
    # def expression_statement(self, expr):
    #     return AstNode(NodeType.EXPRESSION_STATEMENT, for_body=expr)

    def if_statement(self, _, condition, then_branch, else_branch=None):
        return AstNode(NodeType.IF_STATEMENT, condition=condition, then_branch=then_branch, else_branch=else_branch)

    def for_statement(self, _, __, init, cond, update, ___, body):
        # 处理可选部分，如果它们是 None (Lark 在可选规则未匹配时会传递 None)
        # print(f"for_init: {init}, for_cond: {cond}, for_update: {update}")
        return AstNode(NodeType.FOR_STATEMENT, init_clause=init, cond_expr=cond, update_expr=update, for_body=body)

    def goto_statement(self, _, label):
        return AstNode(NodeType.GOTO_STATEMENT, label=label)

    def label_statement(self, label):
        return AstNode(NodeType.LABEL_STATEMENT, label=label)

    def block_statement(self, *statements):
        return AstNode(NodeType.BLOCK_STATEMENT, children=list(statements))
    def print_statement(self, expr):
        return AstNode(NodeType.PRINT_STATEMENT, right=expr)
    def empty_statement(self):
        return AstNode(NodeType.EMPTY_STATEMENT)  # 返回一个元组表示空语句

    # --- 表达式转换 ---
    def comparison(self, left, op, right):
      
        return AstNode(NodeType.COMPARISON, left=left, right=right, token=op)

    def term(self, left, op=None, right=None):
        # print(f"Parsing term: left:{left},op: {op},right: {right}")
        return AstNode(NodeType.TERM, left=left, right=right, token=op)

    def factor(self, left, op, right):
       
        return AstNode(NodeType.FACTOR, left=left, right=right, token=op)

    def neg(self, value):
        return AstNode(NodeType.UNARY_NEG, right=value, token=Token(type=TokenType.OP_SUB))
    
    def not_(self, value):
        return AstNode(NodeType.UNARY_NOT, right=value, token=Token(type=TokenType.NOT))

    def int_literal(self, value):
        return AstNode(NodeType.INT_LITERAL, token=Token(type=TokenType.INT, value=int(value)),value=int(value))

    def float_literal(self, value):
        return AstNode(NodeType.FLOAT_LITERAL, token=Token(type=TokenType.FLOAT, value=float(value)),value=float(value))

    def variable(self, name):
        return AstNode(NodeType.VARIABLE, var_name=name,token=Token(type=TokenType.IDENTIFIER, value=str(name)))

    # 类型转换
    def type(self, type_token):
        match type_token:
            case "int": return TokenType.INT
            case "float": return TokenType.FLOAT
            case _:
                raise ValueError(f"Unsupported type: {type_token}")
        return None  
    # 从 Token 获取字符串值
    def IDENTIFIER(self, s):
        return str(s)

    def INT_NUMBER(self, n):
        return int(n)

    def FLOAT_NUMBER(self, n):
        return float(n)  # Lark 会处理为 Python float

    def COMP_OP(self, op):
        op_type = None
        match op:
            case "<": op_type = TokenType.OP_LT
            case "<=": op_type = TokenType.OP_LE
            case ">": op_type = TokenType.OP_GT
            case ">=": op_type = TokenType.OP_GE
            case "==": op_type = TokenType.OP_EQ
            case "!=": op_type = TokenType.OP_NE
            case "&&": op_type = TokenType.OP_AND
            case "||": op_type = TokenType.OP_OR
            case _:
                raise ValueError(f"Unsupported comparison operator: {op}")
        return Token(type=op_type)

    def ADD_OP(self, op):
        op_type = None
        match op:
            case "+": op_type = TokenType.OP_ADD
            case "-": op_type = TokenType.OP_SUB
            case _:
                raise ValueError(f"Unsupported term operator: {op}")
        return Token(type=op_type)

    def MUL_OP(self, op):
        op_type = None
        match op:
            case "*": op_type = TokenType.OP_MUL
            case "/": op_type = TokenType.OP_DIV
            case "%": op_type = TokenType.OP_MOD
            case _:
                raise ValueError(f"Unsupported factor operator: {op}")
        return Token(type=op_type)