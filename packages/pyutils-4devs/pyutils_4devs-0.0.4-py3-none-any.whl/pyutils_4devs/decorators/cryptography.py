def fernet_key_validator(func):
    def decorator(self, *args, **kwargs):
        if self.fernet_key is None:
            raise ValueError("Fernet key is not set, call method set_fernet_key() and save it")
        else:
            return func(self, *args, *kwargs)
    return decorator
