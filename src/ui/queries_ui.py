import streamlit as st
import pandas as pd

from api.db_client import total_count_of_each_entity, books_and_characters, character_names_and_played_by, houses_info
from api.pandas_client import df_to_html_table

def queries_ui(state, menu):
    with st.form("select_db_form"):
        queries = {"Total count of each entity": total_count_of_each_entity,
                   "List of all book names, authors, release dates and character names, genders and titles mentioned in the book": books_and_characters,
                   "List of all character names and played by actor names.": character_names_and_played_by,
                   "List of all house names, regions, overlord names and sworn member names.": houses_info}

        db_name = st.selectbox("Select from available databases:", state["available_dbs"])
        query = st.selectbox("Select from available queries:", queries)

        select_db_query_btn = st.form_submit_button("Select DB and query")

        if select_db_query_btn:
            function = queries[query]
            output, sql_query = function(db_name)

            st.write("Query:")
            st.code(sql_query)

            st.write("Result:")
            
            if query in [list(queries.keys())[1], list(queries.keys())[3]]:
                st.markdown(df_to_html_table(output), unsafe_allow_html=True)
            st.dataframe(output)
            
