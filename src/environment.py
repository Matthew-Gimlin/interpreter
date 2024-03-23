from src.error import *
from src.token import Token

class Environment:
    """Defines a runtime environment.
    
    Attributes:
        values: Variable names and their values.
    """
    def __init__(self) -> None:
        """Constructor.
        """
        self.values = {}

    def add(self, name: Token, value: object) -> None:
        """Creates a new variable.
        
        Args:
            name: An identifier token with a variable name.
            value: An initial value.
        """
        self.values[name.symbol] = value

    def get(self, name: Token) -> object:
        """Gets the value of a variable.
        
        Args:
            name: An identifier token with a variable name.

        Returns:
            The variable's value.
        """
        # The variable must already be defined.
        if not name.symbol in self.values:
            raise RuntimeError(
                f"Line {name.line}\nError: Undefined variable '{name.symbol}'."
            )
        
        return self.values[name.symbol]
