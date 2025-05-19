# YouTube Video Chat with Gemini AI

A Streamlit application that allows you to chat with any YouTube video using Google's Gemini AI. The app uses video transcripts to answer questions about the video content.

## Features

- 🤖 Powered by Google's Gemini AI
- 🎥 Works with any YouTube video that has captions
- 💬 Interactive chat interface
- 🔒 Secure API key handling
- 🎨 Beautiful and responsive UI

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/youtube-video-chat.git
cd youtube-video-chat
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Get your Gemini API key:
   - Go to https://makersuite.google.com/app/apikey
   - Create a new API key
   - Copy the key

## Running Locally

Run the Streamlit app:
```bash
streamlit run app.py
```

## Deployment

1. Create a GitHub repository
2. Push your code to GitHub
3. Go to [Streamlit Cloud](https://streamlit.io/cloud)
4. Create a new app and connect your GitHub repository
5. Deploy!

## Usage

1. Enter your Gemini API key in the sidebar
2. Paste a YouTube video URL
3. Wait for the transcript to load
4. Ask questions about the video content

## Requirements

- Python 3.8+
- Streamlit
- LangChain
- Google Generative AI
- YouTube Transcript API
- FAISS

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
