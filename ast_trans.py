from lark import Transformer, v_args
import lark
@v_args(inline=True)  # 使转换器方法接收解包后的子节点参数
class AstTransformer(Transformer):
    def program(self, *statements):
        return ("program", list(statements))

    def declaration(self, type, name, value=None):
        # 如果没有初始值，value 会是 None
        return ("declare", type, str(name), value)

    def assignment(self, name, value):
        return ("assign", str(name), value)

    def assign_expr_for_update(self, name, value=""):
        return ("for_update", str(name), value)

    def assign_expr(self, name, value=""):
        return ("assign_expr", str(name), value)

    def for_init_clause(self, name=""):
        return ("for_init", str(name))

    def for_cond_expr(self, name):
        return ("for_cond", str(name))

    def expression_statement(self, expr):
        return ("expr_stmt", expr)

    def if_statement(self, _, condition, then_branch, else_branch=None):
        return ("if", condition, then_branch, else_branch)

    def for_statement(self, _, __, init, cond, update, ___, body):
        # 处理可选部分，如果它们是 None (Lark 在可选规则未匹配时会传递 None)
        # print(f"for_init: {init}, for_cond: {cond}, for_update: {update}")
        return ("for", init, cond, update, body)

    def goto_statement(self, _, label):
        return ("goto", str(label))

    def label_statement(self, label, statement):
        return ("label", str(label), statement)

    def block_statement(self, *statements):
        return ("block", list(statements))

    def empty_statement(self):
        return ("empty_stmt",)  # 返回一个元组表示空语句

    # --- 表达式转换 ---
    def comparison(self, left, op, right):
        return ("binary_op", str(op), left, right)

    def term(self, left, op, right):
        print(f"Parsing term: left:{left},op: {op},right: {right}")
        return ("binary_op", str(op), left, right)

    def factor(self, left, op, right):
        return ("binary_op", str(op), left, right)

    def neg(self, value):
        return ("neg", "-", value)
    
    def not_(self, value):
        return ("not", "!", value)

    def int_literal(self, value):
        return ("literal", int(value))

    def float_literal(self, value):
        return ("literal", float(value))

    def variable(self, name):
        return ("variable", str(name))

    # 类型转换
    def type(self, type_token):
        return ("type", str(type_token))  # 返回类型名称 "int" 或 "float"

    # 从 Token 获取字符串值
    def IDENTIFIER(self, s):
        return str(s)

    def INT_NUMBER(self, n):
        return int(n)

    def FLOAT_NUMBER(self, n):
        return float(n)  # Lark 会处理为 Python float

    def COMP_OP(self, op):
        return str(op)

    def ADD_OP(self, op):
        return str(op)

    def MUL_OP(self, op):
        return str(op)