"""
OpenAI & Azure Text-to-Speech Application
------------------------------------------

This application generates text based on a prompt, then converts the generated text into speech
using OpenAI's GPT models and Azure's Text-to-Speech API. The application offers
multiple input options (URL, text input, or file upload) and a Streamlit web interface for ease of use.

Author: Fabio Carvalho
License: Apache License 2.0

Dependencies:
- See requirements.txt for complete list

Usage:
1. Obtain API keys for OpenAI and Azure, and store them in a .env file:
   - OPENAI_API_KEY=<Your OpenAI API Key>
   - AZURE_SPEECH_KEY=<Your Azure Speech Key>
   - AZURE_SPEECH_REGION=<Your Azure Speech Region>

2. Run the app with Streamlit:
   streamlit run app.py

Features:
- Prompt generation using OpenAI GPT models.
- Text-to-Speech conversion using Azure's Speech Services.
- Options to select different voice profiles for TTS output.
- Audio playback and download of the generated speech.
- Input validation and security measures.
"""

import logging
import os
import re
import tempfile
from typing import Dict, List, Optional, Tuple, Union
from urllib.parse import urlparse

import azure.cognitiveservices.speech as speechsdk
import streamlit as st
import validators
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Constants
MAX_TEXT_LENGTH = 50000  # Maximum characters for input text
MAX_TOKENS = 4000       # Maximum tokens for OpenAI response
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB max file size
SUPPORTED_MODELS = ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"]
AZURE_VOICES = {
    "en-US-AriaNeural": "English (US) - Aria (Female)",
    "en-US-GuyNeural": "English (US) - Guy (Male)",
    "en-US-JennyNeural": "English (US) - Jenny (Female)",
    "en-GB-RyanNeural": "English (UK) - Ryan (Male)",
    "en-GB-SoniaNeural": "English (UK) - Sonia (Female)",
    "es-ES-ElviraNeural": "Spanish (Spain) - Elvira (Female)",
    "fr-FR-DeniseNeural": "French (France) - Denise (Female)",
    "de-DE-KatjaNeural": "German (Germany) - Katja (Female)",
}


class ConfigurationError(Exception):
    """Raised when there's a configuration issue."""
    pass


class APIError(Exception):
    """Raised when there's an API-related error."""
    pass


class SecurityError(Exception):
    """Raised when there's a security-related issue."""
    pass


class AppConfig:
    """Application configuration management with security validations."""
    
    def __init__(self):
        """Initialize configuration with validation."""
        self.openai_api_key = self._get_required_env("OPENAI_API_KEY")
        self.azure_speech_key = self._get_required_env("AZURE_SPEECH_KEY")
        self.azure_speech_region = self._get_required_env("AZURE_SPEECH_REGION")
        
        # Initialize OpenAI client
        try:
            self.openai_client = OpenAI(api_key=self.openai_api_key)
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            raise ConfigurationError(f"OpenAI client initialization failed: {e}")
    
    @staticmethod
    def _get_required_env(key: str) -> str:
        """Get required environment variable with validation."""
        value = os.getenv(key)
        if not value:
            error_msg = f"Missing required environment variable: {key}"
            logger.error(error_msg)
            raise ConfigurationError(error_msg)
        
        # Basic validation for API keys
        if len(value.strip()) < 10:
            error_msg = f"Invalid {key}: too short"
            logger.error(error_msg)
            raise ConfigurationError(error_msg)
        
        return value.strip()


def validate_text_input(text: str, max_length: int = MAX_TEXT_LENGTH) -> str:
    """
    Validate and sanitize text input.
    
    Args:
        text: Input text to validate
        max_length: Maximum allowed length
        
    Returns:
        Sanitized text
        
    Raises:
        SecurityError: If text fails validation
    """
    if not text or not isinstance(text, str):
        raise SecurityError("Invalid text input: must be a non-empty string")
    
    text = text.strip()
    
    if len(text) > max_length:
        raise SecurityError(f"Text too long: {len(text)} characters (max: {max_length})")
    
    # Remove potential XSS content
    text = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
    
    return text


