import streamlit as st
import pandas as pd
import requests

TE_BASE_URL = "https://api.thousandeyes.com/v7/"
TE_HEADERS = {
    "Authorization": f"Bearer {st.secrets["TE_TOKEN"]}",
    # "Authorization": f"Bearer ",
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
TE_AGENT_ID = "9db4eabc-a86d-4fc9-b666-6ea6e8764144"
TE_WINDOW = "1h"

st.set_page_config(
    page_title="NTT Com DD Dashboard",
    layout="wide"
)

st.logo("gallery/logo.png")
st.title(":desktop_computer: NTT Com DD Dashboard")

@st.cache_data
def get_te_network_data():
    url = f"{TE_BASE_URL}endpoint/test-results/scheduled-tests/{TE_TEST_ID}/network/filter?window={TE_WINDOW}"
    response = requests.request('POST', url, headers=TE_HEADERS, data = TE_PAYLOAD)
    # st.json(response.text.encode('utf8'))
    # st.write(response.json())
    return response.json()["results"]
    

@st.cache_data
def get_te_http_data():
    url = f"{TE_BASE_URL}endpoint/test-results/scheduled-tests/{TE_TEST_ID}/http-server?window={TE_WINDOW}"
    response = requests.request('GET', url, headers=TE_HEADERS, data = None)
    # st.json(response.text.encode('utf8'))
    # st.write(response.json())
    data = response.json()["results"]
    return [result for result in data if result["agentId"] == TE_AGENT_ID]
    

st.header("Webex Performance Chart")

http_data = get_te_http_data()
network_data = get_te_network_data()

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Response Time")
        filtered_data = []
        target_keys = ["responseTime"]
        for result in http_data:
            filtered_data.append({key: result[key] for key in target_keys} )
        df = pd.DataFrame(filtered_data)
        st.line_chart(df, y_label="milliseconds")

        st.subheader("Average Latency")
        filtered_data = []
        target_keys = ["avgLatency"]
        for result in network_data:
            filtered_data.append({key: result[key] for key in target_keys} )
        df = pd.DataFrame(filtered_data)
        st.line_chart(df, y_label="milliseconds")

    with col2:
        st.subheader("Packet Loss")
        filtered_data = []
        target_keys = ["loss"]
        for result in network_data:
            filtered_data.append({key: result[key] for key in target_keys} )
        df = pd.DataFrame(filtered_data)
        st.line_chart(df, y_label="%")

        st.subheader("Jitter")
        filtered_data = []
        target_keys = ["jitter"]
        for result in network_data:
            filtered_data.append({key: result[key] for key in target_keys} )
        df = pd.DataFrame(filtered_data)
        st.line_chart(df, y_label="milliseconds")






# with st.container():
#     st.header("Availability")