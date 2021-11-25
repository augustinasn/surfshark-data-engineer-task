import streamlit as st

from constants import *


def data_model_ui(state, name):
    st.image(MODEL_FILEPATH)
    st.write('''Data is fetched from the API using requests library.
                Because of items per page limit, application requires to make multiple queries.
                Above you can see a data model used for storing this data in the SQLite DB.''')