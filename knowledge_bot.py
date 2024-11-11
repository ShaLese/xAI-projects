import os
import streamlit as st
from openai import OpenAI

# Initialize the xAI API client
def create_knowledge_bot(api_key: str, documents: list):
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1",
    )
    
    # Compile the documents into a single system message
    compiled_documents = "\n\n".join(documents)
    system_message = f"""You are a personalized knowledge assistant. Use the following documents as the basis for your responses:\n{compiled_documents}\n\nAnswer questions with references to the documents and maintain a helpful, knowledgeable tone."""
    
    return client, system_message

# Generate a response based on the user query
def generate_knowledge_response(client, system_message, user_query):
    completion = client.chat.completions.create(
        model="grok-beta",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_query},
        ]
    )
    
    return completion.choices[0].message.content

# Streamlit dashboard setup
def main():
    st.title("Personalized Knowledge Bot")
    st.write("Paste documents below (e.g., articles, book excerpts, notes) and ask questions based on the content.")

    # API key input
    api_key = st.text_input("Enter your xAI API Key", type="password")
    
    # Document input
    documents_input = st.text_area("Paste your documents here, separated by two new lines (e.g., use double Enter).")
    
    # Process the document input into a list
    documents = documents_input.split("\n\n") if documents_input else []

    # Query input
    user_query = st.text_input("Enter your query:")

    # Create knowledge bot and generate response on button click
    if st.button("Generate Response") and api_key and user_query and documents:
        # Create the bot
        client, system_message = create_knowledge_bot(api_key, documents)
        
        # Generate and display the response
        try:
            response = generate_knowledge_response(client, system_message, user_query)
            st.write("### Response")
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
