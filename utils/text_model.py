# utils/text_model.py
import random
import time

def analyze_text(text):
    time.sleep(0.4)
    sentiment = random.choice(["Positive", "Neutral", "Negative"])
    confidence = random.uniform(70, 97)
    similarity_score = random.uniform(30, 95)
    return {"sentiment": sentiment, "confidence": confidence, "similarity": similarity_score}
