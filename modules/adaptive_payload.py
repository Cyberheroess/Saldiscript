import random
import string
from sklearn.externals import joblib

class AdaptivePayloadGenerator:
    def __init__(self, model_path):
        self.model = joblib.load(model_path)

    def generate_payload(self, input_data):
        # Prediksi tipe serangan berdasarkan model
        attack_type = self.model.predict([input_data])[0]

        if attack_type == "sql_injection":
            return self._generate_sql_injection_payload()
        elif attack_type == "xss":
            return self._generate_xss_payload()
        else:
            return self._generate_default_payload()

    def _generate_sql_injection_payload(self):
        return "' OR 1=1 --"

    def _generate_xss_payload(self):
        return "<script>alert('XSS')</script>"

    def _generate_default_payload(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=16))
