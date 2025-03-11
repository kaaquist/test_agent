def read_code_from_file(file_path: str) -> str:
    with open(file_path, "r") as file:
        code = file.read()
    return code


def write_code_to_file(file_path: str, code: str):
    with open(file_path, "w") as file:
        file.write(code)