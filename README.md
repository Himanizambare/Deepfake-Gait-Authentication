# DeepSecure.AI

⚡ DeepSecure.AI — Hybrid Deepfake & Gait Authentication

A futuristic AI-powered authentication system that combines Deepfake Detection, Gait Recognition, and Text Analysis into a single secure platform.
Built using Streamlit, Python, and modular ML stubs ready for integration.

## ⭐ Features
🔍 Deepfake Detection

Upload images or videos

Face detection + annotation

Stub-ready for CNN/Transformer deepfake models

## 🚶 Gait Analysis

Extracts keyframes

Performs basic gait verification

Ready to plug in pose-estimation models

## 📊 Text Analysis

Sentiment scoring

Similarity score

NLP-ready for advanced LLM integrations

## 🎨 Modern UI

Animated background (video or gradient)

Futuristic glassmorphism design

Smooth Lottie animations (AI brain, shield, processing, sparks, footer wave)

## 🔐 User Authentication

Register / Login (SQL-based)

Local demo DB (users.db)

Modular for any backend auth

## 🖥️ Tech Stack
Layer	Technology
Frontend UI	Streamlit, Lottie animations
Backend API	Python (modular ML stubs)
Models Folder	Custom ML integration point
Database	SQLite (local demo)
Deployment	Streamlit Cloud / Render

## 📂 Project Structure
```
DeepSecure.AI
│── app.py
│── requirements.txt
│── README.md
│── users.db                # Demo-only DB (ignored in production)
│── .gitignore
│
├── assets/                 # Images / background video / animations
│     └── 262696_small.mp4
│
├── utils/
│     ├── image_model.py    # Deepfake model stub
│     ├── video_model.py    # Gait model stub
│     ├── text_model.py     # NLP analysis
│     └── sql_auth.py       # Auth system
│
├── ML-Model/               # (Optional) Your model files
└── ML-Model-Testing/
```
## 🚀 Local Setup
### 1️⃣ Clone the repository
```git clone https://github.com/<your-user>/<repo>.git
cd <repo>
```

### 2️⃣ Install dependencies
``` pip install -r requirements.txt```

### 3️⃣ Run the app
```streamlit run app.py```









