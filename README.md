# 🎬 Chat With YouTube Video

Welcome to the **Chat With YouTube Video** project! This web application allows you to interactively chat with the content of any YouTube video that has captions, using Google Gemini AI. It's designed for students, educators, and anyone who wants to quickly understand or explore the content of YouTube videos through natural language questions.

---

## 📖 Project Overview

This project was developed as part of the **Information Retrieval** course at Air University Islamabad, BSAI 4th Semester, under the guidance of Ma'am Faiza. The main goal is to demonstrate how modern AI can be used to extract, process, and interact with multimedia content in a user-friendly way.

---

## 👨‍💻 Features

- **Ask Anything:** Paste a YouTube video link and ask questions about its content.
- **AI-Powered:** Uses Google Gemini AI for intelligent, context-aware answers.
- **Modern UI:** Clean, attractive, and responsive interface built with Streamlit.
- **Secure:** Your API key is never stored and is only used for your session.
- **Error Handling:** Friendly messages if captions are missing or the video is not supported.

---

## ⚠️ Important Note About YouTube API Access

When using the app on Streamlit Cloud, you might encounter YouTube API access limitations. This is because:

1. YouTube restricts access from cloud platform IPs
2. Some videos might be temporarily unavailable
3. Rate limiting might occur

**Solutions:**
- Try different videos
- Wait a few minutes between attempts
- Use videos from channels that typically have good caption support
- If issues persist, try running the app locally

---

## 🚀 How to Use

1. **Get a Gemini API Key:**  
   - Visit [Google MakerSuite](https://makersuite.google.com/app/apikey) and generate your API key.

2. **Run the App Locally:**  
   - Clone this repository:
     ```bash
     git clone https://github.com/shamlal-12/YouTubeVideoChatbot.git
     cd YouTubeVideoChatbot
     ```
   - Install the requirements:
     ```bash
     pip install -r requirements.txt
     ```
   - Start the app:
     ```bash
     streamlit run app.py
     ```

3. **Interact:**  
   - Enter your Gemini API key in the sidebar.
   - Paste a YouTube video URL (make sure the video has captions).
   - Wait for the transcript to load.
   - Ask any question about the video content and get instant answers!

---

## 🏛️ Project Details

- **Student Name:** Sham Lal  
- **University:** Air University Islamabad  
- **Subject:** Information Retrieval  
- **Semester:** BSAI 4th Semester  
- **Instructor:** Ma'am Faiza

---

## 📝 Notes

- The app only works with YouTube videos that have captions (either auto-generated or uploaded).
- Your API key is required for Gemini AI access. It is not stored or shared.
- For deployment on [Streamlit Cloud](https://streamlit.io/cloud), push your code to this repository and connect it to Streamlit.

---

## 📂 Repository Structure

```
YouTubeVideoChatbot/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .gitignore          # Files and folders to ignore in git
└── README.md           # Project documentation
```

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome!  
Feel free to open an issue or submit a pull request.

---

## 📄 License

This project is for educational purposes.

---

If you have any questions or need help, please open an issue on this repository.
