import streamlit_authenticator as stauth

hashed_passwords = stauth.Hasher(['Capstone2023%']).generate()

print(hashed_passwords)