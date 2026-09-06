 # ASCII 🎭 Terminal-Mosaic 🎨

Terminal-Mosaic is a Python-powered media processing tool that converts images and videos into high-definition ASCII character mosaics. It features live ANSI color streaming inside your command line interface and preserves original video audio tracks.

---

## 📋 Table of Contents
1. [About the Project](#-about-the-project)
2. [Project Structure](#-project-structure)
3. [How the Pipeline Works](#-how-the-pipeline-works)
4. [Prerequisites](#-prerequisites)
5. [Forking and Local Setup](#-forking-and-local-setup)
6. [Virtual Environment Setup](#-virtual-environment-setup)
7. [Running the Application](#-running-the-application)
8. [Output Gallery](#-output-gallery)

---

## 📄 About the Project

`Terminal-Mosaic` processes images and video frames by evaluating pixel brightness and RGB color values. 
- **Luminance Mapping:** Maps grayscale intensity values to a custom ASCII character set (`$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrft/\|()1{}[]?-_+~<>i!lI;:,"^'`. `).
- **Dual Engine Output:** Simultaneously streams real-time ASCII animations to your console (using ANSI color escape codes) and renders high-resolution media outputs (PNG / MP4).
- **Audio Synchronization:** Extracts audio from source videos using `ffmpeg`, plays it live during terminal playback using `pygame`, and merges it back into the exported MP4 video.

---

## 📁 Project Structure

```text
terminal-mosaic/
├── assets/
│   ├── sample_image.jpg          # Input sample image
│   ├── sample_video.mp4          # Input sample video
│   ├── output_mosaic.png         # Exported ASCII image
│   └── output_mosaic_video.mp4   # Exported ASCII video with sound
├── src/
│   ├── __init__.py               # Package marker
│   └── mosaic_generator.py       # Core image, video, and audio processing logic
├── main.py                       # Application CLI entry point
├── requirements.txt              # Project dependencies
└── README.md                     # Documentation
