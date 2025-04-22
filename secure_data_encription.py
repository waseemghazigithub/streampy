import streamlit as st
import hashlib
from cryptography.fernet import Fernet

# ✅ Fixed Key (don't regenerate every time!)

KEY = b'qW7oMAdKo7GQBAFnrTYqepdCECVL3kRGXYnlIO3D4BQ='  # You can generate yours using Fernet.generate_key()
cipher = Fernet(KEY)

# ✅ Use session_state for memory storage
if 'stored_data' not in st.session_state:
    st.session_state.stored_data = {}

if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = 0

# 🔐 Helper Functions
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()

def decrypt_data(encrypted_text, passkey):
    hashed_passkey = hash_passkey(passkey)
    value = st.session_state.stored_data.get(encrypted_text)

    if value and value["passkey"] == hashed_passkey:
        st.session_state.failed_attempts = 0
        return cipher.decrypt(encrypted_text.encode()).decode()
    else:
        st.session_state.failed_attempts += 1
        return None

# 🔐 Encrypt Section
st.title("🔐 Encrypt & Decrypt Data")

with st.expander("📝 Encrypt Data"):
    data = st.text_area("Enter Data to Encrypt")
    passkey = st.text_input("Enter Passkey", type="password")

    if st.button("Encrypt"):
        if data and passkey:
            encrypted = encrypt_data(data)
            hashed = hash_passkey(passkey)

            st.session_state.stored_data[encrypted] = {
                "passkey": hashed
            }

            st.success("✅ Data Encrypted and Stored")
            st.code(encrypted, language="text")
        else:
            st.error("Please fill in all fields.")

# 🔓 Decrypt Section
with st.expander("🔍 Decrypt Data"):
    encrypted_input = st.text_area("Paste Encrypted Text").strip()
    decrypt_passkey = st.text_input("Enter Passkey", type="password", key="decrypt")

    if st.button("Decrypt"):
        if encrypted_input and decrypt_passkey:
            result = decrypt_data(encrypted_input, decrypt_passkey)

            if result:
                st.success(f"🔓 Decrypted Text: {result}")
            else:
                left = 3 - st.session_state.failed_attempts
                st.error(f"❌ Incorrect passkey! Attempts left: {left}")
                if left <= 0:
                    st.warning("🔒 Locked out. Please re-login.")
        else:
            st.error("Please enter both fields.")
