from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
import time

# Load environment variables from .env
load_dotenv()

# Create a ChatGoogleGenerativeAI model with streaming enabled
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    streaming=True,  # Enable streaming for token-by-token generation
)

# Define a conversation with system and human messages
messages = [
    SystemMessage(
        content="You are an expert explaining complex concepts. Give detailed explanations in paragraphs."
    ),
    HumanMessage(content="Explain how large language models work in simple terms."),
]

print("--- Streaming Response ---")
print("Starting stream...")

# Stream the response token by token
response_chunks = []
for chunk in model.stream(messages):
    # Print each chunk as it arrives
    chunk_content = chunk.content
    print(chunk_content, end="", flush=True)
    response_chunks.append(chunk_content)
    # Slight delay to make the streaming visible
    time.sleep(0.01)

print("\n\n--- Complete Response ---")
# Join all chunks to get the complete response
complete_response = "".join(response_chunks)
print(f"Total length: {len(complete_response)} characters")

# You can also stream with a simpler interface
print("\n--- Alternative Streaming Approach ---")
for chunk in model.stream("Give me three quick facts about neural networks."):
    print(chunk.content, end="", flush=True)
    time.sleep(0.01)

print("\n")
