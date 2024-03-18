from enum import Enum, auto

class TokenType(Enum):
    """Defines the possible token types.
    """
    # One character tokens.
    LEFT_PARENTHESIS = auto()
    RIGHT_PARENTHESIS = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    DOT = auto()
    COMMA = auto()
    COLON = auto()

    # Either one or two character tokens, depending on context.
    PLUS = auto()
    PLUS_EQUAL = auto()
    MINUS = auto()
    MINUS_EQUAL = auto()
    MULTIPLY = auto()
    MULTIPLY_EQUAL = auto()
    DIVIDE = auto()
    DIVIDE_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    BANG = auto()
    BANG_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()

    # Literals.
    INTEGER = auto()
    FLOAT = auto()
    IDENTIFIER = auto()
    STRING = auto()
    CHARACTER = auto()

    # Keywords.
    TRUE = auto()
    FALSE = auto()
    NULL = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    IMPORT = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    FUNC = auto()
    RETURN = auto()
    END = auto()

    NEWLINE = auto()
    EOF = auto()

class Token:
    """Defines a container for a token.
    
    Attributes:
        token_type: The token's type.
        line: The token's line number in the source code.
        symbol: The token's symbol in the source code.
    """
    def __init__(self,
                 token_type: TokenType,
                 line: int,
                 symbol: str = '') -> None:
        """Creates a token.
        
        Args:
            token_type: A token type.
            line: A line number from the source code.
            symbol: A symbol from the source code.
        """
        self.token_type = token_type
        self.line = line
        self.symbol = symbol

    def __str__(self) -> str:
        """Formats the token as a string.
        
        Returns:
            The symbol if it has a unqiue one, or the token type.
        """
        if self.symbol:
            return f'{self.symbol}'
        
        return f'{self.token_type.name}'
