import pandas as pd
import streamlit as st


def query_to_df(query):
    cols = [column[0] for column in query.description]
    df = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
    return df

def df_to_html_table(df):
    return df.to_html().replace("\\n","<br>")

@st.cache
def fetch_col_val_by_url(df, url, col):
    row = df.loc[df["url"] == url]
    if not row.empty:
        return row.iloc[0][col]
    else:
        return " - "

@st.cache
def replace_urls_with_col_vals(urls, df, cols):
    output = ""
    CACHE = {}

    for url in urls.split(";"):
        if url in CACHE.keys():
            output += CACHE[url]
            continue

        col_vals = ""

        for col in cols:
            col_val = fetch_col_val_by_url(df, url, col)
            col_vals += f"{col}: {col_val}\\n"
            
        output += f"{col_vals}\\n"
        CACHE[url] = f"{col_vals}\\n"

    return output