import os


class FilesUtil:

    def __init__(self):
        pass

    # @staticmethod
    def get_file_path(self, wildcard, base_path, suffix):
        file_path = self.resolve_file_path(wildcard, base_path, suffix)

        if suffix and self.is_file_exists(file_path):
            return file_path
        else:
            return self.resolve_file_path(wildcard, base_path, None)


    # @staticmethod
    def resolve_file_path(self, wildcard, base_path, suffix=None):
        suffix = '-' + suffix if suffix else ''
        filename = wildcard + suffix + ".txt"
        return os.path.join(base_path, *filename.split('/'))


    # @staticmethod
    def get_file_content(self, file_path):
        if os.path.exists(file_path):
            print("File found:", file_path)
            with open(file_path, "r") as file:
                return file.read().strip()


    # @staticmethod
    def is_file_exists(self, file_path):
        return os.path.exists(file_path)
