import os

def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_working_path = os.path.abspath(working_directory)
        abs_path = os.path.abspath(full_path)

        if not abs_path.startswith(abs_working_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        abs_path_dirname = os.path.dirname(abs_path)
        if not os.path.exists(abs_path_dirname):
            os.makedirs(abs_path_dirname)

        #if not os.path.isfile(full_path):
        #    return f'Error: "{file_path}" is not a directory'

        with open(abs_path, "w") as f:
            f.write(content)

                    
    except Exception as e:
        return f"Error: {e}"

            
            

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'