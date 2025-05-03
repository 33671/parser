from enum import Enum,auto
from dataclasses import dataclass, fields
from typing import Any, Dict, List, Optional, Union
import json
class TokenType(Enum):
    # 标识符和字面量
    IDENTIFIER = auto()
    INT = "int"
    FLOAT = "float" 
    # 关键字
    IF = "if"
    ELSE = "else"
    FOR = "for"
    GOTO = "goto" 
    # 运算符
    NOT = "!"          # !
    ASSIGN = "="        # =
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

class NodeType(Enum):
    # Program structure
    PROGRAM = auto()
    
    # Statements
    EMPTY_STATEMENT = auto()
    DECLARATION = auto()
    ASSIGNMENT = auto()
    EXPRESSION_STATEMENT = auto()
    IF_STATEMENT = auto()
    FOR_STATEMENT = auto()
    GOTO_STATEMENT = auto()
    LABEL_STATEMENT = auto()
    BLOCK_STATEMENT = auto()
    PRINT_STATEMENT = auto()
    
    # Expressions
    COMPARISON = auto()
    # EXPRESSION = auto()
    TERM = auto() # a or factor + factor
    FACTOR = auto() # a * b
    UNARY_NEG = auto()  # - a
    UNARY_NOT = auto()  # ! a
    INT_LITERAL = auto() 
    FLOAT_LITERAL = auto()
    VARIABLE = auto()
    ASSIGN_EXPR = auto() # a = b
    
    # For loop components
    FOR_INIT_CLAUSE = auto()
    FOR_COND_EXPR = auto()
    FOR_UPDATE_EXPR = auto()
    ASSIGN_EXPR_FOR_UPDATE = auto()

    def to_dict(self):
        return {self.name: self.value}
    
    def to_json(self):
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)

@dataclass
class Token:
    type: TokenType
    value: Optional[Union[str, int, float]] = None
    line: int = 0
    column: int = 0

    def to_dict(self):
        return {
            "type": self.type.name
        }

@dataclass
class AstNode:
    node_type: NodeType
    token: Optional[Token] = None  # 关联的token（如果有）
    
    # 子节点
    children: List['AstNode'] = None  # 用于PROGRAM, BLOCK_STATEMENT等
    left: Optional['AstNode'] = None  # 用于二元操作
    right: Optional['AstNode'] = None # 用于二元操作,assignment,declaration
    
    # 特定节点类型的额外字段
    condition: Optional['AstNode'] = None  # 用于IF_STATEMENT, FOR_STATEMENT等
    then_branch: Optional['AstNode'] = None  # 用于IF_STATEMENT
    else_branch: Optional['AstNode'] = None  # 用于IF_STATEMENT
    
    # For循环特定字段
    init_clause: Optional['AstNode'] = None  # 用于FOR_STATEMENT
    cond_expr: Optional['AstNode'] = None    # 用于FOR_STATEMENT
    update_expr: Optional['AstNode'] = None  # 用于FOR_STATEMENT
    for_body: Optional['AstNode'] = None         # 用于FOR_STATEMENT
    
    # 变量声明/赋值
    var_name: Optional[str] = None  # 用于DECLARATION, ASSIGNMENT等
    var_type: Optional[TokenType] = None  # INT or FLOAT
    
    # 字面量值
    value: Optional[int] = None  # 用于INT_LITERAL
    
    # 标签和goto
    label: Optional[str] = None  # 用于GOTO_STATEMENT, LABEL_STATEMENT
    
    def __post_init__(self):
        if self.children is None:
            self.children = []
    # def to_dict(self,node: 'AstNode') -> Dict[str, Any]:
    #     if not isinstance(node, AstNode):
    #         return node
        
    #     result = {"node_type": str(node.node_type)}
        
    #     for field in fields(node):
    #         value = getattr(node, field.name)
            
    #         # 跳过None值和空children列表
    #         if value is None:
    #             continue
    #         if field.name == 'children' and not value:
    #             continue
                
    #         # 特殊处理各种字段类型
    #         if isinstance(value, AstNode):
    #             result[field.name] = self.to_dict(value)
    #         elif field.name == 'children' and isinstance(value, list):
    #             result[field.name] = [self.to_dict(child) for child in value]
    #         elif hasattr(value, 'to_dict'):
    #             result[field.name] = value.to_dict()  # 假设Token有to_dict方法
    #         else:
    #             result[field.name] = value
                
    #     return result
    # def __str__(self) -> str:
    #     return json.dumps(self.to_dict(self), indent=2, ensure_ascii=False)
    
    # def __repr__(self) -> str:
    #     return self.__str__()