class LexerError(Exception):
    """Defines an error while lexing.
    """
    pass

class ParserError(Exception):
    """Defines a error while parsing.
    """
    pass

class RuntimeError(Exception):
    """Defines a error during runtime.
    """
    pass

class ReturnError(RuntimeError):
    """Defines a pseudo-error during runtime. Used to return from a function.
    """
    def __init__(self, value: object) -> None:
        self.value = value
