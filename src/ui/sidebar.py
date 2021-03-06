import streamlit as st

from constants import *

from .intro_ui import intro_ui
from .db_ui import db_ui
from .queries_ui import queries_ui
from .scheduler_ui import scheduler_ui
from .data_model_ui import data_model_ui

def init_sidebar(state):

    st.set_page_config(page_title=PAGE_TITLE,
                       layout = "wide",
                       initial_sidebar_state = "auto")

    menu_options = {"Introduction": intro_ui,
                    "Model": data_model_ui, 
                    "Init/remove": db_ui,
                    "Queries": queries_ui,
                    "Init scheduler": scheduler_ui}
                    
    header = st.sidebar.markdown(f"**{PAGE_TITLE}**")
    menu = st.sidebar.selectbox("Select menu option:", menu_options.keys())
    fyi = st.sidebar.write("If menu stops working - try refreshing the page with F5.")

    st.write(f"**{menu}**:")
    menu_options[menu](state, menu)

    
    
    return menu