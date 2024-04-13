# speech_user_interface

You need to define a function to run like this:

```
def default_function_to_run(input_text: str):
    reponse_text = send_text_to_chatgpt(input_text)
    speak_text(reponse_text)


main(function_to_run=default_function_to_run):

```

This one is configured by default but it can be anything. We run in a cycle
until "exit the program" is said and that exits the infinite loop. We just keep
reading input and passing that to the `function_to_run` this can do anything
with this input.
