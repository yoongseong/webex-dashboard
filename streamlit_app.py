import streamlit as st
import os
import pandas as pd
import requests

TE_BASE_URL = "https://api.thousandeyes.com/v7/"
TE_HEADERS = {
    "Authorization": f"Bearer {os.environ.get('TE_TOKEN')}",
    "Content-Type": "application/json",
    "Accept": "application/hal+json"
}
TE_PAYLOAD = '''{
    "searchSort": [
        {
            "sort": "round-id",
            "order": "desc"
        }
    ],    
    "searchFilters": {
        "agentId": [
            "9db4eabc-a86d-4fc9-b666-6ea6e8764144"
        ]
    }
}'''
TE_TEST_ID = "289949"
TE_WINDOW = "30m"

st.logo("gallery/logo.png")
st.title(":desktop_computer: NTT Com DD Dashboard")

@st.cache_data
def show_availability():
    url = f"{TE_BASE_URL}endpoint/test-results/scheduled-tests/{TE_TEST_ID}/network/filter?window={TE_WINDOW}"
    response = requests.request('POST', url, headers=TE_HEADERS, data = TE_PAYLOAD)
    # st.json(response.text.encode('utf8'))
    # st.write(response.json())
    st.write(response.json())
    # data = response.json()["results"]
    # filtered_data = []
    # target_keys = ["avgLatency", "jitter"]
    # for result in data:
    #     filtered_data.append({key: result[key] for key in target_keys} )    
    # df = pd.DataFrame(filtered_data)
    # df

show_availability()

# with st.container():
#     st.header("Availability")