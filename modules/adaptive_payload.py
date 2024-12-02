import random
import string

class AdaptivePayload:
    def __init__(self):
        pass
    
    def generate_payload(self, base_payload):
        random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        return f"{base_payload}{random_suffix}"

    def adapt_payload(self, payload):
        adapted_payload = payload.replace("1=1", f"{random.randint(1, 1000)}=1")
        return adapted_payload
        
