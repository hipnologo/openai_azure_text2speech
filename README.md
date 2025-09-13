# 🎙️ OpenAI & Azure Text-to-Speech Application

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green?logo=openai&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-Speech%20Services-blue?logo=microsoft-azure&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-red?logo=streamlit&logoColor=white)

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: Bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)

[![Forks](https://img.shields.io/github/forks/hipnologo/openai_azure_text2speech)](https://github.com/hipnologo/openai_azure_text2speech/network/members)
[![Stars](https://img.shields.io/github/stars/hipnologo/openai_azure_text2speech)](https://github.com/hipnologo/openai_azure_text2speech/stargazers)
[![Issues](https://img.shields.io/github/issues/hipnologo/openai_azure_text2speech)](https://github.com/hipnologo/openai_azure_text2speech/issues)
[![Contributors](https://img.shields.io/github/contributors/hipnologo/openai_azure_text2speech)](https://github.com/hipnologo/openai_azure_text2speech/graphs/contributors)

**A modern, secure, and user-friendly application that combines OpenAI's powerful language models with Azure's speech synthesis services to create an end-to-end text generation and text-to-speech solution.**

[Features](#-features) • [Quick Start](#-quick-start) • [Installation](#-installation) • [Usage](#-usage) • [API Documentation](#-api-documentation) • [Contributing](#-contributing) • [License](#-license)

</div>

---

## 📋 Table of Contents

- [🎙️ OpenAI \& Azure Text-to-Speech Application](#️-openai--azure-text-to-speech-application)
  - [📋 Table of Contents](#-table-of-contents)
  - [✨ Features](#-features)
  - [🎯 Use Cases](#-use-cases)
  - [🚀 Quick Start](#-quick-start)
  - [🛠️ Installation](#️-installation)
    - [Prerequisites](#prerequisites)
    - [Step-by-Step Installation](#step-by-step-installation)
    - [Environment Configuration](#environment-configuration)
  - [📖 Usage](#-usage)
    - [Running the Application](#running-the-application)
    - [Input Methods](#input-methods)
    - [Configuration Options](#configuration-options)
  - [🔧 API Documentation](#-api-documentation)
    - [OpenAI Models Supported](#openai-models-supported)
    - [Azure Voice Options](#azure-voice-options)
  - [🔒 Security Features](#-security-features)
  - [🏗️ Architecture](#️-architecture)
  - [🧪 Testing](#-testing)
  - [📊 Performance](#-performance)
  - [🛣️ Roadmap](#️-roadmap)
  - [🤝 Contributing](#-contributing)
  - [📄 License](#-license)
  - [🙏 Acknowledgments](#-acknowledgments)
  - [📞 Support](#-support)

## ✨ Features

### 🤖 **AI-Powered Text Generation**
- **Latest OpenAI Models**: Support for GPT-4o, GPT-4o-mini, GPT-4-turbo, and GPT-3.5-turbo
- **Intelligent Text Processing**: Smart text truncation with sentence boundary detection
- **Customizable Parameters**: Adjustable creativity (temperature) and response length
- **Context-Aware Generation**: System prompts for consistent, high-quality output

### 🎤 **Advanced Text-to-Speech**
- **Azure Speech Services**: High-quality neural voices with natural intonation
- **Multiple Languages**: Support for English (US/UK), Spanish, French, and German
- **Voice Selection**: Choose from male and female voices with different characteristics
- **High-Quality Audio**: 16kHz MP3 output for clear, professional audio

### 🔒 **Security & Safety**
- **Input Validation**: Comprehensive validation for all user inputs
- **URL Security**: Protection against malicious URLs and local file access
- **File Upload Security**: Safe handling of uploaded files with type and size validation
- **XSS Protection**: Content sanitization to prevent cross-site scripting
- **Rate Limiting**: Built-in protections against API abuse
- **Secure Logging**: Comprehensive logging without exposing sensitive information

### 🖥️ **User-Friendly Interface**
- **Modern Web UI**: Clean, responsive Streamlit interface
- **Multiple Input Methods**: Text input, URL extraction, or file upload
- **Real-Time Preview**: View extracted content before processing
- **Audio Player**: Built-in audio playback with download options
- **Configuration Panel**: Easy-to-use sidebar for all settings
- **Progress Indicators**: Visual feedback during processing

### 🛠️ **Developer-Friendly**
- **Type Hints**: Full type annotation for better IDE support
- **Comprehensive Documentation**: Detailed docstrings and comments
- **Error Handling**: Robust error handling with informative messages
- **Logging**: Structured logging for debugging and monitoring
- **Modular Design**: Clean, maintainable code architecture

## 🎯 Use Cases

- **📚 Educational Content**: Convert articles and documents to audio for learning
- **♿ Accessibility**: Make written content accessible to visually impaired users
- **🎧 Content Creation**: Create audio content for podcasts or presentations
- **🌐 Content Summarization**: Generate summaries from web articles with audio output
- **📱 Mobile Learning**: Create audio versions of text content for on-the-go learning
- **🏢 Business Applications**: Convert reports and documents to audio for busy professionals

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/hipnologo/openai_azure_text2speech.git
cd openai_azure_text2speech

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the application
streamlit run app.py
```

## 🛠️ Installation

### Prerequisites

- **Python 3.8 or higher**
- **OpenAI API Key** - Get yours at [OpenAI Platform](https://platform.openai.com/api-keys)
- **Azure Speech Services Key** - Create at [Azure Portal](https://portal.azure.com/)

### Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/hipnologo/openai_azure_text2speech.git
   cd openai_azure_text2speech
   ```

2. **Create Virtual Environment** (Recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Verify Installation**
   ```bash
   python -c "import streamlit; import openai; import azure.cognitiveservices.speech; print('✅ All dependencies installed successfully!')"
   ```

### Environment Configuration

Create a `.env` file in the project root:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Azure Speech Services Configuration
AZURE_SPEECH_KEY=your_azure_speech_key_here
AZURE_SPEECH_REGION=your_azure_region_here

# Optional: Application Configuration
LOG_LEVEL=INFO
MAX_FILE_SIZE_MB=10
```

**Getting Your API Keys:**

1. **OpenAI API Key:**
   - Visit [OpenAI Platform](https://platform.openai.com/api-keys)
   - Create account or sign in
   - Navigate to "API Keys" section
   - Click "Create new secret key"

2. **Azure Speech Services:**
   - Go to [Azure Portal](https://portal.azure.com/)
   - Create a "Speech Services" resource
   - Copy the key and region from the resource

## 📖 Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`.

### Input Methods

#### 1. **Text Input**
- Direct text entry in the interface
- Maximum 50,000 characters
- Real-time character count
- Perfect for custom content

#### 2. **URL Extraction**
- Extract content from web articles
- Automatic content cleaning
- Security validation for URLs
- Support for most news sites and blogs

#### 3. **File Upload**
- Upload `.txt` files up to 10MB
- Automatic encoding detection
- Content preview before processing
- Secure file handling

### Configuration Options

| Setting | Description | Default | Range |
|---------|-------------|---------|-------|
| **OpenAI Model** | Choose the AI model | gpt-4o-mini | See supported models |
| **Max Tokens** | Response length limit | 1000 | 100-4000 |
| **Temperature** | Creativity level | 0.7 | 0.0-2.0 |
| **Voice** | Speech synthesis voice | en-US-AriaNeural | See voice options |

## 🔧 API Documentation

### OpenAI Models Supported

| Model | Description | Best For | Cost |
|-------|-------------|----------|------|
| **gpt-4o** | Most capable model | Complex reasoning, creative tasks | Higher |
| **gpt-4o-mini** | Balanced performance | General use, cost-effective | Lower |
| **gpt-4-turbo** | Fast, capable model | Most applications | Medium |
| **gpt-3.5-turbo** | Fast, efficient | Simple tasks, high volume | Lowest |

### Azure Voice Options

| Voice ID | Language | Gender | Description |
|----------|----------|---------|-------------|
| `en-US-AriaNeural` | English (US) | Female | Clear, professional |
| `en-US-GuyNeural` | English (US) | Male | Warm, friendly |
| `en-US-JennyNeural` | English (US) | Female | Expressive, natural |
| `en-GB-RyanNeural` | English (UK) | Male | British accent |
| `en-GB-SoniaNeural` | English (UK) | Female | British accent |
| `es-ES-ElviraNeural` | Spanish | Female | European Spanish |
| `fr-FR-DeniseNeural` | French | Female | European French |
| `de-DE-KatjaNeural` | German | Female | Standard German |

## 🔒 Security Features

- **🛡️ Input Validation**: All inputs are validated and sanitized
- **🚫 URL Security**: Protection against local file access and malicious URLs
- **📁 File Security**: Safe file handling with type and size restrictions
- **🔐 API Key Protection**: Secure credential management
- **🧹 XSS Prevention**: Content sanitization to prevent attacks
- **📊 Logging**: Security events are logged for monitoring
- **⏱️ Timeouts**: Network requests have timeout limits

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │───▶│  Input Handler  │───▶│  Content Parser │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Audio Output   │◀───│   OpenAI API    │◀───│ Security Layer  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Azure TTS     │    │ Config Manager  │    │ Logging System  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

## 📊 Performance

- **Text Generation**: 2-10 seconds depending on model and length
- **Speech Synthesis**: 1-5 seconds for typical text length
- **Memory Usage**: ~100-300MB during operation
- **Concurrent Users**: Supports multiple users (limited by API quotas)

## 🛣️ Roadmap

### Version 2.1.0 (Coming Soon)
- [ ] **Batch Processing**: Process multiple files simultaneously
- [ ] **Custom Voices**: Support for custom Azure voice models
- [ ] **Export Options**: Additional audio formats (WAV, OGG)
- [ ] **API Endpoint**: REST API for programmatic access

### Version 2.2.0 (Future)
- [ ] **Multi-language UI**: Interface translations
- [ ] **Voice Cloning**: ElevenLabs integration
- [ ] **Advanced Analytics**: Usage statistics dashboard
- [ ] **Webhook Support**: Integration with external services

### Long-term Goals
- [ ] **Mobile App**: React Native or Flutter app
- [ ] **Enterprise Features**: User management, billing
- [ ] **AI Optimization**: Model fine-tuning capabilities

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Contribution Steps

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Format code
black .
isort .
```

## 📄 License

This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[OpenAI](https://openai.com/)** for providing powerful language models
- **[Microsoft Azure](https://azure.microsoft.com/)** for Speech Services
- **[Streamlit](https://streamlit.io/)** for the amazing web framework
- **Contributors** who help improve this project

## 📞 Support

### 🐛 Found a Bug?
- Check existing [issues](https://github.com/hipnologo/openai_azure_text2speech/issues)
- Create a new issue with detailed description

### 💡 Feature Request?
- Open an [issue](https://github.com/hipnologo/openai_azure_text2speech/issues/new) with the `enhancement` label
- Describe the feature and its benefits

### 💬 Need Help?
- Check the [FAQ](https://github.com/hipnologo/openai_azure_text2speech/wiki/FAQ)
- Join our [Discussions](https://github.com/hipnologo/openai_azure_text2speech/discussions)

### 🌟 Show Your Support
If this project helped you, please consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting new features
- 🤝 Contributing code

---

<div align="center">

**Made with ❤️ by [Fabio Carvalho](https://github.com/hipnologo)**

<a href="https://www.buymeacoffee.com/hipnologod" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174">
</a>

*© 2024 OpenAI & Azure Text-to-Speech Application. All rights reserved.*

</div>
