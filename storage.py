import json
import os
import hashlib
from encryption import encrypt_data, decrypt_data

# Compute SHA-256 hash of the file's binary content
def get_file_hash(filepath):
    with open(filepath, "rb") as f:
        data = f.read()
    return hashlib.sha256(data).hexdigest()

# Save encrypted password data + its hash
def save_passwords(filepath, key, data):
    # Encrypt the password data (dict -> JSON string -> bytes)
    encrypted_data = encrypt_data(key, json.dumps(data))

    # Write encrypted data to file
    with open(filepath, 'wb') as f:
        f.write(encrypted_data)

    # Save file integrity hash
    with open(filepath + ".hash", "w") as hash_file:
        hash_file.write(get_file_hash(filepath))

# Load encrypted data and verify file integrity
def load_passwords(filepath, key):
    if not os.path.exists(filepath):
        return {}

    # Check if the hash matches
    if os.path.exists(filepath + ".hash"):
        with open(filepath + ".hash", "r") as hash_file:
            expected_hash = hash_file.read()
        actual_hash = get_file_hash(filepath)
        if expected_hash != actual_hash:
            print("WARNING: Password file may have been tampered with.")

    with open(filepath, 'rb') as f:
        encrypted_data = f.read()

    try:
        decrypted_data = decrypt_data(key, encrypted_data)
        return json.loads(decrypted_data)
    except:
        return None  # Indicates failure to decrypt (bad key, wrong password, etc.)
