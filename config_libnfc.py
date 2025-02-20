import os
import platform

def create_libnfc_conf():
    content = """# Configuration du lecteur NFC
device.name = "ACR122U"
device.connstring = "usb:072f/2200:libusb"
allow_autoscan = true
"""

    system = platform.system()
    if system == "Windows":
        config_path = os.path.expandvars(r"C:\nfc")
    else:
        config_path = "/etc/nfc"

    os.makedirs(config_path, exist_ok=True)
    file_path = os.path.join(config_path, "libnfc.conf")

    try:
        with open(file_path, "w") as file:
            file.write(content)
        print(f"[SUCCESS] Fichier libnfc.conf créé à : {file_path}")
    except PermissionError:
        print(f"[ERROR] Permission refusée. Exécutez en mode administrateur/sudo.")
    except Exception as e:
        print(f"[ERROR] Échec de la création : {e}")

if __name__ == "__main__":
    create_libnfc_conf()
