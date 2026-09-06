import cv2
import numpy as np
import shutil
import time
from PIL import Image, ImageDraw, ImageFont

ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def _get_font(font_size: int):
    try:
        return ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        return ImageFont.load_default()

def process_frame(
    frame: np.ndarray,
    scale_factor: float = 0.25,
    font_size: int = 10,
    is_mobile_ratio: bool = False
):
    """
    Processes a single frame: crops to 9:16 if needed, computes ASCII characters,
    generates an ANSI string for terminal display, and draws a high-res PIL canvas image.
    """
    h, w, _ = frame.shape

    # Crop to 9:16 mobile aspect ratio if requested
    if is_mobile_ratio:
        target_aspect = 9 / 16
        current_aspect = w / h
        if current_aspect > target_aspect:
            new_w = int(h * target_aspect)
            offset = (w - new_w) // 2
            frame = frame[:, offset:offset + new_w]
        else:
            new_h = int(w / target_aspect)
            offset = (h - new_h) // 2
            frame = frame[offset:offset + new_h, :]
        h, w, _ = frame.shape

    cols = max(1, int(w * scale_factor))
    rows = max(1, int(h * scale_factor))

    resized_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resized_rgb = cv2.resize(resized_rgb, (cols, rows), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(resized_rgb, cv2.COLOR_RGB2GRAY)

    # Font and canvas setup
    font = _get_font(font_size)
    bbox = font.getbbox("A")
    char_w = bbox[2] - bbox[0]
    char_h = bbox[3] - bbox[1] + 2

    out_w = cols * char_w
    out_h = rows * char_h

    canvas = Image.new("RGB", (out_w, out_h), color=(255, 255, 255))
    draw = ImageDraw.Draw(canvas)

    # Terminal size auto-fit setup
    term_cols, term_rows = shutil.get_terminal_size((80, 24))
    term_target_w = min(cols, term_cols - 2)
    term_target_h = min(rows, term_rows - 2)

    term_gray = cv2.resize(gray, (term_target_w, term_target_h), interpolation=cv2.INTER_AREA)
    term_color = cv2.resize(resized_rgb, (term_target_w, term_target_h), interpolation=cv2.INTER_AREA)

    ansi_lines = []
    for r in range(term_target_h):
        row_str = ""
        for c in range(term_target_w):
            intensity = term_gray[r, c]
            char_idx = int((intensity / 255.0) * (len(ASCII_CHARS) - 1))
            char = ASCII_CHARS[char_idx]

            r_val, g_val, b_val = term_color[r, c]
            row_str += f"\033[48;2;255;255;255m\033[38;2;{r_val};{g_val};{b_val}m{char}"
        ansi_lines.append(row_str + "\033[0m")

    terminal_output = "\n".join(ansi_lines)

    # High-Resolution Canvas Rendering
    for r in range(rows):
        for c in range(cols):
            pixel_intensity = gray[r, c]
            char_idx = int((pixel_intensity / 255.0) * (len(ASCII_CHARS) - 1))
            char = ASCII_CHARS[char_idx]

            color = tuple(resized_rgb[r, c])
            x = c * char_w
            y = r * char_h
            draw.text((x, y), char, fill=color, font=font)

    rendered_frame = cv2.cvtColor(np.array(canvas), cv2.COLOR_RGB2BGR)
    return terminal_output, rendered_frame

def generate_ascii_mosaic(
    image_path: str,
    output_path: str = "output_mosaic.png",
    scale_factor: float = 0.25,
    font_size: int = 10,
    mobile: bool = False
):
    """
    Renders high-density ASCII mosaic directly to a PNG file and previews on terminal.
    """
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Image not found.")
        return

    term_str, output_canvas = process_frame(img, scale_factor, font_size, is_mobile_ratio=mobile)

    print("\033[H", end="")
    print(term_str)

    cv2.imwrite(output_path, output_canvas)
    print(f"\nHigh-res ASCII mosaic saved to {output_path}")

def generate_ascii_video(
    video_path: str,
    output_path: str = "output_mosaic_video.mp4",
    scale_factor: float = 0.20,
    font_size: int = 10,
    mobile: bool = True
):
    """
    Processes video frames into a high-density colored ASCII mosaic video stream (MP4).
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    frame_time = 1.0 / fps

    ret, first_frame = cap.read()
    if not ret:
        print("Error: Empty video file.")
        return

    _, sample_rendered = process_frame(first_frame, scale_factor, font_size, is_mobile_ratio=mobile)
    out_h, out_w, _ = sample_rendered.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_writer = cv2.VideoWriter(output_path, fourcc, fps, (out_w, out_h))

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    print("\033[?25l", end="") # Hide cursor

    try:
        while cap.isOpened():
            start_time = time.time()
            ret, frame = cap.read()
            if not ret:
                break

            term_str, ascii_canvas = process_frame(frame, scale_factor, font_size, is_mobile_ratio=mobile)

            print("\033[H", end="")
            print(term_str)

            out_writer.write(ascii_canvas)

            elapsed = time.time() - start_time
            time.sleep(max(0, frame_time - elapsed))

    finally:
        print("\033[?25h\033[0m")
        cap.release()
        out_writer.release()
        print(f"\nHigh-res ASCII video saved to {output_path}")