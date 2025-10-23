import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables from parent directory
load_dotenv()

API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")

if not API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not found.")

client = Anthropic(api_key=API_KEY)

# Simple test to verify API connection
test_response = client.messages.create(
    model=MODEL,
    max_tokens=100,
    messages=[
        {
            "role": "user",
            "content": "Say 'Connection successful!' if you can read this.",
        }
    ],
)

print("API Test Response:")
print(test_response.content[0].text)
print(
    f"\n✓ Token usage: {test_response.usage.input_tokens} in, {test_response.usage.output_tokens} out"
)
