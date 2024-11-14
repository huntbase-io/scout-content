from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import os
import hashlib

# Load the private key
with open('private_key.pem', 'rb') as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

def file_checksum(file_path):
    """Calculate the SHA256 checksum of a file."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        hasher.update(f.read())
    return hasher.hexdigest()

def sign_file(file_path):
    signature_path = f"{file_path}.sig"

    # Check if the .sig file already exists
    if os.path.exists(signature_path):
        # Calculate the current checksum of the file
        original_checksum = file_checksum(file_path)
        # Read the signature file checksum if stored
        with open(signature_path, 'rb') as sig_file:
            existing_signature = sig_file.read()
            existing_signature_checksum = hashlib.sha256(existing_signature).hexdigest()

        # If the checksum matches, skip signing
        if original_checksum == existing_signature_checksum:
            print(f"Skipping {file_path}, signature already up to date.")
            return
        else:
            print(f"Overwriting signature for {file_path}, file has been modified.")

    # Sign the file
    with open(file_path, 'rb') as f:
        content = f.read()
    signature = private_key.sign(content, padding.PKCS1v15(), hashes.SHA256())

    # Write the signature to a file
    with open(signature_path, 'wb') as sig_file:
        sig_file.write(signature)

    print(f"Signed {file_path}, signature saved to {signature_path}")

# Sign all files in scripts and bin directories
for dir_path in ['scripts', 'bin']:
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if not file.endswith('.sig'):  # Ensure we don't attempt to sign existing .sig files
                file_path = os.path.join(root, file)
                sign_file(file_path)