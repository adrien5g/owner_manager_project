from typing import Dict, List
import streamlit as st
from time import sleep

from streamlit_extras.switch_page_button import switch_page

from libs.page import BasePage
from utils import make_request

class RegisterCar(BasePage):

    def __init__(self) -> None:
        super().__init__()
        self.st = st
        self.disable_button = False

    def __get_car_options(self) -> Dict[str, list]:
        _, colors = make_request('/car/get_colors')
        _, types = make_request('/car/get_types')
        data = {
            'types': types['car_types'],
            'colors': colors['car_colors']
        }
        return data
    
    def __get_owners(self) -> List[str]:
        _, owners = make_request('/owner/get_all')
        emails = [owner['email'] for owner in owners['owners'] if owner['cars'] < 3]
        return emails
    
    def drawn(self):
        self.st.title('Register new car')

        car_options = self.__get_car_options()
        owners = self.__get_owners()
        
        col1, col2 = st.columns(2)
    
        color = col1.selectbox('Color', car_options['colors'])
        type = col2.selectbox('Type', car_options['types'])
        owner = self.st.selectbox('Owner', owners)

        if owner == None:
            self.disable_button = True

        placeholder = self.st.empty()

        if placeholder.button(
            'Register car', type='primary', disabled=self.disable_button, key=1
        ):
            placeholder.button('Register car', type='primary', disabled=True, key=2)
            if owner == None:
                owner = ''
            data = {
                'car_color': color,
                'car_type': type,
                'owner_email': owner
            }
            status_code, data = make_request('car/register', body=data, type='post')
            if status_code == 200:
                st.success('Car registered!', icon='✅')
                sleep(1.5)
                switch_page('home')
            else:
                st.error(data['status'], icon='🛑')

register_car = RegisterCar()
register_car.drawn()