import json

def persist_to_file(file_name):
    def decorator(original_func):
        try:
            cache = json.load(open(file_name, 'r'))
        except (IOError, ValueError):
            cache = {}

        def new_func(self):
            nonlocal cache
            if not cache:
                cache = original_func(self)
                json.dump(cache, open(file_name, 'w'))
            return cache

        return new_func

    return decorator
