import json
import hashlib
import re
import os

DB_FILE = "users.json"

def load_users():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def register():
    users = load_users()
    print("\n--- Register ---")
    
    username = input("Enter username: ").strip()
    email = input("Enter email: ").strip()
    password = input("Enter password: ").strip()

    # Validation
    if any(u["username"] == username for u in users):
        print("Error: Username already exists!")
        return
    if any(u["email"] == email for u in users):
        print("Error: Email already exists!")
        return
    if not is_valid_email(email):
        print("Error: Invalid email format!")
        return
    if len(password) < 6:
        print("Error: Password must be at least 6 characters!")
        return

    users.append({
        "username": username,
        "email": email,
        "password": hash_password(password)
    })
    save_users(users)
    print("Registration successful!")

def login():
    users = load_users()
    print("\n--- Login ---")
    
    username = input("Enter username/email: ").strip()
    password = input("Enter password: ").strip()
    hashed = hash_password(password)

    for user in users:
        if (user["username"] == username or user["email"] == username) and user["password"] == hashed:
            print(f"Login successful! Welcome {user['username']}")
            return
    print("Error: Invalid credentials!")

def main():
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()