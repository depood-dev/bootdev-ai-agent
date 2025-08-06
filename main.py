import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

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
    )
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()
