from typing import List, Optional
from src.error import *
from src.token import *
from src.expression import *
from src.statement import *

class Parser:
    """Defines a parser to convert tokens into an expression.

    Attributes:
        tokens: Input tokens.
        position: The current token index in the input tokens.
        token: The current token in the input tokens.
        statements: Output statements.
    """
    def __init__(self, tokens: List[Token]) -> None:
        """Creates a parser.

        Args:
            tokens: Input tokens.
        """
        self.tokens = tokens
        self.position = 0
        self.token = None if len(tokens) == 0 else tokens[0]
        self.statements = []

    def _error(self, message: str) -> None:
        """Raises a parser error.

        Args:
            message: An error message.
        """
        raise ParserError(f'Line {self.token.line}\nError: {message}')

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

            if not self.token or self.token.token_type != TokenType.RIGHT_PARENTHESIS:
                self._error("Expected ')' after expression.")

            self._eat()
            return Grouping(expression)

        self._error('Expected expression.')
        return Expression()

    def _eat_unary(self) -> Expression:
        while self._match([TokenType.BANG,
                           TokenType.PLUS,
                           TokenType.MINUS]):
            operator = self._eat()
            right = self._eat_unary()
            return UnaryExpression(operator, right)

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

    def _eat_expression_statement(self) -> Statement:
        expression = self._eat_expression()

        if not self._match([TokenType.NEWLINE, TokenType.EOF]):
            self._error('Expected newline after expression.')

        self._eat()
        return ExpressionStatement(expression)
    
    def _eat_echo_statement(self) -> Statement:
        expression = self._eat_expression()

        if not self._match([TokenType.NEWLINE, TokenType.EOF]):
            self._error('Expected newline after value.')
        
        self._eat()
        return Echo(expression)

    def _eat_statement(self) -> Statement:
        if self.token.token_type == TokenType.ECHO:
            self._eat()
            return self._eat_echo_statement()
        
        return self._eat_expression_statement()

    def get_statements(self) -> List[Statement]:
        while self.token:
            if self.token.token_type == TokenType.EOF:
                break
            elif self.token.token_type == TokenType.NEWLINE:
                self._eat()
                continue
            
            statement = self._eat_statement()
            self.statements.append(statement)

        return self.statements