def validate_url(url: str) -> str:
    """
    Validate URL for security.
    
    Args:
        url: URL to validate
        
    Returns:
        Validated URL
        
    Raises:
        SecurityError: If URL is invalid or potentially dangerous
    """
    if not url or not isinstance(url, str):
        raise SecurityError("Invalid URL: must be a non-empty string")
    
    url = url.strip()
    
    # Basic URL validation
    if not validators.url(url):
        raise SecurityError("Invalid URL format")
    
    # Parse URL for additional validation
    parsed = urlparse(url)
    
    # Block potentially dangerous schemes
    if parsed.scheme not in ['http', 'https']:
        raise SecurityError("Only HTTP and HTTPS URLs are allowed")
    
    # Block localhost and private IP ranges for security
    if parsed.hostname in ['localhost', '127.0.0.1', '0.0.0.0']:
        raise SecurityError("Local URLs are not allowed")
    
    # Block private IP ranges
    if parsed.hostname and (
        parsed.hostname.startswith('192.168.') or
        parsed.hostname.startswith('10.') or
        parsed.hostname.startswith('172.')
    ):
        raise SecurityError("Private IP addresses are not allowed")
    
    return url


def truncate_text_smart(text: str, max_tokens: int) -> str:
    """
    Intelligently truncate text to stay within token limits.
    
    Args:
        text: The input text to truncate
        max_tokens: The maximum number of tokens allowed
        
    Returns:
        Truncated text
    """
    # Rough estimation: 1 token ≈ 4 characters for English text
    approx_max_chars = max_tokens * 4
    
    if len(text) <= approx_max_chars:
        return text
    
    # Try to truncate at sentence boundaries
    sentences = re.split(r'[.!?]+', text)
    truncated_text = ""
    
    for sentence in sentences:
        if len(truncated_text + sentence) > approx_max_chars:
            break
        truncated_text += sentence + ". "
    
    # If we couldn't get even one sentence, do character truncation
    if not truncated_text.strip():
        truncated_text = text[:approx_max_chars]
    
    return truncated_text.strip()


def get_openai_response(
    config: AppConfig,
    prompt: str,
    model: str = "gpt-4o-mini",
    max_tokens: int = MAX_TOKENS,
    temperature: float = 0.7
) -> str:
    """
    Generate text using OpenAI's API with modern client.
    
    Args:
        config: Application configuration
        prompt: The text prompt for OpenAI to process
        model: The model to use for generation
        max_tokens: Maximum tokens in response
        temperature: Sampling temperature
        
    Returns:
        Generated text from OpenAI
        
    Raises:
        APIError: If the API call fails
    """
    try:
        # Validate inputs
        prompt = validate_text_input(prompt)
        
        if model not in SUPPORTED_MODELS:
            model = "gpt-4o-mini"  # Default to safe model
            
        if max_tokens > MAX_TOKENS:
            max_tokens = MAX_TOKENS
            
        if not 0 <= temperature <= 2:
            temperature = 0.7
        
        logger.info(f"Making OpenAI API call with model: {model}")
        
        response = config.openai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates engaging and informative content."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            timeout=30.0  # Add timeout for security
        )
        
        content = response.choices[0].message.content
        if not content:
            raise APIError("Empty response from OpenAI")
            
        return content.strip()
        
    except Exception as e:
        error_msg = f"OpenAI API error: {str(e)}"
        logger.error(error_msg)
        raise APIError(error_msg)

def text_to_speech_azure(
    config: AppConfig,
    text: str,
    voice_name: str = 'en-US-AriaNeural',
    output_format: str = 'audio-16khz-128kbitrate-mono-mp3'
) -> Optional[bytes]:
    """
    Convert text to speech using Azure Speech Services SDK.
    
    Args:
        config: Application configuration
        text: Text to convert to speech
        voice_name: Voice to use for synthesis
        output_format: Audio output format
        
    Returns:
        Audio content as bytes, or None if error occurs
        
    Raises:
        APIError: If the speech synthesis fails
    """
    try:
        # Validate inputs
        text = validate_text_input(text, max_length=10000)  # Azure TTS limit
        
        if voice_name not in AZURE_VOICES:
            voice_name = 'en-US-AriaNeural'  # Default voice
        
        logger.info(f"Converting text to speech with voice: {voice_name}")
        
        # Configure speech synthesis
        speech_config = speechsdk.SpeechConfig(
            subscription=config.azure_speech_key,
            region=config.azure_speech_region
        )
        speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Audio16Khz128KBitRateMonoMp3
        )
        speech_config.speech_synthesis_voice_name = voice_name
        
        # Create synthesizer with in-memory stream
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config,
            audio_config=None
        )
        
        # Perform synthesis
        result = synthesizer.speak_text_async(text).get()
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return result.audio_data
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            error_msg = f"Speech synthesis canceled: {cancellation_details.reason}"
            if cancellation_details.error_details:
                error_msg += f" - {cancellation_details.error_details}"
            logger.error(error_msg)
            raise APIError(error_msg)
        else:
            error_msg = f"Speech synthesis failed with reason: {result.reason}"
            logger.error(error_msg)
            raise APIError(error_msg)
            
    except Exception as e:
        error_msg = f"Azure Speech synthesis error: {str(e)}"
        logger.error(error_msg)
        raise APIError(error_msg)


