from __future__ import annotations
from typing import Union, Optional, List
from src.error import *
from src.token import *
from src.expression import *
from src.statement import *
from src.environment import *

class Interpreter(ExpressionVisitor, StatementVisitor):
    """Defines a visitor to evaluate an expression.

    Attributes:
        environment: The interpreter's runtime environment.
        line: The current line number in the source code.
    """
    def __init__(self, environment: Optinal[Environment] = None) -> None:
        """Constructor.
        """
        self.environment = environment or Environment()
        self.line = 1

    def _error(self, message: str) -> None:
        """Raises a runtime error.

        Args:
            message: An error message.
        """
        raise RuntimeError(f'Line {self.line}\nError: {message}')

    def _to_number(self, value: object) -> Union[int, float]:
        """Converts a value to a number.
        
        """
        value_type = type(value)
        if value_type in [int, float]:
            return value
            
        self._error('Expected type int or float')
        return None

    def _to_boolean(self, value: object) -> bool:
        """Converts a value to a boolean.

        Args:
            value: An expression value.

        Returns:
            If the value is true.
        """
        value_type = type(value)
        if value_type == None:
            return False
        elif value_type == bool:
            return value
        elif value_type == str:
            return value != ''
        elif value_type == int:
            return value != 0
        elif value_type == float:
            return value != 0.0
        
        return False
    
    def _to_string(self, value: object) -> str:
        if value == None:
            return 'null'
        elif type(value) == bool:
            return 'true' if value else 'false'
        else:
            return str(value)

    def visit_literal(self, literal: Literal) -> object:
        """Evaluates a literal expression.
        
        Args:
            literal: A literal expression.

        Returns:
            The result of the expression.
        """
        literal_type = literal.value.token_type
        literal_symbol = literal.value.symbol
        self.line = literal.value.line
        
        if literal_type == TokenType.NULL:
            return None
        elif literal_type == TokenType.TRUE:
            return True
        elif literal_type == TokenType.FALSE:
            return False
        elif literal_type == TokenType.STRING:
            return str(literal_symbol[1:-1])
        elif literal_type == TokenType.CHARACTER:
            return str(literal_symbol[1:-1])
        elif literal_type == TokenType.INTEGER:
            return int(literal_symbol)
        elif literal_type == TokenType.FLOAT:
            return float(literal_symbol)
        elif literal_type == TokenType.IDENTIFIER:
            return self.environment.get(literal.value)

        return None

    def visit_binary(self, binary: Binary) -> object:
        """Evaluates a binary expression.
        
        Args:
            binary: A binary expression.

        Returns:
            The result of the expression.
        """
        operator_type = binary.operator.token_type
        left_value = self.evaluate(binary.left)
        right_value = self.evaluate(binary.right)

        # Arithmetic operations.
        if operator_type == TokenType.PLUS:
            return self._to_number(left_value) + self._to_number(right_value)
        elif operator_type == TokenType.MINUS:
            return self._to_number(left_value) - self._to_number(right_value)
        elif operator_type == TokenType.MULTIPLY:
            return self._to_number(left_value) * self._to_number(right_value)
        elif operator_type == TokenType.DIVIDE:
            return self._to_number(left_value) / self._to_number(right_value)

        # Logic operations.
        elif operator_type == TokenType.EQUAL_EQUAL:
            return left_value == right_value
        elif operator_type == TokenType.BANG_EQUAL:
            return left_value != right_value
        elif operator_type == TokenType.LESS:
            return left_value < right_value
        elif operator_type == TokenType.LESS_EQUAL:
            return left_value <= right_value
        elif operator_type == TokenType.GREATER:
            return left_value > right_value
        elif operator_type == TokenType.GREATER_EQUAL:
            return left_value >= right_value

        return None

    def visit_unary(self, unary: Unary) -> object:
        """Evaluates a unary expression.
        
        Args:
            unary: A unary expression.

        Returns:
            The result of the expression.
        """
        operator_type = unary.operator.token_type
        right_value = self.evaluate(unary.right)

        if operator_type == TokenType.PLUS:
            return +self._to_number(right_value)
        elif operator_type == TokenType.MINUS:
            return -self._to_number(right_value)
        elif operator_type == TokenType.BANG:
            return not self._to_boolean(right_value)
        elif operator_type == TokenType.NOT:
            return not self._to_boolean(right_value)

        return None

    def visit_grouping(self, grouping: Grouping) -> object:
        """Evaluates a grouping expression.
        
        Args:
            grouping: A grouping expression.

        Returns:
            The result of the expression.
        """
        return self.evaluate(grouping.expression)

    def visit_assignment(self, assignment: Assignment) -> object:
        """Evaluates an assignment expression.
        
        Args:
            assignment: An assignment expression.

        Returns:
            The assigned value.
        """
        value = self.evaluate(assignment.value)
        self.environment.add(assignment.name, value)
        
        return value
    
    def evaluate(self, expression: Expression) -> object:
        """Evaluates an expression.

        Args:
            expression: An expression.

        Returns:
            The result of the expression.
        """
        return expression.accept(self)

    def visit_expression(self, expression: ExpressionStatement) -> None:
        value = self.evaluate(expression.expression)

    def visit_echo(self, echo: Echo) -> None:
        value = self.evaluate(echo.expression)
        print(self._to_string(value))

    def _execute_block(self,
                       statements: List[Statement],
                       environment: Environment) -> None:
        enclosing = self.environment
        
        for statement in statements:
            self.environment = environment
            statement.accept(self)

        self.environment = enclosing

    def visit_block(self, block: Block) -> None:
        self._execute_block(block.statements, Environment(self.environment))

    def interpret(self, statements: List[Statement]) -> None:
        for statement in statements:
            statement.accept(self)
