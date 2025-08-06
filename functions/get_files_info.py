import os


def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)
        abs_working_path = os.path.abspath(working_directory)
        abs_path = os.path.abspath(full_path)

        dir_contents = ""
        output = []
        output.append("Result for current directory:")


        if not abs_path.startswith(abs_working_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        

        dir_contents = os.listdir(abs_path)

        for item in dir_contents:
    
            full_item = os.path.join(abs_path, item)            
            output.append(f"- {item}: file_size={os.path.getsize(full_item)} bytes, is_dir={os.path.isdir(full_item)}")
            
    except Exception as e:
        return f"Error: {e}"

            
            

    return "\n".join(output)



    

