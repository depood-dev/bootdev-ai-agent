import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_working_path = os.path.abspath(working_directory)
        abs_path = os.path.abspath(full_path)

        if not abs_path.startswith(abs_working_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(abs_path):
            return f'Error: File "{file_path}" not found.'
        
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        try:
            run_script = ["python3", abs_path] + args
            completed_process = subprocess.run(
                run_script, 
                timeout=30, 
                capture_output=True, 
                text=True,
                cwd=working_directory)
            
        except Exception as e:
            return f"Error: executing Python file: {e}"
    
    except Exception as e:
        return f"Error: {e}"           

    if completed_process.stdout == "" and completed_process.stderr == "":
        return "No output produced."
    
    output_stdout = "STDOUT:" + completed_process.stdout
    output_stderr = "STDERR:" + completed_process.stderr
          
    if completed_process.returncode != 0:
        return f"{output_stdout}\n{output_stderr}\nProcess exited with code {completed_process.returncode}"
    else:
        return f"{output_stdout}\n{output_stderr}"