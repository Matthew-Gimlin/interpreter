from __future__ import annotations
from typing import List
from src.interpreter import *
from src.statement import *
from src.environment import *
import time

class CoffeeBeanCallable:
    """Defines a Coffee Bean callable object (a function).
    """
    def __init__(self, argument_count: int) -> None:
        self.argument_count = argument_count
    
    def call(self,
             interpreter: Interpreter,
             arguments: List[object]) -> object:
        pass

class CoffeeBeanClock(CoffeeBeanCallable):
    """Defines a callable object for the built-in clock function.
    """
    def __init__(self) -> None:
        super().__init__(0)

    def __str__(self) -> str:
        return f'<built-in function clock>'
        
    def call(self,
             interpreter: Interpreter,
             arguments: List[object]) -> float:
        return time.time()

class CoffeeBeanFunction(CoffeeBeanCallable):
    """Defines a callable object for user-defined functions.
    
    Attributes:
        declaration: The user-defined function declaration.
    """
    def __init__(self, declaration: Function) -> None:
        super().__init__(len(declaration.parameters))
        self.declaration = declaration

    def __str__(self) -> str:
        return f'<function {self.declaration.name}>'

    def call(self,
             interpreter: Interpreter,
             arguments: List[object]) -> object:
        environment = Environment(interpreter.globals)
        for parameter, argument in zip(self.declaration.parameters, arguments):
            environment.add(parameter, argument)

        try:
            interpreter._execute_block(self.declaration.body, environment)
        except ReturnError as return_error:
            return return_error.value

        return None
