import streamlit_authenticator as stauth

# Generate password hashes using bcrypt directly
import bcrypt

passwords = {'demo123': 'demo123', 'admin123': 'admin123'}

print("Generating password hashes...")
for label, password in passwords.items():
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    print(f"{label}: {hashed}")
