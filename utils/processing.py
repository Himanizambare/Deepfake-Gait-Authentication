# utils/processing.py
import cv2
import numpy as np
from PIL import Image, ImageDraw
import io
import math
import tempfile
import os

# -------------------------------
# FRAME EXTRACTION FROM VIDEO
# -------------------------------
def extract_frames(uploaded_file, fps_sample=1):
    """
    Extract frames from a video every 'fps_sample' seconds.
    Returns list of (frame_index, timestamp, frame_bgr).
    """
    # Write to temporary file so OpenCV can read
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    cap = cv2.VideoCapture(tmp_path)
    if not cap.isOpened():
        os.unlink(tmp_path)
        return []

    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    frames = []
    sample_interval = max(1, int(fps * fps_sample))

    frame_index = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_index % sample_interval == 0:
            timestamp = frame_index / fps
            frames.append((frame_index, timestamp, frame.copy()))
        frame_index += 1

    cap.release()
    os.unlink(tmp_path)
    return frames


# -------------------------------
# CONTACT SHEET GENERATOR
# -------------------------------
def make_contact_sheet(frames, max_cols=4, thumb_w=320):
    """
    Create a single image containing multiple thumbnails of frames.
    """
    imgs = []
    for idx, ts, frame in frames:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil = Image.fromarray(rgb)
        w, h = pil.size
        new_h = int(thumb_w * h / w)
        pil = pil.resize((thumb_w, new_h))
        draw = ImageDraw.Draw(pil)
        draw.rectangle([(0, pil.height - 22), (pil.width, pil.height)], fill=(0, 0, 0, 180))
        draw.text((6, pil.height - 20), f"Frame {idx} - {ts:.1f}s", fill=(255, 255, 255))
        imgs.append(pil)

    if not imgs:
        return None

    cols = min(max_cols, len(imgs))
    rows = math.ceil(len(imgs) / cols)
    widths = [img.width for img in imgs[:cols]]
    max_w = max(widths)
    total_w = cols * max_w
    heights = []
    for r in range(rows):
        row_imgs = imgs[r * cols:(r + 1) * cols]
        heights.append(max([im.height for im in row_imgs]))
    total_h = sum(heights)

    sheet = Image.new("RGB", (total_w, total_h), color=(18, 18, 20))
    y = 0
    for r in range(rows):
        row_imgs = imgs[r * cols:(r + 1) * cols]
        x = 0
        h_row = heights[r]
        for im in row_imgs:
            sheet.paste(im, (x, y))
            x += max_w
        y += h_row

    buf = io.BytesIO()
    sheet.save(buf, format="PNG")
    buf.seek(0)
    return buf


# -------------------------------
# FACE DETECTION (OpenCV Haar)
# -------------------------------
# -------------------------------
# FACE DETECTION (OpenCV Haar)
# -------------------------------
_face_cascade = None

def detect_faces_in_frame(frame_bgr):
    """Detect faces in a given BGR frame using OpenCV Haar Cascade."""
    global _face_cascade
    if _face_cascade is None:
        _face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
    gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    faces = _face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)
    return faces.tolist() if len(faces) > 0 else []


# -------------------------------
# DRAW FACE BOXES ON FRAME
# -------------------------------
def draw_face_boxes(frame_bgr, faces):
    """Draw rectangles around detected faces on a given frame."""
    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    pil = Image.fromarray(rgb)
    draw = ImageDraw.Draw(pil)
    for (x, y, w, h) in faces:
        draw.rectangle([x, y, x + w, y + h], outline=(255, 0, 0), width=3)
    buf = io.BytesIO()
    pil.save(buf, format="PNG")
    buf.seek(0)
    return buf
