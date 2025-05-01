from enum import Enum, auto

class TokenType(Enum):
    # 标识符和字面量
    IDENTIFIER = auto()
    INT = auto()
    FLOAT = auto() 
    # 关键字
    IF = auto()
    ELSE = auto()
    FOR = auto()
    GOTO = auto() 
    # 运算符
    PLUS = auto()           # +
    MINUS = auto()          # -
    MULTIPLY = auto()       # *
    DIVIDE = auto()        # /
    MODULO = auto()        # %
    EQUAL = auto()         # ==
    NOT_EQUAL = auto()     # !=
    GREATER = auto()       # >
    LESS = auto()          # <
    GREATER_EQUAL = auto() # >=
    LESS_EQUAL = auto()    # <=
    AND = auto()           # &&
    OR = auto()            # ||
    NOT = auto()           # !
    ASSIGN = auto()        # =

class NodeType(Enum):
    # Program structure
    PROGRAM = auto()
    EMPTY_STATEMENT = auto()
    
    # Statements
    DECLARATION = auto()
    ASSIGNMENT = auto()
    EXPRESSION_STATEMENT = auto()
    IF_STATEMENT = auto()
    FOR_STATEMENT = auto()
    GOTO_STATEMENT = auto()
    LABEL_STATEMENT = auto()
    BLOCK_STATEMENT = auto()
    
    # Expressions
    COMPARISON = auto()
    EXPRESSION = auto()
    TERM = auto() # a or  a*b + a*b
    FACTOR = auto() # a * b
    UNARY_NEG = auto()  # - a
    UNARY_NOT = auto()  # ! a
    INT_LITERAL = auto() 
    FLOAT_LITERAL = auto()
    VARIABLE = auto()
    PAREN_EXPRESSION = auto() # (a + b)
    ASSIGN_EXPR = auto()
    
    # For loop components
    FOR_INIT_CLAUSE = auto()
    FOR_COND_EXPR = auto()
    FOR_UPDATE_EXPR = auto()
    ASSIGN_EXPR_FOR_UPDATE = auto()
    
    # Types
    TYPE_INT = auto()
    TYPE_FLOAT = auto()
    
    # Operators
    OP_EQ = "=="      # ==
    OP_NE = "!="      # !=
    OP_LE = "<="      # <=
    OP_GE = ">="      # >=
    OP_LT = "<"      # <
    OP_GT = ">"      # >
    OP_AND = "&&"     # &&
    OP_OR = "||"      # ||
    OP_ADD = "+"     # +
    OP_SUB = "-"     # -
    OP_MUL = "*"     # *
    OP_DIV = "/"     # /
    OP_MOD = "%"     # %
    

# 示例使用
if __name__ == "__main__":
    # 创建Token示例
    token = TokenType.IDENTIFIER
    print(f"Token类型: {token.name}")
    
    # 创建AST节点示例
    node = NodeType.BINARY_EXPRESSION
    print(f"AST节点类型: {node.name}")