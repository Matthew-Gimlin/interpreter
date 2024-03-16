from typing import List
from src.token import *

ONE_CHARACTER_TYPES = {
    '(': TokenType.LEFT_PARENTHESIS,
    ')': TokenType.RIGHT_PARENTHESIS,
    '[': TokenType.LEFT_BRACKET,
    ']': TokenType.RIGHT_BRACKET,
    '{': TokenType.LEFT_BRACE,
    '}': TokenType.RIGHT_BRACE,
    '.': TokenType.DOT,
    ',': TokenType.COMMA,
    ':': TokenType.COLON,
}

TWO_CHARACTER_TYPES = {
    '+': TokenType.PLUS,
    '+=': TokenType.PLUS_EQUAL,
    '-': TokenType.MINUS,
    '-=': TokenType.MINUS_EQUAL,
    '*': TokenType.MULTIPLY,
    '*=': TokenType.MULTIPLY_EQUAL,
    '/': TokenType.DIVIDE,
    '/=': TokenType.DIVIDE_EQUAL,
    '=': TokenType.EQUAL,
    '==': TokenType.EQUAL_EQUAL,
    '!': TokenType.BANG,
    '!=': TokenType.BANG_EQUAL,
    '<': TokenType.LESS,
    '<=': TokenType.LESS_EQUAL,
    '>': TokenType.GREATER,
    '>=': TokenType.GREATER_EQUAL,
}

KEYWORD_TYPES = {
    'true': TokenType.TRUE,
    'false': TokenType.FALSE,
    'null': TokenType.NULL,
    'and': TokenType.AND,
    'or': TokenType.OR,
    'not': TokenType.NOT,
    'import': TokenType.IMPORT,
    'if': TokenType.IF,
    'else': TokenType.ELSE,
    'while': TokenType.WHILE,
    'for': TokenType.FOR,
    'func': TokenType.FUNC,
    'return': TokenType.RETURN,
    'end': TokenType.END,
}

class Lexer:
    """Defines a lexer to convert source code into tokens.

    Attributes:
        source: Input source code.
        position: The current character index in the source code.
        character: The current character in the source code.
        line: The current line number in the source code.
        tokens: Output tokens.
        error: If an error occurred while lexing.
    """
    def __init__(self, source: str) -> None:
        """Creates a lexer.

        Args:
            source: Input source code.
        """
        self.source = source
        self.position = 0
        self.character = source[0:1]
        self.line = 1
        self.tokens = []
        self.error = False

    def _add_token(self, token_type: TokenType, symbol: str = '') -> None:
        """Adds a token to the list of output tokens.

        Args:
            token_type: The new token's type.
            symbol: The new token's symbol.
        """
        self.tokens.append(Token(token_type, self.line, symbol))

    def _error(self, message: str) -> None:
        """Prints an error message. Puts the lexer into an error state.

        Args:
            message: An error message.
        """
        print(f'Line {self.line}')
        print(f'Error: {message}')
        self.error = True

    def _eat(self) -> str:
        """Eats one character.

        Returns:
            The eaten character.
        """
        eaten = self.character
        self.position += 1
        # Use list slicing to avoid an ``IndexError``.
        self.character = self.source[self.position:self.position + 1]

        return eaten

    def _eat_space(self) -> None:
        """Eats whitespace (except newlines) until the next token. Discards the 
        eaten characters.
        """
        while self.character and self.character in ' \t\r':
            self._eat()

    def _eat_comment(self) -> None:
        """Eats characters until a newline. Discards the eaten characters.
        """
        while self.character and self.character != '\n':
            self._eat()

    def _eat_number(self) -> None:
        """Eats numbers and dots. Creates either an integer or float token.
        """
        token_type = TokenType.INTEGER
        symbol = ''
        while self.character:
            if self.character == '.':
                token_type = TokenType.FLOAT
            elif not self.character.isnumeric():
                break

            symbol += self._eat()

        self._add_token(token_type, symbol)

    def _eat_identifier(self) -> None:
        """Eats letters, numbers, and underscore. Creates either a keyword or
        identifier token.
        """
        symbol = ''
        while self.character:
            if self.character.isalnum():
                pass
            elif self.character == '_':
                pass
            else:
                break

            symbol += self._eat()

        if symbol in KEYWORD_TYPES:
            self._add_token(KEYWORD_TYPES[symbol])
        else:
            self._add_token(TokenType.IDENTIFIER, symbol)

    def _eat_string(self) -> None:
        """Eats characters until a double quote. Creates a string token.
        """
        symbol = self._eat()
        while True:
            if not self.character or self.character == '\n':
                self._error('Unterminated string')
                return
            elif self.character == '"':
                break
            
            symbol += self._eat()

        symbol += self._eat() # Eat the closing double quote.
        self._add_token(TokenType.STRING, symbol)
        
    def _eat_character(self) -> None:
        """Eats characters until a single quote. Creates a character token.
        """
        symbol = self._eat()
        while True:
            if not self.character or self.character == '\n':
                self._error('Unterminated character')
                return
            elif self.character == "'":
                break
            
            symbol += self._eat()

        symbol += self._eat() # Eat the closing single quote.
        self._add_token(TokenType.CHARACTER, symbol)

    def get_tokens(self) -> List[Token]:
        """Converts the source code into tokens.

        Returns:
            The output tokens.
        """
        while self.character:
            if self.error:
                return []

            # Eat whitespace until the next potential token.
            self._eat_space()
            
            # Eat one character tokens.
            if self.character in ONE_CHARACTER_TYPES:
                self._add_token(ONE_CHARACTER_TYPES[self.character])
                self._eat()

            # Eat one or two character tokens.
            elif self.character in TWO_CHARACTER_TYPES:
                symbol = self._eat()
                if symbol + self.character in TWO_CHARACTER_TYPES:
                    symbol += self._eat()
                self._add_token(TWO_CHARACTER_TYPES[symbol])

            # Eat newlines.
            elif self.character == '\n':
                self._add_token(TokenType.NEWLINE)
                self.line += 1
                self._eat()

            # Eat comments.
            elif self.character == '#':
                self._eat_comment()
                
            # Eat literals.
            elif self.character.isnumeric():
                self._eat_number()
            elif self.character.isalpha():
                self._eat_identifier()
            elif self.character == '"':
                self._eat_string()
            elif self.character == "'":
                self._eat_character()

            else:
                self._error(f"Unexpected character '{self.character}'")
                return []
        
        self._add_token(TokenType.EOF)
        return self.tokens
