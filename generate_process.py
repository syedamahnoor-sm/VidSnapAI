# This file looks for new folders inside user_uploads
# and converts them to reels if not already processed

import os
import subprocess

from text_to_audio import text_to_speech_file


def text_to_audio(folder):

    print("TTA - ", folder)

    with open(f"user_uploads/{folder}/desc.txt") as f:
        text = f.read()

    print(text, folder)

    text_to_speech_file(text, folder)


def create_reel(folder):

    folder_path = f"user_uploads/{folder}"

    # Find uploaded image dynamically
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

    command = f""" ffmpeg -y -loop 1 -i "{image_path}" -i "{audio_path}" \
                -vf "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2:black" \
                -c:v libx264 \
                -preset ultrafast \
                -tune stillimage \
                -r 15 \
                -c:a aac \
                -shortest \
                -pix_fmt yuv420p \
                "{output_path}"
                """

    print("Running FFmpeg command...")

    subprocess.run(command, shell=True, check=True)

    print("CR - ", folder)


if __name__ == "__main__":

    # Create done.txt if missing
    if not os.path.exists("done.txt"):

        with open("done.txt", "w") as f:
            pass

    print("Processing queue...")

    with open("done.txt", "r") as f:
        done_folders = f.readlines()

    done_folders = [f.strip() for f in done_folders]

    folders = os.listdir("user_uploads")

    for folder in folders:

        if folder not in done_folders:

            try:

                text_to_audio(folder)

                create_reel(folder)

                with open("done.txt", "a") as f:
                    f.write(folder + "\n")

                print("DONE - ", folder)

            except Exception as e:

                print("ERROR PROCESSING:", folder)

                print(e)
