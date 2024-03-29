#!/usr/bin/env python3

import argparse
from src.error import *
from src.lexer import Lexer
from src.parser import Parser
from src.environment import Environment
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
                            help='a source file')
    arg_parser.add_argument('-d',
                            '--debug',
                            action='store_true',
                            help='enable debug output')

    args = arg_parser.parse_args()
    if args.debug:
        print('Debug output enabled.')
    
    if args.file:
        source = ''
        try:
            with open(args.file, 'r') as file:
                source = file.read()
                
            lexer = Lexer(source)
            tokens = lexer.get_tokens()
            if args.debug:
                print('Tokens:')
                for token in tokens:
                    print(token)
                print()

            parser = Parser(tokens)
            statements = parser.get_statements()
            if args.debug:
                print('Statements:')
                for statement in statements:
                    print(statement)
                print()

            if args.debug:
                print('Output:')
            interpreter = Interpreter()
            interpreter.interpret(statements)

        except FileNotFoundError:
            print(f"Error: Cannot open file '{args.file}'")
            return

        except LexerError as error:
            print(error)
            return
        
        except ParserError as error:
            print(error)
            return

        except RuntimeError as error:
            print(error)
            return
        
    else:
        print('Coffee Bean interpreter (version 0.1)')
        environment = Environment()
        
        while True:
            try:
                line = input('> ')

                lexer = Lexer(line)
                tokens = lexer.get_tokens()
                if args.debug:
                    print('Tokens:')
                    for token in tokens:
                        print(token)
                    print()
                
                parser = Parser(tokens)
                statements = parser.get_statements()
                if args.debug:
                    print('Statements:')
                    for statement in statements:
                        print(statement)
                    print()

                if args.debug:
                    print('Output:')
                interpreter = Interpreter(environment)
                interpreter.interpret(statements)

            except EOFError:
                print()
                break
                
            except KeyboardInterrupt:
                print()
                break

            except LexerError as error:
                print(error)
                continue
            
            except ParserError as error:
                print(error)
                continue

            except RuntimeError as error:
                print(error)
                continue

if __name__ == '__main__':
    main()
