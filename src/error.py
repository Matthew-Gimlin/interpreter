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
