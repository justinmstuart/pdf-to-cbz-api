import os

def save_file_to_directory(file, filename, directory):
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, filename)
    file.save(file_path)

    return file_path

def delete_directory(directory):
    if os.path.exists(directory):
        for root, dirs, files in os.walk(directory, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(directory)
