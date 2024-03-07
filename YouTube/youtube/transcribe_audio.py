import whisper

model = whisper.load_model("medium")
result = model.transcribe("Erick.mp3")


with open("transcription.txt", "w") as f:
    if isinstance(result["text"], list):
        # Join the list into a single string separated by newlines
        f.write("\n".join(result["text"]))
    else:
        # It's already a string, write as is
        f.write(result["text"])
