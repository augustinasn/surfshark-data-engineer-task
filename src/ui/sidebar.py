import streamlit as st

from constants import *

from .intro_ui import intro_ui
from .db_ui import db_ui
from .queries_ui import queries_ui

def init_sidebar(state):

    st.set_page_config(page_title=PAGE_TITLE,
                       layout = "wide",
                       initial_sidebar_state = "auto")

    menu_options = {"Introduction": intro_ui,
                    "Data acquisition & DB Model": intro_ui, 
                    "Init/remove DBs": db_ui,
                    "DB Queries": queries_ui,
                    "DB init scheduler": intro_ui}
                    
    header = st.sidebar.markdown(f"**{PAGE_TITLE}**")
    menu = st.sidebar.selectbox("Select menu option:", menu_options.keys())

    st.write(f"{menu}:")
    menu_options[menu](state, menu)
    
    return menu