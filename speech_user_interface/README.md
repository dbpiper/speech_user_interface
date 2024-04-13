# speech_user_interface

A universal speech user interface for wrapping applications to provide them with a user interface that uses speech rather than text commands or traditional user interfaces

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

If you want to use the default ChatGPT integration make sure that you create
a `.env` file which defines the `OPENAI_API_KEY` environment variable with
a reference to your OpenAI API key.
