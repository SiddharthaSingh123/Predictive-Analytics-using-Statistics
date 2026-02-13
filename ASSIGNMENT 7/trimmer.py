from pydub import AudioSegment

def trim_audio(files, duration):

    trimmed_files = []

    for file in files:
        try:
            sound = AudioSegment.from_file(file)
            trimmed = sound[:duration * 1000]
            trimmed.export(file, format="mp3")
            trimmed_files.append(file)
        except:
            continue

    return trimmed_files
