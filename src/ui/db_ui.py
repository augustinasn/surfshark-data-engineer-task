import streamlit as st

from constants import *
from api.db_client import total_count_of_each_entity, init_db, delete_db, get_list_of_dbs


def db_ui(state, name):
    with st.form("old_dbs_form"):
        db_name = st.selectbox("Available databases:", state.get("available_dbs", ["-"]))
        show_info_btn = st.form_submit_button("Show info")
        delete_db_btn = st.form_submit_button("Delete this DB")

        if show_info_btn:
            info_df, _ = total_count_of_each_entity(db_name)
            st.write(f"Creation date: {db_name.split('_')[1]}, {db_name.split('_')[2][:2]}:{db_name.split('_')[2][2:5]}")
            st.dataframe(info_df)

        if delete_db_btn:
            delete_db(db_name)
            state["available_dbs"].remove(db_name)
            st.success(f"Successfully deleted \"{db_name}\", it's best to refresh the page now.")


    with st.form("new_db_form"):
        st.write("Initialize a new database (takes a couple of minutes):")
        create_db_btn = st.form_submit_button("Create")
        if create_db_btn:
            filename = init_db()
            state["available_dbs"].append(filename)
            st.success(f"Successfully created and saved as \"{filename}\", it's best to refresh the page now.")
            info_df, _ = total_count_of_each_entity(filename)
            st.dataframe(info_df)