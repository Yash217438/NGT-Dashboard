import streamlit as st
import pandas as pd


def login():

    users = pd.read_excel(
        "Security/users.xlsx",
        engine="openpyxl"
    )

    st.title("NGT Dashboard Login")

    username = st.text_input("Username")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        user = users[
            (users["Username"] == username)
            &
            (users["Password"] == password)
        ]

        if len(user) == 1:

            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["role"] = user.iloc[0]["Role"]

            st.rerun()

        else:
            st.error("Invalid Username or Password")


def check_login():

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    return st.session_state["logged_in"]
