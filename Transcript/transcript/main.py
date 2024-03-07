from whispercpp import Whisper

w = Whisper('small')

result = w.transcribe("video.mp3")
text = w.extract_text(result)

# Writing the transcribed text to a .txt file
with open("transcription.txt", "w", encoding="utf-8") as file:
    file.write(text)

print("Transcription saved to transcription.txt.")
