# Chat Model Documents: https://python.langchain.com/docs/integrations/chat/
# OpenAI Chat Model Documents: https://python.langchain.com/docs/integrations/chat/google_generative_ai/

from dotenv import load_dotenv
from langchain_ollama import ChatOllama

# Load environment variables from .env
load_dotenv()

# Create a ChatGoogleGenerativeAI model
model = ChatOllama(model="gpt-oss:20b")

# Invoke the model with a message
result = model.invoke("What is 81 divided by 9?")
print("Full result:")
print(result)
print("Content only:")
print(result.content)
