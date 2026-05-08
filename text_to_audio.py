import asyncio
import edge_tts
import os


async def generate_audio(text, output_file):

    communicate = edge_tts.Communicate(
        text=text,
        voice="en-US-JennyNeural"
    )

    await communicate.save(output_file)


def text_to_speech_file(text: str, folder: str) -> str:

    save_file_path = os.path.join(
        f"user_uploads/{folder}",
        "audio.mp3"
    )

    asyncio.run(
        generate_audio(text, save_file_path)
    )

    print(f"{save_file_path}: Audio generated successfully!")

    return save_file_path