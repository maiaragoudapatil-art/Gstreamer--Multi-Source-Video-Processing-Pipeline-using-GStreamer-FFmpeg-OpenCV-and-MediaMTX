# Gstreamer--Multi-Source-Video-Processing-Pipeline-using-GStreamer-FFmpeg-OpenCV-and-MediaMTX
Multi-Source Video Processing Pipeline using GStreamer, FFmpeg, OpenCV, and MediaMTX. Supports processing multiple video files, combining them into dynamic grid layouts, generating MP4 outputs, and publishing streams via RTSP. Designed for CPU-based video analytics with future support for webcams, RTSP cameras, and real-time streaming.


A CPU-based video processing pipeline that ingests multiple video sources, processes and combines them into a unified output, and supports live streaming through RTSP.

## Features

- Process multiple video files simultaneously
- Dynamic video grid composition
- Video frame processing using OpenCV
- GStreamer integration for multimedia pipelines
- FFmpeg-based encoding and streaming
- MediaMTX RTSP server integration
- Webcam input support (Upcoming)
- RTSP camera input support (Upcoming)
- Automatic output generation as MP4
- Real-time streaming support

## Current Progress

✅ Python 3.11 environment setup

✅ OpenCV video processing

✅ Multi-video grid composer

✅ Combined video generation

✅ FFmpeg integration

✅ MediaMTX RTSP streaming setup

✅ Local RTSP publishing

## Tech Stack

- Python 3.11
- OpenCV
- NumPy
- GStreamer
- FFmpeg
- MediaMTX
- FastAPI (Planned)

## Project Architecture

Video Files / Webcam / RTSP Streams
                │
                ▼
          GStreamer
                │
                ▼
        Frame Processing
           (OpenCV)
                │
                ▼
         Video Combiner
                │
                ▼
     MP4 Output Generation
                │
                ▼
             FFmpeg
                │
                ▼
            MediaMTX
                │
                ▼
           RTSP Stream



