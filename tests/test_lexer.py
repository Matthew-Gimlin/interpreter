import unittest
import sys
sys.path.append('../src')
from src.lexer import *
from src.token import *

class TestLexer(unittest.TestCase):
    def test_empty(self) -> None:
        """Test an empty source code string.
        """
        lexer = Lexer('')
        tokens = lexer.get_tokens()
        
        self.assertEqual(lexer.error, False)
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].token_type, TokenType.EOF)

    def test_unexpected_character(self) -> None:
        """Test an invalid character. The lexer should go into an error state.
        """
        lexer = Lexer('$')
        tokens = lexer.get_tokens()

        self.assertEqual(lexer.error, True)

    def test_one_character_tokens(self) -> None:
        """Test all one character tokens.
        """
        symbols = '()[]{}.,:'
        token_types = [
            TokenType.LEFT_PARENTHESIS,
            TokenType.RIGHT_PARENTHESIS,
            TokenType.LEFT_BRACKET,
            TokenType.RIGHT_BRACKET,
            TokenType.LEFT_BRACE,
            TokenType.RIGHT_BRACE,
            TokenType.DOT,
            TokenType.COMMA,
            TokenType.COLON,
        ]
        lexer = Lexer(symbols)
        tokens = lexer.get_tokens()

        self.assertEqual(lexer.error, False)
        self.assertEqual(len(tokens), len(token_types) + 1)
        for i in range(len(token_types)):
            self.assertEqual(tokens[i].token_type, token_types[i])
        self.assertEqual(tokens[-1].token_type, TokenType.EOF)

    def test_two_character_tokens(self) -> None:
        """Test all one or two character tokens.
        """
        symbols = '+ += - -= * *= / /= = == ! != < <= > >='
        token_types = [
            TokenType.PLUS,
            TokenType.PLUS_EQUAL,
            TokenType.MINUS,
            TokenType.MINUS_EQUAL,
            TokenType.MULTIPLY,
            TokenType.MULTIPLY_EQUAL,
            TokenType.DIVIDE,
            TokenType.DIVIDE_EQUAL,
            TokenType.EQUAL,
            TokenType.EQUAL_EQUAL,
            TokenType.BANG,
            TokenType.BANG_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
        ]
        lexer = Lexer(symbols)
        tokens = lexer.get_tokens()
        
        self.assertEqual(lexer.error, False)
        self.assertEqual(len(tokens), len(token_types) + 1)
        for i in range(len(token_types)):
            self.assertEqual(tokens[i].token_type, token_types[i])
        self.assertEqual(tokens[-1].token_type, TokenType.EOF)
    
    def test_integer(self) -> None:
        """Test an integer.
        """
        lexer = Lexer('1234567890')
        tokens = lexer.get_tokens()
        
        self.assertEqual(lexer.error, False)
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].token_type, TokenType.INTEGER)
        self.assertEqual(tokens[0].symbol, '1234567890')
        self.assertEqual(tokens[1].token_type, TokenType.EOF)
        
    def test_float(self) -> None:
        """Test a float.
        """
        lexer = Lexer('1.234567890')
        tokens = lexer.get_tokens()
        
        self.assertEqual(lexer.error, False)
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].token_type, TokenType.FLOAT)
        self.assertEqual(tokens[0].symbol, '1.234567890')
        self.assertEqual(tokens[1].token_type, TokenType.EOF)
        
    def test_identifier(self) -> None:
        """Test an identifier.
        """
        lexer = Lexer('label')
        tokens = lexer.get_tokens()
        
        self.assertEqual(lexer.error, False)
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].token_type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[0].symbol, 'label')
        self.assertEqual(tokens[1].token_type, TokenType.EOF)

    def test_string(self) -> None:
        """Test a string literal.
        """
        lexer = Lexer('"a string\\n"')
        tokens = lexer.get_tokens()
        
        self.assertEqual(lexer.error, False)
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].token_type, TokenType.STRING)
        self.assertEqual(tokens[0].symbol, '"a string\\n"')
        self.assertEqual(tokens[1].token_type, TokenType.EOF)

    def test_string_error(self) -> None:
        """Test a string literal that does not terminate.
        """
        lexer = Lexer('"a string\\n')
        tokens = lexer.get_tokens()

        self.assertEqual(lexer.error, True)
        
    def test_character(self) -> None:
        """Test a character literal.
        """
        lexer = Lexer("'\\n'")
        tokens = lexer.get_tokens()
        
        self.assertEqual(lexer.error, False)
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].token_type, TokenType.CHARACTER)
        self.assertEqual(tokens[0].symbol, "'\\n'")
        self.assertEqual(tokens[1].token_type, TokenType.EOF)
        
    def test_character_error(self) -> None:
        """Test a character literal that does not terminate. The lexer should go
        into an error state.
        """
        lexer = Lexer("'\\n")
        tokens = lexer.get_tokens()

        self.assertEqual(lexer.error, True)

if __name__ == '__main__':
    unittest.main()
