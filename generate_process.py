# This file looks for new folders inside user_uploads
# and converts them to reels if not already processed

import os
import time
import subprocess

from text_to_audio import text_to_speech_file


def text_to_audio(folder):

    print("TTA - ", folder)

    with open(f"user_uploads/{folder}/desc.txt") as f:
        text = f.read()

    print(text, folder)

    text_to_speech_file(text, folder)


def create_reel(folder):

    command = f"""ffmpeg -f concat -safe 0 -i user_uploads/{folder}/input.txt -i user_uploads/{folder}/audio.mp3 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p static/reels/{folder}.mp4"""

    print("Running FFmpeg command...")

    subprocess.run(command, shell=True, check=True)

    print("CR - ", folder)


if __name__ == "__main__":

    # Create done.txt if missing
    if not os.path.exists("done.txt"):
        with open("done.txt", "w") as f:
            pass

    while True:

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

        time.sleep(4)
