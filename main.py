from flask import Flask, render_template, request, redirect
import uuid
from werkzeug.utils import secure_filename
import os
import subprocess
import sys

UPLOAD_FOLDER = "user_uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs("user_uploads", exist_ok=True)
os.makedirs("static/reels", exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/create", methods=["GET", "POST"])
def create():
    myid = uuid.uuid4()

    if request.method == "POST":

        rec_id = request.form.get("uuid")
        desc = request.form.get("text")

        input_files = []

        upload_path = os.path.join(app.config["UPLOAD_FOLDER"], rec_id)
        os.makedirs(upload_path, exist_ok=True)

        for key, value in request.files.items():

            file = request.files[key]

            if file and allowed_file(file.filename):

                filename = secure_filename(file.filename)

                file.save(os.path.join(upload_path, filename))

                input_files.append(filename)

                print("Saved:", filename)

        # Save description
        with open(os.path.join(upload_path, "desc.txt"), "w") as f:
            f.write(desc)

        # Create input.txt
        with open(os.path.join(upload_path, "input.txt"), "w") as f:
            for fl in input_files:
                f.write(f"file '{fl}'\n")
                f.write("duration 1\n")

        print("input.txt created")

        subprocess.Popen([sys.executable, "generate_process.py"])
    return redirect("/gallery")


@app.route("/gallery")
def gallery():
    reels = os.listdir("static/reels")
    return render_template("gallery.html", reels=reels)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)