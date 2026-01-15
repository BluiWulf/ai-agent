import os

def get_files_info(working_directory, directory="."):
    try:
        workingAbsPath = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(workingAbsPath, directory))
        valid_target_dir = os.path.commonpath([workingAbsPath, target_dir]) == workingAbsPath

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_dir):
            return f'Error: "{directory} is not a directory'

        files = []
        for entry in os.listdir(target_dir):
            filePath = os.path.join(target_dir, entry)
            files.append(f"- {entry}: file_size={os.path.getsize(filePath)} bytes, is_dir={os.path.isdir(filePath)}")

        return "\n".join(files)
    
    except Exception as e:
        return f"Error listing files: {e}"
