import sys
import time
import cv2
import os
from src.renderer import render_high_res_ascii

def clear_screen():
    print("\033[H", end="")

def play_image(image_path: str, max_cols: int = 100):
    frame = cv2.imread(image_path)
    if frame is None:
        print("Error: Could not load image.")
        return
    ascii_art = render_high_res_ascii(frame, max_cols=max_cols, use_half_blocks=True)
    clear_screen()
    print(ascii_art)

def play_video(video_path: str, max_cols: int = 100):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    frame_time = 1.0 / fps

    print("\033[?25l", end="") # Hide cursor
    try:
        while cap.isOpened():
            start_time = time.time()
            ret, frame = cap.read()
            if not ret:
                break
            
            ascii_frame = render_high_res_ascii(frame, max_cols=max_cols, use_half_blocks=True)
            clear_screen()
            print(ascii_frame)

            elapsed = time.time() - start_time
            sleep_time = max(0, frame_time - elapsed)
            time.sleep(sleep_time)
    finally:
        print("\033[?25h\033[0m") # Restore cursor and reset colors
        cap.release()