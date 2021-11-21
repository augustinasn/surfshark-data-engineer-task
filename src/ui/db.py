import streamlit as st

from api.db_client import read_db, show_db_info, init_db

from constants import *


def db_ui(state, name):
    with st.form("old_dbs_form"):
        db_name = st.selectbox("Available databases:", state["available_dbs"])
        show_info_btn = st.form_submit_button("Show info")
        if show_info_btn:
            db = read_db(db_name)
            info = show_db_info(db, db_name)
            st.dataframe(info)
            db.close()

    with st.form("new_db_form"):
        st.write("Initialize a new database (takes a couple of minutes):")
        create_db_btn = st.form_submit_button("Create")
        if create_db_btn:
            db, filename = init_db()
            state["available_dbs"].append(filename)
            st.success(f"Successfully created and saved as \"{filename}\"")
            info = show_db_info(db, filename)
            st.dataframe(info)
            db.close()