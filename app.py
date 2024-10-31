import streamlit as st
import facebook
import pandas as pd
from openpyxl import Workbook

# Facebook API setup
ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'  # Replace with your actual token
PAGE_ID = '100064058797322'  # Limra Chicken Ghazipur Delhi Page ID

# Initialize Facebook Graph API
graph = facebook.GraphAPI(access_token=ACCESS_TOKEN, version="3.0")

# Function to get posts
def get_facebook_posts(page_id, limit=10):
    posts_data = []
    try:
        # Request posts from the page
        posts = graph.get_connections(id=page_id, connection_name='posts', limit=limit)
        for post in posts['data']:
            post_details = graph.get_object(id=post['id'], fields='message,created_time')
            posts_data.append({
                'Message': post_details.get('message', 'No content'),
                'Created Time': post_details.get('created_time')
            })
    except facebook.GraphAPIError as e:
        st.error(f"Error fetching data: {e}")
    return posts_data

# Streamlit app interface
st.title("Facebook Post Scraper")
st.write("Fetch posts from the specified Facebook Page")

# User inputs
num_posts = st.number_input("Number of posts to retrieve", min_value=1, max_value=100, value=10)

if st.button("Fetch Posts"):
    # Fetch posts
    posts_data = get_facebook_posts(PAGE_ID, limit=num_posts)
    if posts_data:
        # Convert to DataFrame
        df = pd.DataFrame(posts_data)
        st.write("Fetched Posts:", df)
        
        # Export to Excel
        excel_file = "facebook_posts.xlsx"
        df.to_excel(excel_file, index=False, engine='openpyxl')
        
        # Download link for Excel file
        st.download_button(
            label="Download as Excel",
            data=open(excel_file, "rb"),
            file_name=excel_file,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.write("No posts found or unable to fetch data.")
