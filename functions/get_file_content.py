import os

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