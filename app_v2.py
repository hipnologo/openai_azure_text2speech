import os
import requests
import streamlit as st
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import openai
import re

load_dotenv()

def truncate_text(text, max_tokens):
    tokens = re.findall(r'\w+|\W+', text)
    truncated_tokens = tokens[:max_tokens]
    return ''.join(truncated_tokens)

def get_openai_text(prompt, limit_chars):
    openai_key = os.environ.get("OPENAI_API_KEY")
    openai.api_key = openai_key  # Set the API key
    try:
        response = openai.Completion.create(
            model="gpt-4",  # Updated to GPT-4
            prompt=prompt,
            max_tokens=limit_chars,
            temperature=0.5
        )
    except requests.exceptions.RequestException as e:
        st.error(f"Error accessing OpenAI API: {e}")
        return None

    return response.choices[0].text  # Corrected access to response data

def get_azure_access_token():
    azure_key = os.environ.get("AZURE_API_KEY")
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
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        return ' '.join([p.text for p in soup.find_all('p')])
    except requests.exceptions.RequestException as e:
        st.error(f"Error retrieving content: {e}")
        return None

def main():
    st.title("Text-to-Speech App")
    st.subheader("Exploring OpenAI and Azure APIs")

    input_option = st.selectbox("Choose input option:", ["URL", "Text Input", "File Upload"])
    prompt_text = None

    if input_option == "URL":
        prompt_url = st.text_input("Enter the URL of the prompt page:")
        if prompt_url:
            prompt_text = extract_content(prompt_url)
    elif input_option == "Text Input":
        prompt_text = st.text_area("Enter or paste the text:")
    elif input_option == "File Upload":
        uploaded_file = st.file_uploader("Upload a text file (.txt)", type="txt")
        if uploaded_file:
            prompt_text = uploaded_file.read().decode("utf-8")

    limit_chars = st.slider("Limit the number of characters (max tokens)", 100, 5000, step=100)

    if prompt_text:
        truncated_prompt_text = truncate_text(prompt_text, 4096 - limit_chars)
        openai_text = get_openai_text(truncated_prompt_text, limit_chars)
        if openai_text:
            st.write("Resulted Text:", openai_text)
            voice_name = st.selectbox("Select a voice:", ['en-US-AriaNeural', 'en-US-GuyNeural', 'en-GB-RyanNeural'])
            speech = text_to_speech(openai_text, voice_name)
            if speech:
                st.audio(speech, format='wav')
                if st.button("Download audio file"):
                    with open("speech.wav", "wb") as f:
                        f.write(speech)

if __name__ == "__main__":
    main()
