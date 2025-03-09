import re
import streamlit as st
import random
import string

def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(length))

def evaluate_password(password):
    score = 0
    feedback = []
    
    # Blacklist common passwords
    common_passwords = {"password123", "12345678", "qwerty", "letmein", "welcome", "admin", "12345", "passw0rd"}
    if password.lower() in common_passwords:
        return "🔴❌ Weak", 0, ["This password is too common. Choose a more unique one."], 0.1
    
    # Custom scoring weights
    length_weight = 2 if len(password) >= 12 else 1 if len(password) >= 8 else 0
    lower_weight = 1 if re.search(r'[a-z]', password) else 0
    upper_weight = 1 if re.search(r'[A-Z]', password) else 0
    digit_weight = 1 if re.search(r'\d', password) else 0
    special_weight = 2 if re.search(r'[!@#$%^&*]', password) else 0
    repeat_penalty = -1 if re.search(r'(.)\1{2,}', password) else 0  # Penalize repeating characters
    
    score = length_weight + lower_weight + upper_weight + digit_weight + special_weight + repeat_penalty
    strength_ratio = max(0.1, min(score / 6, 1.0))  # Ensure progress bar is never fully empty
    
    # Provide feedback
    if length_weight == 0:
        feedback.append("Increase the length to at least 8 characters. 🔢")
    if lower_weight == 0:
        feedback.append("Include lowercase letters. 🔡")
    if upper_weight == 0:
        feedback.append("Include uppercase letters. 🔠")
    if digit_weight == 0:
        feedback.append("Include at least one number (0-9). 🔢")
    if special_weight == 0:
        feedback.append("Include at least one special character (!@#$%^&*). ✨")
    if repeat_penalty == -1:
        feedback.append("Avoid using repeating characters (e.g., 'aaa', '111'). ❌")

    # Check for common patterns
    if re.search(r'(123|password|qwerty|abc)', password, re.IGNORECASE):
        score -= 1
        feedback.append("Avoid common patterns like '123', 'password', or 'qwerty'. 🚫")

    # Determine strength level
    if score >= 6:
        strength = "🟢✅ Strong"
    elif score >= 3:
        strength = "🟠⚠️ Moderate"
    else:
        strength = "🔴❌ Weak"
    
    return strength, score, feedback, strength_ratio

# Streamlit UI
st.title("🔐 Password Strength Meter")
password = st.text_input("Enter a password to check its strength:", type="password")

# Ensure strength_ratio is always defined
strength_ratio = 0.1  # Default when no password is entered

if password:
    strength, score, feedback, strength_ratio = evaluate_password(password)
    st.subheader(f"Password Strength: {strength} (Score: {score})")
    
    if "Strong" in strength:
        st.success("✅ Great job! Your password is strong and secure.")
    else:
        st.warning("⚠️ Your password could be improved. Consider the following suggestions:")
        for tip in feedback:
            st.write(f"- {tip}")

if st.button("🔄 Generate a Strong Password"):
    strong_password = generate_strong_password()
    st.text(f"🔑 Suggested Strong Password: {strong_password}")

# Additional Feature: Password Visibility Toggle
show_password = st.checkbox("👁 Show Generated Password")
if show_password and 'strong_password' in locals():
    st.text(strong_password)

# Additional Feature: Password Strength Bar
st.write("### 📊 Password Strength Indicator")
st.progress(strength_ratio)

