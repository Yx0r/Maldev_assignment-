# ransomware_decryptor.py
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

KEY = b'0123456789abcdef0123456789abcdef'
IV  = b'0123456789abcdef'

def decrypt_file(encrypted_path):
    try:
        with open(encrypted_path, 'rb') as f:
            ciphertext = f.read()
        cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_plain = decryptor.update(ciphertext) + decryptor.finalize()
        # Remove PKCS7 padding
        pad_len = padded_plain[-1]
        plaintext = padded_plain[:-pad_len]
        original_path = encrypted_path[:-10]  # remove '.encrypted'
        with open(original_path, 'wb') as f:
            f.write(plaintext)
        os.remove(encrypted_path)
        return True
    except Exception:
        return False

def main():
    current_dir = os.getcwd()
    decrypted = 0
    for filename in os.listdir(current_dir):
        if filename.endswith('.encrypted'):
            if decrypt_file(os.path.join(current_dir, filename)):
                decrypted += 1
    if decrypted > 0:
        print(f"Successfully decrypted {decrypted} file(s).")
    else:
        print("No encrypted files found.")

if __name__ == "__main__":
    main()
