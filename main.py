import sys
from src.mosaic_generator import generate_ascii_mosaic, generate_ascii_video

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python main.py image assets/sample_image.jpg")
        print("  python main.py video assets/sample_video.mp4")
        sys.exit(1)

    mode = sys.argv[1].lower()
    target_path = sys.argv[2]

    if mode == "image":
        generate_ascii_mosaic(target_path, output_path="assets/output_mosaic.png", scale_factor=0.25)
    elif mode == "video":
        generate_ascii_video(target_path, output_path="assets/output_mosaic_video.mp4", scale_factor=0.20, mobile=True)