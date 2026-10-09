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
MAX_TEXT_LENGTH = 1000

app = Flask(__name__)

# =========================
# Flask Configurations
# =========================

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # reject request bodies over 10 MB
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

        def reject(message):
            return render_template("create.html", myid=myid, error=message), 400

        # The folder name comes from the browser, so it must be a real UUID.
        # (An unchecked value such as "../../x" would let a request write
        # files outside the uploads folder.) str() normalises the format.
        try:
            rec_id = str(uuid.UUID(request.form.get("uuid", "")))
        except ValueError:
            return reject("Invalid request. Please reload the page and try again.")

        desc = (request.form.get("text") or "").strip()

        if not desc:
            return reject("Please enter the text to be used for the voiceover.")

        if len(desc) > MAX_TEXT_LENGTH:
            return reject(f"Text is too long (max {MAX_TEXT_LENGTH} characters).")

        # Only create the folder once the request is known to be valid
        upload_path = os.path.join(app.config["UPLOAD_FOLDER"], rec_id)

        # =========================
        # Save Uploaded Images
        # =========================

        saved_images = []

        for key, file in request.files.items():

            if file and allowed_file(file.filename):

                os.makedirs(upload_path, exist_ok=True)

                filename = secure_filename(file.filename)

                file.save(os.path.join(upload_path, filename))

                saved_images.append(filename)

                print("Saved:", filename)

        if not saved_images:
            return reject("Please upload at least one PNG or JPG image.")

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


@app.errorhandler(413)
def too_large(_error):
    return render_template(
        "create.html",
        myid=uuid.uuid4(),
        error="Upload too large (max 10 MB in total).",
    ), 413


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
    # The Werkzeug debugger allows code execution, so it must never be on in
    # production. Opt in locally with:  FLASK_DEBUG=1 python main.py
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=os.environ.get("FLASK_DEBUG") == "1",
    )
