import streamlit as st
import tensorflow as tf
import numpy as np
import os
import json
import glob
import pandas as pd
from remedies import REMEDIES_DB

# Set page config for premium styling
st.set_page_config(
    page_title="Plant Health Diagnosis System",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom premium CSS styling overrides
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

    /* Global Typography Force */
    * {
        font-family: 'Outfit', sans-serif !important;
    }

    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #030712 !important;
        background-image: 
            linear-gradient(to right, rgba(255, 255, 255, 0.015) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(255, 255, 255, 0.015) 1px, transparent 1px),
            radial-gradient(circle at 15% 15%, rgba(16, 185, 129, 0.12) 0%, transparent 55%),
            radial-gradient(circle at 85% 20%, rgba(6, 182, 212, 0.12) 0%, transparent 55%),
            radial-gradient(circle at 80% 80%, rgba(139, 92, 246, 0.1) 0%, transparent 55%),
            radial-gradient(circle at 20% 85%, rgba(244, 63, 94, 0.08) 0%, transparent 55%) !important;
        background-size: 35px 35px, 35px 35px, auto, auto, auto, auto !important;
        color: #f3f4f6 !important;
    }

    /* Hide default sidebar and collapse button to lock single-page app layout */
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    [data-testid="stSidebar"] {
        display: none !important;
    }
    .main .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }

    /* Floating navigation tabs styling utilizing first horizontal columns block */
    [data-testid="stHorizontalBlock"]:first-of-type {
        background: rgba(17, 24, 39, 0.65) !important;
        backdrop-filter: blur(24px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 50px !important;
        padding: 6px !important;
        max-width: 720px;
        margin-left: auto;
        margin-right: auto;
        margin-bottom: 3.5rem !important;
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.65),
            0 0 30px rgba(16, 185, 129, 0.08) !important;
    }

    [data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"] button {
        border-radius: 40px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        padding: 10px 20px !important;
        color: #9ca3af !important;
        border: none !important;
        background: transparent !important;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: none !important;
        width: 100% !important;
    }

    [data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"] button:hover {
        color: #ffffff !important;
        background: rgba(255, 255, 255, 0.05) !important;
        transform: translateY(-1px) !important;
    }

    /* Styling active vs inactive primary/secondary states inside top navbar */
    [data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"] button[kind="primary"] {
        background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%) !important;
        color: white !important;
        box-shadow: 
            0 8px 20px rgba(16, 185, 129, 0.35),
            0 0 15px rgba(6, 182, 212, 0.25) !important;
    }

    [data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"] button[kind="secondary"] {
        background: transparent !important;
        color: #9ca3af !important;
        border: none !important;
    }

    /* Premium styled glassmorphic cards */
    .glass-card {
        background: rgba(17, 24, 39, 0.4) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.07) !important;
        border-radius: 20px !important;
        padding: 2.2rem !important;
        margin-bottom: 1.8rem !important;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25) !important;
    }
    
    .glass-card:hover {
        transform: translateY(-6px);
        border-color: rgba(6, 182, 212, 0.35) !important;
        background: rgba(17, 24, 39, 0.55) !important;
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.35),
            0 0 25px rgba(6, 182, 212, 0.15) !important;
    }

    /* Color role modifiers for cards */
    .card-green {
        border: 1px solid rgba(16, 185, 129, 0.25) !important;
        background: rgba(16, 185, 129, 0.02) !important;
    }
    .card-green:hover {
        border-color: rgba(16, 185, 129, 0.6) !important;
        background: rgba(16, 185, 129, 0.04) !important;
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.35),
            0 0 25px rgba(16, 185, 129, 0.25) !important;
    }

    .card-blue {
        border: 1px solid rgba(6, 182, 212, 0.25) !important;
        background: rgba(6, 182, 212, 0.02) !important;
    }
    .card-blue:hover {
        border-color: rgba(6, 182, 212, 0.6) !important;
        background: rgba(6, 182, 212, 0.04) !important;
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.35),
            0 0 25px rgba(6, 182, 212, 0.25) !important;
    }

    .card-purple {
        border: 1px solid rgba(139, 92, 246, 0.25) !important;
        background: rgba(139, 92, 246, 0.02) !important;
    }
    .card-purple:hover {
        border-color: rgba(139, 92, 246, 0.6) !important;
        background: rgba(139, 92, 246, 0.04) !important;
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.35),
            0 0 25px rgba(139, 92, 246, 0.25) !important;
    }

    /* Crop Card color schemes with bright vibrant colors & glows */
    .crop-red {
        border: 1px solid rgba(244, 63, 94, 0.25) !important;
        background: rgba(244, 63, 94, 0.02) !important;
    }
    .crop-red:hover {
        border-color: rgba(244, 63, 94, 0.65) !important;
        background: rgba(244, 63, 94, 0.04) !important;
        box-shadow: 
            0 15px 30px rgba(0, 0, 0, 0.35),
            0 0 20px rgba(244, 63, 94, 0.2) !important;
    }

    .crop-gold {
        border: 1px solid rgba(245, 158, 11, 0.25) !important;
        background: rgba(245, 158, 11, 0.02) !important;
    }
    .crop-gold:hover {
        border-color: rgba(245, 158, 11, 0.65) !important;
        background: rgba(245, 158, 11, 0.04) !important;
        box-shadow: 
            0 15px 30px rgba(0, 0, 0, 0.35),
            0 0 20px rgba(245, 158, 11, 0.25) !important;
    }

    .crop-purple {
        border: 1px solid rgba(139, 92, 246, 0.25) !important;
        background: rgba(139, 92, 246, 0.02) !important;
    }
    .crop-purple:hover {
        border-color: rgba(139, 92, 246, 0.65) !important;
        background: rgba(139, 92, 246, 0.04) !important;
        box-shadow: 
            0 15px 30px rgba(0, 0, 0, 0.35),
            0 0 20px rgba(139, 92, 246, 0.25) !important;
    }

    .crop-green {
        border: 1px solid rgba(16, 185, 129, 0.25) !important;
        background: rgba(16, 185, 129, 0.02) !important;
    }
    .crop-green:hover {
        border-color: rgba(16, 185, 129, 0.65) !important;
        background: rgba(16, 185, 129, 0.04) !important;
        box-shadow: 
            0 15px 30px rgba(0, 0, 0, 0.35),
            0 0 20px rgba(16, 185, 129, 0.25) !important;
    }

    .crop-slate {
        border: 1px solid rgba(6, 182, 212, 0.25) !important;
        background: rgba(6, 182, 212, 0.02) !important;
    }
    .crop-slate:hover {
        border-color: rgba(6, 182, 212, 0.65) !important;
        background: rgba(6, 182, 212, 0.04) !important;
        box-shadow: 
            0 15px 30px rgba(0, 0, 0, 0.35),
            0 0 20px rgba(6, 182, 212, 0.25) !important;
    }

    /* Form input uploader overrides */
    [data-testid="stFileUploader"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    [data-testid="stFileUploader"] section {
        background: rgba(17, 24, 39, 0.45) !important;
        backdrop-filter: blur(20px) !important;
        border: 2px dashed rgba(16, 185, 129, 0.3) !important;
        border-radius: 20px !important;
        padding: 3rem 2rem !important;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2) !important;
    }
    [data-testid="stFileUploader"] section:hover {
        border-color: #06b6d4 !important;
        background: rgba(17, 24, 39, 0.55) !important;
        box-shadow: 
            0 15px 35px rgba(0,0,0,0.35),
            0 0 25px rgba(6, 182, 212, 0.18) !important;
    }
    [data-testid="stFileUploader"] section [data-testid="stMarkdownContainer"] p {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        font-size: 15px !important;
    }
    [data-testid="stFileUploader"] section button {
        background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        padding: 0.5rem 1.5rem !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stFileUploader"] section button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 18px rgba(16, 185, 129, 0.45) !important;
    }

    /* Button styles */
    .stButton>button {
        background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.8rem 2.5rem !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        letter-spacing: 0.5px;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.25) !important;
        width: auto;
    }

    .stButton>button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 
            0 12px 30px rgba(16, 185, 129, 0.4),
            0 0 15px rgba(6, 182, 212, 0.25) !important;
        color: white !important;
    }

    /* Text gradient animation */
    @keyframes textShine {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .premium-title {
        background: linear-gradient(135deg, #34d399 0%, #10b981 50%, #06b6d4 100%) !important;
        -webkit-background-clip: text !important;
        background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        color: transparent !important;
        font-weight: 800;
    }
    .premium-title span {
        background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%) !important;
        -webkit-background-clip: text !important;
        background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        color: transparent !important;
    }

    /* 3D floating animation */
    @keyframes float {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-12px) rotate(2deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }

    .floating-card {
        animation: float 5s ease-in-out infinite;
    }

    /* Badges */
    .disease-badge {
        background: rgba(255, 255, 255, 0.04);
        color: #e2e8f0;
        padding: 5px 12px;
        border-radius: 30px;
        font-size: 11.5px;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.08);
        display: inline-block;
        transition: all 0.2s ease;
    }
    
    .disease-badge:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.2);
        transform: scale(1.05);
    }

    /* Image preview wrapper */
    .image-container {
        padding: 12px;
        background: rgba(17, 24, 39, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 20px;
        box-shadow: 
            0 15px 40px rgba(0, 0, 0, 0.45),
            0 0 20px rgba(16, 185, 129, 0.05);
    }

    /* System Flowchart styling */
    .flow-container {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        margin: 2.5rem 0;
        flex-wrap: wrap;
    }
    .flow-step {
        flex: 1;
        min-width: 150px;
        background: rgba(255, 255, 255, 0.015);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        padding: 1.2rem;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .flow-step:hover {
        border-color: rgba(16, 185, 129, 0.4);
        background: rgba(16, 185, 129, 0.03);
        transform: translateY(-4px);
        box-shadow: 0 10px 20px rgba(16, 185, 129, 0.05);
    }
    .flow-number {
        font-size: 1.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #10b981, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.4rem;
    }

    /* Photo Gallery */
    .gallery-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1.5rem;
        margin-top: 1.5rem;
    }
    .gallery-card {
        background: rgba(17, 24, 39, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    .gallery-card:hover {
        transform: translateY(-5px);
        border-color: rgba(139, 92, 246, 0.4);
        box-shadow: 
            0 15px 30px rgba(0, 0, 0, 0.35),
            0 0 15px rgba(139, 92, 246, 0.15);
    }
    .gallery-img {
        width: 100%;
        height: 160px;
        object-fit: cover;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    .gallery-info {
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# Helper function to read live training progress from brain log files
def get_training_progress():
    brain_dir = os.path.expanduser("~/.gemini/antigravity-ide/brain")
    if not os.path.exists(brain_dir):
        return None
    
    # Search for all task logs recursively (including dot directories like .system_generated)
    log_files = []
    for root, dirs, files in os.walk(brain_dir):
        for file in files:
            if file.endswith(".log") and "task-" in file:
                log_files.append(os.path.join(root, file))
                
    if not log_files:
        return None
    
    # Sort by modification time to read the latest active log file
    log_files.sort(key=os.path.getmtime, reverse=True)
    for log_path in log_files:
        try:
            with open(log_path, 'r', errors='ignore') as f:
                lines = f.readlines()
            
            # Verify this is the model training task log
            if any("Starting training" in l for l in lines[:150]):
                # Look for the latest batch/progress line
                for line in reversed(lines):
                    if "/2181" in line:
                        parts = line.strip().split(" - ")
                        progress_part = parts[0].split(" [")[0].strip()  # e.g., "590/2181"
                        
                        eta = "Calculating..."
                        loss = "Calculating..."
                        accuracy = "Calculating..."
                        
                        for part in parts[1:]:
                            if "ETA" in part:
                                eta = part.split(": ")[1].strip()
                            elif "loss" in part:
                                loss = part.split(": ")[1].strip()
                            elif "accuracy" in part:
                                try:
                                    acc_val = float(part.split(": ")[1].strip())
                                    accuracy = f"{acc_val * 100:.1f}%"
                                except:
                                    accuracy = part.split(": ")[1].strip()
                                    
                        # Find current active Epoch label
                        epoch = "Unknown"
                        for l in reversed(lines):
                            if "Epoch " in l and "/" in l:
                                epoch = l.strip()
                                break
                                
                        return {
                            "epoch": epoch,
                            "progress": progress_part,
                            "eta": eta,
                            "loss": loss,
                            "accuracy": accuracy
                        }
        except:
            continue
    return None


def get_crop_style(crop_name):
    name = crop_name.lower().strip()
    if any(k in name for k in ['apple', 'pepper', 'soybean']):
        return 'crop-green'
    elif any(k in name for k in ['cherry', 'strawberry', 'raspberry', 'peach', 'tomato']):
        return 'crop-red'
    elif any(k in name for k in ['grape', 'blueberry']):
        return 'crop-purple'
    elif any(k in name for k in ['corn', 'orange', 'squash']):
        return 'crop-gold'
    else:
        return 'crop-slate'

def get_crop_emoji(crop_name):
    emojis = {
        'apple': '🍎', 'blueberry': '🫐', 'cherry': '🍒', 'corn': '🌽',
        'grape': '🍇', 'orange': '🍊', 'peach': '🍑', 'pepper': '🫑',
        'potato': '🥔', 'raspberry': '🍓', 'soybean': '🫘', 'squash': '🥒',
        'strawberry': '🍓', 'tomato': '🍅'
    }
    return emojis.get(crop_name.lower().strip(), '🌱')


# Cache model loading to optimize performance
@st.cache_resource
def load_prediction_model():
    return tf.keras.models.load_model("trained_plant_disease_model.keras")

# TensorFlow Model Prediction helper
def model_prediction(test_image):
    model = load_prediction_model()
    image = tf.keras.preprocessing.image.load_img(test_image, target_size=(128, 128))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])  # convert single image to batch
    predictions = model.predict(input_arr)
    return np.argmax(predictions)  # return index of max element

# Header Section
st.markdown("""
<div style="text-align: center; margin-top: 1rem; margin-bottom: 2.5rem; background: rgba(17, 24, 39, 0.35); border: 1px solid rgba(255, 255, 255, 0.05); padding: 1.6rem; border-radius: 24px; backdrop-filter: blur(12px); box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
    <div style="font-size: 3rem; font-weight: 900; background: linear-gradient(135deg, #10b981 0%, #a3e635 40%, #06b6d4 75%, #8b5cf6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; display: flex; align-items: center; justify-content: center; gap: 12px; letter-spacing: -1.5px; animation: textShine 6s linear infinite; line-height: 1.2;">
        🌿 PlantHealth.AI
    </div>
    <div style="color: #9ca3af; font-size: 12.5px; font-weight: 700; margin-top: 8px; letter-spacing: 2.5px; text-transform: uppercase; display: flex; align-items: center; justify-content: center; gap: 8px; flex-wrap: wrap;">
        <span style="display:inline-block; width:6px; height:6px; background:#10b981; border-radius:50%;"></span>
        Neural Phytopathology Scanner for Smart Farms
        <span style="display:inline-block; width:6px; height:6px; background:#06b6d4; border-radius:50%;"></span>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize session state for active tab selection if not set
if 'active_tab' not in st.session_state:
    st.session_state['active_tab'] = 0

# Custom top navbar using Streamlit columns & styled buttons
nav_cols = st.columns(3)
with nav_cols[0]:
    btn_type = "primary" if st.session_state['active_tab'] == 0 else "secondary"
    if st.button("🏠 Home Hub", type=btn_type, use_container_width=True):
        st.session_state['active_tab'] = 0
        try: st.rerun()
        except AttributeError: st.experimental_rerun()
with nav_cols[1]:
    btn_type = "primary" if st.session_state['active_tab'] == 1 else "secondary"
    if st.button("📊 Dataset & Curves", type=btn_type, use_container_width=True):
        st.session_state['active_tab'] = 1
        try: st.rerun()
        except AttributeError: st.experimental_rerun()
with nav_cols[2]:
    btn_type = "primary" if st.session_state['active_tab'] == 2 else "secondary"
    if st.button("🔬 Leaf Diagnosis", type=btn_type, use_container_width=True):
        st.session_state['active_tab'] = 2
        try: st.rerun()
        except AttributeError: st.experimental_rerun()

# ================= TAB 1: HOME PAGE =================
if st.session_state['active_tab'] == 0:
    hero_col1, hero_col2 = st.columns([1.2, 1])

    with hero_col1:
        st.markdown("""
        <div style="margin-top: 1rem;">
            <span style="background: rgba(16, 185, 129, 0.08); color: #34d399; padding: 6px 16px; border-radius: 30px; font-size: 13.5px; font-weight: 800; letter-spacing: 0.5px; border: 1px solid rgba(16, 185, 129, 0.15);">
                🌱 DEEP LEARNING AGRO-INTELLIGENCE
            </span>
            <div style="font-size: 3.4rem; line-height: 1.15; margin-top: 1.2rem; margin-bottom: 0.2rem; font-weight: 800; letter-spacing: -1.5px; background: linear-gradient(135deg, #10b981 0%, #a3e635 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; display: inline-block; font-family: 'Outfit', sans-serif;">
                Is Your Plant Sick?
            </div>
            <br>
            <div style="font-size: 3.4rem; line-height: 1.15; margin-top: 0; margin-bottom: 1.2rem; font-weight: 800; letter-spacing: -1.5px; background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; display: inline-block; font-family: 'Outfit', sans-serif;">
                Get Instant Remedies.
            </div>
            <p style="color: #94a3b8; font-size: 1.1rem; line-height: 1.65; margin-bottom: 1.5rem; max-width: 600px;">
                Protect your farm yields in real-time. Simply upload a leaf image to diagnose plant diseases and discover organic or chemical remedies instantly.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Primary Action CTA Button to Programmatically Navigate to Upload Tab
        if st.button("Try It Now ➔", type="primary", key="btn_try_now_cta"):
            st.session_state['active_tab'] = 2
            try: st.rerun()
            except AttributeError: st.experimental_rerun()
            
        st.markdown("""
        <div style="margin-top: 2rem; display: flex; gap: 1.2rem; margin-bottom: 2rem; flex-wrap: wrap;">
            <div style="background: rgba(255,255,255,0.01); padding: 12px 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); min-width: 130px;">
                <div style="font-size: 20px; font-weight: 800; color: #10b981; line-height: 1.2;">97.9%</div>
                <div style="font-size: 11px; color: #94a3b8; margin-top: 2px;">Accuracy</div>
            </div>
            <div style="background: rgba(255,255,255,0.01); padding: 12px 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); min-width: 130px;">
                <div style="font-size: 20px; font-weight: 800; color: #60a5fa; line-height: 1.2;">38</div>
                <div style="font-size: 11px; color: #94a3b8; margin-top: 2px;">Crops Classified</div>
            </div>
            <div style="background: rgba(255,255,255,0.01); padding: 12px 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); min-width: 130px;">
                <div style="font-size: 20px; font-weight: 800; color: #f59e0b; line-height: 1.2;">&lt; 1.5s</div>
                <div style="font-size: 11px; color: #94a3b8; margin-top: 2px;">Speed</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with hero_col2:
        st.markdown("""
        <div class="floating-card image-container" style="text-align: center;">
            <img src="https://images.unsplash.com/photo-1530836369250-ef72a3f5cda8?auto=format&fit=crop&w=800&q=80" style="width: 100%; height: auto; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05); box-shadow: 0 15px 40px rgba(0,0,0,0.4);" alt="Agro-Intelligence Leaf Scan">
            <div style="color: #94a3b8; font-size: 12.5px; font-weight: 600; margin-top: 0.8rem;">🌿 Agro-Intelligence Leaf Scan</div>
        </div>
        """, unsafe_allow_html=True)

    # Core Features Row & Enhanced Visual Sections
    st.markdown("""
    <div style="margin-top: 4rem; margin-bottom: 2rem; border-top: 1px solid rgba(255,255,255,0.04); padding-top: 3rem;">
        <h3 style="color: #ffffff; font-size: 1.7rem; margin-bottom: 1.8rem; font-weight: 700; text-align: center;">Advanced Capabilities</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem;">
            <div class="glass-card card-green">
                <div style="font-size: 2.2rem; margin-bottom: 0.8rem;">🧠</div>
                <h4 style="margin: 0 0 0.6rem 0; font-weight: 700; font-size: 1.15rem;">10-Layer Convolutional Network</h4>
                <p style="margin: 0; color: #94a3b8; font-size: 13.5px; line-height: 1.55;">
                    Utilizes Conv2D blocks with batch normalization, dropouts, and linear units to isolate color anomalies, vein patterns, and mold spotting.
                </p>
            </div>
            <div class="glass-card card-blue">
                <div style="font-size: 2.2rem; margin-bottom: 0.8rem;">🔬</div>
                <h4 style="margin: 0 0 0.6rem 0; font-weight: 700; font-size: 1.15rem;">Scientific Remedy Database</h4>
                <p style="margin: 0; color: #94a3b8; font-size: 13.5px; line-height: 1.55;">
                    Instantly matches identified categories to targeted scientific names, structural symptoms, and chemical or organic control options.
                </p>
            </div>
            <div class="glass-card card-purple">
                <div style="font-size: 2.2rem; margin-bottom: 0.8rem;">🌿</div>
                <h4 style="margin: 0 0 0.6rem 0; font-weight: 700; font-size: 1.15rem;">Ecological Control Priority</h4>
                <p style="margin: 0; color: #94a3b8; font-size: 13.5px; line-height: 1.55;">
                    Recommends organic fertilizers, structural pruning, and bio-controls first, allowing farmers to reduce ecological impacts.
                </p>
            </div>
        </div>
    </div>

    <!-- Diagnostic Pipeline Section -->
    <div style="margin-top: 3.5rem; margin-bottom: 2rem; border-top: 1px solid rgba(255,255,255,0.04); padding-top: 3rem;">
        <h3 style="color: #ffffff; font-size: 1.7rem; margin-bottom: 0.5rem; font-weight: 700; text-align: center;">Deep Learning Diagnostics Pipeline</h3>
        <p style="color: #94a3b8; font-size: 14px; text-align: center; margin-bottom: 2.5rem;">How the AI process transforms a raw field photo into actionable remedies</p>
        <div class="flow-container">
            <div class="flow-step">
                <div class="flow-number">01</div>
                <h5 style="margin: 0 0 0.4rem 0; color: #ffffff; font-weight: 700; font-size: 0.95rem;">Image Capture</h5>
                <p style="margin: 0; color: #94a3b8; font-size: 12px; line-height: 1.4;">High-res crop leaf uploaded via client device.</p>
            </div>
            <div class="flow-step">
                <div class="flow-number">02</div>
                <h5 style="margin: 0 0 0.4rem 0; color: #ffffff; font-weight: 700; font-size: 0.95rem;">Preprocessing</h5>
                <p style="margin: 0; color: #94a3b8; font-size: 12px; line-height: 1.4;">Resized to 128x128 pixels and normalized.</p>
            </div>
            <div class="flow-step">
                <div class="flow-number">03</div>
                <h5 style="margin: 0 0 0.4rem 0; color: #ffffff; font-weight: 700; font-size: 0.95rem;">Inference Pass</h5>
                <p style="margin: 0; color: #94a3b8; font-size: 12px; line-height: 1.4;">10-layer CNN extracts color/texture descriptors.</p>
            </div>
            <div class="flow-step">
                <div class="flow-number">04</div>
                <h5 style="margin: 0 0 0.4rem 0; color: #ffffff; font-weight: 700; font-size: 0.95rem;">Remedy Synthesis</h5>
                <p style="margin: 0; color: #94a3b8; font-size: 12px; line-height: 1.4;">Disease mapping database yields treatment protocols.</p>
            </div>
        </div>
    </div>

    <!-- Smart Farming Gallery Grid Section -->
    <div style="margin-top: 3.5rem; margin-bottom: 2rem; border-top: 1px solid rgba(255,255,255,0.04); padding-top: 3rem;">
        <h3 style="color: #ffffff; font-size: 1.7rem; margin-bottom: 0.5rem; font-weight: 700; text-align: center;">Agro-Tech in Action</h3>
        <p style="color: #94a3b8; font-size: 14px; text-align: center; margin-bottom: 2rem;">Pioneering smart farming and digital phytopathologic solutions</p>
        <div class="gallery-grid">
            <div class="gallery-card">
                <img class="gallery-img" src="https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?auto=format&fit=crop&w=600&q=80" alt="Greenhouse Automation">
                <div class="gallery-info">
                    <h5 style="margin: 0 0 0.3rem 0; color: #10b981; font-weight: 700; font-size: 0.95rem;">Glasshouse Systems</h5>
                    <p style="margin: 0; color: #94a3b8; font-size: 12px; line-height: 1.4;">Controlled climate systems optimize crop vigor and prevent airborne spores.</p>
                </div>
            </div>
            <div class="gallery-card">
                <img class="gallery-img" src="https://images.unsplash.com/photo-1416879595882-3373a0480b5b?auto=format&fit=crop&w=600&q=80" alt="Pathogen Research">
                <div class="gallery-info">
                    <h5 style="margin: 0 0 0.3rem 0; color: #06b6d4; font-weight: 700; font-size: 0.95rem;">Phytopathology Lab</h5>
                    <p style="margin: 0; color: #94a3b8; font-size: 12px; line-height: 1.4;">Microscopic scans map chlorotic spots and structural rust elements.</p>
                </div>
            </div>
            <div class="gallery-card">
                <img class="gallery-img" src="https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?auto=format&fit=crop&w=600&q=80" alt="Sustainable Yields">
                <div class="gallery-info">
                    <h5 style="margin: 0 0 0.3rem 0; color: #a78bfa; font-weight: 700; font-size: 0.95rem;">Yield Optimization</h5>
                    <p style="margin: 0; color: #94a3b8; font-size: 12px; line-height: 1.4;">Organic fertilizer protocols and canopy airflow mapping secure crop output.</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Why Leaf Diagnostics Matter Section -->
    <div style="margin-top: 3.5rem; margin-bottom: 2rem; border-top: 1px solid rgba(255,255,255,0.04); padding-top: 3rem;">
        <h3 style="color: #ffffff; font-size: 1.7rem; margin-bottom: 0.5rem; font-weight: 700; text-align: center;">🌾 Why Plant Pathology Testing Matters</h3>
        <p style="color: #94a3b8; font-size: 14px; text-align: center; margin-bottom: 2.5rem;">Understand the ecological and economic benefits of early diagnostic testing</p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.5rem;">
            <div class="glass-card card-green" style="padding: 1.5rem !important; margin-bottom: 0 !important;">
                <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">🛡️</div>
                <h5 style="margin: 0 0 0.4rem 0; color: #ffffff; font-weight: 700; font-size: 0.95rem;">Early Intervention</h5>
                <p style="margin: 0; color: #cbd5e1; font-size: 12.5px; line-height: 1.45;">
                    Detecting rust, blight, or spotting early stops the pathogen from replicating and devastating neighboring crop rows.
                </p>
            </div>
            <div class="glass-card card-blue" style="padding: 1.5rem !important; margin-bottom: 0 !important;">
                <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">💵</div>
                <h5 style="margin: 0 0 0.4rem 0; color: #ffffff; font-weight: 700; font-size: 0.95rem;">Cost Minimization</h5>
                <p style="margin: 0; color: #cbd5e1; font-size: 12.5px; line-height: 1.45;">
                    Avoid buying expensive broad-spectrum chemicals. Targeting the exact cause (fungal vs. bacterial) saves money and efforts.
                </p>
            </div>
            <div class="glass-card card-purple" style="padding: 1.5rem !important; margin-bottom: 0 !important;">
                <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">💧</div>
                <h5 style="margin: 0 0 0.4rem 0; color: #ffffff; font-weight: 700; font-size: 0.95rem;">Reduced Chemical Load</h5>
                <p style="margin: 0; color: #cbd5e1; font-size: 12.5px; line-height: 1.45;">
                    Applying target organic remedies maintains soil microbiome integrity and keeps toxic runoffs out of local water aquifers.
                </p>
            </div>
            <div class="glass-card card-green" style="padding: 1.5rem !important; margin-bottom: 0 !important;">
                <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">📈</div>
                <h5 style="margin: 0 0 0.4rem 0; color: #ffffff; font-weight: 700; font-size: 0.95rem;">Maximize Yield Vigor</h5>
                <p style="margin: 0; color: #cbd5e1; font-size: 12.5px; line-height: 1.45;">
                    Healthy plants translate to premium grade harvests. Protect crop market value and enhance farm output predictability.
                </p>
            </div>
        </div>
    </div>

    <!-- Farmer Centric Resource Hub Section -->
    <div style="margin-top: 3.5rem; margin-bottom: 2rem; border-top: 1px solid rgba(255,255,255,0.04); padding-top: 3rem;">
        <h3 style="color: #ffffff; font-size: 1.7rem; margin-bottom: 0.5rem; font-weight: 700; text-align: center;">📖 Farmer Educational Hub</h3>
        <p style="color: #94a3b8; font-size: 14px; text-align: center; margin-bottom: 2.5rem;">Access scientific articles and guides to cultivate sustainable, pathogen-resistant farms</p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem;">
            <div class="glass-card card-green" style="padding: 1.5rem !important; margin-bottom: 0 !important; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <img src="https://images.unsplash.com/photo-1593113598332-cd288d649433?auto=format&fit=crop&w=600&q=80" style="width: 100%; height: 160px; object-fit: cover; border-radius: 12px; margin-bottom: 1.2rem; border: 1px solid rgba(255,255,255,0.05);" alt="UN FAO Treaty">
                    <h4 style="margin: 0 0 0.6rem 0; font-weight: 700; font-size: 1.1rem; color: #10b981;">United Nations FAO Plant Treaty</h4>
                    <p style="margin: 0 0 1.2rem 0; color: #cbd5e1; font-size: 13px; line-height: 1.5;">
                        Learn about global agreements on plant genetic resources for food security and sustainable agricultural management.
                    </p>
                </div>
                <a href="https://www.fao.org/plant-treaty/en/" target="_blank" style="color: #10b981; font-weight: 700; font-size: 13.5px; text-decoration: none; display: inline-flex; align-items: center; gap: 4px; margin-top: auto;">
                    Read FAO Treaty ↗
                </a>
            </div>
            <div class="glass-card card-blue" style="padding: 1.5rem !important; margin-bottom: 0 !important; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <img src="https://images.unsplash.com/photo-1464226184884-fa280b87c399?auto=format&fit=crop&w=600&q=80" style="width: 100%; height: 160px; object-fit: cover; border-radius: 12px; margin-bottom: 1.2rem; border: 1px solid rgba(255,255,255,0.05);" alt="USDA Soil Health">
                    <h4 style="margin: 0 0 0.6rem 0; font-weight: 700; font-size: 1.1rem; color: #06b6d4;">USDA Soil Health Resource Guides</h4>
                    <p style="margin: 0 0 1.2rem 0; color: #cbd5e1; font-size: 13px; line-height: 1.5;">
                        Strong crops require healthy soil. Discover soil biology, cover crops cultivation guidelines, and microbiome defense concepts.
                    </p>
                </div>
                <a href="https://www.nrcs.usda.gov/resources/educational-resources/soil-health" target="_blank" style="color: #06b6d4; font-weight: 700; font-size: 13.5px; text-decoration: none; display: inline-flex; align-items: center; gap: 4px; margin-top: auto;">
                    Explore USDA Soil Health ↗
                </a>
            </div>
            <div class="glass-card card-purple" style="padding: 1.5rem !important; margin-bottom: 0 !important; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <img src="https://images.unsplash.com/photo-1470240731273-7821a6eeb6bd?auto=format&fit=crop&w=600&q=80" style="width: 100%; height: 160px; object-fit: cover; border-radius: 12px; margin-bottom: 1.2rem; border: 1px solid rgba(255,255,255,0.05);" alt="EPA IPM">
                    <h4 style="margin: 0 0 0.6rem 0; font-weight: 700; font-size: 1.1rem; color: #a78bfa;">EPA Integrated Pest Management</h4>
                    <p style="margin: 0 0 1.2rem 0; color: #cbd5e1; font-size: 13px; line-height: 1.5;">
                        A comprehensive approach to pest control that combines biological, physical, and chemical tools to minimize farm risks.
                    </p>
                </div>
                <a href="https://www.epa.gov/safepestcontrol/integrated-pest-management-ipm-principles" target="_blank" style="color: #a78bfa; font-weight: 700; font-size: 13.5px; text-decoration: none; display: inline-flex; align-items: center; gap: 4px; margin-top: auto;">
                    Understand IPM Principles ↗
                </a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================= TAB 2: DATASET PAGE =================
elif st.session_state['active_tab'] == 1:
    st.markdown('<div style="font-size: 2.2rem; margin-top: 1rem; margin-bottom: 1.5rem; font-weight: 800; background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; display: inline-block; letter-spacing: -0.5px; font-family: \'Outfit\', sans-serif;">Dataset Architecture & Performance</div>', unsafe_allow_html=True)
    
    # Dataset specs columns
    ds_col1, ds_col2 = st.columns([1.4, 1])
    with ds_col1:
        st.markdown("""
        <div class="glass-card" style="height: 100%;">
            <h3 style="color: #ffffff; margin-top: 0; margin-bottom: 1rem; font-weight: 700; font-size: 1.3rem;">Augmented Offline Dataset</h3>
            <p style="color: #cbd5e1; line-height: 1.65; font-size: 14.5px; margin-bottom: 1.5rem;">
                This deep learning database utilizes offline augmentation (shearing, flipping, brightness adjustments, and zooming) to train the CNN to remain invariant to lighting and angle variations. It classifies leaves into <b>38 distinct crop categories</b>.
            </p>
            <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 140px; background: rgba(255,255,255,0.01); padding: 14px 20px; border-radius: 10px; border-left: 4px solid #10b981; border-top: 1px solid rgba(255,255,255,0.04); border-right: 1px solid rgba(255,255,255,0.04); border-bottom: 1px solid rgba(255,255,255,0.04);">
                    <div style="color: #94a3b8; font-size: 10px; text-transform: uppercase; letter-spacing: 0.8px;">Training Set</div>
                    <div style="color: #ffffff; font-size: 18px; font-weight: 800; margin-top: 4px;">70,295 Items</div>
                </div>
                <div style="flex: 1; min-width: 140px; background: rgba(255,255,255,0.01); padding: 14px 20px; border-radius: 10px; border-left: 4px solid #60a5fa; border-top: 1px solid rgba(255,255,255,0.04); border-right: 1px solid rgba(255,255,255,0.04); border-bottom: 1px solid rgba(255,255,255,0.04);">
                    <div style="color: #94a3b8; font-size: 10px; text-transform: uppercase; letter-spacing: 0.8px;">Validation Set</div>
                    <div style="color: #ffffff; font-size: 18px; font-weight: 800; margin-top: 4px;">17,572 Items</div>
                </div>
                <div style="flex: 1; min-width: 140px; background: rgba(255,255,255,0.01); padding: 14px 20px; border-radius: 10px; border-left: 4px solid #f59e0b; border-top: 1px solid rgba(255,255,255,0.04); border-right: 1px solid rgba(255,255,255,0.04); border-bottom: 1px solid rgba(255,255,255,0.04);">
                    <div style="color: #94a3b8; font-size: 10px; text-transform: uppercase; letter-spacing: 0.8px;">Test Set</div>
                    <div style="color: #ffffff; font-size: 18px; font-weight: 800; margin-top: 4px;">33 Items</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with ds_col2:
        st.markdown("""
        <div class="glass-card" style="height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 1.5rem !important;">
            <img src="https://images.unsplash.com/photo-1533038590840-1cde6e668a91?auto=format&fit=crop&w=600&q=80" style="width: 100%; height: 180px; object-fit: cover; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 0.8rem;" alt="Texture Map">
            <span style="color: #94a3b8; font-size: 12.5px; font-weight: 600;">🔬 Micro-texture Pattern Extraction</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Interactive Performance Charts
    try:
        with open('training_hist.json', 'r') as f:
            hist = json.load(f)
            
        st.markdown('<h3 style="color: #ffffff; font-size: 1.5rem; margin-top: 2.5rem; margin-bottom: 1.2rem; font-weight: 700;">Active Model Learning Curves</h3>', unsafe_allow_html=True)
        
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.markdown('<h4 style="color: #34d399; font-size: 1.1rem; margin-top: 1rem; margin-bottom: 1rem; font-weight: 600;">Training & Validation Accuracy</h4>', unsafe_allow_html=True)
            acc_df = pd.DataFrame({
                'Training': hist['accuracy'],
                'Validation': hist['val_accuracy']
            })
            st.line_chart(acc_df)
            
        with chart_col2:
            st.markdown('<h4 style="color: #60a5fa; font-size: 1.1rem; margin-top: 1rem; margin-bottom: 1rem; font-weight: 600;">Cross-Entropy Loss Curve</h4>', unsafe_allow_html=True)
            loss_df = pd.DataFrame({
                'Training': hist['loss'],
                'Validation': hist['val_loss']
            })
            st.line_chart(loss_df)
    except:
        pass

    # Grid of supported crops and diseases
    st.markdown('<h3 style="color: #ffffff; font-size: 1.5rem; margin-top: 2.5rem; margin-bottom: 1.2rem; font-weight: 700;">Supported Plants & Disease Dictionary</h3>', unsafe_allow_html=True)
    
    # Group by crop type
    crops = {}
    for key, value in REMEDIES_DB.items():
        crop_name = value['crop']
        disease_name = value['display_name'].split(' - ')[-1] if ' - ' in value['display_name'] else value['display_name']
        if crop_name not in crops:
            crops[crop_name] = []
        crops[crop_name].append(disease_name)
        
    crop_cols = st.columns(3)
    for idx, (crop_name, diseases) in enumerate(crops.items()):
        col_idx = idx % 3
        with crop_cols[col_idx]:
            disease_badges = "".join(f'<span class="disease-badge" style="margin-right: 4px; margin-bottom: 4px;">{d}</span>' for d in diseases)
            style_class = get_crop_style(crop_name)
            emoji = get_crop_emoji(crop_name)
            st.markdown(f"""
            <div class="glass-card {style_class}" style="height: 100%; min-height: 160px; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <h4 style="font-weight: 700; font-size: 1.15rem; margin-top:0; margin-bottom: 0.8rem; display: flex; align-items: center; gap: 8px;">
                        {emoji} {crop_name}
                    </h4>
                    <div style="display: flex; flex-wrap: wrap; margin-top: 0.5rem;">
                        {disease_badges}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ================= TAB 3: DIAGNOSTIC CENTER =================
elif st.session_state['active_tab'] == 2:
    st.markdown('<div style="font-size: 2.2rem; margin-top: 1rem; margin-bottom: 0.5rem; font-weight: 800; background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; display: inline-block; letter-spacing: -0.5px; font-family: \'Outfit\', sans-serif;">Agro-Diagnostic Center</div>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94a3b8; margin-bottom: 2rem;">Upload leaf images to verify pathogen status.</p>', unsafe_allow_html=True)
    
    # Check if model is fully trained
    model_exists = os.path.exists("trained_plant_disease_model.keras")
    
    if not model_exists:
        progress_data = get_training_progress()
        if progress_data:
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #f59e0b; background: rgba(245, 158, 11, 0.04); margin-bottom: 2rem;">
                <h3 style="color: #f59e0b; margin-top: 0; margin-bottom: 0.5rem; font-weight: 700; font-size: 1.25rem; display: flex; align-items: center; gap: 8px;">
                    ⚡ AI Model Training in Progress (Live Feed)
                </h3>
                <p style="color: #cbd5e1; font-size: 14px; margin-bottom: 1.2rem; line-height: 1.5;">
                    The 10-layer CNN model is actively learning crop features. Real-time diagnostic prediction will become active automatically as soon as the final training pass is complete.
                </p>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 1rem; margin-bottom: 1.2rem;">
                    <div style="background: rgba(255,255,255,0.01); padding: 12px 16px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.04);">
                        <div style="color: #94a3b8; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px;">Current Cycle</div>
                        <div style="color: #ffffff; font-size: 15px; font-weight: 700; margin-top: 4px;">{progress_data['epoch']}</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.01); padding: 12px 16px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.04);">
                        <div style="color: #94a3b8; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px;">Batch Progress</div>
                        <div style="color: #ffffff; font-size: 15px; font-weight: 700; margin-top: 4px;">{progress_data['progress']}</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.01); padding: 12px 16px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.04);">
                        <div style="color: #94a3b8; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px;">Active Accuracy</div>
                        <div style="color: #34d399; font-size: 15px; font-weight: 700; margin-top: 4px;">{progress_data['accuracy']}</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.01); padding: 12px 16px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.04);">
                        <div style="color: #94a3b8; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px;">Loss Error</div>
                        <div style="color: #f87171; font-size: 15px; font-weight: 700; margin-top: 4px;">{progress_data['loss']}</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.01); padding: 12px 16px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.04);">
                        <div style="color: #94a3b8; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px;">ETA Time</div>
                        <div style="color: #60a5fa; font-size: 15px; font-weight: 700; margin-top: 4px;">{progress_data['eta']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Epoch progress bar
            try:
                curr, total = map(int, progress_data['progress'].split('/'))
                pct = curr / total
                st.progress(pct, text=f"Active Epoch Progress: {pct*100:.1f}%")
            except:
                pass
        else:
            st.warning("⚠️ **Model Training in Progress:** The deep learning model (`trained_plant_disease_model.keras`) is currently being trained in the background. The leaf diagnosis feature will become active automatically as soon as training is complete.")
    
    # File Uploader Slot instructions
    st.markdown("""
    <div style="background: rgba(16, 185, 129, 0.04); border-left: 4px solid #10b981; padding: 14px 20px; border-radius: 12px; margin-top: 1rem; margin-bottom: 1.5rem; box-shadow: 0 5px 15px rgba(0,0,0,0.15);">
        <h4 style="margin: 0; color: #ffffff; font-size: 15px; font-weight: 700; display: flex; align-items: center; gap: 8px;">
            📸 Step 1: Upload the plant photo here
        </h4>
        <p style="margin: 4px 0 0 0; color: #cbd5e1; font-size: 13.5px; line-height: 1.5;">
            Select or drag the leaf image of the plant you want to diagnose into the upload zone below. Supported formats: <b>JPG, JPEG, PNG</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    test_image = st.file_uploader("Upload the plant photo here:", type=["jpg", "jpeg", "png"])
    
    if test_image is not None:
        col_img, col_act = st.columns([1, 1.5])
        
        with col_img:
            st.markdown('<div class="image-container" style="text-align: center;">', unsafe_allow_html=True)
            st.image(test_image, use_column_width=True, caption="Uploaded Crop Image")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_act:
            st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
            predict_button = st.button("Diagnose Crop Leaf")
            
            if predict_button:
                if not model_exists:
                    st.error("Cannot run diagnosis. The model file 'trained_plant_disease_model.keras' has not been saved yet because training is still in progress. Please check back shortly.")
                else:
                    st.snow()
                    
                    with st.spinner("AI is analyzing leaf patterns..."):
                        try:
                            result_index = model_prediction(test_image)
                            
                            # Resolve class names
                            class_keys = list(REMEDIES_DB.keys())
                            predicted_raw = class_keys[result_index]
                            remedy_data = REMEDIES_DB[predicted_raw]
                            
                            status_color = "#10b981" if remedy_data['status'] == 'Healthy' else "#f87171"
                            status_bg = "rgba(16, 185, 129, 0.08)" if remedy_data['status'] == 'Healthy' else "rgba(248, 113, 113, 0.08)"
                            status_icon = "✅" if remedy_data['status'] == 'Healthy' else "⚠️"
                            
                            # Render Premium Diagnosis Card
                            remedies_list_html = "".join(f"<li style='margin-bottom: 8px;'>{r}</li>" for r in remedy_data['remedies'])
                            
                            diagnosis_html = f"""
                            <div class="glass-card" style="border-left: 5px solid {status_color}; margin-top: 1rem; background: rgba(255, 255, 255, 0.035); box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 16px; flex-wrap: wrap; gap: 10px;">
                                    <h3 style="margin: 0; color: #ffffff; font-weight: 700; font-size: 22px;">{remedy_data['display_name']}</h3>
                                    <span style="background-color: {status_bg}; color: {status_color}; padding: 6px 18px; border-radius: 30px; font-weight: 800; font-size: 12px; letter-spacing: 0.5px; border: 1px solid {status_color}30; display: inline-flex; align-items: center; gap: 6px;">
                                        {status_icon} {remedy_data['status'].upper()}
                                    </span>
                                </div>
                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 20px;">
                                    <div>
                                        <div style="color: #34d399; font-size: 11px; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 4px; font-weight: 700;">Crop Category</div>
                                        <div style="color: #ffffff; font-size: 15px; font-weight: 500;">🌿 {remedy_data['crop']}</div>
                                    </div>
                                    <div>
                                        <div style="color: #34d399; font-size: 11px; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 4px; font-weight: 700;">Scientific Cause</div>
                                        <div style="color: #ffffff; font-size: 15px; font-weight: 500;">🔬 {remedy_data['cause']}</div>
                                    </div>
                                </div>
                                <div style="margin-bottom: 24px;">
                                    <div style="color: #34d399; font-size: 11px; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; font-weight: 700;">Pathology & Symptoms</div>
                                    <div style="color: #cbd5e1; font-size: 14.5px; line-height: 1.65; background: rgba(255,255,255,0.01); padding: 12px 16px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.03);">{remedy_data['description']}</div>
                                </div>
                                <div style="background: rgba(16, 185, 129, 0.02); border: 1px solid rgba(16, 185, 129, 0.15); padding: 20px; border-radius: 12px;">
                                    <div style="color: #34d399; font-size: 12px; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 12px; font-weight: 800; display: flex; align-items: center; gap: 6px;">
                                        🛡️ Treatment & Prevention Protocol
                                    </div>
                                    <ul style="margin: 0; padding-left: 20px; color: #e2e8f0; font-size: 14px; line-height: 1.7;">
                                        {remedies_list_html}
                                    </ul>
                                </div>
                            </div>
                            """
                            st.markdown(diagnosis_html, unsafe_allow_html=True)
                            
                        except Exception as e:
                            st.error("Error running prediction. Ensure the model has been trained successfully and is saved as 'trained_plant_disease_model.keras'.")
                            st.exception(e)
