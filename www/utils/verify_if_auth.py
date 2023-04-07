import streamlit as st
from streamlit_extras.switch_page_button import switch_page

def verify_if_auth():
    if 'jwt' not in st.session_state:
        st.session_state['jwt'] = None
    if st.session_state['jwt'] == None:
        switch_page('login')
