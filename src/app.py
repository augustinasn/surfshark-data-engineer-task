import os

import streamlit as st

from constants import *
from ui.sidebar import init_sidebar
from api.db_client import get_list_of_dbs


def init_state():
    if "available_dbs" not in st.session_state:
        st.session_state["available_dbs"] = get_list_of_dbs()
    return st.session_state

def init_ui(state):
    menu = init_sidebar(state)
    return menu

def start_app():
    state = init_state()
    return state, init_ui(state)

if __name__ == "__main__":
    state, ui = start_app()




