import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import disable_sidebar, verify_if_auth

class BasePage:

    def __init__(self, disable_home_button: bool = False) -> None:
        disable_sidebar()
        verify_if_auth()
        if not disable_home_button:
            if st.button('Back to home'):
                switch_page('home')