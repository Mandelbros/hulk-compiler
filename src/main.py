def run_pipeline(file_path): 
    with open(file_path, 'r') as file:
        text = file.read()


if __name__ == "__main__":
    file_path = 'test.hulk'  # replace with your file path
    result = run_pipeline(file_path)