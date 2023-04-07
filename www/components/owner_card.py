from time import sleep
from uuid import uuid4

import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from streamlit_extras.switch_page_button import switch_page
from utils import make_request

class OwnerCard:

    def __init__(
            self, name: str, email: str, cars: str, situation: str, 
            key: int, layout: DeltaGenerator | None = None
    ) -> None:
        self.name = name
        self.email = email
        self.cars = cars
        self.situation = situation
        self.key = key
        self.st = layout

    def drawn(self):
        if not self.st:
            self.st = st
        container = self.st.container()
        container.markdown('---')
        container.text(f'👤 - {self.name}')
        container.text(f'✉️ - {self.email}')
        container.text(f'🚗 - {self.cars}')
        container.text(f'🪪 - {self.situation}')
        col1, col2 = container.columns(2)
        if col1.button('About', key=self.key):
            st.session_state['owner'] = self.email
            switch_page('about_owner')
        if col2.button('Delete', type='primary', key=self.key+1):
            status_code, data = make_request(
                f'owner/delete/{self.email}', type='delete'
            )
            if status_code == 200:
                st.success('Owner deleted')
                sleep(1.5)
                switch_page('home')
            else:
                st.error(data['status'])
        

