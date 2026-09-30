import os
import subprocess
import time

VIDEO_FOLDER = "videos"
RTSP_HOST = "rtsp://localhost:8554"

# Get all mp4 files
video_files = [
    os.path.join(VIDEO_FOLDER, f)
    for f in os.listdir(VIDEO_FOLDER)
    if f.lower().endswith(".mp4")
]

if not video_files:
    print("No videos found!")
    exit()

print(f"\nFound {len(video_files)} videos\n")

publishers = []
rtsp_urls = []

for video in video_files:
    # Generate stream name from filename
    stream_name = os.path.splitext(
        os.path.basename(video)
    )[0].replace(" ", "_")

    rtsp_url = f"{RTSP_HOST}/{stream_name}"

    print(f"Publishing:")
    print(f"  File : {video}")
    print(f"  RTSP : {rtsp_url}\n")

    cmd = [
        "ffmpeg",
        "-re",
        "-stream_loop",
        "-1",
        "-i",
        video,
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        "-f",
        "rtsp",
        rtsp_url,
    ]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    publishers.append(process)
    rtsp_urls.append(rtsp_url)

# Wait for streams to start
print("Waiting for RTSP streams to initialize...\n")
time.sleep(5)

print("=" * 50)
print("AVAILABLE RTSP STREAMS")
print("=" * 50)

for url in rtsp_urls:
    print(url)

print("\nUse VLC or FFplay to test:")
print("ffplay <RTSP_URL>")

print("\nPress Ctrl+C to stop all streams.")

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping all publishers...")

    for process in publishers:
        process.terminate()

    print("Done.")