from src.expression import *

class StatementVisitor:
    """Defines a statement visitor base class.
    """
    def visit_expression(self, expression):
        pass

    def visit_echo(self, echo):
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
