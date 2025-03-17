import streamlit as st
import re
import hashlib
import json
import os

# File to store password history
HISTORY_FILE = "password_history.json"

# Load password history
def load_password_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    return []

# Save password history
def save_password_history(history):
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file)

# Hash password for security (so we don’t store plain text passwords)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Check if password was used before
def is_password_reused(password, history):
    hashed_password = hash_password(password)
    return hashed_password in history

# Update password history
def update_password_history(password, history):
    hashed_password = hash_password(password)
    if len(history) >= 10:
        history.pop(0)  # Remove oldest password
    history.append(hashed_password)
    save_password_history(history)

def calculate_strength(password):
    score = 0
    feedback = []
    
    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long.")
    
    # Upper and Lowercase Check
    if any(c.islower() for c in password) and any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("Use both uppercase and lowercase letters.")
    
    # Digit Check
    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("Include at least one number.")
    
    # Special Character Check
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("Use at least one special character (!@#$%^&* etc.).")
    
    # Consecutive Characters Check
    if re.search(r'(.)\1\1', password):
        feedback.append("Avoid consecutive repeating characters.")
    
    # Determine Strength
    if score <= 1:
        strength = "Weak"
    elif score == 2:
        strength = "Moderate"
    else:
        strength = "Strong"
    
    return strength, feedback, score

# Streamlit UI
st.title("🔒 Password Strength Meter")
st.write("Enter a password to check its strength and get improvement suggestions.")

password = st.text_input("Enter Password", type="password")

if password:
    history = load_password_history()

    if is_password_reused(password, history):
        st.error("❌ This password was used in the last 10 entries. Choose a different one!")
    else:
        strength, feedback, score = calculate_strength(password)
        
        st.subheader(f"Password Strength: {strength}")
        
        # Strength Bar
        st.progress(score / 4)  # Normalizing score to range 0-1
        
        if feedback:
            st.warning("\n".join(feedback))
        else:
            st.success("Your password is strong!")
        
        # Update password history
        update_password_history(password, history)
