import uuid
from time import sleep
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from streamlit_extras.switch_page_button import switch_page

from utils import make_request

class CarCard:

    def __init__(
            self, color: str, type: str, uuid: str, 
            key: int, layout: DeltaGenerator | None = None
    ) -> None:
        self.color = color
        self.type = type
        self.uuid = uuid
        self.key = key
        self.st = layout

    def drawn(self):
        if not self.st:
            self.st = st
        container = self.st.container()
        container.markdown('---')
        container.text(f'🎨 - {self.color}')
        container.text(f'🚘 - {self.type}')
        container.text(f'🪧 - {self.uuid[:8]}')
        if container.button('Delete', key=self.key, type='primary'):
            self.__delete_car()

    def __delete_car(self):
        status_code, data = make_request(f'car/delete/{self.uuid}', type='delete')
        if status_code == 200:
            self.st.success('Car deleted!')
            sleep(1.5)
            switch_page('about_owner')
        else:
            self.st.error(data['status'])
