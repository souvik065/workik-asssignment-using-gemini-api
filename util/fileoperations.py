import os
from util.handler import FileLimitExceededError

def create_structure(base_path, data, file_limit):
    file_count = 0

    def create_files(directory, structure, prefix=''):
        nonlocal file_count
        for name, content in structure.items():
            if file_count >= file_limit:
                raise FileLimitExceededError(file_limit)

            path = os.path.join(directory, f"{prefix}{name}")
            if isinstance(content, dict):
                os.makedirs(path, exist_ok=True)
                create_files(path, content)
            elif isinstance(content, list):
                os.makedirs(path, exist_ok=True)
                for idx, item in enumerate(content):
                    item_name = f"{name}_{idx}.txt"
                    if isinstance(item, dict):
                        create_files(path, item, prefix=f"{name}_{idx}_")
                    else:
                        item_path = os.path.join(path, item_name)
                        with open(item_path, 'w') as file:
                            file.write(item)
                        file_count += 1
                        if file_count >= file_limit:
                            raise FileLimitExceededError(file_limit)
            else:
                with open(path, 'w') as file:
                    file.write(content)
                file_count += 1

    create_files(base_path, data)
