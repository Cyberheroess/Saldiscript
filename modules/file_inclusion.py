class FileInclusion:
    def __init__(self):
        pass

    def include_file(self, url, file_name):
        # Simulate file inclusion attack
        file_url = f"{url}?file={file_name}"
        print(f"Attempting Local File Inclusion on: {file_url}")
        response = requests.get(file_url)
        if response.status_code == 200:
            print(f"File inclusion successful on: {file_url}")
        else:
            print(f"File inclusion failed on: {file_url}, Status Code: {response.status_code}")
