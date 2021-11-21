import streamlit as st

from constants import *

from .intro import intro_ui
from .db import db_ui
from .queries import queries_ui

def init_sidebar(state):

    st.set_page_config(page_title=PAGE_TITLE,
                       layout = "wide",
                       initial_sidebar_state = "auto")

    menu_options = {"Intro": intro_ui,
                    "DB Model": intro_ui, 
                    "Create DB": db_ui,
                    "DB Queries": queries_ui,
                    "Scheduler": intro_ui}
                    
    header = st.sidebar.markdown(f"**{PAGE_TITLE}**")
    menu = st.sidebar.selectbox("Select menu option:", menu_options.keys())

    st.write(f"{menu}:")
    menu_options[menu](state, menu)
    
    return menu