from app.decorators.file import handle_file_exists


class File:
    @classmethod
    def save_file(cls, filepath, content):
        with open(filepath, 'wb') as file:
            file.write(content)
    
    @classmethod
    @handle_file_exists
    def read_file(cls, filepath):
        with open(filepath, 'rb') as file:
            return file.read()
