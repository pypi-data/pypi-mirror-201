import openai
import os
from rich.console import Console
from rich.markdown import Markdown
import subprocess

openai.api_key = os.getenv("OPENAI_API_KEY")
messages = [
        {"role": "system", "content": "Your are an helpful coding assistant. You write responses in markdown"},
    ]

result = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=messages,)

while True:
    message = input("You: ")
    messages.append({"role": "user", "content": message})
    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    content = result['choices'][0]['message']['content']
    # write content to a log file
    with open('log.txt', 'a') as f:
        f.write(content)
    messages.append({"role": "assistant", "content": content})
    proc = subprocess.Popen(['glow'], stdin=subprocess.PIPE)
    proc.communicate(content.encode())
