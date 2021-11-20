import streamlit as st

from api.db_client import read_table


def init_state():
    if "is_authentcated" not in st.session_state:
        st.session_state["is_authentcated"] = True

def start_app():
    init_state()

    st.write("hello world!")
    table = read_table("characters")
    st.write(table)

if __name__ == "__main__":
    start_app()




