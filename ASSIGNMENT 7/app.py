import os
import zipfile
import shutil
from flask import Flask, render_template, request
from downloader import download_videos
from converter import convert_to_audio
from trimmer import trim_audio
from merger import merge_audio
from mailer import send_email

app = Flask(__name__)

BASE_DIR = "workspace"

def clean_workspace():
    if os.path.exists(BASE_DIR):
        shutil.rmtree(BASE_DIR)
    os.makedirs(BASE_DIR)
    os.makedirs(os.path.join(BASE_DIR, "downloads"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create", methods=["POST"])
def create():

    singer = request.form.get("singer")
    videos = request.form.get("videos")
    duration = request.form.get("duration")
    email = request.form.get("email")

    if not singer or not videos or not duration or not email:
        return "All fields are required."

    try:
        n = int(videos)
        d = int(duration)
    except:
        return "Videos and Duration must be integers."

    if n <= 10:
        return "Number of videos must be greater than 10."

    if d <= 20:
        return "Duration must be greater than 20 seconds."

    try:
        clean_workspace()

        download_videos(singer, n, BASE_DIR)
        audio_files = convert_to_audio(BASE_DIR)
        trimmed_files = trim_audio(audio_files, d)
        
        output_path = os.path.join(BASE_DIR, "mashup.mp3")
        merge_audio(trimmed_files, output_path)

        zip_path = os.path.join(BASE_DIR, "mashup.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            zipf.write(output_path, "mashup.mp3")

        send_email(email, zip_path)

        return "Mashup created and sent successfully!"

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
