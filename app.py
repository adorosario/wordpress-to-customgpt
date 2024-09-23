import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
from customgpt_client import CustomGPT
from customgpt_client.types import File
from requests.exceptions import HTTPError
from urllib.parse import urlparse
import time
import re
from datetime import datetime

def get_wordpress_data(api_url, username, app_password, content_type, num_docs):
    auth = HTTPBasicAuth(username, app_password)
    endpoint = f"{api_url}/wp-json/wp/v2/{content_type}"
    all_items = []
    page = 1
    per_page = 100  # Maximum allowed by WordPress API

    while len(all_items) < num_docs:
        params = {
            "per_page": min(per_page, num_docs - len(all_items)),
            "page": page,
            "status": "publish",
            "_embed": "true"  # This will include featured media in the response
        }
        
        response = requests.get(endpoint, auth=auth, params=params)
        
        if response.status_code == 200:
            items = response.json()
            all_items.extend(items)
            if len(items) < params["per_page"]:  # No more items to fetch
                break
            page += 1
        else:
            st.error(f"Error fetching data: {response.status_code}")
            return None

    return all_items[:num_docs]  # Ensure we don't return more than num_docs

def get_featured_media_url(item):
    if "_embedded" in item and "wp:featuredmedia" in item["_embedded"]:
        media = item["_embedded"]["wp:featuredmedia"]
        if media and len(media) > 0 and "source_url" in media[0]:
            return media[0]["source_url"]
    return None

def get_content_size(content):
    return len(content)

def create_short_description(content):
    # Remove HTML tags
    text = re.sub('<[^<]+?>', '', content)
    # Remove extra whitespace
    text = ' '.join(text.split())
    # Truncate to 160 characters
    return text[:157] + '...' if len(text) > 160 else text

def transfer_to_customgpt(project_name, docs, api_key):
    CustomGPT.api_key = api_key
    
    project = CustomGPT.Project.create(project_name=project_name)
    if project.status_code != 201:
        st.error(f"Failed to create project. Status code: {project.status_code}")
        return None
    
    project_id = project.parsed.data.id
    
    for idx, doc in enumerate(docs):
        file_name = f"document_{idx}.doc"
        file_content = doc["content"]
        file_metadata = {
            "source": doc["link"],
            "title": doc["title"],
            "description": doc["short_description"],
            "image": doc["featured_media"]
        }
        file_obj = File(file_name=file_name, payload=file_content)
        
        add_source = CustomGPT.Source.create(project_id=project_id, file=file_obj)
        if add_source.status_code != 201:
            st.error(f"Failed to upload file {file_name}. Status code: {add_source.status_code}")
            continue
        
        page_id = add_source.parsed.data.pages[0].id
        update_metadata = CustomGPT.PageMetadata.update(
            project_id, 
            page_id, 
            url=file_metadata["source"],
            title=file_metadata["title"],
            description=file_metadata["description"],
            image=file_metadata["image"]
        )
        if update_metadata.status_code != 200:
            st.error(f"Failed to update metadata for {file_name}. Status code: {update_metadata.status_code}")
    
    st.success(f"Data transferred to CustomGPT project: {project_name}")
    return project_id

def check_indexing_status(project_id, api_key):
    CustomGPT.api_key = api_key
    page_n = 1 # Pagination
    all_documents_indexed = False
    
    while not all_documents_indexed:
        documents_response = CustomGPT.Page.get(project_id=project_id, page=page_n)
        if documents_response.status_code != 200:
            st.error(f"Failed to retrieve documents. Status code: {documents_response.status_code}")
            return False
        
        documents_data = documents_response.parsed.data.pages
        documents = documents_data.data
        
        page_n_completed = True
        for doc in documents:
            # st.text(f"{doc.filename}: {doc.index_status}")
            if doc.index_status == "queued":
                time.sleep(5)
                page_n_completed = False
                break
        
        # At this point, all documents found in paginated responses until page_n have been indexed
        if page_n_completed:
            if documents_data.next_page_url:
                page_n += 1
            else:
                all_documents_indexed = True 
    
    st.success("All documents indexed successfully!")
    return True

