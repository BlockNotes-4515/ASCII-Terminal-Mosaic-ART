import cv2
import numpy as np
import shutil

# Fine character density scale
ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def render_high_res_ascii(
    frame: np.ndarray, 
    max_cols: int = 100, 
    use_half_blocks: bool = True
) -> str:
    """
    Renders an image array into a compact, ultra-dense ANSI ASCII/Block layout 
    that fits completely inside terminal dimensions without line wraps.
    """
    term_cols, term_rows = shutil.get_terminal_size((80, 24))
    
    # Restrict character columns to fit inside current terminal window
    target_width = min(max_cols, term_cols - 2)

    h, w, _ = frame.shape

    if use_half_blocks:
        # 1 character = 2 vertical pixels -> Perfect 1:1 square pixel aspect ratio
        target_height = int((h / w) * target_width)
        # Ensure height is even for half-block pairing
        if target_height % 2 != 0:
            target_height -= 1
        
        # Clamp height to fit terminal viewport
        if (target_height // 2) > (term_rows - 2):
            target_height = (term_rows - 2) * 2
            target_width = int((w / h) * target_height)

        resized = cv2.resize(frame, (target_width, target_height), interpolation=cv2.INTER_AREA)
        
        output = []
        # Step by 2 rows at a time using upper half block '▀'
        for r in range(0, target_height, 2):
            row_str = ""
            for c in range(target_width):
                # Top pixel -> Foreground color
                b_top, g_top, r_top = resized[r, c]
                # Bottom pixel -> Background color
                b_bot, g_bot, r_bot = resized[r + 1, c] if (r + 1 < target_height) else (0, 0, 0)
                
                # 38;2 = Foreground RGB, 48;2 = Background RGB
                row_str += f"\033[38;2;{r_top};{g_top};{b_top}m\033[48;2;{r_bot};{g_bot};{b_bot}m▀"
            output.append(row_str)
            
        return "\n".join(output) + "\033[0m"

    else:
        # Character-based micro ASCII mode
        aspect_ratio_correction = 0.42
        target_height = int((h / w) * target_width * aspect_ratio_correction)
        
        if target_height > (term_rows - 2):
            target_height = term_rows - 2
            target_width = int((w / h) * (target_height / aspect_ratio_correction))

        resized = cv2.resize(frame, (target_width, target_height), interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        
        normalized = gray / 255.0
        char_indices = (normalized * (len(ASCII_CHARS) - 1)).astype(int)

        output = []
        for r in range(target_height):
            row_str = ""
            for c in range(target_width):
                char = ASCII_CHARS[char_indices[r, c]]
                b, g, r_val = resized[r, c]
                row_str += f"\033[38;2;{r_val};{g};{b}m{char}"
            output.append(row_str)

        return "\n".join(output) + "\033[0m"