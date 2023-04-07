import os

import streamlit as st
import requests
from typing import Any, Dict, Literal, Tuple

def make_request(
    endpoint: str,base_url: str = 'http://localhost:5000',
    type: Literal['get', 'post', 'delete'] = 'get',
    body: Dict[str, Any] = {}, headers: Dict[str, Any] = {},
    auth: bool = True
) -> Tuple[int, Dict]:
    url = os.getenv('API_URL')
    if not url == None:
        base_url = url
    request = getattr(requests, type)
    if auth:
        jwt = st.session_state['jwt']
        headers['Authorization'] = jwt
    try:
        data = request(f'{base_url}/{endpoint}', json=body, headers=headers)
    except:
        return(None, {})

    status_code = data.status_code
    return (status_code, data.json())
    