# Function to get posts with additional error handling
def get_facebook_posts(page_id, limit=10):
    posts_data = []
    try:
        # Request posts from the page
        posts = graph.get_connections(id=page_id, connection_name='posts', limit=limit)
        
        for post in posts['data']:
            try:
                post_details = graph.get_object(id=post['id'], fields='message,created_time')
                # Only add posts if 'message' and 'created_time' exist
                if 'message' in post_details and 'created_time' in post_details:
                    posts_data.append({
                        'Message': post_details['message'],
                        'Created Time': post_details['created_time']
                    })
            except facebook.GraphAPIError as e:
                st.warning(f"Could not fetch details for a post: {e}")

    except facebook.GraphAPIError as e:
        st.error(f"Error fetching data: {e}")
    
    if not posts_data:
        st.warning("No posts found or unable to fetch data.")
    
    return posts_data
