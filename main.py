import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.config import system_prompt
from functions.get_file_content import *
from functions.get_files_info import *
from functions.run_python_file import *
from functions.write_file import *

def main():
    # Load environment variables from a .env file so we can access sensitive keys
    load_dotenv()

    # Check if the '--verbose' option was provided by the user to enable extra output
    verbose = "--verbose" in sys.argv

    # Gather all positional arguments (ignore options/flags that start with '--')
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your promt here" [--verbose]')
        print('Example: python main.py "How di I build a calculator app?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # Join positional aurguments into a single string
    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)

def generate_content(client, messages, verbose):

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)        
    print("Response:")


    if len(response.function_calls) > 0:
        for call in response.function_calls:            
            function_call_result = call_function(call, verbose)
            if (
                not function_call_result.parts or
                not hasattr(function_call_result.parts[0], "function_response") or
                not hasattr(function_call_result.parts[0].function_response, "response")
            ):
                raise Exception("Fatal: No function response in content part.")

            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
        else:
                print(response.text)

def call_function(call, verbose=False):

    function_map = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file
    }

    if call.name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=call.name,
                    response={"error": f"Unknown function: {call.name}"},
            )
            ],
        )
    
    args = call.args.copy()          # Copy the original args
    args["working_directory"] = "./calculator"  # Add the required key
    func = function_map[call.name]
    
    if verbose:
        print(f"Calling function: {call.name}({call.args})")

    function_result = func(**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=call.name,
                response={"result": function_result},
            )
        ],
    )



if __name__ == "__main__":
    main()
