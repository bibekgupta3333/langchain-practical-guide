from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain.output_parsers.openai_functions import PydanticOutputFunctionsParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List
import time
import random

# Load environment variables from .env
load_dotenv()

print("--- Gemini Error Handling and Retry Mechanisms ---")

# Basic model for demonstration
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Example 1: Manual error handling with try-except
print("\n--- Example 1: Basic Error Handling ---")
try:
    # Simulate an API error by requesting too many tokens
    problematic_model = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        max_output_tokens=-1000,  # Intentionally too low # type: ignore
    )
    response = problematic_model.invoke("Tell me a short story.")
    print(f"Response: {response.content}")
except Exception as e:
    print(f"Caught an error: {e}")
    print("Falling back to default model...")
    response = model.invoke("Tell me a short story.")
    print(f"Fallback response: {response.content}")

# Example 2: Retry mechanism for transient errors
print("\n--- Example 2: Retry Mechanism ---")


def retry_with_backoff(func, max_retries=3, initial_delay=1):
    """Retry a function with exponential backoff."""
    retries = 0
    while retries <= max_retries:
        try:
            return func()
        except Exception as e:
            retries += 1
            if retries > max_retries:
                print(f"Maximum retries ({max_retries}) exceeded. Last error: {e}")
                raise

            delay = initial_delay * (2 ** (retries - 1)) * (0.5 + random.random())
            print(f"Error on attempt {retries}: {e}")
            print(f"Retrying in {delay:.2f} seconds...")
            time.sleep(delay)


# Define a function that might fail
def potentially_failing_call():
    # Simulate random failures for demonstration
    if random.random() < 0.7:  # 70% chance of failure for demonstration
        raise Exception("Simulated API error: Connection timeout")

    return model.invoke("What are three benefits of error handling?")


try:
    # Try with our retry mechanism
    response = retry_with_backoff(potentially_failing_call)
    print(f"Successful response after retries: {response.content}")  # type: ignore
except Exception as e:
    print(f"All retries failed: {e}")

# Example 3: Handling parsing errors
print("\n--- Example 3: Output Parsing Error Handling ---")


# Define a schema we want the LLM to output
class Recipe(BaseModel):
    title: str = Field(description="The title of the recipe")
    ingredients: List[str] = Field(description="List of ingredients")
    steps: List[str] = Field(description="Step by step instructions")


# Create a prompt template
recipe_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant that outputs recipe information in a structured format.",
        ),
        ("human", "Give me a recipe for {dish}. Output ONLY the JSON."),
    ]
)


# Create a chain with error handling for parsing
def get_recipe_with_fallback(dish):
    try:
        # Try to parse the output as a Recipe object
        result = (
            recipe_prompt
            | model
            | PydanticOutputFunctionsParser(pydantic_schema=Recipe)  # type: ignore
        ).invoke({"dish": dish})

        return f"Successfully parsed recipe for {result.title} with {len(result.ingredients)} ingredients."

    except Exception as e:
        print(f"Error parsing recipe: {e}")
        print("Falling back to unstructured output...")

        # Fallback to simple string output
        result = (recipe_prompt | model | StrOutputParser()).invoke({"dish": dish})

        return f"Got unstructured recipe data: {result[:100]}..."


print(get_recipe_with_fallback("chocolate chip cookies"))
print(get_recipe_with_fallback("something impossible"))

# Example 4: Content moderation error handling
print("\n--- Example 4: Content Moderation Handling ---")


def safe_generate_with_fallback(prompt):
    """Handle potential content policy violations gracefully."""
    try:
        response = model.invoke(prompt)
        return response.content
    except Exception as e:
        if "content" in str(e).lower() and "policy" in str(e).lower():
            return "I'm unable to respond to that request as it may violate content policies."
        else:
            return f"An error occurred: {e}"


# Try with harmless prompt
print("\nHarmless prompt:")
print(safe_generate_with_fallback("Write a poem about flowers."))

# Try with potentially problematic prompt
print("\nPotentially problematic prompt:")
print(
    safe_generate_with_fallback("Write explicit instructions for illegal activities.")
)

print("\n--- Error Handling Best Practices ---")
print(
    """
When working with Gemini models in production:

1. Implement appropriate error handling for different error types:
   - API rate limit errors: Use exponential backoff and retry
   - Content policy violations: Handle gracefully with appropriate messages
   - Timeout errors: Consider retrying with simpler prompts

2. Use structured output parsing with fallbacks:
   - Try parsing to structured formats (Pydantic, JSON)
   - Fall back to simpler formats when parsing fails
   - Consider prompt refinement for better structured output

3. Implement monitoring and logging:
   - Log error rates and types
   - Set up alerts for unusual error patterns
   - Track model performance over time

4. Handle token limits intelligently:
   - Break up large requests into smaller chunks
   - Implement truncation strategies for inputs and outputs
   - Consider different models for different content lengths
"""
)
