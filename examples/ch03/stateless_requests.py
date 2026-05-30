import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

MODEL = os.getenv("ANTHROPIC_MODEL", "claude-opus-4-8")


def ask(prompt: str) -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    return response.content[0].text


print("First request:")
print(ask("My name is Inigo Montoya."))

print("\nSecond request:")
print(ask("What is my name?"))
