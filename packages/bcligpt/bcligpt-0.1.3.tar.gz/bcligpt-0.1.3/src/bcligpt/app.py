import openai
import os
import subprocess
import tiktoken
from openai.error import InvalidRequestError
def start():
    print("Loading...")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    messages = [
            {"role": "system", "content": "Your are an helpful coding assistant. You write responses in markdown"},
        ]

    model = "gpt-3.5-turbo"
    encoding = tiktoken.encoding_for_model(model)
    result = openai.ChatCompletion.create(
      model=model,
      messages=messages,)

    tokens = 0
    while True:
        message = input(f"(Tokens: {tokens}) - You: ")
        message_token_count = len(encoding.encode(message))
        while tokens + message_token_count > 3500:
            popped_message = messages.pop(1)
            tokens -= len(encoding.encode(popped_message["content"]))

        messages.append({"role": "user", "content": message})

        try:
            result = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            content = result['choices'][0]['message']['content']
            messages.append({"role": "assistant", "content": content})
            proc = subprocess.Popen(['glow'], stdin=subprocess.PIPE)
            proc.communicate(content.encode())
            tokens = result["usage"]["total_tokens"]
        except InvalidRequestError as e:
            while tokens > 3500:
                popped_message = messages.pop(1)
                tokens -= len(encoding.encode(popped_message["content"]))

