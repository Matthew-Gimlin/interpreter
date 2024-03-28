from __future__ import annotations
from typing import Optional
from src.error import *
from src.token import Token

class Environment:
    """Defines a runtime environment.
    
    Attributes:
        enclosing: The enclosing environment.
        values: Variable names and their values.
    """
    def __init__(self, enclosing: Optional[Environment] = None) -> None:
        """Constructor.

        Args:
            enclosing: An enclosing environment.
        """
        self.enclosing = enclosing
        self.values = {}

    def _in_enclosing(self, name: Token) -> bool:
        """Checks if a variable is defined in the enclosing environment.

        Args:
            name: An identifier with a variable name.
        
        Returns:
            If the enclosing environment has the variable.
        """
        if not self.enclosing:
            return False

        if name.symbol in self.enclosing.values:
            return True

        return self.enclosing._in_enclosing(name)

    def add(self, name: Token, value: object) -> None:
        """Creates a new variable.
        
        Args:
            name: An identifier token with a variable name.
            value: An initial value.
        """
        if self._in_enclosing(name):
            self.enclosing.add(name, value)
            return
        
        self.values[name.symbol] = value

    def get(self, name: Token) -> object:
        """Gets the value of a variable.
        
        Args:
            name: An identifier token with a variable name.

        Returns:
            The variable's value.
        """
        if name.symbol in self.values:
            return self.values[name.symbol]

        if self.enclosing:
            return self.enclosing.get(name)

        raise RuntimeError(f"Line {name.line}\nError: Undefined variable '{name.symbol}'.")
