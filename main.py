import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("API Key is missing")
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    user_prompt = args.user_prompt

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    
    client = genai.Client(api_key=api_key)
    avail_functions = types.Tool(
        function_declarations=[schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file]
    )
    aiConfig = types.GenerateContentConfig(
        tools=[avail_functions],
        system_instruction=system_prompt,
        temperature=0
    )
    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents=messages,
        config=aiConfig,
    )

    if response.usage_metadata is None:
        raise RuntimeError("Failed API request")
    
    if args.verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    if response.function_calls:
        for call in response.function_calls:
            print(f"Calling function: {call.name}({call.args})")
    else:
        print(f"Response:\n{response.text}")

if __name__ == "__main__":
    main()
