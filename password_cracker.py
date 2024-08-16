import hashlib
import itertools
import string
import os
# NOTE: DO not use for illegal purposes. ONly allowed to obtain hash LEGALLY and with PERMISSION
# YOu can test on your own devices not others.
# This is simply a simple one and a brute force one at that, so it isn't good but is still dangerous.

def hash_password(password):
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def load_dictionary(file_path):
    """Loads a list of common passwords from a file."""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def dictionary_attack(hash_to_crack, dictionary):
    """Tries to find the password by comparing its hash against a list of hashes."""
    for password in dictionary:
        if hash_password(password) == hash_to_crack:
            return password
    return "Password not found."

def brute_force_attack(hash_to_crack, max_length=8):
    """Generates all possible combinations of characters up to 'max_length' to find the password."""
    chars = string.ascii_lowercase + string.digits + string.punctuation
    for length in range(1, max_length + 1):
        for password in itertools.product(chars, repeat=length):
            if hash_password(''.join(password)) == hash_to_crack:
                return ''.join(password)
    return "Password not found."

def get_user_hash(username):
    """ Retrieves the password hash for a specified user from /etc/shadow (Linux/Unix only) """
    try:
        with open("/etc/shadow", 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith(username + ':'):
                    return line.split(':')[1].split('$')[2]  # Extracting the actual hash part
    except PermissionError:
        return "You need root privileges to access password hashes."

# Example usage for password cracking (I randomly came up with a  password)
password_to_test = "b1gman!"
password_hash = hash_password(password_to_test)
print(f"Trying to crack hash of '{password_to_test}': {password_hash}")

dictionary = load_dictionary("passwords.txt") # Draws from text
cracked_password = dictionary_attack(password_hash, dictionary)

if cracked_password == "Password not found.":
    cracked_password = brute_force_attack(password_hash, max_length=8) 

print(f"Cracked Password: {cracked_password}")

# Example usage for hash retrieval (educational purposes on your own Linux system, in my case I would do this on my kali)
username = 'your_username'  # Replace with your actual username
user_password_hash = get_user_hash(username)
print(f"Hash for {username}: {user_password_hash}")
