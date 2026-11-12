# Secure Password Manager

A locally stored, encrypted password manager built in Python with a simple Tkinter GUI. Credentials are encrypted on your machine and nothing is ever sent over the network.

## Features

- AES encryption using Fernet from the `cryptography` library
- PBKDF2-HMAC key derivation from your master password and a random salt
- Master password is never stored, only a hash used to verify it
- Built-in password generator and password strength checker
- Auto logout after inactivity
- Temporary lockout after repeated failed login attempts
- SHA-256 integrity check on the encrypted data file

## Project structure

- `main.py` launches the app
- `gui.py` handles the interface and user events
- `encryption.py` handles key derivation and encryption
- `storage.py` handles saving, loading, and file hashing
- `generator.py` generates secure passwords
- `strength_checker.py` evaluates password strength
- `requirements.txt` lists dependencies

## How to run

Requires Python 3.7 or higher with Tkinter.

```bash
git clone https://github.com/godsona-codes/secure-password-manager.git
cd secure-password-manager
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 main.py
```

On first launch you will be asked to create a master password. The app then creates `salt.bin`, `master.hash`, and `passwords.json` locally. These files are listed in `.gitignore` so they never get committed.

## How it works

1. Your master password is hashed and the hash is saved so the app can verify you on later launches.
2. The master password and a random salt are run through PBKDF2 to derive an encryption key.
3. Every saved credential is encrypted with that key before it is written to disk.
4. After 3 failed login attempts the app locks temporarily, and it logs you out after 2 minutes of inactivity.
5. The data file is checked for tampering on each run.

## Notes

This was built as a class project to practice applied cryptography and defensive coding. It is not audited, so do not use it as your only copy of important passwords.
