import base64
import os

FILE = "encrypted_data.txt"

def encrypt(text, shift=3):
    shifted = ''.join(chr((ord(c) + shift) % 256) for c in text)
    encoded = base64.b64encode(shifted.encode()).decode()
    return encoded

def decrypt(text, shift=3):
    try:
        decoded = base64.b64decode(text).decode()
        original = ''.join(chr((ord(c) - shift) % 256) for c in decoded)
        return original
    except:
        return "Error: Invalid encrypted data!"

def save_to_file(data):
    with open(FILE, "w") as f:
        f.write(data)
    print(f"Saved to {FILE}")

def load_from_file():
    if not os.path.exists(FILE):
        print("No file found!")
        return None
    with open(FILE, "r") as f:
        return f.read().strip()

def main():
    while True:
        print("\n1. Encrypt Data\n2. Decrypt Data\n3. Save to File\n4. Load & Decrypt\n5. Exit")
        choice = input("Choose: ")
        
        if choice == "1":
            text = input("Enter text to encrypt: ")
            encrypted = encrypt(text)
            print(f"Encrypted: {encrypted}")
        
        elif choice == "2":
            text = input("Enter text to decrypt: ")
            decrypted = decrypt(text)
            print(f"Decrypted: {decrypted}")
        
        elif choice == "3":
            data = input("Enter encrypted text to save: ")
            save_to_file(data)
        
        elif choice == "4":
            data = load_from_file()
            if data:
                print(f"Loaded: {data}")
                print(f"Decrypted: {decrypt(data)}")
        
        elif choice == "5":
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()