# VidSnapAI 🎬

VidSnapAI is an AI-powered reel generation web application built using Python, Flask, SQLite, FFmpeg, and Microsoft Edge-TTS. The application allows users to upload images, generate AI voiceovers from text prompts, and automatically create vertical short-form videos suitable for platforms like TikTok, Instagram Reels, and YouTube Shorts.

---

# Features 🚀

* Upload images for reel generation
* Generate realistic AI voiceovers using Edge-TTS
* Automatically create short-form vertical videos
* Combine images and audio into reels using FFmpeg
* Database-driven reel management using SQLite
* Automatic reel status updates (Processing → Completed)
* Dynamic reel gallery with auto-refresh
* Background reel processing system
* Lightweight Flask backend architecture
* Responsive gallery UI

---

# Tech Stack 🛠️

## Backend

* Python
* Flask
* Flask-SQLAlchemy

## Database

* SQLite

## Media Processing

* FFmpeg

## AI Services

* Microsoft Edge-TTS

## Frontend

* HTML
* CSS
* Bootstrap
* Vanilla JavaScript

---

# Project Workflow ⚙️

1. User uploads image
2. User enters text prompt/description
3. Reel metadata is stored in SQLite database
4. Edge-TTS generates AI voice narration
5. FFmpeg combines image + audio into vertical reel
6. Reel status updates automatically
7. Final reel appears in gallery dynamically

---

# Architecture Improvements 🔥

This project was upgraded from a folder-based architecture to a database-driven workflow.

### Previous Architecture

* `desc.txt`
* `done.txt`
* folder scanning queue

### Current Architecture

* SQLite database
* SQLAlchemy models
* Reel status tracking
* Database-driven gallery
* Dynamic processing updates

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
├── database.py
├── models.py
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
git clone https://github.com/syedamahnoor-sm/VidSnapAI.git

cd VidSnapAI
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 4. Install FFmpeg

Download and install FFmpeg:

## Windows

* Download FFmpeg
* Add FFmpeg `bin` path to Environment Variables

Verify installation:

```bash
ffmpeg -version
```

---

# 5. Run Flask Application

```bash
python main.py
```

---

# Requirements 📦

Major dependencies:

* Flask
* Flask-SQLAlchemy
* edge-tts
* FFmpeg
* gunicorn

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

# Future Improvements 🔥

Planned future upgrades:

* User authentication
* AI subtitle generation
* Background music support
* Multiple image slideshow reels
* Reel templates
* PostgreSQL integration
* Cloudinary/S3 storage
* Celery & Redis queue workers
* Download reel feature
* AI thumbnail generation

---

# Learning Outcomes 📚

This project helped in learning:

* Flask backend development
* SQLite database integration
* SQLAlchemy ORM
* AI/TTS integration
* FFmpeg media processing
* Background processing workflows
* Dynamic frontend updates
* Full-stack project structuring
* Deployment workflows

---

# Author 👨‍💻

Developed by:

**Syeda Mahnoor**
BS Software Engineering Student

---

# License 📄

This project is developed for educational and portfolio purposes.
