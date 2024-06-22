import streamlit as st
from googleapiclient.discovery import build
import re
from collections import Counter
import time

# Set up Google API key
api_key = 'AIzaSyDCvbnrh3_ynhBqozI6dRFCKtrf_GHyrNU'  # Replace with your own API key
youtube = build('youtube', 'v3', developerKey=api_key)

# Function to fetch video details
def get_video_details(query):
    request = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=50  # You can adjust this number for more results
    )
    response = request.execute()
    return response['items']

# Function to extract hashtags from text
def extract_hashtags(text):
    hashtags = re.findall(r'#\w+', text)
    return hashtags

# إضافة تنسيق CSS لإخفاء الروابط عند تمرير الفأرة فوق النصوص
hide_links_style = """
    <style>
    a {
        text-decoration: none;
        color: inherit;
        pointer-events: none;
    }
    a:hover {
        text-decoration: none;
        color: inherit;
        cursor: default;
    }
    </style>
    """
st.markdown(hide_links_style, unsafe_allow_html=True)

# Streamlit UI
def main():
    st.title('YouTube Hashtag Generator')

    keyword = st.text_input('Enter a keyword')

    if st.button('Generate Hashtags'):
        with st.spinner('Generating hashtags...'):
            time.sleep(2)  # Simulate a delay for demonstration purposes
            videos = get_video_details(keyword)
            all_hashtags = []

            for video in videos:
                title = video['snippet']['title']
                description = video['snippet']['description']
                all_hashtags.extend(extract_hashtags(title))
                all_hashtags.extend(extract_hashtags(description))

            hashtag_counts = Counter(all_hashtags)
            common_hashtags = hashtag_counts.most_common(10)  # Get top 10 most common hashtags

            st.subheader(f"Top hashtags for '{keyword}':")

            # Display results in a table
            table_data = {"Hashtag": [], "Count": []}
            for hashtag, count in common_hashtags:
                table_data["Hashtag"].append(hashtag)
                table_data["Count"].append(count)

            st.table(table_data)

if __name__ == "__main__":
    main()
