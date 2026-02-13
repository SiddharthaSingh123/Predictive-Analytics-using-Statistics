import sys
from downloader import download_videos
from converter import convert_to_audio
from trimmer import trim_audio
from merger import merge_audio

def main():

    if len(sys.argv) != 5:
        print("Usage: python 102303838.py <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)

    singer = sys.argv[1]

    try:
        n = int(sys.argv[2])
        duration = int(sys.argv[3])
    except ValueError:
        print("NumberOfVideos and AudioDuration must be integers.")
        sys.exit(1)

    output = sys.argv[4]

    if n <= 10:
        print("NumberOfVideos must be greater than 10.")
        sys.exit(1)

    if duration <= 20:
        print("AudioDuration must be greater than 20 seconds.")
        sys.exit(1)

    try:
        print("Downloading videos...")
        download_videos(singer, n)

        print("Converting to audio...")
        audio_files = convert_to_audio()

        print("Trimming audio...")
        trimmed_files = trim_audio(audio_files, duration)

        print("Merging audio...")
        merge_audio(trimmed_files, output)

        print("Mashup created successfully:", output)

    except Exception as e:
        print("Error occurred:", str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
