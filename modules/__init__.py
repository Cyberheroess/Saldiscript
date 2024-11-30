import logging
import os

# Setup basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Inisialisasi variabel global atau pengaturan
ATTACK_MODE = 'aggressive'  # Bisa diset ke 'stealth' atau lainnya tergantung mode serangan
TARGET_PLATFORM = 'web'     # Menandakan platform yang diserang (misalnya web, api, dsb.)

# Informasi dan konfigurasi lebih lanjut
PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
CONFIG_PATH = os.path.join(PROJECT_PATH, 'config')

def init_attack():
    """
    Fungsi untuk inisialisasi pengaturan serangan.
    Bisa digunakan untuk menetapkan profil serangan atau logika khusus.
    """
    if ATTACK_MODE == 'aggressive':
        logger.info("Aggressive attack mode enabled. Using full payload set.")
    else:
        logger.info("Stealth attack mode enabled. Using minimal payloads.")

def load_config():
    """
    Fungsi untuk memuat file konfigurasi atau file profil serangan.
    """
    config_file = os.path.join(CONFIG_PATH, 'attack_config.json')
    if os.path.exists(config_file):
        logger.info(f"Loading configuration from {config_file}")
        # Bisa diisi dengan kode untuk memuat file JSON konfigurasi
    else:
        logger.warning("Configuration file not found. Using default settings.")

# Impor modul serangan dari folder
from .sql_injection import SQLInjection
from .xss_attack import XSSAttack
from .ddos_attack import DDoSAttack
from .webshell_upload import WebShellUpload
from .file_inclusion import FileInclusion
from .reconnaissance import Reconnaissance
from .exploit_chain import ExploitChain
from .adaptive_payload import AdaptivePayload
from .cloud_waf_bypass import CloudWAFBypass
from .data_exfiltration import DataExfiltration

# Inisialisasi dan muat konfigurasi saat paket ini pertama kali dipanggil
init_attack()
load_config()

logger.info("Attack module initialized successfully.")
