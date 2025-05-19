import os
import streamlit as st
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from youtube_transcript_api.formatters import TextFormatter
from langchain.chains import RetrievalQA
# from langchain.vectorstores import FAISS
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
import google.generativeai as genai
import re

# Page config
st.set_page_config(
    page_title="YouTube Video Chat",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTextInput>div>div>input {
        font-size: 1.2rem;
    }
    .stButton>button {
        width: 100%;
        font-size: 1.2rem;
        background-color: #FF0000;
        color: white;
    }
    .stButton>button:hover {
        background-color: #CC0000;
    }
    .css-1d391kg {
        padding: 2rem 1rem;
    }
    .error-box {
        background-color: #ffebee;
        border: 1px solid #ffcdd2;
        border-radius: 4px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #e3f2fd;
        border: 1px solid #bbdefb;
        border-radius: 4px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .header-box {
        background-color: #f5f5f5;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .student-info {
        font-size: 1.1rem;
        color: #333;
        margin: 0.5rem 0;
    }
    .subject-info {
        font-size: 1.3rem;
        color: #1a237e;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .course-info {
        font-size: 1.1rem;
        color: #333;
        margin: 0.5rem 0;
    }
    .main-heading {
        text-align: center;
        color: #fff;
        font-size: 2.8rem;
        margin-top: 0.5rem;
        margin-bottom: 2.2rem;
        font-weight: 800;
        letter-spacing: 1px;
        text-shadow: 0 2px 16px #1a237e, 0 1px 1px #000;
        background: linear-gradient(90deg, #1a237e 0%, #3949ab 100%);
        border-radius: 18px;
        padding: 1.2rem 0 1.2rem 0;
        box-shadow: 0 4px 24px rgba(26,35,126,0.15);
    }
    .chat-section {
        background: #23272f;
        border-radius: 16px;
        padding: 2.2rem 2rem 2rem 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.12);
    }
    .chat-title {
        color: #fff;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1.2rem;
        text-shadow: 0 1px 8px #1a237e;
    }
    .answer-title {
        color: #90caf9;
        font-size: 1.3rem;
        font-weight: 700;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for API Key
with st.sidebar:
    st.title("⚙️ Settings")
    st.markdown("---")
    
    # API Key Input
    api_key = st.text_input(
        "Enter your Gemini API Key",
        type="password",
        help="Get your API key from https://makersuite.google.com/app/apikey"
    )
    
    st.markdown("---")
    st.markdown("### 📝 How to use")
    st.markdown("""
    1. Enter your Gemini API key
    2. Paste a YouTube video URL
    3. Wait for the transcript to load
    4. Ask questions about the video
    """)
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    This app uses Gemini AI to chat about YouTube videos.
    Make sure the video has captions enabled.
    """)

# Main project heading (always visible)
st.markdown("""
    <div class='main-heading'>
        🎬 Chat With YouTube Video
    </div>
""", unsafe_allow_html=True)

# Only show intro/header if API key is NOT entered
if not api_key:
    # Header with Student Information
    st.markdown("""
        <div class="header-box">
            <h1 style="text-align: center; color: #1a237e; margin-bottom: 1rem;">🏛️Air University Islamabad</h1>  
            <div style="text-align: center;">
                <p class="student-info">👨‍🎓 <strong>Student Name:</strong> Sham Lal</p>
                <p class="subject-info">🎓 <strong>Subject Name:</strong> Information Retrieval</p>
                <p class="course-info">📚 BSAI 4th Semester</p>
                <p class="course-info">👩‍🏫 <strong>Instructor:</strong> Ma'am Faiza</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.title("🎥 Chat with YouTube Video")
    st.markdown("Chat with any YouTube video using Gemini AI!")
    st.info("""
        <div style='text-align:center; font-size:1.2rem;'>
            <b>👋 Welcome! Please enter your Gemini API key in the sidebar to get started.</b>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# --- Chatbot interface below this line ---

# Configure the Gemini API
genai.configure(api_key=api_key)

# Initialize Gemini Model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=api_key,
    temperature=0.4,
    convert_system_message_to_human=True,
    safety_settings={
        1: 2,  # HARM_CATEGORY_HARASSMENT: BLOCK_MEDIUM_AND_ABOVE
        2: 2,  # HARM_CATEGORY_HATE_SPEECH: BLOCK_MEDIUM_AND_ABOVE
        3: 2,  # HARM_CATEGORY_SEXUALLY_EXPLICIT: BLOCK_MEDIUM_AND_ABOVE
        4: 2   # HARM_CATEGORY_DANGEROUS_CONTENT: BLOCK_MEDIUM_AND_ABOVE
    }
)

embed_model = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=api_key
)

# Get YouTube URL
youtube_url = st.text_input(
    "Enter YouTube Video URL",
    placeholder="https://www.youtube.com/watch?v=..."
)

# Extract video ID from the link
def extract_video_id(url):
    if not url:
        return None
        
    # Regular expression to match YouTube video IDs
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',
        r'(?:embed\/)([0-9A-Za-z_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

# Fetch transcript and process
def get_transcript_text(video_id):
    try:
        # Try to get available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Try to get English transcript first
        try:
            transcript = transcript_list.find_transcript(['en'])
        except:
            # If no English transcript, get the first available one
            transcript = transcript_list.find_transcript(['en-US', 'en-GB', 'en-CA', 'en-AU'])
        
        # Get the transcript
        transcript_data = transcript.fetch()
        
        # Format the transcript
        formatter = TextFormatter()
        formatted_transcript = formatter.format_transcript(transcript_data)
        
        return formatted_transcript
        
    except TranscriptsDisabled:
        st.error("""
        🚫 This video has captions disabled.
        
        Please try a different video that has captions enabled. You can check if a video has captions by:
        1. Looking for the CC (Closed Captions) button in YouTube
        2. Checking if the video has auto-generated captions
        """)
        st.stop()
    except NoTranscriptFound:
        st.error("""
        🚫 No captions found for this video.
        
        Please try a different video that has captions available. You can:
        1. Try a different video
        2. Check if the video has captions enabled
        3. Look for videos with auto-generated captions
        """)
        st.stop()
    except Exception as e:
        st.error(f"""
        🚫 Error: {str(e)}
        
        This might be because:
        1. The video is private or restricted
        2. The video doesn't exist
        3. There's an issue with the YouTube API
        
        Please try a different video URL.
        """)
        st.stop()

# Main logic
if youtube_url:
    try:
        video_id = extract_video_id(youtube_url)
        if not video_id:
            st.error("""
            🚫 Invalid YouTube URL.
            
            Please enter a valid YouTube video URL. It should look like:
            - https://www.youtube.com/watch?v=VIDEO_ID
            - https://youtu.be/VIDEO_ID
            """)
        else:
            with st.spinner("🔍 Checking video and fetching transcript..."):
                raw_text = get_transcript_text(video_id)

                # Split text and embed
                splitter = CharacterTextSplitter(separator=". ", chunk_size=1000, chunk_overlap=200)
                texts = splitter.split_text(raw_text)
                docs = [Document(page_content=t) for t in texts]

                # Vector store
                db = FAISS.from_documents(docs, embed_model)
                retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 5})

                # QA chain
                chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

            st.success("✅ Transcript fetched! Ask your questions below.")

            # Chat interface
            st.markdown("### 💬 Chat")
            query = st.text_input("Ask a question about the video:", key="query")
            
            if query:
                with st.spinner("🤔 Thinking..."):
                    response = chain.run(query)
                    st.markdown("#### Answer:")
                    st.write(response)

    except Exception as e:
        st.error(f"""
        🚫 An unexpected error occurred: {str(e)}
        
        Please try:
        1. Using a different video
        2. Checking your internet connection
        3. Refreshing the page
        """)
