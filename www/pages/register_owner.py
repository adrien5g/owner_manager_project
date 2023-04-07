import streamlit as st
from time import sleep

from streamlit_extras.switch_page_button import switch_page

from libs.page import BasePage
from utils import make_request

class RegisterOwner(BasePage):

    def __init__(self) -> None:
        super().__init__()
        self.st = st

    def drawn(self):
        self.st.title('Register new owner')
        name = self.st.text_input('Name')
        email = self.st.text_input('Email')

        placeholder = self.st.empty()

        if placeholder.button('Register', type='primary', key=1):
            placeholder.button('Register', type='primary', key=2, disabled=True)
            data = {
                'email': email,
                'name': name 
            }
            status_code, response = make_request(
                'owner/register', body=data, type='post'
            )
            if status_code == 200:
                st.success('Owner registered!', icon='✅')
                sleep(1.5)
                switch_page('home')
            else:
                st.error(response['status'], icon='🛑')
                sleep(1.5)
                st.experimental_rerun()

register_owner = RegisterOwner()
register_owner.drawn()