def generate_project_name(wp_url):
    # Extract domain name from the URL
    domain = urlparse(wp_url).netloc
    
    # Remove 'www.' if present
    domain = re.sub(r'^www\.', '', domain)
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d:%H%M%S")
    
    # Combine domain and timestamp
    project_name = f"{domain} - {timestamp}"
    
    return project_name

st.set_page_config(page_title="WordPress Private Content to CustomGPT Data Transfer", layout="wide")

st.title("WordPress Private Content to CustomGPT Data Transfer")
st.markdown("*Securely sync your WordPress content to CustomGPT to build your AI agent*")
st.markdown("---")

# WordPress inputs
# Source Section
st.header("Source: WordPress")
col1, col2, col3 = st.columns(3)

with col1:
    wp_url = st.text_input(
        "WordPress Website URL",
        help="Enter the full URL of your WordPress website (e.g., https://www.example.com)"
    )

with col2:
    wp_username = st.text_input(
        "WordPress Username",
        help="Enter your WordPress username with sufficient permissions to access private content"
    )

with col3:
    wp_app_password = st.text_input(
        "WordPress Application Password",
        type="password",
        help="Enter your WordPress application password. This is different from your login password. Generate it in WordPress under Users > Application Passwords."
    )

# Checkboxes for content types
fetch_posts = True
fetch_pages = True

# Uncomment this if you want to control what is sync'ed
# col1, col2 = st.columns(2)
# with col1:
#     fetch_posts = st.checkbox("Fetch Posts", value=True)
# with col2:
#     fetch_pages = st.checkbox("Fetch Pages", value=True)

# Configure this based on on your CustomGPT plan limits (Standard plan is 1000)
num_docs = 1000

# Uncomment this if you want to have the user input his limits
# st.number_input("Number of documents", min_value=1, value=1000)

# Destination Section
st.header("Destination: CustomGPT")
customgpt_api_key = st.text_input(
    "CustomGPT API Key",
    type="password",
    help="Enter your [CustomGPT API key](https://app.customgpt.ai/profile#api). You can find this in your CustomGPT account settings."
)
customgpt_project_name = generate_project_name(wp_url)

# Action Button
if st.button("Fetch and Transfer Data", help="Click to start the data transfer process"):
    if not wp_url or not wp_username or not wp_app_password or not customgpt_api_key:
        st.error("Please fill in all required fields before proceeding.")
    else:
        all_data = []
        total_content_size = 0
        
        content_types = []
        if fetch_posts:
            content_types.append("posts")
        if fetch_pages:
            content_types.append("pages")
        
        for content_type in content_types:
            data = get_wordpress_data(wp_url, wp_username, wp_app_password, content_type, num_docs)
            
            if data:
                for item in data:
                    content = item["content"]["rendered"]
                    content_size = get_content_size(content)

                    # Skip items with zero content size
                    if content_size == 0:
                        continue

                    total_content_size += content_size
                    all_data.append({
                        "title": item["title"]["rendered"],
                        "link": item["link"],
                        "content": content,
                        "short_description": create_short_description(content),
                        "featured_media": get_featured_media_url(item),
                        "type": content_type,
                        "content_size": content_size
                    })
        
        if all_data:
            df = pd.DataFrame(all_data)
            st.table(df[["title", "link", "type", "content_size"]])
            
            total_documents = len(all_data)
            
            st.info(f"Beginning sync of {total_documents} documents to CustomGPT ...")
            project_id = transfer_to_customgpt(customgpt_project_name, all_data, customgpt_api_key)
            if project_id:
                st.info("Checking indexing status...")
                indexing_successful = check_indexing_status(project_id, customgpt_api_key)
                if indexing_successful:
                    st.markdown(f"""
                    ### :tada: Data Successfully Synced!
                    
                    Your WordPress content has been successfully transferred to CustomGPT and indexed.
                    
                    You can now query your data using the CustomGPT dashboard:
                    
                    **[Open CustomGPT Dashboard](https://app.customgpt.ai/projects/{project_id}/ask-me-anything)**
                    """)
        else:
            st.warning("No data fetched. Please check your inputs and try again.")