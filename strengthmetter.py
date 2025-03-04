import streamlit as st
import re

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
    
    return strength, feedback

# Streamlit UI
st.title("🔒 Password Strength Meter")
st.write("Enter a password to check its strength and get improvement suggestions.")

password = st.text_input("Enter Password", type="password")
if password:
    strength, feedback = calculate_strength(password)
    
    st.subheader(f"Password Strength: {strength}")
    
    if feedback:
        st.warning("\n".join(feedback))
    else:
        st.success("Your password is strong!")
