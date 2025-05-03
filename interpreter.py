from ast_visitor import ASTVisitor
from tokens import TokenType, NodeType, Token, AstNode
from typing import Optional, List, Union
class Interpreter(ASTVisitor):
    """AST解释执行器"""
    
    def __init__(self):
        self.variables = {}  # 变量存储
        self.current_label = None  # 当前标签(用于GOTO)
        self.pc = 0  # 程序计数器(用于控制流)
    
    def visit(self, node: AstNode, parent: Optional[AstNode] = None):
        # 根据节点类型分派到具体处理方法
        method_name = f'visit_{node.node_type.name.lower()}'
        if hasattr(self, method_name):
            return getattr(self, method_name)(node, parent)
        else:
            raise NotImplementedError(f"No visit method for {node.node_type}")
    
    def visit_program(self, node: AstNode, parent: AstNode):
        for stmt in node.children:
            self.visit(stmt, node)
    def visit_block_statement(self, node: AstNode, parent: AstNode):
        # 处理块语句
        for stmt in node.children:
            self.visit(stmt, node) 
    def visit_declaration(self, node: AstNode, parent: AstNode):
        var_name = node.var_name
        # if var_name in self.variables:
        #     raise RuntimeError(f"Variable {var_name} already declared")
        
        # 处理初始化值
        if node.right:
            value = self.visit(node.right, node)
            self.variables[var_name] = value
        else:
            # 默认初始化
            self.variables[var_name] = 0 if node.var_type == TokenType.INT else 0.0
    
    def visit_assignment(self, node: AstNode, parent: AstNode):
        var_name = node.var_name
        if var_name not in self.variables:
            raise RuntimeError(f"Variable {var_name} not declared")
        
        value = self.visit(node.right, node)
        self.variables[var_name] = value
        return value
    
    def visit_term(self, node: AstNode, parent: AstNode):
        if node.left and node.right:
            left_value = self.visit(node.left, node)
            right_value = self.visit(node.right, node)
            if node.token.type == TokenType.OP_ADD:
                return left_value + right_value
            elif node.token.type == TokenType.OP_SUB:
                return left_value - right_value
        elif node.left:
            return self.visit(node.left, node)
        elif node.right:
            return self.visit(node.right, node)
        
    def visit_factor(self, node: AstNode, parent: AstNode):
        if node.left and node.right:
            left_value = self.visit(node.left, node)
            right_value = self.visit(node.right, node)
            if node.token.type == TokenType.OP_MUL:
                return left_value * right_value
            elif node.token.type == TokenType.OP_DIV:
                return left_value / right_value
            elif node.token.type == TokenType.OP_MOD:
                return left_value % right_value
        elif node.left:
            return self.visit(node.left, node)
        elif node.right:
            return self.visit(node.right, node)
        
    def visit_unary_neg(self, node: AstNode, parent: AstNode):
        if node.right:
            value = self.visit(node.right, node)
            return -value
        return 0
    def visit_unary_not(self, node: AstNode, parent: AstNode):
        if node.right:
            value = self.visit(node.right, node)
            return not value
        return False
    
    def visit_int_literal(self, node: AstNode, parent: AstNode) -> int:
        return node.value
    def visit_float_literal(self, node: AstNode, parent: AstNode) -> float:
        return node.value
    def visit_assign_expr(self, node: AstNode, parent: AstNode):
        # 处理赋值表达式
        var_name = node.var_name
        if var_name not in self.variables:
            raise RuntimeError(f"Variable {var_name} not declared")
        
        value = self.visit(node.right, node)
        self.variables[var_name] = value
        return value
    
    def visit_comparison(self, node: AstNode, parent: AstNode):
        left_value = self.visit(node.left, node)
        right_value = self.visit(node.right, node)
        if node.token.type == TokenType.OP_LT:
            return left_value < right_value
        elif node.token.type == TokenType.OP_LE:
            return left_value <= right_value
        elif node.token.type == TokenType.OP_GT:
            return left_value > right_value
        elif node.token.type == TokenType.OP_GE:
            return left_value >= right_value
        elif node.token.type == TokenType.OP_EQ:
            return left_value == right_value
        elif node.token.type == TokenType.OP_NE:
            return left_value != right_value
        elif node.token.type == TokenType.OP_AND:
            return left_value and right_value
        elif node.token.type == TokenType.OP_OR:
            return left_value or right_value
        raise RuntimeError(f"Unknown comparison operator: {node.token.type}")

    def visit_variable(self, node: AstNode, parent: AstNode):
        if node.var_name not in self.variables:
            raise RuntimeError(f"Variable {node.var_name} not found")
        return self.variables[node.var_name]
    
    def visit_empty_statement(self, node: AstNode, parent: AstNode):
        # 空语句，什么都不做
        pass
    
    def visit_if_statement(self, node: AstNode, parent: AstNode):
        condition = self.visit(node.condition, node)
        if condition:
            self.visit(node.then_branch, node)
        elif node.else_branch:
            self.visit(node.else_branch, node)
    
    def visit_for_statement(self, node: AstNode, parent: AstNode):
        # 初始化
        if node.init_clause:
            self.visit(node.init_clause, node)
        
        # 条件判断
        while True:
            if node.cond_expr:
                condition = self.visit(node.cond_expr, node)
                print("for condition:",condition,node.cond_expr)
                if not condition:
                    print("for break")
                    break
            
            # 执行循环体
            if node.for_body:
                print("for excuted")
                self.visit(node.for_body, node)
            
            # 更新表达式
            if node.update_expr:
                self.visit(node.update_expr, node)
        # 结束循环

    def visit_print_statement(self, node: AstNode, parent: AstNode):
        # 打印变量或字面量
        if node.right:
            value = self.visit(node.right, node)
            print("PROGRAM PRINT:",value)

    def visit_for_init_clause(self,node: AstNode, parent: AstNode):
        # 处理for循环的初始化语句
        if node.init_clause:
            self.visit(node.init_clause, node)
        return None
    def visit_for_cond_expr(self,node: AstNode, parent: AstNode):
        # 处理for循环的条件表达式
        if node.cond_expr:
            return self.visit(node.cond_expr, node)
        return None
    def visit_for_update_expr(self,node: AstNode, parent: AstNode):
        # 处理for循环的更新表达式
        if node.update_expr:
            self.visit(node.update_expr, node)
        return None
    def visit_assign_expr_for_update(self,node: AstNode, parent: AstNode):
        # 处理for循环的更新表达式
        var_name = self.visit(node.left)
        return None
    # may be its impossible to implement goto and label,let's just ignore it