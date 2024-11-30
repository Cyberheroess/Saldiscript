import requests
import re

def reconnaissance(url):
    # Mencari informasi header
    try:
        response = requests.get(url)
        print(f"Response headers for {url}:")
        for header, value in response.headers.items():
            print(f"{header}: {value}")
        
        # Mencari file robots.txt untuk mengetahui direktori terlarang
        robots_url = f"{url}/robots.txt"
        robots_response = requests.get(robots_url)
        if robots_response.status_code == 200:
            print("\nDisallowed paths found in robots.txt:")
            print(robots_response.text)
        else:
            print("\nNo robots.txt found.")
        
        html_content = response.text
        meta_tags = re.findall(r'<meta[^>]*name=["\'](.*?)["\'][^>]*content=["\'](.*?)["\']', html_content)
        print("\nMeta tags found:")
        for tag in meta_tags:
            print(f"{tag[0]}: {tag[1]}")
        
    except requests.exceptions.RequestException as e:
        print(f"Reconnaissance failed: {e}")

# Contoh penggunaan:
# reconnaissance("http://target.com")
