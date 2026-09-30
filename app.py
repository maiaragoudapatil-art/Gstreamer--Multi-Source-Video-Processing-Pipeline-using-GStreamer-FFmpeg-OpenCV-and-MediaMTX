import cv2
import numpy as np
import os
import math
import subprocess

# ------------------------
# CONFIG
# ------------------------

VIDEO_FOLDER = "videos"
OUTPUT_FOLDER = "outputs"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

TEMP_OUTPUT = os.path.join(
    OUTPUT_FOLDER,
    "combined_temp.mp4"
)

FINAL_OUTPUT = os.path.join(
    OUTPUT_FOLDER,
    "combined.mp4"
)

# ------------------------
# FIND VIDEOS
# ------------------------

video_files = [
    os.path.join(VIDEO_FOLDER, f)
    for f in os.listdir(VIDEO_FOLDER)
    if f.lower().endswith(".mp4")
]

if not video_files:
    print("No videos found!")
    exit()

print(f"Found {len(video_files)} videos")

# ------------------------
# OPEN VIDEOS
# ------------------------

caps = []

for video in video_files:

    cap = cv2.VideoCapture(video)

    if not cap.isOpened():
        print(f"Failed: {video}")
        continue

    print(f"Opened: {video}")
    caps.append(cap)

if not caps:
    print("No valid videos found!")
    exit()

# ------------------------
# GRID SETUP
# ------------------------

cell_w = 640
cell_h = 360

num_videos = len(caps)

cols = math.ceil(math.sqrt(num_videos))
rows = math.ceil(num_videos / cols)

output_width = cols * cell_w
output_height = rows * cell_h

fps = caps[0].get(cv2.CAP_PROP_FPS)

if fps <= 0:
    fps = 25

print(f"FPS: {fps}")

# ------------------------
# DELETE OLD FILES
# ------------------------

for file in [TEMP_OUTPUT, FINAL_OUTPUT]:
    if os.path.exists(file):
        os.remove(file)

# ------------------------
# VIDEO WRITER
# ------------------------

out = cv2.VideoWriter(
    TEMP_OUTPUT,
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (output_width, output_height)
)

if not out.isOpened():
    print("Failed to create VideoWriter")
    exit()

print("Processing started...")

# ------------------------
# COMBINE VIDEOS
# ------------------------

while True:

    frames = []
    active_frames = 0

    for i, cap in enumerate(caps):

        ret, frame = cap.read()

        if ret:

            active_frames += 1

            frame = cv2.resize(
                frame,
                (cell_w, cell_h)
            )

            name = os.path.basename(
                video_files[i]
            )

            cv2.putText(
                frame,
                name,
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        else:

            frame = np.zeros(
                (cell_h, cell_w, 3),
                dtype=np.uint8
            )

            cv2.putText(
                frame,
                "Video Ended",
                (150, 180),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

        frames.append(frame)

    if active_frames == 0:
        break

    while len(frames) < rows * cols:

        frames.append(
            np.zeros(
                (cell_h, cell_w, 3),
                dtype=np.uint8
            )
        )

    row_frames = []

    for r in range(rows):

        start = r * cols
        end = start + cols

        row = np.hstack(
            frames[start:end]
        )

        row_frames.append(row)

    combined = np.vstack(row_frames)

    out.write(combined)

    cv2.imshow(
        "Combined Video",
        combined
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# ------------------------
# CLEANUP
# -----------------------

for cap in caps:
    cap.release()

out.release()
cv2.destroyAllWindows()

print("Combination complete.")
print("Converting to H264...")

# ------------------------
# MP4V -> H264
# ------------------------

ffmpeg_cmd = [
    "ffmpeg",
    "-y",
    "-i",
    TEMP_OUTPUT,
    "-c:v",
    "libx264",
    "-preset",
    "fast",
    "-crf",
    "23",
    "-pix_fmt",
    "yuv420p",
    FINAL_OUTPUT
]

subprocess.run(ffmpeg_cmd)

print()
print("Done!")
print(f"H264 Output: {FINAL_OUTPUT}")