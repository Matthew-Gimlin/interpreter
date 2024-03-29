# interpreter

A tree-walk interpreter for a custom programming language named Coffee Bean.

## Running the Interpreter

Run `coffee_bean.py` with a file name to execute source code.

```
$ cat hello.cb
echo "Hello, world!"

$ python3 coffee_bean.py hello.cb
Hello, world!
```

Run `coffee_bean.py` with no arguments to use the REPL.

```
$ python3 coffee_bean.py
Coffee Bean interpreter (version 0.1)
> echo "Hello, world!"
Hello, world!
```

## Resources

I used the book [Crafting Interpreters](https://craftinginterpreters.com/) to
write this interpreter.
