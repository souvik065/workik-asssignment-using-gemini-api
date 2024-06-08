import asyncio
import google.generativeai as genai
import os
from dotenv import find_dotenv, load_dotenv
import json
from util import  fileoperations as fl, content_generator as cn
import sys
import shutil

from util.handler import FileLimitExceededError

load_dotenv()
gemini_api_key = os.environ.get("GEMINI_API_KEY")
# defaults to getting the key using os.environ.get("OPENAI_API_KEY")
# if you saved the key under a different environment variable name, you can do something like:
# client = OpenAI(
#   api_key=os.environ.get("CUSTOM_ENV_NAME"),
# )


genai.configure(api_key=gemini_api_key)
"""
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)        
"""

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config,)

def parse_multiple_json(response):
    """Parse multiple JSON objects from a string."""
    decoder = json.JSONDecoder()
    pos = 0
    while pos < len(response):
        response = response.lstrip()
        try:
            obj, pos = decoder.raw_decode(response)
            yield obj
            response = response[pos:]
        except json.JSONDecodeError:
            break

def menu():
    print("Welcome to Gemini AI Assistant :")
    print("1. Create a Project with using Gemini")
    print("3. Exit")



def option1():
    prompt = input("Enter what you want to create : ")
    response = asyncio.run(cn.generate_content_async(model=model,prompt=prompt))
    print("\n Response : ", response)
    project_name = input("Enter Project Name : ")

    # Parse the JSON data
    try:
        all_data = parse_multiple_json(response)
        for data in all_data:
            base_directory = f"projects/{project_name or 'default_project'}"
            os.makedirs(base_directory, exist_ok=True)
            fl.create_structure(base_directory, data, file_limit=20)

            # Zip the project directory
            zip_file = f"{base_directory}.zip"
            shutil.make_archive(base_directory, 'zip', base_directory)
            print(f"Project zipped successfully at {zip_file}")
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e.msg} at line {e.lineno} column {e.colno} (char {e.pos})")
    except FileLimitExceededError as e:
        print(f"Error: {e}")


def exit_program():
    print("Exiting program...")
    sys.exit()

def main():
    menu()
    choice = input("Enter your choice : ")
    match choice:
        case '1':
            option1()
        case '2':
            exit_program()
        case _:
            print("Invalid choice. Please choose a valid option.")



if __name__ == "__main__":
    main()
