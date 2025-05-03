from tokens import TokenType, NodeType,Token,AstNode
from abc import ABC, abstractmethod
from typing import Optional

class ASTVisitor(ABC):
    
    @abstractmethod
    def visit(self, node: AstNode, parent: Optional[AstNode] = None):
        pass

    def visit_children(self, node: AstNode):
        for child in node.children:
            self.visit(child, node)