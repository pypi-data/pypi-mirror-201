import os


def connection(func):
    def decorator(self, *args, **kwargs):
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)
        return func(self, *args, **kwargs)

    return decorator


def extensions_validator(func):
    def decorator(self, filepath, *args, **kwargs):
        *_, file_extension = os.path.splitext(filepath)
        file_extension = file_extension[1:]

        if self.extensions_accepted == '__all__' or file_extension in self.extensions_accepted:
            return func(self, filepath, *args, **kwargs)
        else:
            raise TypeError(f"Expected extensions: {self.extensions_accepted}, got: {file_extension}")
    return decorator
