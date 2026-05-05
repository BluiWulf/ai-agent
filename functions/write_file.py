import os

from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        workingAbsPath = os.path.abspath(working_directory)
        targetFile = os.path.normpath(os.path.join(workingAbsPath, file_path))
        valid_target_file = os.path.commonpath([workingAbsPath, targetFile]) == workingAbsPath

        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(targetFile):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(targetFile), exist_ok=True)
        with open(targetFile, "w") as file:
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error writing to file: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites contents of specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of Python file to execute, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Contents to be written to specified file",
            ),
        },
        required=["file_path", "content"],
    ),
)
