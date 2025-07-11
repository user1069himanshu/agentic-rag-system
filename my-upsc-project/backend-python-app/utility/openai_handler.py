# This would go in a new utility/openai_handler.py file

from openai import OpenAI
from .config import get_openai_api_key

def call_openai_api(system_prompt: str, user_prompt: str):
    """
    Makes a synchronous API call to the OpenAI GPT-3.5-Turbo API.
    """
    api_key = get_openai_api_key()
    if not api_key:
        raise ValueError("OpenAI API Key is not configured.")

    try:
        client = OpenAI(api_key=api_key)

        completion = client.chat.completions.create(
            model="o3-2025-04-16",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"An error occurred during the OpenAI API call: {e}")
        raise