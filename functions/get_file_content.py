import os

from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        workingAbsPath = os.path.abspath(working_directory)
        targetFile = os.path.normpath(os.path.join(workingAbsPath, file_path))
        valid_target_file = os.path.commonpath([workingAbsPath, targetFile]) == workingAbsPath

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(targetFile):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(targetFile, "r") as entry:
            file_contents = entry.read(10000)
            if entry.read(1):
                file_contents += f'[...File "{file_path}" truncated at 10000 characters]'

        return file_contents
    
    except Exception as e:
        return f"Error listing file contents: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads contents of a specified file (truncated at 10000 characters) relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read contents of, relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["file_path"],
    ),
)
