def get_facebook_posts(page_id, limit=10):
    posts_data = []
    try:
        # Fetch posts from the page
        posts = graph.get_connections(id=page_id, connection_name='posts', limit=limit)
        
        for post in posts['data']:
            try:
                # Request only 'created_time' initially
                post_details = graph.get_object(id=post['id'], fields='created_time')
                
                # Check and fetch 'message' if it exists
                message = post_details.get('message', 'No content available')
                posts_data.append({
                    'Message': message,
                    'Created Time': post_details['created_time']
                })
            except facebook.GraphAPIError as e:
                st.warning(f"Could not fetch details for a post: {e}")
            except KeyError:
                st.warning("A post is missing expected fields and was skipped.")

    except facebook.GraphAPIError as e:
        st.error(f"Error fetching data: {e}")

    if not posts_data:
        st.warning("No posts found or unable to fetch data.")
    
    return posts_data
