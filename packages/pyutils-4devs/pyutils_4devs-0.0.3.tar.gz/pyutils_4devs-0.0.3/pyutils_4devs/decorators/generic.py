from typing import Any


def handle_exceptions(*exceptions):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                return {'status_code': getattr(e, 'status', 400), 'detail': getattr(e, 'detail', str(e))}
        return wrapper
    return decorator


def return_type_validator(*types):
    def decorator(func):
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            response_type = type(response)
            if Any in types or response_type in types:
                return response
            raise TypeError(f"Expected types: {types}, got: {response_type}")
        return wrapper
    return decorator
