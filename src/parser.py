from typing import List, Optional
from src.token import *
from src.expression import *

class Parser:
    """Defines a parser to convert tokens into an expression.

    Attributes:
        tokens: Input tokens.
        position: The current token index in the input tokens.
        token: The current token in the input tokens.
        error: If an error occurred while parsing.
    """
    def __init__(self, tokens: List[Token]) -> None:
        """Creates a parser.

        Args:
            tokens: Input tokens.
        """
        self.tokens = tokens
        self.position = 0
        if len(tokens) > 0:
            self.token = tokens[0]
        else:
            self.token = None
        self.error = False

    def _error(self, message: str) -> None:
        """Prints an error message. Puts the parser into an error state.

        Args:
            message: An error message.
        """
        # print(f'Line {self.token.line}')
        print(f'Error: {message}')
        self.error = True

    def _match(self, token_types: List[TokenType]) -> bool:
        """Checks if the current token matches any token types.
        
        Args:
            token_types: Token types to check.

        Returns:
            If the current token matches one of the token types.
        """
        for token_type in token_types:
            if self.token and self.token.token_type == token_type:
                return True
        
        return False

    def _eat(self) -> Optional[Token]:
        """Eats a single token.

        Returns:
            The eaten token.
        """
        eaten = self.token
        self.position += 1
        if self.position < len(self.tokens):
            self.token = self.tokens[self.position]
        else:
            self.token = None

        return eaten

    def _eat_primary(self) -> Expression:
        if self._match([TokenType.NULL,
                        TokenType.FALSE,
                        TokenType.TRUE,
                        # TokenType.STRING,
                        # TokenType.CHARACTER,
                        TokenType.INTEGER,
                        TokenType.FLOAT]):
            return Literal(self._eat())

        if self._match([TokenType.LEFT_PARENTHESIS]):
            self._eat()
            expression = self._eat_expression()

            token = self._eat()
            if not token or token.token_type != TokenType.RIGHT_PARENTHESIS:
                self._error("Expected ')' after expression.")
                return Expression()

            return Grouping(expression)

        self._error('Expected expression.')
        return Expression()

    def _eat_unary(self) -> Expression:
        while self._match([TokenType.BANG,
                           TokenType.PLUS,
                           TokenType.MINUS]):
            operator = self._eat()
            right = self._eat_unary()
            return UnaryExpression(operator, expression)

        return self._eat_primary()

    def _eat_factor(self) -> Expression:
        expression = self._eat_unary()

        while self._match([TokenType.MULTIPLY, TokenType.DIVIDE]):
            operator = self._eat()
            right = self._eat_unary()
            expression = BinaryExpression(expression, operator, right)

        return expression

    def _eat_term(self) -> Expression:
        expression = self._eat_factor()

        while self._match([TokenType.PLUS, TokenType.MINUS]):
            operator = self._eat()
            right = self._eat_factor()
            expression = BinaryExpression(expression, operator, right)

        return expression

    def _eat_comparison(self) -> Expression:
        expression = self._eat_term()

        while self._match([TokenType.LESS,
                           TokenType.LESS_EQUAL,
                           TokenType.GREATER,
                           TokenType.GREATER_EQUAL]):
            operator = self._eat()
            right = self._eat_term()
            expression = BinaryExpression(expression, operator, right)

        return expression

    def _eat_equality(self) -> Expression:
        expression = self._eat_comparison()

        while self._match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]):
            operator = self._eat()
            right = self._eat_comparison()
            expression = BinaryExpression(expression, operator, right)

        return expression

    def _eat_expression(self) -> Expression:
        return self._eat_equality()

    def get_expression(self) -> Expression:
        expression = self._eat_expression()
        if self.error:
            return Expression()
        
        return expression