def extract_content_from_url(url: str, max_paragraphs: int = 50) -> str:
    """
    Safely extract text content from a URL with security validations.
    
    Args:
        url: URL to extract content from
        max_paragraphs: Maximum number of paragraphs to extract
        
    Returns:
        Extracted text content
        
    Raises:
        APIError: If content extraction fails
        SecurityError: If URL validation fails
    """
    try:
        # Validate URL
        url = validate_url(url)
        
        logger.info(f"Extracting content from URL: {url}")
        
        # Make secure HTTP request
        import requests
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(
            url,
            headers=headers,
            timeout=10,  # 10 second timeout
            allow_redirects=True,
            verify=True  # Verify SSL certificates
        )
        response.raise_for_status()
        
        # Check content type
        content_type = response.headers.get('content-type', '').lower()
        if 'text/html' not in content_type:
            raise APIError("URL does not return HTML content")
        
        # Parse HTML safely
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Extract paragraphs
        paragraphs = soup.find_all('p')
        
        if not paragraphs:
            raise APIError("No paragraph content found on the page")
        
        # Limit number of paragraphs for security
        paragraphs = paragraphs[:max_paragraphs]
        
        # Extract and clean text
        text_content = ' '.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
        
        if not text_content:
            raise APIError("No readable text content found")
        
        return validate_text_input(text_content)
        
    except SecurityError:
        raise
    except Exception as e:
        error_msg = f"Content extraction error: {str(e)}"
        logger.error(error_msg)
        raise APIError(error_msg)


def process_uploaded_file(uploaded_file) -> str:
    """
    Safely process uploaded text file with security validations.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        File content as string
        
    Raises:
        SecurityError: If file validation fails
    """
    try:
        if uploaded_file is None:
            raise SecurityError("No file uploaded")
        
        # Check file size
        file_size = uploaded_file.size if hasattr(uploaded_file, 'size') else len(uploaded_file.getvalue())
        if file_size > MAX_FILE_SIZE:
            raise SecurityError(f"File too large: {file_size} bytes (max: {MAX_FILE_SIZE})")
        
        # Check file type
        if uploaded_file.type not in ['text/plain', 'application/octet-stream']:
            raise SecurityError(f"Invalid file type: {uploaded_file.type}. Only .txt files are allowed.")
        
        # Check file extension
        if not uploaded_file.name.lower().endswith('.txt'):
            raise SecurityError("Only .txt files are allowed")
        
        logger.info(f"Processing uploaded file: {uploaded_file.name}")
        
        # Read and decode file content
        content = uploaded_file.read()
        
        # Try different encodings
        for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']:
            try:
                text_content = content.decode(encoding)
                return validate_text_input(text_content)
            except UnicodeDecodeError:
                continue
        
        raise SecurityError("Unable to decode file content. Please ensure it's a valid text file.")
        
    except SecurityError:
        raise
    except Exception as e:
        error_msg = f"File processing error: {str(e)}"
        logger.error(error_msg)
        raise SecurityError(error_msg)


