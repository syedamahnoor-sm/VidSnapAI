# VidSnapAI 🎬

VidSnapAI is an AI-powered reel generation web application built using Python, Flask, FFmpeg, and ElevenLabs Text-to-Speech APIs.
The application allows users to upload images, generate AI voiceovers from text prompts, and automatically create vertical short-form videos suitable for platforms like TikTok, Instagram Reels, and YouTube Shorts.

---

# Features 🚀

* Upload multiple images
* Generate realistic AI voiceovers using ElevenLabs
* Automatically create short-form vertical videos
* Combine images and audio into reels using FFmpeg
* Reel gallery to preview generated videos
* Queue-based processing system
* Simple and lightweight Flask backend

---

# Tech Stack 🛠️

## Backend

* Python
* Flask

## Media Processing

* FFmpeg

## AI Services

* ElevenLabs Text-to-Speech API

## Frontend

* HTML
* CSS
* Bootstrap

---

# Project Workflow ⚙️

1. User uploads images
2. User enters text prompt/description
3. AI generates voice narration
4. Images and audio are processed using FFmpeg
5. Final reel is generated automatically
6. Reel is displayed in the gallery

---

# Folder Structure 📁

```bash
VidSnapAI/
│
├── static/
│   ├── reels/
│   └── css/
│
├── templates/
│
├── user_uploads/
│
├── main.py
├── generate_process.py
├── text_to_audio.py
├── requirements.txt
└── README.md
```

---

# Installation & Setup 💻

## 1. Clone Repository

```bash
git clone https://github.com/syedamahnoor9e-eng/VidSnapAI.git
cd VidSnapAI
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/Mac

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Install FFmpeg

Download and install FFmpeg:

### Windows

* Download FFmpeg
* Add FFmpeg `bin` path to Environment Variables

Verify installation:

```bash
ffmpeg -version
```

---

## 5. Configure ElevenLabs API Key

Create a `.env` file:

```env
ELEVENLABS_API_KEY=your_api_key_here
```

---

## 6. Run Flask Application

```bash
python main.py
```

---

## 7. Run Background Processing Script

Open another terminal:

```bash
python generate_process.py
```

---

# Requirements 📦

Some major dependencies:

* Flask
* requests
* python-dotenv
* FFmpeg
* ElevenLabs API

Install all using:

```bash
pip install -r requirements.txt
```

---

# Future Improvements 🔥

Planned features:

* User authentication
* AI subtitle generation
* Background music support
* Reel templates
* Modern dashboard UI
* Database integration
* Queue workers with Celery/Redis
* Cloud deployment
* API support

---

# Learning Outcomes 📚

This project helped in learning:

* Flask backend development
* File handling in Python
* AI API integration
* FFmpeg media processing
* Background task automation
* Video generation workflows
* Full-stack project structuring

---

# Author 👨‍💻

Developed by:

**Syeda Mahnoor**
BS Software Engineering Student

---

# License 📄

This project is developed for educational and portfolio purposes.
