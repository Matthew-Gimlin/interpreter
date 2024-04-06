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

    # TODO
    def _recover(self) -> Expression:
        """Recovers from an error.
        
        Returns:
            The next valid statement.
        """
        pass

    def _match(self, token_types: List[TokenType]) -> bool:
        """Checks if the current token matches any token types.
        
        Args:
            token_types: Token types to check.

        Returns:
            If the current token matches one of the token types.
        """
        if not self.token:
            return False

        return self.token.token_type in token_types

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
        """Eats literals and grouping expressions.
        
        Returns:
            The eaten expression.
        """
        if self._match([TokenType.NULL,
                        TokenType.FALSE,
                        TokenType.TRUE,
                        TokenType.STRING,
                        TokenType.CHARACTER,
                        TokenType.INTEGER,
                        TokenType.FLOAT,
                        TokenType.IDENTIFIER]):
            return Literal(self._eat())

        # A grouping.
        elif self._match([TokenType.LEFT_PARENTHESIS]):
            self._eat()
            expression = self._eat_expression()

            if not self.token or self.token.token_type != TokenType.RIGHT_PARENTHESIS:
                self._error("Expected ')' after expression.")

            self._eat() # Eat the right paranthesis.
            return Grouping(expression)

        # An array.
        elif self._match([TokenType.LEFT_BRACE]):
            values = []
            self._eat()
            while not self._match([TokenType.RIGHT_BRACE]):
                values.append(self._eat_expression())
                if not self._match([TokenType.COMMA]):
                    break
                self._eat()

            if not self._match([TokenType.RIGHT_BRACE]):
                self._error("Expected '}' after values.")

            self._eat() # Eat the right curly brace.
            return Array(values)

        self._error('Expected expression.')

    def _eat_index(self) -> Expression:
        expression = self._eat_primary()

        while self._match([TokenType.LEFT_BRACKET]):
            self._eat()
            index = self._eat_expression()
            
            if not isinstance(expression, Literal):
                self._error('Can only index arrays.')
            expression = Index(expression.value, index)
            if not self._match([TokenType.RIGHT_BRACKET]):
                self._error("Expected ']' after index.")
            self._eat()

        return expression

    def _finish_call(self, callee: Expression) -> Expression:
        arguments = []
        if not self._match([TokenType.RIGHT_PARENTHESIS]):
            while True:
                if self._match([TokenType.COMMA]):
                    self._eat()
                if self._match([TokenType.RIGHT_PARENTHESIS]):
                    self._eat()
                    break
                    
                arguments.append(self._eat_expression())

        right_parenthesis = self._eat()
        return Call(callee, right_parenthesis, arguments)

    def _eat_call(self) -> Expression:
        expression = self._eat_index()

        while True:
            if self._match([TokenType.LEFT_PARENTHESIS]):
                self._eat()
                expression = self._finish_call(expression)
            else:
                break

        return expression

    def _eat_unary(self) -> Expression:
        """Eats unary expressions.
        
        Returns:
            The eaten unary expression.
        """
        while self._match([TokenType.BANG,
                           TokenType.NOT,
                           TokenType.PLUS,
                           TokenType.MINUS]):
            operator = self._eat()
            right = self._eat_unary()
            return Unary(operator, right)

        return self._eat_call()

    def _eat_factor(self) -> Expression:
        expression = self._eat_unary()

        while self._match([TokenType.MULTIPLY, TokenType.DIVIDE]):
            operator = self._eat()
            right = self._eat_unary()
            expression = Binary(expression, operator, right)

        return expression

    def _eat_term(self) -> Expression:
        expression = self._eat_factor()

        while self._match([TokenType.PLUS, TokenType.MINUS]):
            operator = self._eat()
            right = self._eat_factor()
            expression = Binary(expression, operator, right)

        return expression

    def _eat_comparison(self) -> Expression:
        expression = self._eat_term()

        while self._match([TokenType.LESS,
                           TokenType.LESS_EQUAL,
                           TokenType.GREATER,
                           TokenType.GREATER_EQUAL]):
            operator = self._eat()
            right = self._eat_term()
            expression = Binary(expression, operator, right)

        return expression

    def _eat_equality(self) -> Expression:
        expression = self._eat_comparison()

        while self._match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]):
            operator = self._eat()
            right = self._eat_comparison()
            expression = Binary(expression, operator, right)

        return expression

    def _eat_and(self) -> Expression:
        expression = self._eat_equality()

        while self._match([TokenType.AND]):
            operator = self._eat()
            right = self._eat_equality()
            expression = Logical(expression, operator, right)

        return expression

    def _eat_or(self) -> Expression:
        expression = self._eat_and()

        if self._match([TokenType.OR]):
            operator = self._eat()
            right = self._eat_and()
            expression = Logical(expression, operator, right)

        return expression

    def _eat_assignment(self) -> Expression:
        expression = self._eat_or()

        if self._match([TokenType.EQUAL]):
            equals = self._eat()
            value = self._eat_assignment()

            if isinstance(expression, Literal):
                return Assignment(expression.value, value)
            elif isinstance(expression, Index):
                return ArrayAssignment(expression, value)

            self._error('Invalid assignment target.')

        return expression

    def _eat_expression(self) -> Expression:
        return self._eat_assignment()

    def _eat_expression_statement(self) -> ExpressionStatement:
        expression = self._eat_expression()

        return ExpressionStatement(expression)
    
    def _eat_echo_statement(self) -> Echo:
        expression = self._eat_expression()
        
        return Echo(expression)
    
    def _eat_block(self) -> Block:
        statements = []

        while not self._match([TokenType.END, TokenType.EOF]):
            statements.append(self._eat_statement())

        if not self._match([TokenType.END]):
            self._error('Expected `end` after block.')

        self._eat() # Eating closing end keyword.
        return Block(statements)

    def _eat_if_statement(self) -> If:
        condition = self._eat_expression()

        then = self._eat_statement()
        _else = None
        if self._match([TokenType.ELSE]):
            self._eat()
            _else = self._eat_statement()

        return If(condition, then, _else)

    def _eat_while_statement(self) -> While:
        condition = self._eat_expression()
        body = self._eat_statement()

        return While(condition, body)

    def _eat_function(self) -> Function:
        if not self._match([TokenType.IDENTIFIER]):
            self._error('Expected function name.')
        name = self._eat()

        if not self._match([TokenType.LEFT_PARENTHESIS]):
            self._error("Expected '(' after function name.")
        self._eat() # Eat the left parenthesis.
        
        parameters = []
        if not self._match([TokenType.RIGHT_PARENTHESIS]):
            while True:
                if self._match([TokenType.COMMA]):
                    self._eat()
                    
                if self._match([TokenType.RIGHT_PARENTHESIS]):
                    self._eat()
                    break
                elif self._match([TokenType.IDENTIFIER]):
                    parameters.append(self._eat())
                else:
                    self._error('Expected parameter name.')
                    
        if not self._match([TokenType.DO]):
            self._error('Expected `do` before function body.')
        self._eat() # Eat the do keyword.

        block = self._eat_block()
        return Function(name, parameters, block.statements)

    def _eat_return(self) -> Return:
        keyword = self._eat()
        value = self._eat_expression()

        return Return(keyword, value)

    def _eat_statement(self) -> Statement:
        if self._match([TokenType.ECHO]):
            self._eat()
            return self._eat_echo_statement()
        
        elif self._match([TokenType.DO]):
            self._eat()
            return self._eat_block()

        elif self._match([TokenType.IF]):
            self._eat()
            return self._eat_if_statement()

        elif self._match([TokenType.WHILE]):
            self._eat()
            return self._eat_while_statement()

        elif self._match([TokenType.FUNCTION]):
            self._eat()
            return self._eat_function()

        elif self._match([TokenType.RETURN]):
            # self._eat()
            return self._eat_return()
        
        return self._eat_expression_statement()

    def get_statements(self) -> List[Statement]:
        while self.token:
            if self.token.token_type == TokenType.EOF:
                break
            
            statement = self._eat_statement()
            self.statements.append(statement)

        return self.statements
