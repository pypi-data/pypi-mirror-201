import openai
import os
import subprocess
import tiktoken
from openai.error import InvalidRequestError
from rich.console import Console
from rich.markdown import Markdown
import json

def start():
    print("Loading...")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    code_theme = os.getenv("BCLIGPT_CODE_THEME", "monokai")
    model = os.getenv("BCLIGPT_MODEL", "gpt-3.5-turbo")
    messages = [
            {"role": "system", "content": "Your are an helpful coding assistant. You write responses in markdown. In code blocks, always add the language of the code to enable syntax highlighting. For code blocks containing commands, always add bash as a language near the ``` mark, like this: ```bash"},
        ]

    message_database = []
    encoding = tiktoken.encoding_for_model(model)
    result = openai.ChatCompletion.create(
      model=model,
      messages=messages,)

    tokens = 0
    console = Console()
    while True:
        message = input(f"(Tokens: {tokens}) - You: ")
        message_token_count = len(encoding.encode(message))
        tokens += message_token_count
        while tokens > 3500:
            popped_message = messages.pop(1)
            tokens -= len(encoding.encode(popped_message["content"]))
        messages.append({"role": "user", "content": message})

        try:
            result = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                stream=True,
            )
            full_content = ''
            new_lines = 0
            for chunk in result:
                # get "finish_reason" from delta, otherwise return None
                finish_reason = chunk["choices"][0].get("finish_reason")
                if "content" in chunk["choices"][0]["delta"]:
                    content = chunk['choices'][0]['delta']['content']
                    full_content += content
                    md = Markdown(full_content, code_theme=code_theme)
                    with console.capture() as capture:
                        console.print(md)
                    # count the number of new lines in the capture
                    new_lines = capture.get().count('\n')
                    console.print(md)
                    print("\r", end="")
                    if new_lines > 0:
                        for i in range(new_lines):
                            print("\033[F", end="")
                if finish_reason == "stop":
                    for i in range(new_lines):
                        print("\n", end="")
            message_token_count = len(encoding.encode(full_content))
            tokens += message_token_count
            messages.append({"role": "assistant", "content": full_content})
        except InvalidRequestError as e:
            print("Error: ", e)
            while tokens > 3500:
                popped_message = messages.pop(1)
                tokens -= len(encoding.encode(popped_message["content"]))
