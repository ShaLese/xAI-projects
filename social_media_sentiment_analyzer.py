import streamlit as st
from openai import OpenAI

def create_sentiment_analyzer(api_key: str, topic: str, social_media_posts: list):
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1",
    )
    
    # Compiling posts to analyze sentiment
    compiled_posts = "\n\n".join(social_media_posts)
    system_message = f"""You are an AI assistant specialized in sentiment analysis. Analyze the following social media posts about '{topic}' and provide a sentiment analysis (positive, negative, or neutral) and a brief summary of overall sentiment trends. Here are the posts:\n{compiled_posts}"""
    
    return client, system_message

def generate_sentiment_response(client, system_message):
    completion = client.chat.completions.create(
        model="grok-beta",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": "Provide a sentiment analysis and summary of the above posts."},
        ]
    )
    
    return completion.choices[0].message.content

# Streamlit dashboard setup
def main():
    st.title("Social Media Sentiment Analyzer")
    st.write("Enter a topic or company name to analyze recent social media sentiment.")

    # API key input
    api_key = st.text_input("Enter your xAI API Key", type="password")
    
    # Topic input
    topic = st.text_input("Enter the topic or company name:")
    
    # Social media posts input area
    social_media_input = st.text_area("Paste sample social media posts here, separated by double new lines.")
    
    # Process the social media input into a list of posts
    social_media_posts = social_media_input.split("\n\n") if social_media_input else []

    # Generate sentiment analysis on button click
    if st.button("Analyze Sentiment") and api_key and topic and social_media_posts:
        # Create the sentiment analyzer
        client, system_message = create_sentiment_analyzer(api_key, topic, social_media_posts)
        
        # Generate and display the sentiment analysis
        try:
            response = generate_sentiment_response(client, system_message)
            st.write("### Sentiment Analysis Result")
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