def create_streamlit_interface():
    """Create the main Streamlit interface with security considerations."""
    st.set_page_config(
        page_title="OpenAI & Azure Text-to-Speech",
        page_icon="🎙️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🎙️ OpenAI & Azure Text-to-Speech Application")
    st.markdown("---")
    
    # Initialize configuration with error handling
    try:
        config = AppConfig()
    except ConfigurationError as e:
        st.error(f"⚠️ Configuration Error: {e}")
        st.info("Please check your environment variables in the .env file.")
        st.stop()
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        model = st.selectbox(
            "OpenAI Model:",
            options=SUPPORTED_MODELS,
            index=1,  # Default to gpt-4o-mini
            help="Choose the OpenAI model for text generation"
        )
        
        max_tokens = st.slider(
            "Max Response Tokens:",
            min_value=100,
            max_value=MAX_TOKENS,
            value=1000,
            step=100,
            help="Maximum tokens in OpenAI response"
        )
        
        temperature = st.slider(
            "Creativity (Temperature):",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
            help="Higher values make output more creative but less focused"
        )
        
        voice_name = st.selectbox(
            "Voice Selection:",
            options=list(AZURE_VOICES.keys()),
            format_func=lambda x: AZURE_VOICES[x],
            help="Choose voice for text-to-speech conversion"
        )
    
    # Main interface
    st.subheader("📝 Input Options")
    
    input_option = st.radio(
        "Choose your input method:",
        options=["Text Input", "URL", "File Upload"],
        horizontal=True
    )
    
    prompt_text = None
    
    try:
        if input_option == "Text Input":
            prompt_text = st.text_area(
                "Enter or paste your text:",
                height=200,
                max_chars=MAX_TEXT_LENGTH,
                help=f"Maximum {MAX_TEXT_LENGTH} characters allowed"
            )
            
        elif input_option == "URL":
            url_input = st.text_input(
                "Enter URL:",
                placeholder="https://example.com/article",
                help="Enter a valid HTTP/HTTPS URL to extract content"
            )
            
            if url_input and st.button("🔗 Extract Content", type="secondary"):
                with st.spinner("Extracting content from URL..."):
                    try:
                        prompt_text = extract_content_from_url(url_input)
                        st.success("✅ Content extracted successfully!")
                        with st.expander("View extracted content"):
                            st.text_area(
                                "Extracted text:",
                                value=prompt_text[:1000] + ("..." if len(prompt_text) > 1000 else ""),
                                height=200,
                                disabled=True
                            )
                    except (APIError, SecurityError) as e:
                        st.error(f"❌ {e}")
                        prompt_text = None
                        
        elif input_option == "File Upload":
            uploaded_file = st.file_uploader(
                "Upload a text file:",
                type=['txt'],
                help="Maximum file size: 10MB"
            )
            
            if uploaded_file:
                try:
                    prompt_text = process_uploaded_file(uploaded_file)
                    st.success(f"✅ File '{uploaded_file.name}' processed successfully!")
                    with st.expander("View file content"):
                        st.text_area(
                            "File content:",
                            value=prompt_text[:1000] + ("..." if len(prompt_text) > 1000 else ""),
                            height=200,
                            disabled=True
                        )
                except SecurityError as e:
                    st.error(f"❌ {e}")
                    prompt_text = None
    
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")
        logger.error(f"Unexpected error in interface: {e}")
    
    # Generate and convert text
    if prompt_text and prompt_text.strip():
        st.markdown("---")
        st.subheader("🤖 Text Generation & Speech Synthesis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 Generate & Synthesize", type="primary"):
                try:
                    # Truncate text smartly
                    input_tokens = max_tokens + 500  # Reserve tokens for prompt
                    truncated_text = truncate_text_smart(prompt_text, 4000 - input_tokens)
                    
                    # Generate text with OpenAI
                    with st.spinner("Generating text with OpenAI..."):
                        generated_text = get_openai_response(
                            config, 
                            truncated_text, 
                            model=model,
                            max_tokens=max_tokens,
                            temperature=temperature
                        )
                    
                    st.success("✅ Text generated successfully!")
                    
                    # Display generated text
                    with st.expander("📄 Generated Text", expanded=True):
                        st.write(generated_text)
                    
                    # Convert to speech
                    with st.spinner("Converting to speech..."):
                        audio_data = text_to_speech_azure(
                            config,
                            generated_text,
                            voice_name=voice_name
                        )
                    
                    if audio_data:
                        st.success("✅ Speech synthesis completed!")
                        
                        # Audio player
                        st.audio(audio_data, format='audio/mp3')
                        
                        # Download button
                        st.download_button(
                            label="📥 Download Audio",
                            data=audio_data,
                            file_name=f"speech_{voice_name}_{model}.mp3",
                            mime="audio/mp3"
                        )
                
                except (APIError, SecurityError, ConfigurationError) as e:
                    st.error(f"❌ {e}")
                except Exception as e:
                    st.error(f"❌ An unexpected error occurred: {e}")
                    logger.error(f"Unexpected error in generation: {e}")
        
        with col2:
            st.info("""
            **ℹ️ Information:**
            - Text will be intelligently truncated if too long
            - Generation may take 10-30 seconds
            - Audio format: MP3, 16kHz
            - All inputs are validated for security
            """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>Made with ❤️ using OpenAI API and Azure Speech Services</p>
            <p>⚠️ Please ensure you have proper API keys configured in your .env file</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def main():
    """Main application entry point."""
    try:
        create_streamlit_interface()
    except Exception as e:
        st.error(f"❌ Application error: {e}")
        logger.error(f"Application error: {e}")


if __name__ == "__main__":
    main()
