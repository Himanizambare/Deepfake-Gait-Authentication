# utils/video_model.py
import random
import time
from utils.processing import extract_frames, make_contact_sheet, detect_faces_in_frame, draw_face_boxes
import io

def analyze_video(uploaded_file, sample_seconds=1):
    """
    uploaded_file: streamlit UploadedFile
    Returns:
      {
        verdict, confidence,
        gait_ok, gait_confidence,
        frames_info: [ {index, timestamp, faces: [bboxes], annotated_frame_bytes} ],
        contact_sheet: png bytes
      }
    """
    # rewind file to start
    uploaded_file.seek(0)
    frames = extract_frames(uploaded_file, fps_sample=sample_seconds)
    frames_info = []
    for idx, ts, frame in frames:
        faces = detect_faces_in_frame(frame)
        annotated_buf = draw_face_boxes(frame, faces) if faces else None
        frames_info.append({
            "index": int(idx),
            "timestamp": float(ts),
            "faces": [ [int(x),int(y),int(w),int(h)] for (x,y,w,h) in faces ],
            "annotated_frame": annotated_buf
        })
    contact_buf = make_contact_sheet(frames, max_cols=4, thumb_w=320)
    # dummy deepfake + gait predictions (replace with actual model inference)
    time.sleep(0.9)
    verdict = random.choice(["authentic", "deepfake"])
    confidence = random.uniform(65, 97)
    gait_ok = random.choice([True, False])
    gait_confidence = random.uniform(60, 98)
    return {
        "verdict": verdict,
        "confidence": confidence,
        "gait_ok": gait_ok,
        "gait_confidence": gait_confidence,
        "frames_info": frames_info,
        "contact_sheet": contact_buf
    }
