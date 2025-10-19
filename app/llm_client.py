# app/llm_client.py
from openai import OpenAI
from .config import settings

# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def ask_openai(prompt: str, model: str = "gpt-4o-mini") -> str:
    """
    Sends a user prompt to OpenAI and returns the model's response.
    """
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an AI assistant for Wazuh MCP Server."},
                {"role": "user", "content": prompt},
            ],
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error from OpenAI: {str(e)}"


        
