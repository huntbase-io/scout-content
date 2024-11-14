from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import os

# Load the private key
with open('private_key.pem', 'rb') as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

def sign_file(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
    signature = private_key.sign(content, padding.PKCS1v15(), hashes.SHA256())
    signature_path = f"{file_path}.sig"
    with open(signature_path, 'wb') as sig_file:
        sig_file.write(signature)
    print(f"Signed {file_path}, signature saved to {signature_path}")

# Sign all files in scripts and bin directories
for dir_path in ['scripts', 'bin']:
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            sign_file(file_path)
