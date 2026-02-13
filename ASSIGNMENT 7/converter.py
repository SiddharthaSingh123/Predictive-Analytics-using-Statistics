import os
from moviepy.editor import AudioFileClip

def convert_to_audio(base_dir):

    download_path = os.path.join(base_dir, "downloads")
    audio_files = []

    for file in os.listdir(download_path):
        file_path = os.path.join(download_path, file)

        try:
            audio = AudioFileClip(file_path)
            mp3_path = file_path.rsplit(".", 1)[0] + ".mp3"
            audio.write_audiofile(mp3_path, verbose=False, logger=None)
            audio.close()
            audio_files.append(mp3_path)
        except:
            continue

    return audio_files
