import cv2
import numpy as np

# Use a dedicated Katakana character set for matrix mode for a more authentic feel.
_ASCIIMatrix = np.array(list("アァポヴッン@%#*+=-:. "), dtype="<U1")
# A more standard, perceptually-ordered character set for other modes.
_ASCIINormal = np.array(list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,. "), dtype="<U1")

def to_ascii_image(frame_bgr: np.ndarray, out_w: int, out_h: int, cols: int, rows: int, ascii_mode: str = "colored", matrix_state=None, rain_cols: int = 70, rain_words=None):
    
    if rain_words is None:
        rain_words = []

    # Select the appropriate character set based on the mode.
    if ascii_mode == "matrix": 
        _ASCII = _ASCIIMatrix
    else:
        _ASCII = _ASCIINormal
        
    h, w = frame_bgr.shape[:2]
    gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    small = cv2.resize(gray, (cols, rows), interpolation=cv2.INTER_AREA)

    # Base character mapping from video brightness
    brightness_map = (small.astype(np.float32) / 255.0 * (len(_ASCII) - 1)).astype(np.int32)
    base_idx = np.clip(len(_ASCII) - 1 - brightness_map, 0, len(_ASCII) - 1) # Invert brightness

    # --- Color and Animation Logic ---
    if ascii_mode == "colored":
        colors = cv2.resize(frame_bgr, (cols, rows), interpolation=cv2.INTER_AREA)
    elif ascii_mode == "grayscale":
        colors = cv2.cvtColor(small, cv2.COLOR_GRAY2BGR)
    elif ascii_mode == "black-and-white":
        _, bw_img = cv2.threshold(small, 127, 255, cv2.THRESH_BINARY)
        colors = cv2.cvtColor(bw_img, cv2.COLOR_GRAY2BGR)
    elif ascii_mode == "matrix":
        # Base layer is green-tinted video
        colors = np.stack([np.zeros_like(small), small, np.zeros_like(small)], axis=-1)

        if matrix_state is None:
            num_drops = min(rain_cols, cols)
            matrix_state = {
                'drop_y': np.random.uniform(-rows, 0, size=num_drops).astype(np.float32),
                'drop_x': np.random.choice(np.arange(cols), size=num_drops, replace=False),
                'flicker_map': np.random.randint(0, len(_ASCII), size=(rows, cols))
            }
            if rain_words:
                matrix_state['word_indices'] = np.random.randint(0, len(rain_words), size=num_drops)
        
        state = matrix_state
        state['drop_y'] += 0.7 # Advance drops

    # --- Supersampling Rendering Pipeline for Maximum Clarity ---
    # Render to a larger canvas first, then downsample. This is key for readable small text.
    render_scale = 4
    cell_w = max(1, (out_w // cols) * render_scale)
    cell_h = max(1, (out_h // rows) * render_scale)
    
    font_face = cv2.FONT_HERSHEY_PLAIN
    thickness = 1
    
    (text_w, text_h), _ = cv2.getTextSize("W", font_face, 1.0, thickness)
    font_scale = min(cell_w / text_w, cell_h / text_h) * 0.9

    img = np.zeros((rows * cell_h, cols * cell_w, 3), dtype=np.uint8)

    # 1. Draw the base ASCII video layer
    for r in range(rows):
        for c in range(cols):
            char_code = _ASCII[base_idx[r, c]]
            color = tuple(int(v) for v in colors[r, c])
            (text_w, text_h), _ = cv2.getTextSize(char_code, font_face, font_scale, thickness)
            text_x = c * cell_w + (cell_w - text_w) // 2
            text_y = r * cell_h + (cell_h + text_h) // 2
            cv2.putText(img, char_code, (text_x, text_y), font_face, font_scale, color, thickness, cv2.LINE_AA)

    # 2. If in matrix mode, draw the rain animation on top
    if ascii_mode == 'matrix':
        drop_y = state['drop_y']
        drop_x = state['drop_x']

        for i in range(len(drop_y)):
            y_pos = int(drop_y[i])
            x_pos = drop_x[i]

            if y_pos >= rows:
                drop_y[i] = np.random.uniform(-rows * 0.5, 0)
                if rain_words:
                    state['word_indices'][i] = np.random.randint(0, len(rain_words))
                continue

            if 0 <= y_pos < rows:
                if not rain_words:
                    char_code = _ASCII[state['flicker_map'][y_pos, x_pos]]
                    (text_w, text_h), _ = cv2.getTextSize(char_code, font_face, font_scale, thickness)
                    text_x = x_pos * cell_w + (cell_w - text_w) // 2
                    cv2.putText(img, char_code, (text_x, y_pos * cell_h + (cell_h + text_h) // 2), font_face, font_scale, (200, 255, 200), thickness, cv2.LINE_AA)
                    for t in range(1, 8):
                        trail_y = y_pos - t
                        if 0 <= trail_y < rows:
                            fade = 1.0 - (t / 10.0)
                            trail_char = _ASCII[state['flicker_map'][trail_y, x_pos]]
                            (tw, th), _ = cv2.getTextSize(trail_char, font_face, font_scale, thickness)
                            tx = x_pos * cell_w + (cell_w - tw) // 2
                            cv2.putText(img, trail_char, (tx, trail_y * cell_h + (cell_h + th) // 2), font_face, font_scale, (0, int(255 * fade), 0), thickness, cv2.LINE_AA)
                else:
                    word = rain_words[state['word_indices'][i]]
                    for char_idx, char in enumerate(word):
                        trail_y = y_pos - (len(word) - 1 - char_idx)
                        if 0 <= trail_y < rows:
                            color = (200, 255, 200) if char_idx == len(word) - 1 else (0, int(220 * (1.0 - ((len(word) - char_idx) / 15.0))), 0)
                            (text_w, text_h), _ = cv2.getTextSize(char, font_face, font_scale, thickness)
                            text_x = x_pos * cell_w + (cell_w - text_w) // 2
                            text_y = trail_y * cell_h + (cell_h + text_h) // 2
                            cv2.putText(img, char, (text_x, text_y), font_face, font_scale, color, thickness, cv2.LINE_AA)

    # Downsample the high-resolution rendered image to the final output size.
    final_img = cv2.resize(img, (out_w, out_h), interpolation=cv2.INTER_AREA)
    
    return final_img, matrix_state
