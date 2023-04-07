from itertools import cycle
from typing import List

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from utils import make_request
from components import OwnerCard
from libs.page import BasePage

class Home(BasePage):

    def __init__(self) -> None:
        super().__init__(True)
        self.st = st

    def drawn(self) -> None:
        self.st.button('Logout', on_click=lambda: self.__logout())
        self.st.title('General info')

        st.markdown(f'##### 👥 Owners on system - {self.__get_owners_count()}')
        st.markdown(f'##### 🚙 Cars on system - {self.__get_cars_count()}')
        
        cols = st.columns(5)
        with cols[0]:
            if self.st.button('Register owner', type='primary'):
                switch_page('register_owner')
        with cols[1]:
            if self.st.button('Register car'):
                switch_page('register_car')

        filter = self.st.checkbox('Filter by "Sale Oportunity"')
        self.st.markdown('---')
        data = self.__get_cards_info(filter)
        if isinstance(data, list):
            if len(data) == 0:
                st.subheader('No owners found')
                return
            st.subheader('List of owners')
            cols = cycle(self.st.columns(3))
            key = 0
            for card in data:
                col = next(cols)
                card = OwnerCard(**card, key=key, layout=col)
                card.drawn()
                key += 2
        else:
            self.st.error(data)
        
    def __get_cards_info(self, filter: bool) -> List[dict]:
        filter = 'true' if filter else 'false'
        url = f'owner/get_all?sale_opportunity={filter}'
        status_code, data = make_request(url)
        if status_code == 200:
            return data['owners']
        else:
            if 'status' in data:
                return data['status']
            else:
                return 'Offline API'

    def __get_cars_count(self) -> int | str:
        status_code, data = make_request('car/count')
        if status_code == 200:
            return data['car_count']
        else:
            'Error on get'

    def __get_owners_count(self) -> int | str:
        status_code, data = make_request('owner/count')
        if status_code == 200:
            return data['owner_count']
        else:
            'Error on get'

    def __logout(self) -> None:
        st.session_state['jwt'] = None

home = Home()
home.drawn()
