# modul
from .sql_injection import execute_sql_injection
from .xss_attack import execute_xss_attack
from .ddos_attack import execute_ddos_attack
from .webshell_upload import upload_webshell
from .file_inclusion import exploit_file_inclusion
from .reconnaissance import reconnaissance
from .exploit_chain import exploit_chain
from .adaptive_payload import adaptive_payload
from .cloud_waf_bypass import cloud_waf_bypass
from .data_exfiltration import data_exfiltration

__all__ = [
    "execute_sql_injection",
    "execute_xss_attack",
    "execute_ddos_attack",
    "upload_webshell",
    "exploit_file_inclusion",
    "reconnaissance",
    "exploit_chain",
    "adaptive_payload",
    "cloud_waf_bypass",
    "data_exfiltration"
]

print("Web Attack Package Initialized.")
