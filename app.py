import streamlit as st
from streamlit_lottie import st_lottie
import requests
from utils.image_model import analyze_image
from utils.video_model import analyze_video
from utils.text_model import analyze_text
import streamlit.components.v1 as components

# optionally import your auth functions
try:
    from utils.sql_auth import register_user, authenticate_user
except Exception:
    from utils.sql_auth import register_user, authenticate_user  # fallback


# ----------------------- PAGE CONFIG -----------------------
st.set_page_config(page_title="DeepSecure.AI", page_icon="🧠", layout="wide")


# ---------------------- LOTTIE LOADER ----------------------
@st.cache_data(show_spinner=False)
def load_lottie_url(url: str):
    """Load a Lottie animation from URL."""
    try:
        r = requests.get(url, timeout=6)
        if r.status_code == 200:
            return r.json()
    except Exception:
        return None
    return None


# ✅ Futuristic Animations (verified and working)
LOTTIE_HERO = load_lottie_url("https://lottie.host/6a1f88e8-1e6a-4a28-b81a-43d40e35b7f2/ohYQrqxD8D.json")        # AI Brain Glow
LOTTIE_PROCESS = load_lottie_url("https://lottie.host/20c4f34d-c96c-49c2-a17a-38c79c8b5799/ZOP3NymOBz.json")    # Data Processing Circuit
LOTTIE_SECURE = load_lottie_url("https://lottie.host/3a1776b5-0a48-4a2e-96cd-38df9f6178f7/lDQdUV7RyU.json")     # Cyber Shield Pulse
LOTTIE_SPARK = load_lottie_url("https://lottie.host/5aee33d1-dbe1-4b86-8b0d-02c9f25de92d/gxtFiPc6Zz.json")      # Floating sparks
LOTTIE_FOOTER = load_lottie_url("https://lottie.host/04fae0a1-ccbe-48e5-8a6d-56fa23cfb64c/bzChb2HkM8.json")     # Glowing wave


# ---------------------- ANIMATED BACKGROUND ----------------------
def add_bg_animation():
    """Adds a futuristic animated gradient and floating particles background."""
    components.html("""
    <style>
      .stApp {
          background: transparent !important;
          overflow: hidden;
      }

      /* Animated gradient background */
      body::before {
          content: "";
          position: fixed;
          top: 0;
          left: 0;
          width: 200%;
          height: 200%;
          background: radial-gradient(circle at 20% 20%, rgba(0, 255, 200, 0.2), transparent 70%),
                      radial-gradient(circle at 80% 80%, rgba(0, 200, 255, 0.2), transparent 70%),
                      linear-gradient(120deg, #0f172a, #1e293b, #0f3460);
          animation: moveGradient 20s ease-in-out infinite alternate;
          z-index: -3;
          filter: brightness(0.6);
      }

      /* Floating particles */
      .particles {
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          overflow: hidden;
          z-index: -2;
      }

      .particle {
          position: absolute;
          background: rgba(0,255,255,0.15);
          border-radius: 50%;
          animation: floatUp 12s infinite ease-in-out;
      }

      @keyframes moveGradient {
          0% { transform: translate(0, 0) scale(1); }
          100% { transform: translate(-20%, -20%) scale(1.3); }
      }

      @keyframes floatUp {
          0% {
              transform: translateY(100vh) scale(0.5);
              opacity: 0;
          }
          50% {
              opacity: 1;
          }
          100% {
              transform: translateY(-10vh) scale(1);
              opacity: 0;
          }
      }
    </style>

    <div class="particles">
      <div class="particle" style="width:8px; height:8px; left:10%; animation-delay:0s;"></div>
      <div class="particle" style="width:10px; height:10px; left:25%; animation-delay:3s;"></div>
      <div class="particle" style="width:6px; height:6px; left:45%; animation-delay:1s;"></div>
      <div class="particle" style="width:12px; height:12px; left:65%; animation-delay:2s;"></div>
      <div class="particle" style="width:9px; height:9px; left:80%; animation-delay:4s;"></div>
      <div class="particle" style="width:5px; height:5px; left:90%; animation-delay:6s;"></div>
    </div>
    """, height=0)


# ---------------------- SESSION DEFAULTS ----------------------
if "auth" not in st.session_state:
    st.session_state.auth = {"logged_in": False, "user": None}
if "page" not in st.session_state:
    st.session_state.page = "home"


