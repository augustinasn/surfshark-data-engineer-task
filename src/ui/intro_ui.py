import streamlit as st


def intro_ui(state, name):
    with open("README.md") as fh:
        st.markdown(fh.read())