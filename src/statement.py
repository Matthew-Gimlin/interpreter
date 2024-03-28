from __future__ import annotations
from typing import List
from src.expression import *

class StatementVisitor:
    """Defines a statement visitor base class.
    """
    def visit_expression(self, expression: ExpressionStatement):
        pass

    def visit_echo(self, echo: Echo):
        pass

    def visit_block(self, block: Block):
        pass

class Statement:
    """Defines a statement base class.
    """
    def accept(self, visitor: StatementVisitor):
        pass

class ExpressionStatement(Statement):
    """Defines a container for an expression statement.

    Attributes:
        expression: An expression.
    """
    def __init__(self, expression: Expression) -> None:
        """Constructor.

        Args:
            expression: An expression.
        """
        self.expression = expression

    def __str__(self) -> str:
        """Formats the expression statement as a string.

        Returns:
            The expression.
        """
        return f'{self.expression}'

    def accept(self, visitor):
        return visitor.visit_expression(self)

class Echo(Statement):
    """Defines a container for the built-in echo statement.
    
    Attributes:
        expression: The expression to echo (print out).
    """
    def __init__(self, expression: Expression) -> None:
        """Constructor.

        Args:
            expression: An expression to echo.
        """
        self.expression = expression

    def __str__(self) -> str:
        """Formats the echo statement as a string.

        Returns:
            The echo keyword and the expression.
        """
        return f'echo {self.expression}'

    def accept(self, visitor: StatementVisitor):
        return visitor.visit_echo(self)

class Block(Statement):
    """Defines a container for a block statement.

    Attributes:
        statements: The statements inside the block.
    """
    def __init__(self, statements: List[Statement]) -> None:
        """Constructor.

        Args:
            statements: statements inside the block.
        """
        self.statements = statements

    def __str__(self) -> str:
        """Formats the block statement as a string.
        
        Returns:
            Each statement on a separate line.
        """
        return '\n'.join(f'{statement}' for statement in self.statements)

    def accept(self, visitor: StatementVisitor):
        return visitor.visit_block(self)
