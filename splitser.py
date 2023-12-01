import os
import subprocess

def get_video_duration(input_file):
    ffprobe_cmd = f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 \"{input_file}\""
    result = subprocess.run(ffprobe_cmd, shell=True, capture_output=True, text=True)
    duration = float(result.stdout)
    return duration

def split_video_by_size(input_file, output_pattern, min_segment_size):
    duration = get_video_duration(input_file)
    file_size = os.path.getsize(input_file)

    # Calculate the approximate number of segments required to meet the minimum size
    num_segments = max(file_size // min_segment_size, 1)
    segment_duration = duration / num_segments

    ffmpeg_cmd = f"ffmpeg -i \"{input_file}\" -c copy -f segment -segment_time {segment_duration} -reset_timestamps 1 -map 0 \"{output_pattern}\""
    subprocess.run(ffmpeg_cmd, shell=True)

def main():
    # Get folder path from user input
    folder_path = input("Enter the folder path containing the video files: ").strip()

    # Check if the folder path is valid
    if not os.path.isdir(folder_path):
        print("Invalid folder path. Please provide a valid path.")
        return

    # Minimum segment size in bytes (30MB)
    min_segment_size = 25 * 1024 * 1024  # 30MB in bytes

    # Get all video files in the folder
    video_files = [file for file in os.listdir(folder_path) if file.endswith('.mp4')]

    # Split each video file into segments with a minimum size of 30MB
    for file in video_files:
        input_file = os.path.join(folder_path, file)
        output_pattern = os.path.join(folder_path, f"{os.path.splitext(file)[0]}_segment_%03d.mp4")
        split_video_by_size(input_file, output_pattern, min_segment_size)

if __name__ == "__main__":
    main()
