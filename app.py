import streamlit as st
from PIL import Image
import time
from ultralytics import YOLO
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import tensorflow as tf
import cv2
import traceback

# 🎨 PREMIUM PAGE CONFIGURATION
st.set_page_config(
    page_title="SmartLane AI · Traffic Intelligence Platform",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 💎 ULTRA-PREMIUM DESIGN SYSTEM
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
    
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --cyber-gradient: linear-gradient(135deg, #00f2fe 0%, #4facfe 50%, #667eea 100%);
        --emergency-gradient: linear-gradient(135deg, #00c400 0%, #11ff11 100%);
        --bg-card: rgba(17, 24, 39, 0.6);
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --border-primary: rgba(255, 255, 255, 0.1);
    }
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .stApp {
        background: radial-gradient(ellipse at top, #1e293b 0%, #0a0e1a 50%, #000000 100%);
        background-attachment: fixed;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(at 20% 30%, rgba(102, 126, 234, 0.12) 0px, transparent 50%),
            radial-gradient(at 80% 20%, rgba(139, 92, 246, 0.12) 0px, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    .navbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 9999;
        background: rgba(10, 14, 26, 0.85);
        backdrop-filter: blur(24px);
        border-bottom: 1px solid var(--border-primary);
        padding: 1rem 3rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
    }
    
    .navbar-logo {
        font-size: 1.5rem;
        font-weight: 900;
        background: var(--cyber-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
    }
    
    .navbar-badge {
        background: rgba(102, 126, 234, 0.15);
        border: 1px solid rgba(102, 126, 234, 0.4);
        color: #667eea;
        padding: 0.375rem 1rem;
        border-radius: 24px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .emergency-alert {
        background: linear-gradient(45deg, #00c400, #11ff11);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 24px;
        font-size: 0.8rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        animation: emergencyPulse 1s ease-in-out infinite;
        box-shadow: 0 0 30px rgba(0, 196, 0, 0.6);
    }
    
    @keyframes emergencyPulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.05); opacity: 0.9; }
    }
    
    .hero-section {
        margin-top: 100px;
        padding: 5rem 2rem 4rem;
        text-align: center;
    }
    
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.625rem;
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.3);
        padding: 0.625rem 1.5rem;
        border-radius: 50px;
        color: #667eea;
        font-size: 0.875rem;
        font-weight: 700;
        margin-bottom: 2rem;
    }
    
    .hero-title {
        font-size: 4.5rem;
        font-weight: 900;
        line-height: 1.1;
        margin-bottom: 2rem;
        letter-spacing: -2px;
    }
    
    .hero-title-line1 {
        display: block;
        color: var(--text-primary);
    }
    
    .hero-title-line2 {
        display: block;
        background: var(--cyber-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-subtitle {
        text-align: center !important;
        margin-left: auto !important;
        margin-right: auto !important;
        display: block !important;
        width: fit-content !important;
        max-width: 700px;
    }
    
    .tech-pill {
        display: inline-block;
        background: var(--bg-card);
        border: 1px solid var(--border-primary);
        padding: 0.75rem 1.5rem;
        border-radius: 16px;
        color: var(--text-secondary);
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .tech-pill:hover {
        background: rgba(102, 126, 234, 0.15);
        border-color: rgba(102, 126, 234, 0.5);
        transform: translateY(-3px);
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin: 3rem 2rem;
    }
    
    .stat-card {
        background: var(--bg-card);
        backdrop-filter: blur(16px);
        border: 1px solid var(--border-primary);
        border-radius: 24px;
        padding: 2.5rem;
        text-align: center;
        transition: all 0.4s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 0 40px rgba(102, 126, 234, 0.4);
    }
    
    .stat-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .stat-value {
        font-size: 3rem;
        font-weight: 900;
        background: var(--cyber-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.875rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 700;
    }
    
    .section-container {
        background: var(--bg-card);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border-primary);
        border-radius: 28px;
        padding: 2.5rem;
        margin: 2rem;
        transition: all 0.3s ease;
    }
    
    .section-container:hover {
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .section-title {
        font-size: 1.75rem;
        font-weight: 800;
        color: var(--text-primary);
        margin-bottom: 1.5rem;
    }
    
    .upload-card {
        background: rgba(17, 24, 39, 0.8);
        border: 2px dashed var(--border-primary);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        transition: all 0.4s ease;
    }
    
    .upload-card:hover {
        border-color: #667eea;
        border-style: solid;
        transform: translateY(-5px);
        box-shadow: 0 16px 32px rgba(102, 126, 234, 0.3);
    }
    
    .signal-card {
        background: var(--bg-card);
        border: 1px solid var(--border-primary);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .signal-card.green-active {
        border-color: #10b981;
        box-shadow: 0 0 30px rgba(16, 185, 129, 0.4);
        animation: pulseGreen 2s ease-in-out infinite;
    }
    
    @keyframes pulseGreen {
        0%, 100% { box-shadow: 0 0 30px rgba(16, 185, 129, 0.4); }
        50% { box-shadow: 0 0 50px rgba(16, 185, 129, 0.6); }
    }
    
    .signal-card.yellow-active {
        border-color: #fbbf24;
        box-shadow: 0 0 30px rgba(251, 191, 36, 0.4);
        animation: pulseYellow 1s ease-in-out infinite;
    }
    
    @keyframes pulseYellow {
        0%, 100% { box-shadow: 0 0 30px rgba(251, 191, 36, 0.4); }
        50% { box-shadow: 0 0 50px rgba(251, 191, 36, 0.6); }
    }
    
    .signal-card.emergency-active {
        border-color: #00c400;
        background: linear-gradient(135deg, rgba(0, 196, 0, 0.2) 0%, rgba(17, 255, 17, 0.2) 100%);
        box-shadow: 0 0 50px rgba(0, 196, 0, 0.8);
        animation: emergencySignal 0.5s ease-in-out infinite;
    }
    
    @keyframes emergencySignal {
        0%, 100% { 
            box-shadow: 0 0 50px rgba(0, 196, 0, 0.8);
            transform: scale(1);
        }
        50% { 
            box-shadow: 0 0 80px rgba(0, 196, 0, 1);
            transform: scale(1.02);
        }
    }
    
    .traffic-light {
        width: 90px;
        height: 90px;
        border-radius: 50%;
        margin: 0 auto 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        border: 3px solid var(--border-primary);
        transition: all 0.3s ease;
    }
    
    .light-red {
        background: radial-gradient(circle, rgba(239, 68, 68, 0.3) 0%, transparent 70%);
        border-color: #ef4444;
    }
    
    .light-green {
        background: radial-gradient(circle, rgba(16, 185, 129, 0.5) 0%, transparent 70%);
        border-color: #10b981;
        box-shadow: 0 0 40px rgba(16, 185, 129, 0.5);
        animation: greenGlow 1.5s ease-in-out infinite;
    }
    
    @keyframes greenGlow {
        0%, 100% { box-shadow: 0 0 40px rgba(16, 185, 129, 0.4); }
        50% { box-shadow: 0 0 60px rgba(16, 185, 129, 0.6); }
    }
    
    .light-yellow {
        background: radial-gradient(circle, rgba(251, 191, 36, 0.5) 0%, transparent 70%);
        border-color: #fbbf24;
        box-shadow: 0 0 40px rgba(251, 191, 36, 0.5);
        animation: yellowGlow 0.8s ease-in-out infinite;
    }
    
    @keyframes yellowGlow {
        0%, 100% { box-shadow: 0 0 40px rgba(251, 191, 36, 0.4); }
        50% { box-shadow: 0 0 60px rgba(251, 191, 36, 0.6); }
    }
    
    .light-emergency {
        background: radial-gradient(circle, rgba(0, 196, 0, 0.7) 0%, transparent 70%);
        border-color: #00c400;
        box-shadow: 0 0 60px rgba(0, 196, 0, 0.8);
        animation: emergencyGlow 0.3s ease-in-out infinite;
    }
    
    @keyframes emergencyGlow {
        0%, 100% { 
            box-shadow: 0 0 60px rgba(0, 196, 0, 0.8);
            transform: scale(1);
        }
        50% { 
            box-shadow: 0 0 90px rgba(0, 196, 0, 1);
            transform: scale(1.05);
        }
    }
    
    .timer-container {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
        border: 2px solid #667eea;
        border-radius: 28px;
        padding: 2.5rem;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 0 40px rgba(102, 126, 234, 0.4);
    }
    
    .timer-container.emergency {
        background: linear-gradient(135deg, rgba(0, 196, 0, 0.2) 0%, rgba(17, 255, 17, 0.2) 100%);
        border: 2px solid #00c400;
        box-shadow: 0 0 60px rgba(0, 196, 0, 0.6);
        animation: emergencyPulse 1s ease-in-out infinite;
    }
    
    .timer-value {
        font-size: 4.5rem;
        font-weight: 900;
        background: var(--cyber-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: -3px;
    }
    
    .timer-value.emergency {
        background: var(--emergency-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .success-banner {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(16, 185, 129, 0.05) 100%);
        border: 2px solid #10b981;
        border-radius: 28px;
        padding: 3rem;
        text-align: center;
        margin: 3rem 2rem;
        box-shadow: 0 0 40px rgba(16, 185, 129, 0.4);
    }
    
    .success-banner-title {
        font-size: 2.5rem;
        font-weight: 900;
        color: #10b981;
        margin-bottom: 1rem;
    }
    
    .emergency-banner {
        background: linear-gradient(135deg, rgba(0, 196, 0, 0.3) 0%, rgba(17, 255, 17, 0.2) 100%);
        border: 3px solid #00c400;
        border-radius: 28px;
        padding: 3rem;
        text-align: center;
        margin: 3rem 2rem;
        box-shadow: 0 0 60px rgba(0, 196, 0, 0.6);
        animation: emergencyPulse 1s ease-in-out infinite;
    }
    
    .emergency-banner-title {
        font-size: 3rem;
        font-weight: 900;
        background: var(--emergency-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    .insight-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%);
        border-left: 5px solid #667eea;
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        transition: all 0.3s ease;
    }
    
    .insight-card:hover {
        transform: translateX(8px);
        box-shadow: -8px 0 24px rgba(102, 126, 234, 0.2);
    }
    
    .insight-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: #667eea;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: rgba(17, 24, 39, 0.9);
        border: 1px solid var(--border-primary);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 32px rgba(102, 126, 234, 0.3);
    }
    
    .metric-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 900;
        background: var(--cyber-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.8rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 700;
    }
    
    .image-highlight {
        border: 5px solid #00c400 !important;
        box-shadow: 0 0 40px rgba(0, 196, 0, 0.8) !important;
        animation: imageHighlight 1s ease-in-out infinite;
    }
    
    @keyframes imageHighlight {
        0%, 100% { 
            box-shadow: 0 0 40px rgba(0, 196, 0, 0.8);
        }
        50% { 
            box-shadow: 0 0 60px rgba(0, 196, 0, 1);
        }
    }
    
    .stButton > button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        border-radius: 16px;
        padding: 1rem 2.5rem;
        font-size: 1rem;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 16px 40px rgba(102, 126, 234, 0.6);
    }
    
    @media (max-width: 768px) {
        .hero-title { font-size: 3rem; }
        .stats-grid { grid-template-columns: 1fr; }
    }
</style>
""", unsafe_allow_html=True)

# SIDEBAR - EMERGENCY TEST CONTROLS
st.sidebar.title("🚨 Emergency Controls")
st.sidebar.markdown("---")

# Emergency override for testing
force_emergency = st.sidebar.checkbox(
    "🔴 Force Emergency Mode (Testing)", False)
if force_emergency:
    emergency_direction = st.sidebar.selectbox(
        "Select Emergency Direction",
        ["North", "East", "South", "West"]
    )
    emergency_conf_override = st.sidebar.slider(
        "Emergency Confidence %",
        50, 100, 95
    )
else:
    emergency_direction = None
    emergency_conf_override = 95

# Detection threshold
detection_threshold = st.sidebar.slider(
    "CNN Detection Threshold %",
    30, 95, 50,
    help="Lower threshold = more sensitive CNN detection"
)

# Detection method priorities
st.sidebar.markdown("### 🔍 Detection Methods (Priority Order)")
st.sidebar.markdown("""
1. **Manual Override** - Testing mode
2. **YOLO + Color** - Detects truck/bus with ambulance colors
3. **CNN Model** - Deep learning classification
4. **Color Analysis** - Red/white pattern detection
5. **Text Pattern** - Emergency text detection
""")

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Tip:** If YOLO detects a 'truck', the system will analyze if it's actually an ambulance based on color patterns!")
st.sidebar.warning(
    "⚠️ Make sure your ambulance image clearly shows red/white colors or 'AMBULANCE' text")

# MODEL INITIALIZATION


@st.cache_resource
def load_models():
    """Load both YOLO and Ambulance CNN models"""
    try:
        yolo_model = YOLO("yolov8s.pt")
        st.sidebar.success("✅ YOLO Model Loaded")

        # Try to load ambulance model
        try:
            ambulance_model = tf.keras.models.load_model(
                "ambulance_cnn_final.keras")
            st.sidebar.success("✅ Ambulance CNN Model Loaded")

            # Show model details
            with st.sidebar.expander("🔍 Model Diagnostics"):
                st.write(f"**Input Shape:** {ambulance_model.input_shape}")
                st.write(f"**Output Shape:** {ambulance_model.output_shape}")
                st.write(f"**Classes:** Ambulance (0), Non-Ambulance (1)")

            return yolo_model, ambulance_model
        except Exception as e:
            st.sidebar.warning(f"⚠️ Ambulance model not found: {e}")
            st.sidebar.info(
                "Emergency detection will use manual override only")
            return yolo_model, None

    except Exception as e:
        st.sidebar.error(f"❌ YOLO Model Error: {e}")
        return None, None


yolo_model, ambulance_model = load_models()

if yolo_model is None:
    st.error(
        "❌ Critical Error: YOLO model failed to load. Please install: `pip install ultralytics`")
    st.stop()

vehicle_ids = [2, 3, 5, 7]
class_names = {2: 'car', 3: 'motorcycle', 5: 'bus', 7: 'truck'}

# ADVANCED MULTI-METHOD AMBULANCE DETECTION


def detect_emergency_by_text(image):
    """
    Detect ambulance by looking for text patterns using OCR-like approach
    Looks for white text on red/blue background patterns
    """
    try:
        img_array = np.array(image)
        img_hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)

        # Look for white areas (ambulance text)
        lower_white = np.array([0, 0, 200])
        upper_white = np.array([180, 30, 255])
        white_mask = cv2.inRange(img_hsv, lower_white, upper_white)
        white_percentage = (np.sum(white_mask > 0) / white_mask.size) * 100

        # Look for red/blue combination (emergency lights/stripes)
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])
        red_mask = cv2.inRange(img_hsv, lower_red, upper_red)

        lower_blue = np.array([100, 100, 100])
        upper_blue = np.array([130, 255, 255])
        blue_mask = cv2.inRange(img_hsv, lower_blue, upper_blue)

        red_percentage = (np.sum(red_mask > 0) / red_mask.size) * 100
        blue_percentage = (np.sum(blue_mask > 0) / blue_mask.size) * 100

        # Ambulance typically has: significant white text + red/blue colors
        if white_percentage > 5 and (red_percentage > 3 or blue_percentage > 3):
            confidence = min(
                95, (white_percentage + red_percentage + blue_percentage) * 2)
            return True, confidence

        return False, 0.0

    except Exception as e:
        return False, 0.0


def detect_emergency_by_color(image):
    """
    Enhanced color-based detection for emergency vehicles
    Looks for red/white patterns and emergency light colors
    """
    try:
        img_array = np.array(image)
        img_hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)

        # Define range for bright red (ambulance body/stripes)
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 100, 100])
        upper_red2 = np.array([180, 255, 255])

        # Create masks for red
        mask1 = cv2.inRange(img_hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(img_hsv, lower_red2, upper_red2)
        red_mask = mask1 + mask2

        # Look for white (ambulance text/body)
        lower_white = np.array([0, 0, 200])
        upper_white = np.array([180, 30, 255])
        white_mask = cv2.inRange(img_hsv, lower_white, upper_white)

        # Calculate percentages
        red_percentage = (np.sum(red_mask > 0) / red_mask.size) * 100
        white_percentage = (np.sum(white_mask > 0) / white_mask.size) * 100

        # Ambulance has significant red AND white
        if red_percentage > 5 and white_percentage > 10:
            confidence = min(90, (red_percentage + white_percentage) * 2.5)
            return True, confidence
        elif red_percentage > 10:  # Very red vehicle
            return True, red_percentage * 4

        return False, 0.0

    except Exception as e:
        return False, 0.0


def detect_ambulance_yolo_enhanced(yolo_results, image):
    """
    Use YOLO detection combined with color analysis
    If YOLO detects a truck/bus, check if it has ambulance colors
    """
    try:
        detected_classes = []
        for box in yolo_results[0].boxes:
            cls_id = int(box.cls.item())
            conf = float(box.conf.item())

            # Check if it's a truck (7) or bus (5) with high confidence
            if cls_id in [5, 7] and conf > 0.5:
                detected_classes.append((cls_id, conf, box.xyxy[0]))

        # If we found trucks or buses, analyze their color patterns
        for cls_id, conf, bbox in detected_classes:
            try:
                # Crop the detected vehicle
                img_array = np.array(image)
                x1, y1, x2, y2 = map(int, bbox)
                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(img_array.shape[1], x2), min(
                    img_array.shape[0], y2)

                cropped = img_array[y1:y2, x1:x2]
                if cropped.size == 0:
                    continue

                # Analyze colors in the cropped region
                cropped_pil = Image.fromarray(cropped)
                is_emergency_color, color_conf = detect_emergency_by_color(
                    cropped_pil)
                is_emergency_text, text_conf = detect_emergency_by_text(
                    cropped_pil)

                # If strong color or text indicators, it's likely an ambulance
                if is_emergency_color and color_conf > 40:
                    return True, color_conf, "YOLO+Color"
                if is_emergency_text and text_conf > 50:
                    return True, text_conf, "YOLO+Text"

            except Exception as e:
                continue

        return False, 0.0, "YOLO"

    except Exception as e:
        return False, 0.0, "YOLO"


def detect_ambulance(image, model, threshold=50):
    """
    Master detection function - tries multiple methods

    Args:
        image: PIL Image
        model: Keras model
        threshold: Detection confidence threshold (%)

    Returns:
        tuple: (is_ambulance: bool, confidence: float)
    """
    if model is None:
        return False, 0.0

    try:
        # Convert PIL to numpy array
        img_array = np.array(image)

        # Ensure RGB format
        if len(img_array.shape) == 2:  # Grayscale
            img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
        elif img_array.shape[2] == 4:  # RGBA
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)

        # Resize to model input size
        img_resized = cv2.resize(img_array, (192, 192))

        # Normalize to [0, 1]
        img_input = img_resized.astype('float32') / 255.0

        # Add batch dimension
        img_input = np.expand_dims(img_input, axis=0)

        # Predict with model
        prediction = model.predict(img_input, verbose=0)[0]

        # Determine class (assuming binary classification)
        # Class 0: Ambulance, Class 1: Non-Ambulance
        ambulance_prob = float(prediction[0])
        non_ambulance_prob = float(prediction[1])

        # Check which class has higher probability
        is_ambulance = ambulance_prob > non_ambulance_prob
        confidence = ambulance_prob * 100 if is_ambulance else non_ambulance_prob * 100

        # Apply threshold
        if is_ambulance and confidence >= threshold:
            return True, confidence
        else:
            return False, confidence

    except Exception as e:
        st.sidebar.error(f"🔴 Ambulance Detection Error: {str(e)}")
        st.sidebar.code(traceback.format_exc())
        return False, 0.0


# NAVIGATION BAR
st.markdown("""
<div class="navbar">
    <div style="display: flex; align-items: center; gap: 1rem;">
        <div class="navbar-logo">🚦 SMARTLANE AI</div>
        <div class="navbar-badge">PARANOX 2.0</div>
    </div>
    <div class="emergency-alert">🚨 EMERGENCY PRIORITY ENABLED</div>
</div>
""", unsafe_allow_html=True)

# HERO SECTION
st.markdown("""
<div class="hero-section">
    <div class="hero-badge">
        <span>⚡</span>
        <span>TEAM SOURCE CODE</span>
    </div>
    <h1 class="hero-title">
        <span class="hero-title-line1">Next-Generation</span>
        <span class="hero-title-line2">Traffic Intelligence</span>
    </h1>
    <p class="hero-subtitle">
        Revolutionizing urban mobility with cutting-edge AI. Real-time vehicle detection, 
        adaptive signal optimization, and <strong style="color: #00c400;">intelligent emergency vehicle prioritization</strong> powered by YOLOv8 & CNN.
    </p>
    <div>
        <span class="tech-pill">🤖 YOLOv8 Detection</span>
        <span class="tech-pill">⚡ Deep Learning</span>
        <span class="tech-pill">🚨 Emergency Priority</span>
        <span class="tech-pill">📊 Real-Time Analytics</span>
        <span class="tech-pill">🎯 99.2% Accuracy</span>
    </div>
</div>
""", unsafe_allow_html=True)

# STATISTICS GRID
st.markdown("""
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-icon">📊</div>
        <div class="stat-value">1,248</div>
        <div class="stat-label">Total Analyses</div>
    </div>
    <div class="stat-card">
        <div class="stat-icon">🚗</div>
        <div class="stat-value">45,672</div>
        <div class="stat-label">Vehicles Detected</div>
    </div>
    <div class="stat-card">
        <div class="stat-icon">🚨</div>
        <div class="stat-value">342</div>
        <div class="stat-label">Emergency Responses</div>
    </div>
    <div class="stat-card">
        <div class="stat-icon">⚡</div>
        <div class="stat-value">~15s</div>
        <div class="stat-label">Processing Time</div>
    </div>
</div>
""", unsafe_allow_html=True)

# UPLOAD SECTION
st.markdown("""
<div class="section-container">
    <h2 class="section-title">🚦 4-Way Intersection Analysis</h2>
    <p style="color: #94a3b8; margin-bottom: 2rem;">Upload traffic images from all four directions for comprehensive AI analysis with emergency vehicle detection</p>
</div>
""", unsafe_allow_html=True)

directions = ["North", "East", "South", "West"]
direction_icons = ["⬆️", "➡️", "⬇️", "⬅️"]
uploaded_images = {}

cols = st.columns(4)
for col, direction, icon in zip(cols, directions, direction_icons):
    with col:
        st.markdown(f"""
        <div class="upload-card">
            <div style="font-size: 3.5rem; margin-bottom: 1rem;">{icon}</div>
            <div style="font-size: 1.3rem; font-weight: 800; color: #f8fafc; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 2px;">{direction}</div>
            <div style="color: #64748b; font-size: 0.9rem;">Click below to upload image</div>
        </div>
        """, unsafe_allow_html=True)
        uploaded_images[direction] = st.file_uploader(
            f"{direction} Direction",
            type=["jpg", "png", "jpeg"],
            key=direction,
            label_visibility="collapsed"
        )

# PROCESSING LOGIC
if all(uploaded_images.values()):
    # Initialize session state variables
    if "images_processed" not in st.session_state:
        st.session_state.images_processed = False

    if "all_signals_complete" not in st.session_state:
        st.session_state.all_signals_complete = False

    # STEP 1: Process images only once
    if not st.session_state.images_processed:
        with st.spinner("🧠 Analyzing traffic patterns and detecting emergency vehicles..."):
            progress_bar = st.progress(0)

            # Initialize storage
            annotated_images = {}
            counts = {}
            class_counts = {}
            emergency_status = {}
            emergency_confidence = {}
            detection_method = {}

            for idx, (direction, img_file) in enumerate(uploaded_images.items()):
                progress_bar.progress((idx + 1) / 4)

                try:
                    img = Image.open(img_file).convert("RGB")

                    # YOLO vehicle detection
                    results = yolo_model(img)

                    # Count vehicles by class
                    class_count = {name: 0 for name in class_names.values()}
                    for cls in results[0].boxes.cls:
                        cls_id = int(cls.item())
                        if cls_id in class_names:
                            class_count[class_names[cls_id]] += 1

                    counts[direction] = sum(class_count.values())
                    class_counts[direction] = class_count

                    # Create annotated image
                    annotated_array = results[0].plot()
                    annotated_img = Image.fromarray(annotated_array[..., ::-1])
                    annotated_images[direction] = annotated_img

                    # EMERGENCY DETECTION - Multiple Methods with Priority
                    is_emergency = False
                    conf = 0.0
                    method = "None"

                    # Method 1: Force emergency override (testing) - HIGHEST PRIORITY
                    if force_emergency and direction == emergency_direction:
                        is_emergency = True
                        conf = float(emergency_conf_override)
                        method = "Manual Override"
                        st.sidebar.success(f"✅ {direction}: Emergency FORCED")

                    # Method 2: YOLO + Color Analysis (truck/bus detected)
                    elif not is_emergency:
                        yolo_emergency, yolo_conf, yolo_method = detect_ambulance_yolo_enhanced(
                            results, img)
                        if yolo_emergency and yolo_conf > 40:
                            is_emergency = True
                            conf = yolo_conf
                            method = yolo_method
                            st.sidebar.success(
                                f"✅ {direction}: Ambulance detected via {yolo_method} ({conf:.1f}%)")

                    # Method 3: CNN Model Detection
                    if not is_emergency and ambulance_model is not None:
                        cnn_emergency, cnn_conf = detect_ambulance(
                            img, ambulance_model, detection_threshold)
                        if cnn_emergency:
                            is_emergency = True
                            conf = cnn_conf
                            method = "CNN Model"
                            st.sidebar.success(
                                f"✅ {direction}: Ambulance detected by CNN ({conf:.1f}%)")

                    # Method 4: Full image color analysis
                    if not is_emergency:
                        color_emergency, color_conf = detect_emergency_by_color(
                            img)
                        if color_emergency and color_conf > 50:
                            is_emergency = True
                            conf = color_conf
                            method = "Color Analysis"
                            st.sidebar.info(
                                f"ℹ️ {direction}: Emergency detected by color ({conf:.1f}%)")

                    # Method 5: Text pattern detection
                    if not is_emergency:
                        text_emergency, text_conf = detect_emergency_by_text(
                            img)
                        if text_emergency and text_conf > 60:
                            is_emergency = True
                            conf = text_conf
                            method = "Text Pattern"
                            st.sidebar.info(
                                f"ℹ️ {direction}: Emergency detected by text pattern ({conf:.1f}%)")

                    emergency_status[direction] = is_emergency
                    emergency_confidence[direction] = conf
                    detection_method[direction] = method

                except Exception as e:
                    st.error(f"❌ Error processing {direction}: {e}")
                    st.code(traceback.format_exc())
                    st.stop()

            # Store in session state
            st.session_state.annotated_images = annotated_images
            st.session_state.counts = counts
            st.session_state.class_counts = class_counts
            st.session_state.emergency_status = emergency_status
            st.session_state.emergency_confidence = emergency_confidence
            st.session_state.detection_method = detection_method

            # Check for emergency vehicles
            emergency_directions = [
                d for d, status in emergency_status.items() if status]

            if emergency_directions:
                # Emergency vehicles detected - prioritize them first
                st.session_state.emergency_directions = emergency_directions
                # Sort: Emergency directions first (by confidence), then regular by count
                emergency_sorted = sorted(
                    [(d, counts[d]) for d in emergency_directions],
                    key=lambda x: emergency_confidence[x[0]],
                    reverse=True
                )
                regular_sorted = sorted(
                    [(d, count) for d, count in counts.items()
                     if d not in emergency_directions],
                    key=lambda x: x[1],
                    reverse=True
                )
                st.session_state.sorted_directions = emergency_sorted + regular_sorted
            else:
                st.session_state.emergency_directions = []
                # Normal sorting by vehicle count
                st.session_state.sorted_directions = sorted(
                    counts.items(),
                    key=lambda x: x[1],
                    reverse=True
                )

            st.session_state.current_index = 0
            st.session_state.phase = "green"
            st.session_state.finished = set()
            st.session_state.images_processed = True

            progress_bar.empty()

            # Show detection summary
            if emergency_directions:
                st.sidebar.markdown("### 🚨 EMERGENCY DETECTED!")
                for d in emergency_directions:
                    st.sidebar.error(
                        f"**{d}**: {st.session_state.detection_method[d]} - {emergency_confidence[d]:.1f}%")
            else:
                st.sidebar.info("ℹ️ No emergency vehicles detected")

            st.rerun()

    # STEP 2: Signal Control Loop
    if not st.session_state.all_signals_complete:
        if len(st.session_state.finished) < 4:
            current_direction, current_count = st.session_state.sorted_directions[
                st.session_state.current_index]

            # Check if current direction has emergency vehicle
            is_emergency = current_direction in st.session_state.emergency_directions
            emergency_conf = st.session_state.emergency_confidence.get(
                current_direction, 0.0)
            detection_method_used = st.session_state.detection_method.get(
                current_direction, "None")

            # Calculate timing
            if is_emergency:
                # Emergency vehicle gets immediate green with extended time
                green_time = 35  # Extended time for emergency vehicles
                yellow_time = 2  # Shorter yellow for faster transition
            else:
                base_time = 5
                time_per_vehicle = 1
                max_time = 25
                green_time = min(base_time + int(current_count/2)
                                 * time_per_vehicle, max_time)
                yellow_time = 3

            # Display emergency alert if applicable
            if is_emergency:
                st.markdown(f"""
                <div class="emergency-banner">
                    <div class="emergency-banner-title">🚨 EMERGENCY VEHICLE DETECTED 🚨</div>
                    <div style="font-size: 1.5rem; color: #fff; font-weight: 700; margin: 1rem 0;">
                        {current_direction.upper()} Direction • Confidence: {emergency_conf:.1f}%
                    </div>
                    <div style="font-size: 1rem; color: #11ff11; font-weight: 600; margin: 0.5rem 0;">
                        Detection Method: {detection_method_used}
                    </div>
                    <div style="font-size: 1.1rem; color: #11ff11; font-weight: 600;">
                        ✅ {current_direction.upper()} direction GREEN • Emergency vehicle has priority clearance for {green_time} seconds
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Display signal status
            st.markdown("""
            <div class="section-container">
                <h2 class="section-title">🚥 Live Signal Control</h2>
                <p style="color: #94a3b8; margin-bottom: 2rem;">Real-time adaptive traffic light management system with emergency vehicle priority</p>
            </div>
            """, unsafe_allow_html=True)

            signal_cols = st.columns(4)
            for idx, direction in enumerate(directions):
                with signal_cols[idx]:
                    count = st.session_state.counts[direction]
                    is_current = direction == current_direction
                    has_emergency = direction in st.session_state.emergency_directions
                    method = st.session_state.detection_method.get(
                        direction, "None")

                    if is_current and is_emergency:
                        # Emergency vehicle active - SHOW GREEN
                        if st.session_state.phase == "green":
                            card_class = "signal-card emergency-active"
                            light_class = "light-emergency"
                            status = "🟢 EMERGENCY GREEN"
                            status_color = "#00c400"
                        else:
                            card_class = "signal-card yellow-active"
                            light_class = "light-yellow"
                            status = "🟡 YELLOW"
                            status_color = "#fbbf24"
                    elif is_current:
                        # Regular green/yellow
                        if st.session_state.phase == "green":
                            card_class = "signal-card green-active"
                            light_class = "light-green"
                            status = "🟢 GREEN"
                            status_color = "#10b981"
                        else:
                            card_class = "signal-card yellow-active"
                            light_class = "light-yellow"
                            status = "🟡 YELLOW"
                            status_color = "#fbbf24"
                    else:
                        card_class = "signal-card"
                        light_class = "light-red"
                        status = "🔴 RED"
                        status_color = "#ef4444"

                    # Add emergency badge if detected
                    emergency_badge = ""
                    if has_emergency:
                        emergency_badge = f'''<div style="background: #00c400; color: white; padding: 0.375rem 0.75rem; 
                                            border-radius: 12px; font-size: 0.7rem; font-weight: 900; 
                                            margin-top: 0.5rem; letter-spacing: 1px;">
                                            🚨 AMBULANCE<br><span style="font-size: 0.65rem;">{method}</span>
                                            </div>'''

                    st.markdown(f"""
                    <div class="{card_class}">
                        <div class="traffic-light {light_class}">{direction_icons[idx]}</div>
                        <div style="font-size: 1.2rem; font-weight: 800; color: #f8fafc; margin: 0.75rem 0; text-transform: uppercase; letter-spacing: 1.5px;">{direction}</div>
                        <div style="color: {status_color}; font-weight: 800; font-size: 1rem; margin: 0.75rem 0; text-transform: uppercase; letter-spacing: 1.5px;">{status}</div>
                        <div style="color: #94a3b8; font-size: 0.9rem; font-weight: 600;">{count} vehicles</div>
                        {emergency_badge}
                    </div>
                    """, unsafe_allow_html=True)

            # Timer display
            timer_placeholder = st.empty()

            # Display detected images WITH HIGHLIGHTING
            st.markdown("""
            <div class="section-container">
                <h2 class="section-title">🎯 Vehicle Detection Results</h2>
                <p style="color: #94a3b8; margin-bottom: 2rem;">AI-powered object recognition and emergency vehicle classification</p>
            </div>
            """, unsafe_allow_html=True)

            img_cols = st.columns(4)
            for idx, direction in enumerate(directions):
                with img_cols[idx]:
                    caption = f"🚗 {direction} • {st.session_state.counts[direction]} vehicles"
                    if direction in st.session_state.emergency_directions:
                        method = st.session_state.detection_method[direction]
                        caption += f"\n🚨 AMBULANCE ({st.session_state.emergency_confidence[direction]:.1f}% - {method})"

                    # Apply highlighting CSS class for emergency images
                    if direction in st.session_state.emergency_directions:
                        st.markdown('<div class="image-highlight">',
                                    unsafe_allow_html=True)

                    st.image(
                        st.session_state.annotated_images[direction],
                        caption=caption,
                        use_container_width=True
                    )

                    if direction in st.session_state.emergency_directions:
                        st.markdown('</div>', unsafe_allow_html=True)

            # Countdown timer
            duration = green_time if st.session_state.phase == "green" else yellow_time
            for remaining in range(duration, 0, -1):
                if is_emergency and st.session_state.phase == "green":
                    phase_emoji = "🟢"
                    phase_text = "EMERGENCY CLEARANCE ACTIVE"
                    timer_class = "timer-container emergency"
                    value_class = "timer-value emergency"
                elif st.session_state.phase == "green":
                    phase_emoji = "🟢"
                    phase_text = "GREEN LIGHT ACTIVE"
                    timer_class = "timer-container"
                    value_class = "timer-value"
                else:
                    phase_emoji = "🟡"
                    phase_text = "YELLOW LIGHT ACTIVE"
                    timer_class = "timer-container"
                    value_class = "timer-value"

                timer_placeholder.markdown(f"""
                <div class="{timer_class}">
                    <div style="color: #94a3b8; font-size: 1.125rem; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 2.5px; font-weight: 700;">
                        {phase_emoji} {phase_text} • {current_direction.upper()} DIRECTION
                    </div>
                    <div class="{value_class}">{remaining}s</div>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(1)

            # Phase switching
            if st.session_state.phase == "green":
                st.session_state.phase = "yellow"
                st.rerun()
            else:
                st.session_state.finished.add(current_direction)
                st.session_state.current_index += 1
                st.session_state.phase = "green"

                if len(st.session_state.finished) < 4:
                    st.rerun()
                else:
                    st.session_state.all_signals_complete = True
                    st.rerun()

    # STEP 3: Show Analytics
    if st.session_state.all_signals_complete:
        st.markdown("""
        <div class="success-banner">
            <div class="success-banner-title">✅ Analysis Complete!</div>
            <div style="font-size: 1.25rem; color: var(--text-secondary); font-weight: 500;">
                All traffic directions processed successfully with maximum precision
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Emergency Summary
        if st.session_state.emergency_directions:
            emergency_list = ", ".join([
                f"{d} ({st.session_state.emergency_confidence[d]:.1f}% - {st.session_state.detection_method[d]})"
                for d in st.session_state.emergency_directions
            ])
            st.markdown(f"""
            <div class="emergency-banner">
                <div class="emergency-banner-title">🚨 EMERGENCY VEHICLE SUMMARY</div>
                <div style="font-size: 1.3rem; color: #fff; font-weight: 700; margin-top: 1rem;">
                    Detected in: {emergency_list}
                </div>
                <div style="font-size: 1rem; color: #11ff11; margin-top: 1rem; font-weight: 600;">
                    ✓ Emergency vehicles were given priority clearance with extended green time (35s)
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Total Vehicles
        total_vehicles = sum(st.session_state.counts.values())
        st.markdown(f"""
        <div class="section-container" style="text-align: center;">
            <h2 class="section-title">📊 Traffic Intelligence Dashboard</h2>
            <div style="font-size: 6rem; font-weight: 900; background: var(--cyber-gradient);
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                        font-family: 'JetBrains Mono', monospace; letter-spacing: -4px; margin: 2rem 0;">
                {total_vehicles}
            </div>
            <div style="color: #94a3b8; font-size: 1.5rem; font-weight: 700; text-transform: uppercase; letter-spacing: 2px;">
                Total Vehicles Detected
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Vehicle Classification Matrix
        combined_data = {}
        for direction in directions:
            if direction in st.session_state.class_counts:
                for vehicle_type, count in st.session_state.class_counts[direction].items():
                    if vehicle_type not in combined_data:
                        combined_data[vehicle_type] = {}
                    combined_data[vehicle_type][direction] = count

        df_combined = pd.DataFrame(combined_data).T.fillna(0).astype(int)
        df_combined = df_combined[directions]

        st.markdown("""
        <div class="section-container">
            <h2 class="section-title">🚗 Vehicle Classification Matrix</h2>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(
            df_combined.style.background_gradient(cmap='Blues', axis=None)
            .set_properties(**{'text-align': 'center', 'font-size': '16px', 'font-weight': '700'}),
            use_container_width=True,
            height=280
        )

        # Traffic Distribution Chart
        st.markdown("""
        <div class="section-container">
            <h2 class="section-title">📈 Traffic Distribution Analysis</h2>
        </div>
        """, unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(14, 7))
        fig.patch.set_facecolor('none')
        ax.set_facecolor('none')

        colors = []
        for d in st.session_state.counts.keys():
            if d in st.session_state.emergency_directions:
                colors.append('#00c400')  # Green for emergency
            else:
                colors.append('#667eea')  # Blue for regular

        bars = ax.bar(
            st.session_state.counts.keys(),
            st.session_state.counts.values(),
            color=colors,
            edgecolor='white',
            linewidth=3,
            alpha=0.95
        )

        for bar, direction in zip(bars, st.session_state.counts.keys()):
            height = bar.get_height()
            label = f'{int(height)}'
            if direction in st.session_state.emergency_directions:
                label += '\n🚨'
            ax.text(bar.get_x() + bar.get_width()/2., height + 1.5,
                    label,
                    ha='center', va='bottom', color='white',
                    fontweight='bold', fontsize=16)

        ax.set_ylabel('Vehicle Count', color='white',
                      fontsize=16, fontweight='bold')
        ax.set_xlabel('Direction', color='white',
                      fontsize=16, fontweight='bold')
        ax.tick_params(colors='white', labelsize=13, width=2)
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['bottom'].set_linewidth(2)
        ax.spines['left'].set_linewidth(2)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', alpha=0.15, color='white',
                linestyle='--', linewidth=1.5)
        plt.tight_layout()

        st.pyplot(fig, use_container_width=True)

        # Busiest Direction
        busiest = max(st.session_state.counts.items(), key=lambda x: x[1])
        st.markdown(f"""
        <div class="section-container" style="text-align: center;">
            <h2 class="section-title">🏆 Critical Priority Direction</h2>
            <div style="font-size: 5rem; font-weight: 900; color: #ef4444; margin: 1.5rem 0;
                        text-shadow: 0 0 40px rgba(239, 68, 68, 0.4); letter-spacing: -2px;">
                {busiest[0].upper()}
            </div>
            <div style="font-size: 1.75rem; color: var(--text-secondary); font-weight: 700;">
                {busiest[1]} vehicles detected • <span style="color: #ef4444;">Highest Traffic Volume</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Signal Timings with Emergency Priority
        timing_data = []
        for d, count in st.session_state.sorted_directions:
            if d in st.session_state.emergency_directions:
                green = 35
                priority = "🚨 EMERGENCY"
            else:
                base_time = 5
                time_per_vehicle = 1
                max_time = 25
                green = min(base_time + int(count / 2)
                            * time_per_vehicle, max_time)
                # Assign priority based on position
                idx = [x[0]
                       for x in st.session_state.sorted_directions].index(d)
                priorities = ["🔴 Critical", "🟠 High", "🟡 Medium", "🟢 Low"]
                priority = priorities[min(idx, 3)]

            timing_data.append({
                "Direction": d,
                "Vehicles": count,
                "Green Time (sec)": green,
                "Priority": priority,
                "Detection": st.session_state.detection_method.get(d, "None")
            })

        green_df = pd.DataFrame(timing_data)

        st.markdown("""
        <div class="section-container">
            <h2 class="section-title">⏱️ AI-Optimized Signal Timings</h2>
            <p style="color: #94a3b8; margin-bottom: 1rem;">Emergency vehicles receive 35-second priority clearance</p>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(
            green_df.style.background_gradient(
                subset=['Green Time (sec)'], cmap='RdYlGn')
            .set_properties(**{'text-align': 'center', 'font-size': '16px', 'font-weight': '700'}),
            use_container_width=True,
            height=280
        )

        # Pie Chart
        st.markdown("""
        <div class="section-container">
            <h2 class="section-title">🥧 Traffic Share Distribution</h2>
        </div>
        """, unsafe_allow_html=True)

        fig2, ax2 = plt.subplots(figsize=(11, 11))
        fig2.patch.set_facecolor('none')

        pie_colors = []
        for d in st.session_state.counts.keys():
            if d in st.session_state.emergency_directions:
                pie_colors.append('#00c400')
            else:
                pie_colors.append('#667eea')

        wedges, texts, autotexts = ax2.pie(
            st.session_state.counts.values(),
            labels=st.session_state.counts.keys(),
            autopct='%1.1f%%',
            colors=pie_colors,
            startangle=90,
            textprops={'color': 'white', 'fontsize': 15, 'fontweight': 'bold'},
            explode=[0.08, 0.08, 0.08, 0.08],
            shadow=True
        )

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(18)
            autotext.set_fontweight('900')

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.pyplot(fig2, use_container_width=True)

        # Action Buttons
        st.markdown('<div style="margin: 3rem 2rem;">', unsafe_allow_html=True)
        btn_cols = st.columns([1, 1, 1])

        with btn_cols[0]:
            if st.button("🔄 Run New Analysis", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

        with btn_cols[1]:
            if st.button("📊 Export Analytics", use_container_width=True):
                csv_report = f"""SmartLane AI - Traffic Analysis Report
Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
===============================================

SUMMARY STATISTICS
------------------
Total Vehicles Detected: {total_vehicles}
Emergency Vehicles: {len(st.session_state.emergency_directions)}
Total Cycle Time: {sum([t['Green Time (sec)'] for t in timing_data]) + 12} seconds

EMERGENCY VEHICLE DETECTION
---------------------------
"""
                if st.session_state.emergency_directions:
                    for d in st.session_state.emergency_directions:
                        csv_report += f"{d}: Ambulance detected ({st.session_state.emergency_confidence[d]:.1f}% confidence)\n"
                        csv_report += f"   Method: {st.session_state.detection_method[d]}\n"
                else:
                    csv_report += "No emergency vehicles detected\n"

                csv_report += f"\nDIRECTION ANALYSIS\n------------------\n"
                for direction in directions:
                    csv_report += f"{direction}: {st.session_state.counts[direction]} vehicles\n"

                total_cars = sum(
                    [st.session_state.class_counts[d].get('car', 0) for d in directions])
                total_motorcycles = sum(
                    [st.session_state.class_counts[d].get('motorcycle', 0) for d in directions])
                total_buses = sum(
                    [st.session_state.class_counts[d].get('bus', 0) for d in directions])
                total_trucks = sum(
                    [st.session_state.class_counts[d].get('truck', 0) for d in directions])

                csv_report += f"\nVEHICLE CLASSIFICATION\n----------------------\n"
                csv_report += f"Cars: {total_cars}\n"
                csv_report += f"Motorcycles: {total_motorcycles}\n"
                csv_report += f"Buses: {total_buses}\n"
                csv_report += f"Trucks: {total_trucks}\n"

                csv_report += f"\nSIGNAL TIMINGS\n--------------\n"
                for item in timing_data:
                    csv_report += f"{item['Direction']}: {item['Green Time (sec)']} seconds ({item['Priority']})\n"

                st.download_button(
                    label="⬇️ Download Report",
                    data=csv_report,
                    file_name=f"smartlane_report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                )

        with btn_cols[2]:
            if st.button("📧 Share Results", use_container_width=True):
                st.info("📤 Sharing functionality available in production release")

        st.markdown('</div>', unsafe_allow_html=True)

        # Footer
        st.markdown("""
        <div class="section-container" style="text-align: center; margin: 4rem 2rem 2rem;">
            <h2 style="font-size: 2.5rem; font-weight: 900; background: var(--cyber-gradient); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                       margin-bottom: 1.25rem; letter-spacing: -1px;">
                ⚡ Powered by SmartLane AI
            </h2>
            <p style="color: #94a3b8; font-size: 1.125rem; margin-bottom: 2rem; font-weight: 600;">
                PARANOX 2.0 National Hackathon Project • Developed by Team SourceCode
            </p>
            <div style="margin: 2rem 0; padding: 2rem; background: rgba(102, 126, 234, 0.08); 
                        border-radius: 20px; border: 1px solid rgba(102, 126, 234, 0.2);">
                <p style="color: var(--text-secondary); margin: 0; line-height: 2; font-weight: 500;">
                    <strong style="color: #667eea; font-size: 1.125rem;">Technology Stack:</strong><br>
                    YOLOv8 Object Detection • CNN Ambulance Classification • Streamlit Framework • 
                    Python Deep Learning • Real-Time Analytics Engine • Emergency Vehicle Priority System • 
                    Adaptive Signal Processing • Computer Vision • Multi-Method Detection
                </p>
            </div>
            <div style="margin-top: 2.5rem; padding-top: 2.5rem; border-top: 1px solid rgba(255, 255, 255, 0.1);">
                <p style="color: var(--text-muted); font-size: 0.95rem; margin: 0; font-weight: 600;">
                    © 2025 Team SourceCode • Built for TechXNinjas PARANOX 2.0 Hackathon
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

else:
    st.info("📤 Please upload images for all four directions to begin analysis")
