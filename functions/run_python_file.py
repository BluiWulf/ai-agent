import os, subprocess

from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        workingAbsPath = os.path.abspath(working_directory)
        targetFile = os.path.normpath(os.path.join(workingAbsPath, file_path))
        valid_target_file = os.path.commonpath([workingAbsPath, targetFile]) == workingAbsPath

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(targetFile):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not targetFile.lower().endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", targetFile]
        if not args is None:
            command.extend(args)
        completed = subprocess.run(command, cwd=working_directory, capture_output=True, text=True, timeout=30)

        output = ""
        if completed.returncode != 0:
            output += f"Process exited with code {completed.returncode}\n"
        if len(completed.stdout) == 0 and len(completed.stderr) == 0:
            output += "No output produced\n"
        else:
            if len(completed.stdout) != 0:
                output += f"STDOUT: {completed.stdout}\n"
            if len(completed.stderr) != 0:
                output += f"STDERR: {completed.stderr}\n"
        
        return output

    except Exception as e:
        return f"Error executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python files, with optional arguments, relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional arguments for executing Python file",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)
