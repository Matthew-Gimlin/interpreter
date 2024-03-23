from typing import Optional
from src.expression import *

class StatementVisitor:
    """Defines a statement visitor base class.
    """
    def visit_expression(self, expression):
        pass

    def visit_echo(self, echo):
        pass

    def visit_variable(self, variable):
        pass

class Statement:
    """Defines a statement base class.
    """
    def accept(self, visitor):
        pass

class ExpressionStatement(Statement):
    def __init__(self, expression: Expression) -> None:
        self.expression = expression

    def __str__(self) -> str:
        return f'{self.expression}'

    def accept(self, visitor):
        return visitor.visit_expression(self)

class Echo(Statement):
    def __init__(self, expression: Expression) -> None:
        self.expression = expression

    def __str__(self) -> str:
        return f'echo {self.expression}'

    def accept(self, visitor):
        return visitor.visit_echo(self)

class Variable(Statement):
    def __init__(self,
                 name: Token,
                 initializer: Optional[Expression] = None) -> None:
        self.name = name
        self.initializer = initializer

    def __str__(self) -> str:
        if self.initializer:
            return f'{self.name} = {self.initializer}'
        
        return f'{self.name}'

    def accept(self, visitor):
        return visitor.visit_variable(self)
