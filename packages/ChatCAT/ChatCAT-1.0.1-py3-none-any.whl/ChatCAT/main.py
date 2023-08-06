import re
from typing import Optional
import urllib.request


def clean_text(text: str) -> str:
    """Clean input text by removing non-alphabetic characters and converting to lowercase."""
    sub: str = re.sub(r'[^a-z]+', ' ', text.lower())
    return sub


def match_input(input_text: str, patterns_responses: dict[str, str]) -> Optional[str]:
    """Match user input with stored patterns and return the best matching response."""
    cleaned_input = clean_text(input_text)
    best_match: Optional[str] = None
    best_match_score: int = 0

    for pattern, response in patterns_responses.items():
        score = sum(1 for word in cleaned_input.split() if word in pattern.split())

        if score > best_match_score:
            best_match_score = score
            best_match = response

    return best_match


def update_patterns_responses(input_text: str, response: str, patterns_responses: dict[str, str]) -> None:
    """Update patterns and responses based on user input."""
    cleaned_input = clean_text(input_text)
    patterns_responses[cleaned_input] = response

data = urllib.request.urlopen('https://chatbot-database.tjwllms52.repl.co/database.txt')
patterns_responses: dict[str, str] = {}
for line in data:
  line = line.decode('ascii')
  if '||' in line:
    input_text, response = line.split('||', 1)
    response = response.replace('/[NEWLINE]/', '\n', response.count('/[NEWLINE]/'))
    update_patterns_responses(input_text.strip(), response.strip(), patterns_responses)

def get_response(prompt):
  chatbot_response = match_input(prompt, patterns_responses)
  if chatbot_response:
      return str(chatbot_response)
  else:
      return str("I don't understand")