"""
OpenAI & Azure Text-to-Speech Application
------------------------------------------

This application generates text based on a prompt, then converts the generated text into speech
using OpenAI's GPT-4 Turbo model and Azure's Text-to-Speech API. The application offers
multiple input options (URL, text input, or file upload) and a Streamlit web interface for ease of use.

Author: Fabio Carvalho
License: Apache License 2.0

Dependencies:
- Streamlit: pip install streamlit
- OpenAI: pip install openai
- Requests: pip install requests
- BeautifulSoup: pip install beautifulsoup4
- Python-dotenv: pip install python-dotenv

Usage:
1. Obtain API keys for OpenAI and Azure, and store them in a .env file:
   - OPENAI_API_KEY=<Your OpenAI API Key>
   - AZURE_API_KEY=<Your Azure API Key>

2. Run the app with Streamlit:
   streamlit run app.py

Features:
- Prompt generation using OpenAI GPT-4 Turbo model.
- Text-to-Speech conversion using Azure's TTS API.
- Options to select different voice profiles for TTS output.
- Audio playback and download of the generated speech.

"""

import os
import requests
import streamlit as st
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import openai
import re
import io

load_dotenv()

def truncate_text(text, max_tokens):
    """
    Truncates the input text to stay within the maximum token limit.

    Args:
        text (str): The input text to truncate.
        max_tokens (int): The maximum number of tokens allowed.

    Returns:
        str: The truncated text.
    """
    tokens = re.findall(r'\w+|\W+', text)
    truncated_tokens = tokens[:max_tokens]
    return ''.join(truncated_tokens)

def get_openai_text(prompt, limit_tokens):
    """
    Sends a prompt to the OpenAI API and retrieves a generated response.

    Args:
        prompt (str): The text prompt for OpenAI to process.
        limit_tokens (int): The maximum number of tokens in the response.

    Returns:
        str: The generated text from OpenAI, or None if an error occurs.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=limit_tokens,
            temperature=0.5
        )
        return response['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        st.error(f"Error accessing OpenAI API: {e}")
        return None

def get_azure_access_token():
    """
    Retrieves an access token from Azure's Text-to-Speech API.

    Returns:
        str: The access token if successful, or None if an error occurs.
    """
    azure_key = os.getenv("AZURE_API_KEY")
    try:
        response = requests.post(
            "https://eastus.api.cognitive.microsoft.com/sts/v1.0/issuetoken",
            headers={
                "Ocp-Apim-Subscription-Key": azure_key
            }
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        st.error(f"Error accessing Azure API: {e}")
        return None

    return response.text

def text_to_speech(text, voice_name='en-US-AriaNeural'):
    """
    Converts text to speech using Azure's Text-to-Speech API.

    Args:
        text (str): The text to convert to speech.
        voice_name (str): The name of the voice for the speech output.

    Returns:
        bytes: The audio content in binary format, or None if an error occurs.
    """
    access_token = get_azure_access_token()
    if not access_token:
        return None

    try:
        response = requests.post(
            "https://eastus.tts.speech.microsoft.com/cognitiveservices/v1",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/ssml+xml",
                "X-MICROSOFT-OutputFormat": "riff-24khz-16bit-mono-pcm",
                "User-Agent": "TextToSpeechApp",
            },
            data=f"""
                <speak version='1.0' xml:lang='en-US'>
                <voice name='{voice_name}'>
                    {text}
                </voice>
                </speak>
            """,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        st.error(f"Error generating speech: {e}")
        return None

    return response.content

def extract_content(url):
    """
    Extracts and concatenates paragraph text content from a specified URL.

    Args:
        url (str): The URL of the webpage to extract content from.

    Returns:
        str: The concatenated text content of all paragraphs, or None if an error occurs.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        return ' '.join([p.text for p in soup.find_all('p')])
    except requests.exceptions.RequestException as e:
        st.error(f"Error retrieving content from URL: {e}")
        return None

def main():
    """
    The main function for running the Streamlit app. It provides the interface
    for users to input text or URLs, select options, and generate text-to-speech output.
    """
    st.title("OpenAI & Azure Text-to-Speech App")
    st.subheader("Generate Text with OpenAI and Convert it to Speech with Azure")
    st.info("Use OpenAI's API to generate text and Azure's API for text-to-speech. Choose to upload text, enter a URL, or paste text directly.")

    input_option = st.selectbox("Choose input option:", ["URL", "Text Input", "File Upload"])
    prompt_text = None

    if input_option == "URL":
        prompt_url = st.text_input("Enter the URL:")
        if prompt_url:
            prompt_text = extract_content(prompt_url)
    elif input_option == "Text Input":
        prompt_text = st.text_area("Enter or paste the text:")
    elif input_option == "File Upload":
        uploaded_file = st.file_uploader("Upload a text file (.txt)", type="txt")
        if uploaded_file:
            prompt_text = uploaded_file.read().decode("utf-8")

    limit_tokens = st.slider("Limit tokens for OpenAI response:", 100, 5000, step=100)

    if prompt_text:
        truncated_prompt_text = truncate_text(prompt_text, 4096 - limit_tokens)

        openai_text = get_openai_text(truncated_prompt_text, limit_tokens)
        if openai_text:
            st.write("Generated Text:", openai_text)
            voice_name = st.selectbox("Choose voice for TTS:", ['en-US-AriaNeural', 'en-US-GuyNeural', 'en-GB-RyanNeural'])
            speech = text_to_speech(openai_text, voice_name)
            if speech:
                st.audio(speech, format='audio/wav')
                if st.button("Download audio file"):
                    st.download_button(label="Download", data=speech, file_name="speech.wav", mime="audio/wav")

if __name__ == "__main__":
    main()
