from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parents[1]))

from ollama import chat
from util.llm_utils import pretty_stringify_chat, ollama_seed as seed

# Add you code below
sign_your_name = 'Austin Turner'
model = 'llama3.1'
options = {'temperature': 0.7, 'max_tokens': 50}
messages = [
  {'role': 'system', 'content': 'You should embrace the role of a Dungeon Master from the Dungeons and Dragons game' },
]


# But before here.

options |= {'seed': seed(sign_your_name)}
# Chat loop
while True:
  # Add you code below
  message = {'role': 'user', 'content': input('You: ')}
  messages.append(message)
  if messages[-1]['content'] == '/exit':
    break
  response = chat(model=model, messages=messages, stream=False, options=options)
  print(f'Agent: {response.message.content}')
  messages.append({'role': 'assistant', 'content': response.message.content})
  

  # But before here.

# Save chat
with open(Path('lab03/attempts.txt'), 'a') as f:
  file_string  = ''
  file_string +=       '-------------------------NEW ATTEMPT-------------------------\n\n\n'
  file_string += f'Model: {model}\n'
  file_string += f'Options: {options}\n'
  file_string += pretty_stringify_chat(messages)
  file_string += '\n\n\n------------------------END OF ATTEMPT------------------------\n\n\n'
  f.write(file_string)

