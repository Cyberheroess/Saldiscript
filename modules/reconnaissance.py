import dns.resolver
import requests
import random

class Reconnaissance:
    def __init__(self, target_domain):
        self.target_domain = target_domain

    def get_subdomains(self):
        """
        Using DNS brute force to find subdomains of the target.
        """
        subdomains = ["www", "api", "mail", "ftp", "admin"]
        discovered_subdomains = []

        for subdomain in subdomains:
            domain = f"{subdomain}.{self.target_domain}"
            try:
                dns.resolver.resolve(domain, 'A')
                discovered_subdomains.append(domain)
                print(f"Discovered subdomain: {domain}")
            except dns.resolver.NoAnswer:
                continue
        return discovered_subdomains

    def get_http_headers(self):
        """
        Fetch the HTTP headers of the target to gather information.
        """
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        }
        try:
            response = requests.get(f"http://{self.target_domain}", headers=headers)
            print(f"HTTP headers: {response.headers}")
            return response.headers
        except requests.exceptions.RequestException as e:
            print(f"Error fetching HTTP headers: {e}")
            return {}

    def run_recon(self):
        """
        Run the full reconnaissance on the target.
        """
        print(f"Starting reconnaissance on {self.target_domain}")
        subdomains = self.get_subdomains()
        headers = self.get_http_headers()
        return subdomains, headers
