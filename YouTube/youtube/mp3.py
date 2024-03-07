import subprocess


def convert_video_to_mp3(input_file, output_file):
    ffmpeg_cmd = ["ffmpeg",
                  "-i", input_file,
                  "-acodec", "libmp3lame",
                  "-ab", "192k",
                  "-ar", "44100",
                  "-y", output_file
                  ]

    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print("Conversion successful!")
    except subprocess.CalledProcessError as e:
        print("Conversion failed!")


convert_video_to_mp3("FULL TIMES  1 DE FEBRERO DE 2024.mp4", "FULL TIMES  1 DE FEBRERO DE 2024.mp3")
