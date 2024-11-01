# OpenAI & Azure Text-to-Speech Application

This is a Python application that accepts text input (via URL, text, or file), uses OpenAI's GPT-4 Turbo model to generate a response based on the prompt, and then converts the generated text to speech using Azure's Text-to-Speech API. The app is built with `streamlit` for an intuitive web interface.

[![License: Apache License 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Forks](https://img.shields.io/github/forks/hipnologo/openai_azure_text2speech)](https://github.com/hipnologo/openai_azure_text2speech/network/members)
[![Stars](https://img.shields.io/github/stars/hipnologo/openai_azure_text2speech)](https://github.com/hipnologo/openai_azure_text2speech/stargazers)
[![Issues](https://img.shields.io/github/issues/hipnologo/openai_azure_text2speech)](https://github.com/hipnologo/openai_azure_text2speech/issues)
[![GitHub contributors](https://img.shields.io/github/contributors/hipnologo/openai_azure_text2speech)](https://github.com/hipnologo/openai_azure_text2speech/graphs/contributors)

## Prerequisites

- **OpenAI API Key**: Obtain from [OpenAI's website](https://platform.openai.com/signup).
- **Azure API Key**: Obtain from [Azure's website](https://portal.azure.com/).
- **Libraries**: Install the necessary libraries using pip:
  ```bash
  pip install requests streamlit openai beautifulsoup4 python-dotenv
  ```

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/hipnologo/openai_azure_text2speech.git
   cd openai_azure_text2speech
   ```

2. **Configure Environment Variables**:
   Create a `.env` file in the project root and add your API keys:
   ```plaintext
   OPENAI_API_KEY=YOUR_OPENAI_API_KEY
   AZURE_API_KEY=YOUR_AZURE_API_KEY
   ```

3. **Run the Application**:
   Launch the app using Streamlit:
   ```bash
   streamlit run app.py
   ```

## How to Use

1. **Input Options**:
   - Choose an input method (URL, direct text input, or file upload).
   
2. **Customize Prompt Length**:
   - Use the slider to set the character limit (up to 5000 tokens).

3. **Generate and Play Text-to-Speech**:
   - Generated text will display in the interface.
   - Play the audio using the built-in audio player or download it by clicking the "Download" button.

## Features

- **Multi-Input Options**: Accepts URLs, text input, or text files.
- **Voice Selection**: Choose between `en-US-AriaNeural`, `en-US-GuyNeural`, and `en-GB-RyanNeural` voices for Azure TTS.
- **OpenAI GPT-4 Turbo Model**: Uses the latest model for better responses.
- **Customizable Token Limit**: Limit the response length to suit your requirements.
- **Audio Download**: Easily download the generated audio file in WAV format.

## Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a branch for your feature or bug fix.
3. Make and test your changes.
4. Submit a pull request.

For a detailed guide, please refer to our [CONTRIBUTING.md](CONTRIBUTING.md) file.

Make sure to follow the coding style and add test cases for any new code. Feel free to reach out if you have any questions.

<a href="https://www.buymeacoffee.com/hipnologod" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>