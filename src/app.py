import streamlit as st

from api.data_acquisition import get_soiaf_data

st.write("hello world!")

chars = get_soiaf_data(entity="characters", qty=100)

st.write(chars)
