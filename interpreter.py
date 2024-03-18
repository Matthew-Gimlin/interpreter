#!/usr/bin/env python3

import argparse
from src.lexer import Lexer
from src.parser import Parser

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
            with open(args.file, 'r') as f:
                source = f.read()

        except:
            print(f"Error: Cannot open file '{args.file}'")
            return
        
        lexer = Lexer(source)
        tokens = lexer.get_tokens()
        if lexer.error:
            return

        parser = Parser(tokens)
        expression = parser.get_expression()
        if parser.error:
            return

        print(expression)
        
    else:
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

                print(expression)
            
            except EOFError:
                print()
                break
                
            except KeyboardInterrupt:
                print()
                break

if __name__ == '__main__':
    main()
