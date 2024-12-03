import requests
import socket
import subprocess
import whois
from urllib.parse import urlparse
from requests.exceptions import RequestException
import threading

class ReconnaissanceAdvanced:
    def __init__(self, target_url, headers=None):
        self.target_url = target_url
        self.headers = headers if headers else {'User-Agent': 'Mozilla/5.0'}

    def port_scan(self, target_ip):
        """
        Perform a simple port scan to find open ports.
        """
        open_ports = []
        for port in range(1, 1025):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        print(f"Open ports on {target_ip}: {open_ports}")
        return open_ports

    def service_identification(self, target_ip, ports):
        """
        Identify services running on open ports using banner grabbing.
        """
        services = {}
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((target_ip, port))
                banner = sock.recv(1024).decode().strip()
                services[port] = banner
                sock.close()
            except:
                services[port] = "Service not identified"
        print(f"Services on {target_ip}: {services}")
        return services

    def directory_brute_force(self):
        """
        Perform directory brute-forcing using a common wordlist to find hidden directories.
        """
        common_dirs = ["admin", "login", "dashboard", "uploads", "config", "adminpanel"]
        found_dirs = []
        for directory in common_dirs:
            url = f"{self.target_url}/{directory}"
            try:
                response = requests.get(url, headers=self.headers)
                if response.status_code == 200:
                    found_dirs.append(url)
            except RequestException as e:
                print(f"Error accessing {url}: {e}")
        print(f"Found directories: {found_dirs}")
        return found_dirs

    def subdomain_enumeration(self):
        """
        Attempt to enumerate subdomains using a simple wordlist.
        """
        subdomain_list = ["www", "mail", "api", "dev", "test"]
        found_subdomains = []
        domain = urlparse(self.target_url).netloc
        for sub in subdomain_list:
            subdomain = f"{sub}.{domain}"
            try:
                response = requests.get(f"http://{subdomain}", headers=self.headers)
                if response.status_code == 200:
                    found_subdomains.append(subdomain)
            except RequestException:
                continue
        print(f"Found subdomains: {found_subdomains}")
        return found_subdomains

    def whois_lookup(self):
        """
        Perform a WHOIS lookup to gather domain registration details.
        """
        domain = urlparse(self.target_url).netloc
        try:
            w = whois.whois(domain)
            print(f"WHOIS information for {domain}: {w}")
            return w
        except Exception as e:
            print(f"Error during WHOIS lookup: {e}")
            return None

    def perform_reconnaissance(self):
        """
        Perform the full reconnaissance process: Port Scan -> Service Identification -> Directory Brute Force -> Subdomain Enumeration -> WHOIS Lookup.
        """
        print(f"Starting reconnaissance on {self.target_url}")
        
        # Step 1: Port Scan
        target_ip = socket.gethostbyname(urlparse(self.target_url).hostname)
        open_ports = self.port_scan(target_ip)
        
        # Step 2: Service Identification
        services = self.service_identification(target_ip, open_ports)
        
        # Step 3: Directory Brute Forcing
        found_dirs = self.directory_brute_force()
        
        # Step 4: Subdomain Enumeration
        found_subdomains = self.subdomain_enumeration()
        
        # Step 5: WHOIS Lookup
        whois_info = self.whois_lookup()
        
        print("Reconnaissance completed.")
