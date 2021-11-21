import pandas as pd
import streamlit as st
import requests
import math

from constants import *

def requests_get(url):
    response = requests.get(url)
    return response.json()

@st.cache
def get_soiaf_data(entity):
    output = []
    curr_page = 1

    while True:
        url = f"{SOIAF_ENDPOINT}/{entity}/?page={curr_page}&pageSize={SOIAF_PAGE_SIZE}"
        data = requests_get(url)
        
        if data:
            output += data
            curr_page += 1
        else:
            break
    return output



