import asyncio
import pathlib
import textwrap
import google.generativeai as genai
import os
from dotenv import find_dotenv, load_dotenv
import json
from util import  fileoperations as fl

load_dotenv()
gemini_api_key = os.environ.get("GEMINI_API_KEY")
# defaults to getting the key using os.environ.get("OPENAI_API_KEY")
# if you saved the key under a different environment variable name, you can do something like:
# client = OpenAI(
#   api_key=os.environ.get("CUSTOM_ENV_NAME"),
# )

def to_markdown(text):
    text = text.replace('•', ' *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

genai.configure(api_key=gemini_api_key)

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config,)
print(model)




async def generate_content_async():
    # Your asynchronous content generation logic
    response = await model.generate_content_async("Make an nodejs application to peforme CURD operation with the project structure")
    return response.text


response = asyncio.run(generate_content_async())
print("\n Response : ", response)



# Parse the JSON data
try:
    data = json.loads(response)
    # Base directory for the project
    base_directory = 'projects/project-2'

    # Create the base directory if it doesn't exist
    os.makedirs(base_directory, exist_ok=True)

    # Create the project structure
    fl.create_structure(base_directory, data)
except json.JSONDecodeError as e:
    print(f"JSONDecodeError: {e.msg} at line {e.lineno} column {e.colno} (char {e.pos})")



"""
# Clean the response if necessary
#cleaned_response = response.strip()

# Load the cleaned response as a JSON object

try:
    data = json.loads(cleaned_response)
    # Pretty print the JSON object
    print(type(data))
    print(json.dumps(data, indent=4))
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
"""

