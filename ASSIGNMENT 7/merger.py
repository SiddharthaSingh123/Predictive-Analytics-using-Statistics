from pydub import AudioSegment

def merge_audio(files, output_path):

    combined = AudioSegment.empty()

    for file in files:
        sound = AudioSegment.from_mp3(file)
        combined += sound

    combined.export(output_path, format="mp3")
