import os
from google.genai import types
from functions.config import file_char_limit

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads a file in the specified diectory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to a file to read, relative to the working directory. If not provided, lists files in the working directory itself."
                )            
            }
    )
)


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to a file to execute, relative to the working directory."
            ),
            "arguments": types.Schema(
                type=types.Type.STRING,
                description="Optional argments to execute the file with"
            )
            
        }
    )
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes a file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to a file to write, relative to the working directory. If not provided, lists files in the working directory itself."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file"
            )

        }
    )
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
        ]
    )

def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_working_path = os.path.abspath(working_directory)
        abs_path = os.path.abspath(full_path)

        file_content = ""
        output = []
        output.append("Result for current directory:")


        if not abs_path.startswith(abs_working_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(full_path, "r") as f:
            file_content = f.read(file_char_limit)

        if len(file_content) == 10000:
            file_content += f'[...File "{file_path}" truncated at 10000 characters]'    

        return file_content
    except Exception as e:
        return f"Error: {e}"
    
