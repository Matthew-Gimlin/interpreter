from typing import Union
from src.token import *
from src.error import *

def _to_number(value: object) -> Union[int, float]:
    """Converts an expression value into a number for arithmetic operations.

    Args:
        value: An expression value.

    Returns:
        The value as a number.
    """
    if type(value) in [int, float]:
        return value

    raise RuntimeError('Operand must be an int or float.')

def _to_boolean(value: object) -> bool:
    """Converts an expression value into a boolean for logic operations.

    Args:
        value: An expression value.

    Returns:
        If the value is true.
    """
    if type(value) == None:
        return False
    elif type(value) == bool:
        return value
    elif type(value) == int:
        return value != 0
    elif type(value) == float:
        return value != 0.0

    return False

class Expression:
    """Defines an expression base class.
    """
    def evaluate(self) -> object:
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

    def evaluate(self) -> object:
        value_type = self.value.token_type

        if value_type == TokenType.NULL:
            return None
        elif value_type == TokenType.TRUE:
            return True
        elif value_type == TokenType.FALSE:
            return False
        elif value_type == TokenType.INTEGER:
            return int(self.value.symbol)
        elif value_type == TokenType.FLOAT:
            return float(self.value.symbol)

        return None

class BinaryExpression(Expression):
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

    def evaluate(self) -> object:
        operator_type = self.operator.token_type
        left_value = self.left.evaluate()
        right_value = self.right.evaluate()
        
        # Arithmetic operations.
        if operator_type == TokenType.PLUS:
            return _to_number(left_value) + _to_number(right_value)
        elif operator_type == TokenType.MINUS:
            return _to_number(left_value) - _to_number(right_value)
        elif operator_type == TokenType.MULTIPLY:
            return _to_number(left_value) * _to_number(right_value)
        elif operator_type == TokenType.DIVIDE:
            return _to_number(left_value) / _to_number(right_value)

        # Logic operations.
        elif operator_type == TokenType.EQUAL_EQUAL:
            return left_value == right_value
        elif operator_type == TokenType.BANG_EQUAL:
            return left_value != right_value

        return None

class UnaryExpression(Expression):
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

    def evaluate(self) -> object:
        operator_type = self.operator.token_type
        right_value = self.right.evaluate()
        
        if operator_type == TokenType.PLUS:
            return +right_value
        elif operator_type == TokenType.MINUS:
            return -right_value
        elif operator_type == TokenType.BANG:
            return not _to_boolean(right_value)

        return None

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

    def evaluate(self) -> object:
        return self.expression.evaluate()
