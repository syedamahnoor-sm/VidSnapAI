import os
import sys
import subprocess

from flask import Flask

from database import db
from models import Reel

from text_to_audio import text_to_speech_file

# =========================
# Flask App Setup
# =========================

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vidsnap.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# =========================
# Get Reel ID from main.py
# =========================

reel_id = int(sys.argv[1])


# =========================
# Text To Audio Function
# =========================


def text_to_audio(reel, folder):

    print("Generating Audio For:", folder)

    text = reel.description

    print("TEXT:", text)

    audio_path = os.path.join("user_uploads", folder, "audio.mp3")

    # Generate audio using Edge-TTS
    text_to_speech_file(text, folder)

    # Save audio path in DB
    reel.audio_path = audio_path

    db.session.commit()

    print("Audio Generated")


# =========================
# Reel Creation Function
# =========================


def create_reel(reel, folder):

    folder_path = f"user_uploads/{folder}"

    # =========================
    # Find Uploaded Image
    # =========================

    image_file = None

    for file in os.listdir(folder_path):

        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            image_file = file
            break

    if not image_file:
        raise Exception("No image file found")

    image_path = os.path.join(folder_path, image_file)

    audio_path = os.path.join(folder_path, "audio.mp3")

    output_path = f"static/reels/{folder}.mp4"

    # =========================
    # FFmpeg Command
    # =========================
    print(os.path.exists(audio_path))
    command = [
        "ffmpeg",
        "-y",
        "-loop",
        "1",
        "-i",
        image_path,
        "-i",
        audio_path,
        "-vf",
        "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2:black",
        "-c:v",
        "libx264",
        "-preset",
        "ultrafast",
        "-tune",
        "stillimage",
        "-r",
        "15",
        "-c:a",
        "aac",
        "-shortest",
        "-pix_fmt",
        "yuv420p",
        output_path,
    ]

    print("Running FFmpeg Command...")
    print("Image Path:", image_path)
    print("Audio Path:", audio_path)
    print("Output Path:", output_path)
    subprocess.run(command, check=True)

    print("Reel Generated")

    # =========================
    # Save Video Path in DB
    # =========================

    reel.video_path = output_path

    reel.status = "completed"

    db.session.commit()


# =========================
# Main Processing Logic
# =========================

if __name__ == "__main__":

    with app.app_context():

        # =========================
        # Fetch Reel From Database
        # =========================

        reel = Reel.query.get(reel_id)

        if not reel:

            print("Reel Not Found")

            sys.exit(1)

        try:

            print("Processing Reel ID:", reel.id)

            # =========================
            # Get Folder Name
            # =========================

            folder = reel.title.replace("Reel-", "")

            # =========================
            # Update Status
            # =========================

            reel.status = "processing"

            db.session.commit()

            # =========================
            # Generate Audio
            # =========================

            text_to_audio(reel, folder)

            # =========================
            # Generate Video Reel
            # =========================

            create_reel(reel, folder)

            print("Processing Completed")

        except Exception as e:

            reel.status = "failed"

            db.session.commit()

            print("ERROR:", e)
