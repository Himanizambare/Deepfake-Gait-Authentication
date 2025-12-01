# utils/image_model.py
import random
import time
from utils.processing import detect_faces_in_frame, draw_face_boxes
from PIL import Image
import numpy as np
import io

def analyze_image(uploaded_file):
    """
    uploaded_file: streamlit UploadedFile
    Returns dict:
      { verdict, confidence, faces: [{bbox:[x,y,w,h]}], annotated_image_bytes }
    """
    # read bytes and open
    data = uploaded_file.read()
    img = Image.open(io.BytesIO(data)).convert("RGB")
    arr = np.array(img)[:, :, ::-1].copy()  # convert RGB -> BGR for OpenCV
    # detect faces (demo)
    faces = detect_faces_in_frame(arr)
    annotated = draw_face_boxes(arr, faces) if faces else None
    # dummy prediction (replace with your TF/PyTorch model)
    time.sleep(0.6)
    verdict = random.choice(["authentic", "deepfake"])
    confidence = random.uniform(65, 98)
    result = {
        "verdict": verdict,
        "confidence": confidence,
        "faces": [{"bbox": [int(x), int(y), int(w), int(h)]} for (x,y,w,h) in faces],
        "annotated_image": annotated  # BytesIO or None
    }
    return result
