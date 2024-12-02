class FileInclusion:
    def __init__(self):
        pass

    def include_file(self, url, file_name):
        file_url = f"{url}?file={file_name}"
        print(f"Attempting file inclusion on: {file_url}")
        return file_url
