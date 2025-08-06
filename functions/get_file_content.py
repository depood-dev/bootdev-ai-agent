import os
from functions.config import file_char_limit

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
    