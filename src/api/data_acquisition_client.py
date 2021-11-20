import pandas as pd
import requests
import math

from constants import *

def requests_get(url):
    response = requests.get(url)
    return response.json()

def get_soiaf_data(entity):
    # Entities = ['characters', 'books', 'houses']
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



