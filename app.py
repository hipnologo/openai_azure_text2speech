import requests
import streamlit as st

def get_openai_text(prompt, limit_chars):
    openai_key = "YOUR_OPENAI_API_KEY"
    response = requests.post(
        "https://api.openai.com/v1/engines/davinci/jobs",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_key}"
        },
        json={
            "prompt": prompt,
            "max_tokens": limit_chars,
            "temperature": 0.5,
        }
    )

    response.raise_for_status()
    return response.json()['choices'][0]['text']

def text_to_speech(text, voice_name='en-US-Jessa24kRUS'):
    azure_key = "YOUR_AZURE_API_KEY"
    response = requests.post(
        "https://centralus.tts.speech.microsoft.com/cognitiveservices/v1",
        headers={
            "Authorization": f"Bearer {azure_key}",
            "Content-Type": "application/ssml+xml",
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
    return response.content

def main():
    st.title("OpenAI to Text-to-Speech")
    prompt = st.text_input("Enter the URL of the prompt page:")
    limit_chars = st.slider("Limit the number of characters (max tokens)", 100, 5000, step=100)
    openai_text = get_openai_text(prompt, limit_chars)
    st.write("Resulted Text:", openai_text)
    speech = text_to_speech(openai_text)
    st.audio(speech, format='wav')
    if st.button("Download audio file"):
        with open("speech.wav", "wb") as f:
            f.write(speech)

if __name__ == "__main__":
    main()
