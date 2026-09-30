import cv2
import numpy as np
import os
import math
import subprocess

# Create output folder
os.makedirs("outputs", exist_ok=True)

# Get all MP4 videos
video_folder = "videos"

video_files = [
    os.path.join(video_folder, f)
    for f in os.listdir(video_folder)
    if f.lower().endswith(".mp4")
]

if not video_files:
    print("No videos found!")
    exit()

print(f"Found {len(video_files)} videos")

# Open videos
caps = [
    cv2.VideoCapture(url)
    for url in rtsp_urls
]

# Cell size
cell_w = 640
cell_h = 360

# Calculate grid
num_videos = len(caps)
cols = math.ceil(math.sqrt(num_videos))
rows = math.ceil(num_videos / cols)

output_width = cols * cell_w
output_height = rows * cell_h

# FPS
fps = caps[0].get(cv2.CAP_PROP_FPS)

if fps <= 0:
    fps = 25

temp_output = "outputs/combined_temp.mp4"
final_output = "outputs/combined.mp4"

# Remove old files
for file in [temp_output, final_output]:
    if os.path.exists(file):
        os.remove(file)

# OpenCV writes MP4V
out = cv2.VideoWriter(
    temp_output,
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (output_width, output_height)
)

print("Processing started...")

while True:
    frames = []
    active_frames = 0

    for i, cap in enumerate(caps):
        ret, frame = cap.read()

        if ret:
            active_frames += 1

            frame = cv2.resize(frame, (cell_w, cell_h))

            # Display filename
            filename = rtsp_urls[i].split("/")[-1]

            cv2.putText(
                frame,
                filename,
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        else:
            frame = np.zeros((cell_h, cell_w, 3), dtype=np.uint8)

            cv2.putText(
                frame,
                "Video Ended",
                (180, 180),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

        frames.append(frame)

    # stop when all videos finished
    if active_frames == 0:
        break

    # fill blank slots
    while len(frames) < rows * cols:
        frames.append(
            np.zeros((cell_h, cell_w, 3), dtype=np.uint8)
        )

    grid_rows = []

    for r in range(rows):
        start = r * cols
        end = start + cols

        row = np.hstack(frames[start:end])
        grid_rows.append(row)

    combined = np.vstack(grid_rows)

    out.write(combined)

    cv2.imshow("Combined Video", combined)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
for cap in caps:
    cap.release()

out.release()
cv2.destroyAllWindows()

print("Video combination completed.")
print("Converting to H.264...")

ffmpeg_cmd = [
    "ffmpeg",
    "-y",
    "-i",
    temp_output,
    "-c:v",
    "libx264",
    "-preset",
    "fast",
    "-crf",
    "23",
    "-pix_fmt",
    "yuv420p",
    final_output
]

subprocess.run(ffmpeg_cmd)

# Cleanup RTSP publishers
for process in publishers:
    process.terminate()

print("\nDone!")
print(f"H264 Output: {final_output}")