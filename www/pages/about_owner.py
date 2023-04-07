from time import sleep
from itertools import cycle

import streamlit as st

from libs.page import BasePage
from utils import make_request
from components import CarCard
from streamlit_extras.switch_page_button import switch_page

class AboutOwner(BasePage):

    def __init__(self) -> None:
        super().__init__()
        self.st = st
        if 'owner' in self.st.session_state:
            owner = self.st.session_state['owner']
        else:
            switch_page('home')
        status_code, data = make_request(f'/owner/about/{owner}')

        if status_code == 200:
            self.data = {
                'name': data['name'],
                'email': data['email'],
                'cars': data['cars']
            }
        else:
            self.st.error(data['status'])
            sleep(1.5)
            switch_page('home')

    def drawn(self):
        st.title('Owner information')
        st.markdown(
            f'''
            #### 👤 Name: {self.data['name']}
            #### ✉️ Email: {self.data['email']}
            '''
        )
        self.st.markdown('---')
        if len(self.data['cars']) == 0:
            return st.subheader('No car found')
        st.subheader('List of cars')
        key = 0
        cols = cycle(self.st.columns(3))
        for car in self.data['cars']:
            col = next(cols)
            card_car = CarCard(**car, key=key, layout=col)
            card_car.drawn()
            key += 1

about_owner = AboutOwner()
about_owner.drawn()