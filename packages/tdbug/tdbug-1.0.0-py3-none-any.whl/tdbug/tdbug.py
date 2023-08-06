import sys
import openai
from dotenv import load_dotenv
import os
from rich.console import Console

load_dotenv()

# Check if OPENAI_API_KEY is set in the environment
if not os.getenv("OPENAI_API_KEY"):

    # Prompt user for OPENAI_API_KEY value
    openai_api_key = input("Please enter your OpenAI API key: ")

    # Write value to .env file
    with open(".env", "w") as f:
        f.write(f"OPENAI_API_KEY={openai_api_key}")
    
    load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

error_message = input("Please paste your error code here: ")

console = Console()

if sys.version_info < (3, 7):
    console.print("[bold red]Error:[/bold red] DBUG requires Python 3.7 or higher to run.")
    console.print("Please update to a newer version of Python.\n")
    console.print("[bold]Suggestions:[/bold]")
    console.print("- Install the latest version of Python 3 from the official Python website (https://www.python.org/downloads/).")
    console.print("- Use a Python version manager like pyenv to easily switch between multiple versions of Python.\n")
    sys.exit(1)

def get_error_explanation(error_message):
    prompt = (f'''Generate an explanation and solution for the following error message: `{error_message}`. Preface the explanation with "Explanation: " and the solution with "Solution: " and put Explanation and Solution on separate lines.''')
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    response_text = response.choices[0].text.strip()
    print(response_text)

get_error_explanation(error_message)