from .CommandArgs import CommandArgs


def send_text_to_chatgpt(args: CommandArgs):
    """
    Asynchronously send text to the ChatGPT model with a limit on the response size and get the response.
    """
    try:
        if args.client:
            response = args.client.chat.completions.create(
                messages=[{"role": "user", "content": args.text}],
                model="gpt-4-turbo-preview",
                max_tokens=args.max_response_length,  # Limiting the maximum length of the response
            )
        else:
            return "You need to pass in a client"
        return response.choices[0].message.content
    except Exception as e:
        return str(e)
