import os

import streamlit as st

from constants import *
from ui import init_sidebar


def init_state():
    if "available_dbs" not in st.session_state:
        st.session_state["available_dbs"] = os.listdir(DB_FOLDERPATH)
    return st.session_state

def init_ui(state):
    menu = init_sidebar(state)

    return menu

def start_app():
    state = init_state()
    ui = init_ui(state)

if __name__ == "__main__":
    start_app()




