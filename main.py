from flask import Flask, render_template, request
import uuid
from werkzeug.utils import secure_filename
import os
import subprocess
import sys

from database import db
from models import Reel

UPLOAD_FOLDER = "user_uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__)

# =========================
# Flask Configurations
# =========================

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vidsnap.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# =========================
# Initialize Database
# =========================

db.init_app(app)

with app.app_context():
    db.create_all()

# =========================
# Create Required Folders
# =========================

os.makedirs("user_uploads", exist_ok=True)
os.makedirs("static/reels", exist_ok=True)


# =========================
# Allowed File Checker
# =========================


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# =========================
# Home Route
# =========================


@app.route("/")
def home():
    return render_template("index.html")


# =========================
# Create Reel Route
# =========================


@app.route("/create", methods=["GET", "POST"])
def create():

    myid = uuid.uuid4()

    if request.method == "POST":

        rec_id = request.form.get("uuid")
        desc = request.form.get("text")

        # Create upload path
        upload_path = os.path.join(app.config["UPLOAD_FOLDER"], rec_id)

        os.makedirs(upload_path, exist_ok=True)

        # =========================
        # Save Uploaded Images
        # =========================

        for key, value in request.files.items():

            file = request.files[key]

            if file and allowed_file(file.filename):

                filename = secure_filename(file.filename)

                file.save(os.path.join(upload_path, filename))

                print("Saved:", filename)

        # =========================
        # Save Reel Data in Database
        # =========================

        new_reel = Reel(title=f"Reel-{rec_id}", description=desc, status="processing")

        db.session.add(new_reel)
        db.session.commit()

        print("Reel saved in database")
        print("Reel ID:", new_reel.id)

        # =========================
        # Start Reel Generation
        # =========================

        subprocess.Popen([sys.executable, "generate_process.py", str(new_reel.id)])

    return render_template("create.html", myid=myid)


# =========================
# Gallery Route
# =========================


@app.route("/gallery")
def gallery():

    reels = Reel.query.all()

    return render_template("gallery.html", reels=reels)


# =========================
# Run App
# =========================


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
