import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd

def get_wordpress_data(api_url, username, app_password, content_type, num_docs):
    auth = HTTPBasicAuth(username, app_password)
    endpoint = f"{api_url}/wp-json/wp/v2/{content_type}"
    params = {
        "per_page": num_docs,
        "status": "publish"
    }
    
    response = requests.get(endpoint, auth=auth, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching data: {response.status_code}")
        return None

st.title("WordPress to CustomGPT Data Transfer")

# WordPress inputs
wp_url = st.text_input("WordPress Website URL")
wp_username = st.text_input("WordPress Username")
wp_app_password = st.text_input("WordPress Application Password", type="password")

# Checkboxes for content types
col1, col2 = st.columns(2)
with col1:
    fetch_posts = st.checkbox("Fetch Posts", value=True)
with col2:
    fetch_pages = st.checkbox("Fetch Pages", value=True)

num_docs = st.number_input("Number of documents to pull (per content type)", min_value=1, value=10)

if st.button("Fetch WordPress Data"):
    all_data = []
    
    content_types = []
    if fetch_posts:
        content_types.append("posts")
    if fetch_pages:
        content_types.append("pages")
    
    for content_type in content_types:
        data = get_wordpress_data(wp_url, wp_username, wp_app_password, content_type, num_docs)
        
        if data:
            for item in data:
                all_data.append({
                    "Title": item["title"]["rendered"],
                    "URL": item["link"],
                    "Type": content_type
                })
    
    if all_data:
        df = pd.DataFrame(all_data)
        st.table(df)
    else:
        st.warning("No data fetched. Please check your inputs and try again.")