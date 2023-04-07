import streamlit as st

def disable_sidebar():
    st.set_page_config(initial_sidebar_state="collapsed")

    st.markdown(
        """
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """,
        unsafe_allow_html=True,
    )