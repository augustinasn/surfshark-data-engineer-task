import pandas as pd
import requests
import math

from environment import SOIAF_ENDPOINT, SOIAF_PAGE_SIZE

def requests_get(url):
    response = requests.get(url)
    return response.json()

def get_soiaf_data(entity, qty=False, id_=False):
    if qty:
        output = []
        page_from = 1
        page_to = math.ceil(float(qty) / float(SOIAF_PAGE_SIZE))
        page_curr = page_from

        while True:
            url = f"{SOIAF_ENDPOINT}/{entity}/?page={page_curr}&pageSize={SOIAF_PAGE_SIZE}"
            data = requests_get(url)
            
            if data and page_curr <= page_to:
                output += data
                page_curr += 1
            else:
                break
        return output

    elif id_:
        url = f"{SOIAF_ENDPOINT}/{entity}/{id_}"
        data = requests_get(url)
        return data


