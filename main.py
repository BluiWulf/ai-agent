import os
import argparse
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import *

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("API Key is missing")
    
    parser = argparse.ArgumentParser(description = "Chatbot")
    parser.add_argument("user_prompt", type = str, help = "User Prompt")
    parser.add_argument("--verbose", action = "store_true", help = "Enable verbose output")
    args = parser.parse_args()
    user_prompt = args.user_prompt

    messages = [types.Content(role = "user", parts = [types.Part(text = user_prompt)])]
    
    client = genai.Client(api_key=api_key)
    response = None
    for _ in range(20):
        response = generate_content(client, messages, args.verbose, user_prompt)
        if not response.function_calls:
            if response.text:
                print(f"Response:\n{response.text}")
            return
    print(f"Model took too long to process prompt")
    sys.exit(1)

def generate_content(client, messages, verbose, user_prompt):
    aiConfig = types.GenerateContentConfig(
        tools = [avail_functions],
        system_instruction = system_prompt,
        temperature = 0
    )
    response = client.models.generate_content(
        model = 'gemini-2.5-flash',
        contents = messages,
        config = aiConfig,
    )

    if response.usage_metadata is None:
        raise RuntimeError("Failed API request")
    
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)
    
    function_responses = []
    if response.function_calls:
        for call in response.function_calls:
            result = call_function(call, verbose)
            if not result.parts:
                raise Exception("No parts returned from function call")
            if not result.parts[0].function_response:
                raise Exception("FunctionResponse object cannot be None")
            if not result.parts[0].function_response.response:
                raise Exception("Response of FunctionResponse object cannot be None")
            function_responses.append(result.parts[0])
            if verbose:
                print(f"-> {result.parts[0].function_response.response}")
    
    messages.append(types.Content(role = "user", parts = function_responses))

    return response

if __name__ == "__main__":
    main()
