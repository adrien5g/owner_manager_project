import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import disable_sidebar
from utils import make_request

disable_sidebar()

class Login:

    def __init__(self) -> None:
        self.st = st

    def drawn(self) -> None:
        self.st.markdown(
            '''
            # Car Owner System
            ## Login
            '''
        )
        self.username = self.st.text_input('Login')
        self.password = self.st.text_input('Password', type='password')
        if self.st.button('Login'):
            self.login()

    def login(self) -> None:
        data = {
            'username': self.username,
            'password': self.password
        }
        status_code, response = make_request('user/login', type='post', body=data, auth=False)
        if status_code == 200:
            self.st.session_state['jwt'] = f'Bearer {response["access_token"]}'
            switch_page('home')
        else:
            try:
                self.st.error(response['status'])
            except KeyError:
                self.st.error('Offline API')

login = Login()
login.drawn()