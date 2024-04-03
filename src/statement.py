from __future__ import annotations
from typing import List, Optional
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

    def visit_if(self, _if: If):
        pass

    def visit_while(self, _while: While):
        pass

    def visit_function(self, function: Function):
        pass

    def visit_return(self, _return: Return):
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

class If(Statement):
    """Defines a container for an if statement.

    """
    def __init__(self,
                 condition: Expression,
                 then: Statement,
                 _else: Optional[Statement] = None) -> None:
        self.condition = condition
        self.then = then
        self._else = _else

    def __str__(self) -> None:
        if self._else:
            return f'if {self.condition}\n{self.then}\nelse {self._else}'
        
        return f'if {self.condition}\n{self.then}'

    def accept(self, visitor: StatementVisitor):
        return visitor.visit_if(self)

class While(Statement):
    """Defines a container for a while statement.

    """
    def __init__(self, condition: Expression, body: Statement) -> None:
        self.condition = condition
        self.body = body

    def __str__(self) -> str:
        return f'while {self.condition}\n{self.body}'

    def accept(self, visitor: StatementVisitor):
        return visitor.visit_while(self)

class Function(Statement):
    """Defines a container for a function declaration statement.
    
    Attributes:
        name: The function identifier.
        parameters: The function's parameters.
        body: The function's body.
    """
    def __init__(self,
                 name: Token,
                 parameters: List[Token],
                 body: List[Statement]) -> None:
        self.name = name
        self.parameters = parameters
        self.body = body

    def __str__(self) -> str:
        return f'{self.name}({", ".join(self.parameters)})\n{self.body}'

    def accept(self, visitor: StatementVisitor):
        return visitor.visit_function(self)

class Return(Statement):
    """Defines a container for a return statement.
    
    Attributes:
        keyword: The return keyword.
        value: The value to return.
    """
    def __init__(self, keyword: Token, value: Expression) -> None:
        """Constructor.

        Args:
            keyword: A return keyword.
            value: A value to return.
        """
        self.keyword = keyword
        self.value = value

    def __str__(self) -> str:
        """Formats the return statement as a string.

        Returns:
            The return value.
        """
        return f'return {self.value}'

    def accept(self, visitor: StatementVisitor):
        return visitor.visit_return(self)