# ---------------------- HEADER NAVIGATION ----------------------
def render_header():
    st.markdown("""
    <style>
    .logo {
        font-weight: 800;
        font-size: 26px;
        letter-spacing: 1px;
        background: linear-gradient(90deg,#8b5cf6,#06b6d4);
        -webkit-background-clip: text;
        color: transparent;
    }
    div[data-testid="column"] > div > button {
        width: 100%;
        background: linear-gradient(90deg,#4f46e5,#06b6d4);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.2s ease-in-out;
    }
    div[data-testid="column"] > div > button:hover {
        transform: scale(1.05);
        box-shadow: 0px 0px 12px #06b6d4;
    }
    </style>
    """, unsafe_allow_html=True)

    user = st.session_state.auth.get("user")
    logged_in = st.session_state.auth.get("logged_in", False)

    c1, c2, c3, c4 = st.columns([1, 1, 1, 2])
    with c1:
        st.markdown('<div class="logo">⚡ DeepSecure.AI</div>', unsafe_allow_html=True)
    with c2:
        if st.button("🏠 Home"):
            st.session_state.page = "home"
            st.rerun()
    with c3:
        if st.button("📊 Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()
    with c4:
        if st.button("ℹ️ About"):
            st.session_state.page = "about"
            st.rerun()

    if logged_in:
        st.info(f"👋 Logged in as **{user.get('full_name','User')}**", icon="🔐")
    else:
        st.warning("⚠️ Not logged in. Use the sidebar to log in.")


# ---------------------- SIDEBAR AUTH ----------------------
def auth_sidebar():
    st.sidebar.title("🔑 Account")
    if st.session_state.auth["logged_in"]:
        st.sidebar.success(f"✅ Logged in as {st.session_state.auth['user'].get('full_name','')}")
        if st.sidebar.button("Logout"):
            st.session_state.auth = {"logged_in": False, "user": None}
            st.rerun()
    else:
        mode = st.sidebar.selectbox("Action", ["Login", "Register"])
        email = st.sidebar.text_input("📧 Email")
        pwd = st.sidebar.text_input("🔒 Password", type="password")
        name = st.sidebar.text_input("🪪 Full name (register only)")
        if mode == "Register":
            if st.sidebar.button("🆕 Create account"):
                ok, msg = register_user(email.strip().lower(), pwd, name)
                if ok:
                    st.sidebar.success("✅ Registered. Now login.")
                else:
                    st.sidebar.error(msg)
        else:
            if st.sidebar.button("➡️ Login"):
                ok, info = authenticate_user(email.strip().lower(), pwd)
                if ok:
                    st.session_state.auth = {"logged_in": True, "user": info}
                    st.sidebar.success("✅ Logged in.")
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.sidebar.error(info)


auth_sidebar()
render_header()


# ---------------------- HOME PAGE ----------------------
def home_page():
    add_bg_animation()
    st.title("🤖 Hybrid Deepfake & Gait Authentication")
    st.write("Welcome to **DeepSecure.AI**, a futuristic authentication framework integrating **Deepfake Detection** and **Gait Recognition** for next-gen biometric trust.")

    st.markdown("---")
    cols = st.columns(3)
    cols[0].metric("🧠 Mode", "Hybrid (Image + Gait)")
    cols[1].metric("🔐 Auth Strength", "Multi-modal")
    cols[2].metric("🧪 Demo Type", "Local")

    if LOTTIE_HERO:
        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
        st_lottie(LOTTIE_HERO, height=320, key="hero_anim", speed=1.0, loop=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.caption("AI-powered hybrid authentication combining vision & motion intelligence.")

    if LOTTIE_SPARK:
        st_lottie(LOTTIE_SPARK, height=80, key="spark_anim", speed=1.2)


# ---------------------- ABOUT PAGE ----------------------
def about_page():
    add_bg_animation()
    st.header("🧬 About DeepSecure.AI")
    st.markdown("""
    **DeepSecure.AI** is a cutting-edge research project blending **Deepfake Detection** with **Gait Analysis**.  
    It ensures identity protection and integrity using advanced AI pipelines.

    - 🧠 **Deepfake Detection** — Transformer + CNN analysis for tampered media.  
    - 🚶 **Gait Recognition** — Pose-based movement analysis for identity verification.  
    - 🛡️ **Security-Enhanced** — Privacy-preserving local processing.  
    """)

    if LOTTIE_SECURE:
        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
        st_lottie(LOTTIE_SECURE, height=260, key="secure_anim")
        st.markdown("</div>", unsafe_allow_html=True)
        st.caption("Ensuring biometric trust through deep learning innovation.")


# ---------------------- DASHBOARD PAGE ----------------------
def dashboard_page():
    add_bg_animation()

    if not st.session_state.auth["logged_in"]:
        st.warning("🔒 Please login (sidebar) to access the dashboard.")
        return

    st.header("📊 Dashboard — Upload & Analyze")

    col1, col2 = st.columns([2, 1])

    with col1:
        mode = st.selectbox("🧾 Select Input Type", ["Image", "Video", "Text"])

        if mode == "Image":
            uploaded = st.file_uploader("🖼️ Upload an image", type=["png", "jpg", "jpeg"])
            if uploaded and st.button("🚀 Analyze Image"):
                with st.spinner("Analyzing image..."):
                    if LOTTIE_PROCESS:
                        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
                        st_lottie(LOTTIE_PROCESS, height=150, key="proc_img")
                        st.markdown("</div>", unsafe_allow_html=True)
                    res = analyze_image(uploaded)
                st.success(f"Verdict: **{res['verdict'].upper()}** ({res['confidence']:.2f}%)")
                if res["annotated_image"] is not None:
                    st.image(res["annotated_image"], caption="Detected Faces (Annotated)")
                st.json({k: v for k, v in res.items() if k != "annotated_image"})

        elif mode == "Video":
            uploaded = st.file_uploader("🎥 Upload a short video", type=["mp4", "avi"])
            sample_sec = st.slider("Frame Sampling Interval (seconds)", 1, 5, 1)
            if uploaded and st.button("🚀 Analyze Video"):
                with st.spinner("Analyzing video... this may take a few seconds"):
                    if LOTTIE_PROCESS:
                        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
                        st_lottie(LOTTIE_PROCESS, height=150, key="proc_vid")
                        st.markdown("</div>", unsafe_allow_html=True)
                    uploaded.seek(0)
                    res = analyze_video(uploaded, sample_seconds=sample_sec)
                st.success(f"Verdict: **{res['verdict'].upper()}** ({res['confidence']:.2f}%)")
                st.metric("Gait Verification", "✅ PASS" if res["gait_ok"] else "❌ FAIL")
                st.progress(min(1.0, res["gait_confidence"] / 100.0))
                if res.get("contact_sheet"):
                    st.image(res["contact_sheet"], caption="Extracted Keyframes", use_column_width=True)
                st.markdown("### 🎞️ Frame Details")
                for fi in res["frames_info"]:
                    cols = st.columns([1, 4, 2])
                    with cols[0]:
                        if fi["annotated_frame"]:
                            st.image(fi["annotated_frame"], width=120)
                    with cols[1]:
                        st.write(f"Frame #{fi['index']} — {fi['timestamp']:.2f}s")
                        st.write("Faces: " + (str(fi["faces"]) if fi["faces"] else "None"))
                    with cols[2]:
                        if fi["faces"]:
                            st.button(f"🔍 Zoom #{fi['index']}", key=f"zoom{fi['index']}")
                st.json({k: v for k, v in res.items() if k not in ["contact_sheet", "frames_info"]})

        else:
            txt = st.text_area("💬 Enter text to analyze (for similarity / sentiment)", height=160)
            if st.button("🚀 Analyze Text"):
                if not txt.strip():
                    st.error("Enter some text.")
                else:
                    with st.spinner("Running text analysis..."):
                        res = analyze_text(txt)
                    st.success(f"Sentiment: {res['sentiment']}")
                    st.metric("Confidence", f"{res['confidence']:.2f}%")
                    st.progress(min(1.0, res["similarity"] / 100.0))
                    st.json(res)

    with col2:
        st.markdown("### ⚙️ Quick Help & Info")
        st.markdown("- 🖼️ **Image:** Deepfake detection stub (face box marking).")
        st.markdown("- 🎥 **Video:** Gait + deepfake hybrid verification.")
        st.markdown("- 💬 **Text:** Sentiment & similarity analyzer.")
        st.info("Replace model stubs in `utils/image_model.py` & `utils/video_model.py` with your AI inference code.")

    # Footer micro animation
    if LOTTIE_FOOTER:
        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
        st_lottie(LOTTIE_FOOTER, height=120, key="footer_anim")
        st.markdown("</div>", unsafe_allow_html=True)


# ---------------------- ROUTING ----------------------
page = st.session_state.page
if page == "home":
    home_page()
elif page == "about":
    about_page()
elif page == "dashboard":
    dashboard_page()
else:
    home_page()
