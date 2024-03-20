#!/usr/bin/env python3

import argparse
from src.error import *
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter

def to_string(value: object) -> str:
    if value == None:
        return 'null'
    elif type(value) == bool:
        return 'true' if value else 'false'
    else:
        return str(value)

def main() -> None:
    arg_parser = argparse.ArgumentParser(description='Interpret source code.')
    arg_parser.add_argument('file',
                            nargs='?',
                            default=None,
                            help='A source file.')

    args = arg_parser.parse_args()
    if args.file:
        source = ''
        try:
            with open(args.file, 'r') as file:
                source = file.read()
                
            lexer = Lexer(source)
            tokens = lexer.get_tokens()
            if lexer.error:
                return

            parser = Parser(tokens)
            expression = parser.get_expression()
            if parser.error:
                return

            interpreter = Interpreter()
            print(to_string(interpreter.evaluate(expression)))
            
        except FileNotFoundError:
            print(f"Error: Cannot open file '{args.file}'")
            return
        
    else:
        print('Coffee Bean interpreter.')
        
        while True:
            try:
                line = input('> ')

                lexer = Lexer(line)
                tokens = lexer.get_tokens()
                if lexer.error:
                    continue
                
                parser = Parser(tokens)
                expression = parser.get_expression()
                if parser.error:
                    continue

                interpreter = Interpreter()
                print(to_string(interpreter.evaluate(expression)))
            
            except EOFError:
                print()
                break
                
            except KeyboardInterrupt:
                print()
                break

            except RuntimeError as error:
                print(f'Error: {error}')
                continue

if __name__ == '__main__':
    main()
