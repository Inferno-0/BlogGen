import requests
import streamlit as st

def publish_to_wordpress(blog_data: dict) -> str:
    """
    Publishes a generated blog post to a WordPress site as a draft.
    
    Args:
        blog_data (dict): A dictionary containing 'title' and 'html_content'.
        
    Returns:
        str: The URL of the newly created WordPress draft, or an empty string 
             if the publication fails.
    """
    try:
        # Pull WP credentials from Streamlit secrets
        wp_username = st.secrets["WP_USERNAME"]
        wp_app_password = st.secrets["WP_APP_PASSWORD"]
        wp_url = st.secrets["WP_URL"]
    except KeyError as e:
        print(f"Configuration Error: Missing secret {e}")
        return ""

    # Construct the WordPress REST API endpoint
    endpoint = f"{wp_url.rstrip('/')}/wp-json/wp/v2/posts"

    # Map the blog_data to the WordPress payload
    payload = {
        "title": blog_data.get("title", "Untitled Post"),
        "content": blog_data.get("html_content", ""),
        "status": "draft"
    }

    try:
        # Make the POST request with Basic Authentication
        response = requests.post(
            endpoint,
            auth=(wp_username, wp_app_password),
            json=payload
        )
        
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()
        
        # Parse the JSON response
        publish_data = response.json()
        
        # Return the URL of the newly created WordPress draft
        return str(publish_data.get("link", ""))

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        if http_err.response is not None:
            print(f"Raw response text: {http_err.response.text}")
        return ""
    except Exception as err:
        print(f"An unexpected error occurred: {err}")
        # If response was defined prior to the exception, log it
        if 'response' in locals() and hasattr(response, 'text'):
            print(f"Raw response text: {response.text}")
        return ""
