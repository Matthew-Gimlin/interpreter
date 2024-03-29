from __future__ import annotations
from src.token import *

class ExpressionVisitor:
    """Defines an expression visitor base class.
    """
    def visit_literal(self, literal: Literal):
        pass

    def visit_binary(self, binary: Binary):
        pass

    def visit_unary(self, unary: Unary):
        pass

    def visit_grouping(self, grouping: Grouping):
        pass

    def visit_assignment(self, assignment: Assignment):
        pass

    def visit_logical(self, logical: Logical):
        pass

class Expression:
    """Defines an expression base class.
    """
    def accept(self, visitor: ExpressionVisitor):
        pass

class Literal(Expression):
    """Defines a container for a literal expression.

    Attributes:
        value: The literal expression's value.
    """
    def __init__(self, value: Token) -> None:
        """Constructor.

        Args:
            value: A literal value.
        """
        self.value = value

    def __str__(self) -> str:
        """Formats the literal expression as a string.

        Returns:
            The value.
        """
        return f'{self.value}'

    def accept(self, visitor: ExpressionVisitor):
        return visitor.visit_literal(self)

class Binary(Expression):
    """Defines a container for a binary expression.

    Attributes:
        left: The expression on the left side of the operator.
        operator: The binary operator.
        right: The expression on the right side of the operator.
    """
    def __init__(self,
                 left: Expression,
                 operator: Token,
                 right: Expression) -> None:
        """Creates a binary expression.

        Args:
            left: An expression on the left side of the operator.
            operator: A binary operator.
            right: An expression on the right side of the operator.
        """
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self) -> str:
        """Formats the binary expression as a string.

        Returns:
            The operator and the left and right expression.
        """
        return f'({self.operator} {self.left} {self.right})'

    def accept(self, visitor: ExpressionVisitor):
        return visitor.visit_binary(self)

class Unary(Expression):
    """Defines a container for a unary expression.

    Attributes:
        operator: A unary operator.
        right: The right hand side of the unary expression.
    """
    def __init__(self, operator: Token, right: Expression) -> None:
        """Constructor.

        Args:
            operator: A unary operator.
            right: An expression on the right side of the operator.
        """
        self.operator = operator
        self.right = right

    def __str__(self) -> str:
        """Formats the unary expression as a string.

        Returns:
            The operator and the right expression.
        """
        return f'({self.operator} {self.right})'
    
    def accept(self, visitor: ExpressionVisitor):
        return visitor.visit_unary(self)

class Grouping(Expression):
    """Defines a container for a grouping (an expression in parentheses).

    Attributes:
        expression: The expression in parentheses.
    """
    def __init__(self, expression: Expression) -> None:
        """Constructor.

        Args:
            expression: An expression in parentheses.
        """
        self.expression = expression

    def __str__(self) -> str:
        """Formats the grouping as a string.

        Returns:
            The expression in parentheses.
        """
        return f'{self.expression}'
    
    def accept(self, visitor: ExpressionVisitor):
        return visitor.visit_grouping(self)

class Assignment(Expression):
    """Defines a container for an assigment.
    
    Attributes:
        name: The identifier token with the variable name.
        value: The value to assign to the variable.
    """
    def __init__(self, name: Token, value: Expression) -> None:
        """Constructor.

        Args:
            name: An identifier token with a variable name.
            value: An value to assign to the variable.
        """
        self.name = name
        self.value = value

    def __str__(self) -> str:
        """Formats the assignment expression as a strign.

        Returns:
            The variable name and value.
        """
        return f'(EQUAL {self.name} {self.value})'

    def accept(self, visitor: ExpressionVisitor):
        return visitor.visit_assignment(self)

class Logical(Expression):
    """Defines a container for a logical expression.

    Attributes:
        left: The expression on the left side of the operator.
        operator: The binary operator.
        right: The expression on the right side of the operator.
    """
    def __init__(self,
                 left: Expression,
                 operator: Token,
                 right: Expression) -> None:
        """Constructor.
        
        Args:
            left: An expression on the left side of the operator.
            operator: A binary operator.
            right: An expression on the right side of the operator.
        """
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self) -> str:
        """Formats the logical expression as a string.

        Returns:
            The operator and the left and right expressions.
        """
        return f'({self.operator} {self.left} {self.right})'

    def accept(self, visitor: ExpressionVisitor):
        return visitor.visit_logical(self)
