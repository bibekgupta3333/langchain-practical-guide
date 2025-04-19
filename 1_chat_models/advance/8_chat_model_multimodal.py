from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os
import base64
from PIL import Image
from io import BytesIO

# Load environment variables from .env
load_dotenv()

print("--- Gemini Multimodal Capabilities ---")

# Create a ChatGoogleGenerativeAI model configured for multimodal inputs
model = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")

# Define file paths for images
# Create an "images" directory in the same folder as this script
current_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(current_dir, "images")
os.makedirs(images_dir, exist_ok=True)

# Create example image paths (you'll need to add actual images to this directory)
chart_image = os.path.join(images_dir, "chart.png")
code_image = os.path.join(images_dir, "code.png")
diagram_image = os.path.join(images_dir, "diagram.png")


# Function to check if image exists and convert to base64 if it exists
def get_image_data(image_path):
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        print(f"Please add an image file at this location or update the path.")
        return None

    # Open the image and convert to base64
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")

    # Determine MIME type based on file extension
    if image_path.lower().endswith(".png"):
        mime_type = "image/png"
    elif image_path.lower().endswith((".jpg", ".jpeg")):
        mime_type = "image/jpeg"
    else:
        mime_type = "image/png"  # Default to PNG

    # Create the data URL format
    image_url = f"data:{mime_type};base64,{image_data}"
    return image_url


# Example 1: Image analysis with context
print("\n--- Example 1: Image Analysis ---")
image_url = get_image_data(chart_image)
if image_url:
    # Create a message with image content
    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": "What does this chart show? What are the key insights?",
            },
            {"type": "image_url", "image_url": image_url},
        ]
    )

    # Get response from the model
    response = model.invoke([message])
    print(f"Analysis response:\n{response.content}\n")

# Example 2: Code analysis from image
print("\n--- Example 2: Code Analysis from Image ---")
image_url = get_image_data(code_image)
if image_url:
    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": "Explain what this code does and suggest any improvements:",
            },
            {"type": "image_url", "image_url": image_url},
        ]
    )

    response = model.invoke([message])
    print(f"Code analysis response:\n{response.content}\n")

# Example 3: Combining multiple images
print("\n--- Example 3: Multiple Images ---")
diagram_url = get_image_data(diagram_image)
chart_url = get_image_data(chart_image)
if diagram_url and chart_url:
    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": "Compare these two images and tell me how they relate to each other:",
            },
            {"type": "image_url", "image_url": diagram_url},
            {"type": "image_url", "image_url": chart_url},
        ]
    )

    response = model.invoke([message])
    print(f"Comparison response:\n{response.content}\n")

# Example 4: Following up on an image analysis
print("\n--- Example 4: Conversation with Image Context ---")
diagram_url = get_image_data(diagram_image)
if diagram_url:
    # Initial message with image
    message1 = HumanMessage(
        content=[
            {"type": "text", "text": "What is shown in this diagram?"},
            {"type": "image_url", "image_url": diagram_url},
        ]
    )

    # Get first response
    response1 = model.invoke([message1])
    print(f"Initial response:\n{response1.content}\n")


print("\n--- Using Multimodal Features ---")
print(
    """
To use multimodal features with Gemini:

1. Create a "images" directory with example images:
   - chart.png: A chart or graph image
   - code.png: An image containing code
   - diagram.png: A diagram or schematic

2. Use the proper model:
   - gemini-1.5-pro-latest supports multimodal inputs

3. Format messages with both text and images:
   - Use a list of content items with "type" field
   - "text" type for text content
   - "image_url" type for image content with base64 encoding

4. For production applications:
   - Host images on public URLs or use base64 encoding (as shown in this example)
   - Consider privacy implications of sharing images
   - Be aware of higher token usage for image analysis
"""
)
