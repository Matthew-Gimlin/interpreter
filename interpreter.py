#!/usr/bin/env python3

import argparse
from src.lexer import Lexer

def main() -> None:
    parser = argparse.ArgumentParser(description='Interpret source code.')
    parser.add_argument('file',
                        nargs='?',
                        default=None,
                        help='A source file.')

    args = parser.parse_args()
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
        
        for t in tokens:
            print(t)

    else:
        while True:
            try:
                line = input('> ')

                lexer = Lexer(line)
                tokens = lexer.get_tokens()
                if lexer.error:
                    continue
                
                for t in tokens:
                    print(t)
            
            except EOFError:
                print()
                break
                
            except KeyboardInterrupt:
                print()
                break

if __name__ == '__main__':
    main()
