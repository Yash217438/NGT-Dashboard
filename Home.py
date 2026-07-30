import streamlit as st

st.set_page_config(
    page_title="NGT Dashboard",
    layout="wide"
)

if not check_login():
    login()
    st.stop()
    
st.title("NGT Sewage Management Dashboard")

st.markdown("""
### Available Dashboards

- ULB 2023
- ULB 2025
- ULB 2026
""")
