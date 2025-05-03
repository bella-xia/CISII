import ffmpeg, os


def convert_mkv_to_mp4(input_file, output_file):
    try:
        ffmpeg.input(input_file).output(
            output_file, vcodec="libx264", acodec="aac"
        ).run()
        print(f"Successfully converted {input_file} to {output_file}")
    except ffmpeg.Error as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    input_dir = "C:/Users/zhiha/OneDrive/Desktop/Lab/CIS II/data"
    mkv_videos = [file for file in os.listdir(input_dir) if file.endswith(".mkv")]
    print(mkv_videos)
    for mkv_video in mkv_videos:
        convert_mkv_to_mp4(mkv_video, mkv_video.replace(".mkv", ".mp4"))
