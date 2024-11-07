import basic
running = True
while running:
    text = input("basic > ")
    if text == "quit()":
        running = False
    else:
        output, error = basic.run(text, "<stdin>")

        if error: print(error.return_errror())
        else: print(output)
