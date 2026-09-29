import cv2
import numpy as np
import os
import math

# Create output folder
os.makedirs("outputs", exist_ok=True)

# Get all mp4 videos
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

# Open all videos
caps = [cv2.VideoCapture(v) for v in video_files]

# Frame size for each video
cell_w = 640
cell_h = 360

# Determine grid size
num_videos = len(caps)
cols = math.ceil(math.sqrt(num_videos))
rows = math.ceil(num_videos / cols)

output_width = cols * cell_w
output_height = rows * cell_h

# Use FPS from first video
fps = caps[0].get(cv2.CAP_PROP_FPS)

if fps <= 0:
    fps = 25

# Output writer
out = cv2.VideoWriter(
    "outputs/combined.mp4",
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (output_width, output_height)
)

print("Processing started...")

while True:
    frames = []

    for cap in caps:
        ret, frame = cap.read()

        if not ret:
            frame = np.zeros((cell_h, cell_w, 3), dtype=np.uint8)
            cv2.putText(
                frame,
                "Video Ended",
                (150, 180),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
            )
        else:
            frame = cv2.resize(frame, (cell_w, cell_h))

        frames.append(frame)

    # Stop when all videos finished
    ended_count = 0

    for cap in caps:
        if cap.get(cv2.CAP_PROP_POS_FRAMES) >= cap.get(
            cv2.CAP_PROP_FRAME_COUNT
        ):
            ended_count += 1

    if ended_count == len(caps):
        break

    # Fill empty slots
    while len(frames) < rows * cols:
        frames.append(
            np.zeros((cell_h, cell_w, 3), dtype=np.uint8)
        )

    rows_list = []

    for r in range(rows):
        start = r * cols
        end = start + cols

        row = np.hstack(frames[start:end])
        rows_list.append(row)

    combined = np.vstack(rows_list)

    out.write(combined)

    cv2.imshow("Combined Video", combined)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
for cap in caps:
    cap.release()

out.release()

cv2.destroyAllWindows()

print("Done!")
print("Saved to outputs/combined.mp4")