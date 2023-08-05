import openai
import os

def ask_openai(prompt, config):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.ChatCompletion.create(
        model = config.openai.model,
        messages = [
            {"role": "user", "content": prompt},
        ]
    )

    message = None
    if response['choices'][0]['finish_reason'] == 'stop':
        message = response['choices'][0]['message']['content']

    return message