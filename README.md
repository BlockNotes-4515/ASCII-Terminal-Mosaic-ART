# Terminal-Mosaic 🎬🎨

Terminal-Mosaic is a high-performance Python application that transforms standard images and video clips into high-definition ASCII character mosaics. It offers real-time ANSI color streaming inside your command-line interface alongside high-resolution file exports with preserved audio tracks.

---

## 📋 Table of Contents
1. [About the Project](#-about-the-project)
2. [Project Architecture](#-project-architecture)
3. [How the Media Pipeline Works](#-how-the-media-pipeline-works)
4. [Prerequisites & System Setup](#-prerequisites--system-setup)
5. [Installation & Virtual Environment](#-installation--virtual-environment)
6. [Running on Your Local Machine](#-running-on-your-local-machine)
7. [Real-time Processing & File Exports](#-real-time-processing--file-exports)
8. [Output Gallery & Results](#-output-gallery--results)

---

## 📄 About the Project

`Terminal-Mosaic` processes visual media by evaluating pixel luminance and TrueColor RGB vectors.

* **Luminance Character Mapping:** Translates pixel brightness into dense character layers (`$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrft/\|()1{}[]?-_+~<>i!lI;:,"^'`. `).
* **Dual Output Stream Engine:** Streams full-color ANSI text frames live to your terminal at 30 FPS while rendering pixel-perfect HD outputs (`.png` / `.mp4`).
* **Synchronized Audio Preservation:** Uses `ffmpeg` to extract source audio and `pygame` to synchronize sound with live terminal playback and final MP4 file encoding.

---

## 🏗️ Project Architecture

```text
                     +-----------------------+
                     |   Input File Source   |
                     | (Image / MP4 Video)   |
                     +-----------+-----------+
                                 |
                                 v
                     +-----------------------+
                     |    main.py (CLI)      |
                     +-----------+-----------+
                                 |
                                 v
                     +-----------------------+
                     | process_frame() Engine|
                     |  - Brightness Map     |
                     |  - RGB TrueColor      |
                     |  - 9:16 Mobile Crop   |
                     +----+-------------+----+
                          |             |
           +--------------+             +--------------+
           |                                           |
           v                                           v
+-----------------------+                   +-----------------------+
|  Terminal Live Stream |                   | HD Canvas File Stream |
|  - ANSI Escape Codes  |                   |  - PIL Image Drawing  |
|  - Realtime Audio Sync|                   |  - OpenCV MP4 Writer  |
+-----------------------+                   +-----------+-----------+
                                                        |
                                                        v
                                            +-----------------------+
                                            |  FFmpeg Audio Muxer   |
                                            |  - AAC Audio Merge    |
                                            +-----------+-----------+
                                                        |
                                                        v
                                            +-----------------------+
                                            |  Final Output Files   |
                                            | (PNG / Audio MP4)     |
                                            +-----------------------+

```
## ⚙️ How the Media Pipeline Works

1. **`process_frame()`** (`src/mosaic_generator.py`):
   - Accepts an uncompressed OpenCV image array (`np.ndarray`).
   - Applies an automatic 9:16 vertical mobile aspect ratio crop if requested (`is_mobile_ratio=True`).
   - Resizes pixel resolution based on `scale_factor`.
   - Extracts grayscale brightness maps for ASCII character selection and RGB true-colors for cell coloring.
   - Outputs an ANSI-encoded string for console streaming and draws a high-resolution PIL image canvas.

2. **`generate_ascii_mosaic()`**:
   - Reads an input image using OpenCV (`cv2.imread`).
   - Renders the terminal preview and outputs a high-resolution PNG image file.

3. **`generate_ascii_video()`**:
   - Extracts the source audio track to a temporary WAV buffer (`temp_audio.wav`) via `ffmpeg`.
   - Plays audio live through `pygame.mixer` while rendering terminal frames at 30 FPS.
   - Clears terminal output in place (`\033[H`) to eliminate screen flickering.
   - Encodes high-res ASCII frames into a silent MP4 buffer before merging the audio track back into the file.

---

## 🛠️ Prerequisites & System Setup

Ensure the following prerequisites are installed before setting up the application:

* **Python:** Version 3.10 or higher
* **Git:** For cloning the repository
* **FFmpeg:** System binary required for video audio extraction and muxing
  * **Windows:** Run `winget install ffmpeg` or download from [ffmpeg.org](https://ffmpeg.org/) and add `ffmpeg/bin` to your System Environment Variables (PATH).
  * **macOS:** Run `brew install ffmpeg`
  * **Linux (Ubuntu/Debian):** Run `sudo apt update && sudo apt install ffmpeg`

---

## 🐍 Installation & Virtual Environment

Follow these commands step-by-step to set up your environment:

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/terminal-mosaic.git](https://github.com/your-username/terminal-mosaic.git)
cd terminal-mosaic
