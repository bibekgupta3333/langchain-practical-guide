from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# Load environment variables from .env
load_dotenv()

# Define a creative writing prompt
creative_prompt = "Write a short, imaginative description of a futuristic city."

print("--- Exploring Gemini Model Parameters ---")

# 1. Default parameters
print("\n--- Default Parameters ---")
default_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
response = default_model.invoke([HumanMessage(content=creative_prompt)])
print(f"Default response:\n{response.content}\n")

# 2. High temperature (more creative/random)
print("\n--- High Temperature (1.0) ---")
creative_model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=1.0,  # Higher values make output more random/creative
)
response = creative_model.invoke([HumanMessage(content=creative_prompt)])
print(f"Creative response (temp=1.0):\n{response.content}\n")

# 3. Low temperature (more deterministic/focused)
print("\n--- Low Temperature (0.1) ---")
focused_model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.1,  # Lower values make output more deterministic/focused
)
response = focused_model.invoke([HumanMessage(content=creative_prompt)])
print(f"Focused response (temp=0.1):\n{response.content}\n")

# 4. Adjusting top_p (nucleus sampling)
print("\n--- Adjusted Top-p (0.5) ---")
nucleus_model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.7,
    top_p=0.5,  # Only consider tokens with cumulative probability < 0.5
)
response = nucleus_model.invoke([HumanMessage(content=creative_prompt)])
print(f"Top-p adjusted response:\n{response.content}\n")

# 5. Limiting maximum output tokens
print("\n--- Limited Output Length (50 tokens) ---")
limited_model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    max_output_tokens=50,  # Limit response to approximately 50 tokens # type: ignore
)
response = limited_model.invoke([HumanMessage(content=creative_prompt)])
print(f"Length-limited response:\n{response.content}\n")

# 6. Comparison: Factual question with different temperatures
factual_prompt = "What are the main components of a computer?"

print("\n--- Factual Question with High Temperature (1.0) ---")
response = creative_model.invoke([HumanMessage(content=factual_prompt)])
print(f"Factual response (temp=1.0):\n{response.content}\n")

print("\n--- Factual Question with Low Temperature (0.1) ---")
response = focused_model.invoke([HumanMessage(content=factual_prompt)])
print(f"Factual response (temp=0.1):\n{response.content}\n")

# Summary of parameters
print("\n--- Parameter Summary ---")
print(
    """
Temperature (0.0 to 1.0):
- Controls randomness and creativity
- Higher values (0.7-1.0): More creative, varied, and potentially surprising outputs
- Lower values (0.0-0.3): More deterministic, focused, and predictable outputs
- Default: Usually around 0.7

Top-p (0.0 to 1.0):
- Controls diversity via nucleus sampling
- Lower values: Consider only the most likely tokens
- Higher values: Consider a wider range of tokens
- Default: Usually 0.95

Max Output Tokens:
- Limits the length of the response
- Useful for controlling response size and API costs
- Default: Model-specific maximum
"""
)
