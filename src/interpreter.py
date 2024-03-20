from src.token import *
from src.expression import *

class Interpreter(Visitor):
    """Defines a visitor to evaluate an expression.
    """
    def __init__(self):
        pass

    def evaluate(self, expression: Expression) -> object:
        return expression.accept(self)
        
    def visit_literal(self, literal: Literal) -> object:
        literal_type = literal.value.token_type
        literal_symbol = literal.value.symbol
        
        if literal_type == TokenType.NULL:
            return None
        elif literal_type == TokenType.TRUE:
            return True
        elif literal_type == TokenType.FALSE:
            return False
        elif literal_type == TokenType.INTEGER:
            return int(literal_symbol)
        elif literal_type == TokenType.FLOAT:
            return float(literal_symbol)

        return None

    def visit_binary(self, binary: BinaryExpression) -> object:
        operator_type = binary.operator.token_type
        left_value = self.evaluate(binary.left)
        right_value = self.evaluate(binary.right)

        # Arithmetic operations.
        if operator_type == TokenType.PLUS:
            return left_value + right_value
        elif operator_type == TokenType.MINUS:
            return left_value - right_value
        elif operator_type == TokenType.MULTIPLY:
            return left_value * right_value
        elif operator_type == TokenType.DIVIDE:
            return left_value / right_value

        # Logic operations.
        elif operator_type == TokenType.EQUAL_EQUAL:
            return left_value == right_value
        elif operator_type == TokenType.BANG_EQUAL:
            return left_value != right_value

        return None

    def visit_unary(self, unary: UnaryExpression) -> object:
        operator_type = unary.operator.token_type
        right_value = self.evaluate(unary.right)

        if operator_type == TokenType.PLUS:
            return +right_value
        elif operator_type == TokenType.MINUS:
            return -right_value
        elif operator_type == TokenType.BANG:
            return not right_value

        return None

    def visit_grouping(self, grouping: Grouping) -> object:
        return self.evaluate(grouping.expression)
