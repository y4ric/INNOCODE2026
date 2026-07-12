import streamlit as st
from streamlit import session_state

st.title("""Регистрация""")

if "login" not in session_state:
    session_state["login"] = ""

if "psw" not in session_state:
    session_state["psw"] = ""

st.subheader("Логин")
login = st.text_input("Логин", value=session_state["login"], placeholder="Введите логин...")

st.subheader("Пароль")
psw = st.text_input("Пароль", value=session_state["psw"], placeholder="Введите пароль...")

if st.button("Другая страница"):
    st.switch_page("Frontend/views/another.py")

st.text(f"Ваш пароль: {psw}")
st.text(f"Ваше Имя: {login}")

st.session_state["login"] = login
st.session_state["psw"] = psw
