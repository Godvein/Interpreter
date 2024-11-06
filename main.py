import shell

while True:
    text = input("adshell > ")
    output, error = shell.run(text, "<stdin>")

    if error: print(error.return_errror())
    else: print(output)
