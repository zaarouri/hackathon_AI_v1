
from dotenv import load_dotenv
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Load environment variables from .env
load_dotenv()


# Base GitHub API URL
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1"
# Access the token
token = os.environ["GITHUB_TOKEN"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

response = client.complete(
    messages=[
        SystemMessage("You are a helpful assistant."),
        UserMessage("who is the president of the united states?"),
    ],
    temperature=1.0,
    top_p=1.0,
    model=model
)

print(response.choices[0].message.content)






def call_model(prompt: str) -> str:
    try:
        response = client.complete(
            messages=[
                SystemMessage("You are a helpful assistant."),
                UserMessage(prompt)
            ],
            temperature=1.0,
            top_p=1.0,
            model=model
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error from GPT-4.1 model: {str(e)}"
   

def transform(filepath ):
    with open(filepath, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines