import tkinter as tk
from tkinter import simpledialog, messagebox
from encryption import derive_key
from storage import save_passwords, load_passwords
from generator import generate_password
from strength_checker import check_strength
import os
import base64
import hashlib


class PasswordManagerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Secure Password Manager")
        self.filepath = "passwords.json"
        self.salt_path = "salt.bin"
        self.password_data = {}
        self.attempts = 0
        self.locked = False
        print("[INIT] self.locked initialized")
        print("[INIT] self is:", self)

        self.setup_login_screen()

    def setup_login_screen(self):
        self.clear_window()

        label = tk.Label(self.master, text="Enter Master Password:")
        label.pack()

        self.master_password_entry = tk.Entry(self.master, show='*')
        self.master_password_entry.pack()

        login_button = tk.Button(self.master, text="Login", command=self.verify_master_password)
        login_button.pack()

    def verify_master_password(self):
        print("[VERIFY] Checking self.locked")
        print("[VERIFY] self.locked = ", getattr(self, "locked", "NOT FOUND"))
        print("[VERIFY] self is:", self)

        if self.locked:

            messagebox.showwarning("Locked", "Too many failed attempts. Try again later.")
            return

        password = self.master_password_entry.get()

        # Load or generate salt
        if os.path.exists(self.salt_path):
            with open(self.salt_path, "rb") as f:
                salt = f.read()
        else:
            salt = os.urandom(16)
            with open(self.salt_path, "wb") as f:
                f.write(salt)

        # Derive encryption key from password and salt
        self.key = derive_key(password, salt)

        # Hash the master password
        def hash_password(pwd):
            import hashlib
            return hashlib.sha256(pwd.encode()).hexdigest()

        # Store hashed password if it doesn't exist
        if not os.path.exists("master.hash"):
            with open("master.hash", "w") as f:
                f.write(hash_password(password))
        else:
            with open("master.hash", "r") as f:
                stored_hash = f.read()
            if hash_password(password) != stored_hash:
                self.attempts += 1
                if self.attempts >= 3:
                    self.locked = True
                    self.master.after(30000, self.unlock)  # 30-second lockout
                    messagebox.showwarning("Locked", "Too many failed attempts. Locked for 30 seconds.")
                else:
                    messagebox.showerror("Error", "Incorrect master password!")
                return

        # Load data and go to main screen
        self.password_data = load_passwords(self.filepath, self.key)
        self.setup_main_screen()




    def setup_main_screen(self):
        self.clear_window()

        tk.Label(self.master, text="Website:").pack()
        self.website_entry = tk.Entry(self.master)
        self.website_entry.pack()

        tk.Label(self.master, text="Username:").pack()
        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack()

        tk.Label(self.master, text="Password:").pack()
        self.password_entry = tk.Entry(self.master)
        self.password_entry.pack()

        tk.Button(self.master, text="Check Strength", command=self.check_strength).pack()
        tk.Button(self.master, text="Generate Password", command=self.generate_new_password).pack()
        tk.Button(self.master, text="Save Password", command=self.save_entry).pack()
        tk.Button(self.master, text="Retrieve Password", command=self.retrieve_entry).pack()

    def generate_new_password(self):
        password = generate_password()
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

        self.reset_timer()


    def check_strength(self):
        pwd = self.password_entry.get()
        strength = check_strength(pwd)
        messagebox.showinfo("Password Strength", f"Strength: {strength}")

        self.reset_timer()


    def save_entry(self):
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if website and username and password:
            self.password_data[website] = {"username": username, "password": password}
            save_passwords(self.filepath, self.key, self.password_data)
            messagebox.showinfo("Saved", "Password saved successfully.")
        else:
            messagebox.showwarning("Error", "Please fill in all fields.")
        
        self.reset_timer()


    def retrieve_entry(self):
        website = self.website_entry.get()
        entry = self.password_data.get(website)

        if entry:
            self.username_entry.delete(0, tk.END)
            self.username_entry.insert(0, entry['username'])
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, entry['password'])
        else:
            messagebox.showwarning("Not found", "No password saved for this site.")

        self.reset_timer()


    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def unlock(self):
        self.attempts = 0
        self.locked = False

    def reset_timer(self):
        if hasattr(self, 'logout_timer'):
            self.master.after_cancel(self.logout_timer)
        self.logout_timer = self.master.after(120000, self.logout)  # 2 minutes

    def logout(self):
        messagebox.showinfo("Auto Logout", "You’ve been logged out for inactivity.")
        self.setup_login_screen()


        
