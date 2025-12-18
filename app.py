import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="CineMetrics • Movie Analytics",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# MODERN STYLING
# ============================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    /* Live Animated Background */
    .stApp {
        background: linear-gradient(180deg, #09090b 0%, #0c0c0e 50%, #09090b 100%);
        position: relative;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(ellipse at 0% 100%, rgba(34, 211, 238, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse at 100% 0%, rgba(245, 158, 11, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 50%, rgba(6, 182, 212, 0.05) 0%, transparent 70%);
        background-size: 200% 200%, 200% 200%, 100% 100%;
        animation: gradientShift 20s ease-in-out infinite;
        z-index: 0;
        pointer-events: none;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 100%, 100% 0%, 50% 50%; }
        50% { background-position: 100% 0%, 0% 100%, 50% 50%; }
    }
    
    /* Animated Particles */
    .stApp::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20% 30%, rgba(34, 211, 238, 0.3), transparent),
            radial-gradient(2px 2px at 60% 70%, rgba(245, 158, 11, 0.3), transparent),
            radial-gradient(1px 1px at 50% 50%, rgba(34, 211, 238, 0.4), transparent),
            radial-gradient(1px 1px at 80% 10%, rgba(245, 158, 11, 0.3), transparent),
            radial-gradient(2px 2px at 90% 50%, rgba(34, 211, 238, 0.2), transparent),
            radial-gradient(1px 1px at 33% 60%, rgba(245, 158, 11, 0.3), transparent),
            radial-gradient(1px 1px at 70% 80%, rgba(34, 211, 238, 0.2), transparent),
            radial-gradient(2px 2px at 40% 90%, rgba(245, 158, 11, 0.3), transparent);
        background-size: 200% 200%;
        animation: particleMove 25s linear infinite;
        z-index: 0;
        pointer-events: none;
    }
    
    @keyframes particleMove {
        0% { background-position: 0% 0%, 100% 100%, 50% 50%, 80% 20%, 20% 80%, 60% 40%, 40% 60%, 90% 10%; }
        100% { background-position: 100% 100%, 0% 0%, 50% 50%, 20% 80%, 80% 20%, 40% 60%, 60% 40%, 10% 90%; }
    }
    
    /* Floating Shapes */
    .floating-shapes {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100vh;
        overflow: visible;
        z-index: 0;
        pointer-events: none;
    }
    
    .shape {
        position: absolute;
        border-radius: 50%;
        opacity: 0.1;
        animation: float 20s infinite ease-in-out;
    }
    
    .shape:nth-child(1) {
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(34, 211, 238, 0.3), transparent);
        top: 10%;
        left: 10%;
        animation-delay: 0s;
    }
    
    .shape:nth-child(2) {
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, rgba(245, 158, 11, 0.3), transparent);
        top: 60%;
        right: 10%;
        animation-delay: 5s;
    }
    
    .shape:nth-child(3) {
        width: 250px;
        height: 250px;
        background: radial-gradient(circle, rgba(34, 211, 238, 0.2), transparent);
        bottom: 20%;
        left: 50%;
        animation-delay: 10s;
    }
    
    .shape:nth-child(4) {
        width: 180px;
        height: 180px;
        background: radial-gradient(circle, rgba(245, 158, 11, 0.2), transparent);
        top: 30%;
        right: 30%;
        animation-delay: 15s;
    }
    
    @keyframes float {
        0%, 100% { transform: translate(0, 0) scale(1); }
        25% { transform: translate(50px, -50px) scale(1.1); }
        50% { transform: translate(-30px, 30px) scale(0.9); }
        75% { transform: translate(30px, 50px) scale(1.05); }
    }
    
    /* Ensure content is above background and scrollable */
    .main .block-container,
    section[data-testid="stSidebar"],
    header[data-testid="stHeader"] {
        position: relative;
        z-index: 1;
    }
    
    /* Ensure scrolling works properly */
    html, body {
        overflow-x: hidden !important;
        overflow-y: auto !important;
    }
    
    /* Streamlit app container */
    .stApp {
        overflow-x: hidden !important;
        overflow-y: visible !important;
    }
    
    /* Main content area */
    .main {
        overflow: visible !important;
    }
    
    /* Streamlit view container */
    [data-testid="stAppViewContainer"] {
        overflow: visible !important;
    }
    
    /* Ensure fixed elements don't block */
    .title-bar,
    div[data-testid="stTabs"] > div:first-child {
        pointer-events: auto;
    }
    
    section[data-testid="stSidebar"] {
        position: relative !important;
        z-index: 1;
    }
    
    /* Header */
    .header {
        text-align: center;
        padding: 30px 0 20px 0;
    }
    
    .logo {
        font-size: 3rem;
        font-weight: 700;
        color: #fafafa;
        letter-spacing: -1px;
    }
    
    .logo span { color: #22d3ee; }
    
    .tagline {
        color: #71717a;
        font-size: 0.9rem;
        margin-top: 5px;
    }
    
    /* Stat Cards - Enhanced */
    .stat-card {
        background: linear-gradient(145deg, #27272a 0%, #1f1f23 100%);
        border: 1px solid #3f3f46;
        border-radius: 20px;
        padding: 28px 24px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1), 0 1px 3px rgba(0,0,0,0.08);
        position: relative;
        overflow: hidden;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(34, 211, 238, 0.1), transparent);
        transition: left 0.5s ease;
    }
    
    .stat-card:hover::before {
        left: 100%;
    }
    
    .stat-card:hover {
        border-color: #22d3ee;
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0 20px 40px rgba(34, 211, 238, 0.15), 0 8px 16px rgba(0,0,0,0.2);
    }
    
    .stat-icon { 
        font-size: 2.5rem; 
        margin-bottom: 12px; 
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
        transition: transform 0.3s ease;
    }
    
    .stat-card:hover .stat-icon {
        transform: scale(1.1) rotate(5deg);
    }
    
    .stat-value { 
        font-size: 2.2rem; 
        font-weight: 700; 
        color: #fafafa; 
        margin: 8px 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .stat-label { 
        font-size: 0.8rem; 
        color: #a1a1aa; 
        text-transform: uppercase; 
        letter-spacing: 1.5px; 
        margin-top: 6px;
        font-weight: 500;
    }
    
    /* Section Title - Enhanced */
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #fafafa;
        margin: 40px 0 24px 0;
        padding-bottom: 16px;
        border-bottom: 3px solid transparent;
        border-image: linear-gradient(90deg, #22d3ee, #f59e0b) 1;
        display: inline-block;
        position: relative;
        letter-spacing: -0.5px;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -3px;
        left: 0;
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, #22d3ee, transparent);
    }
    
    /* Info Card - Enhanced */
    .info-card {
        background: linear-gradient(145deg, #27272a 0%, #1f1f23 100%);
        border: 1px solid #3f3f46;
        border-radius: 16px;
        padding: 24px;
        margin: 12px 0;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .info-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #22d3ee, #f59e0b);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .info-card:hover {
        border-color: #22d3ee;
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(34, 211, 238, 0.15), 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .info-card:hover::before {
        opacity: 1;
    }
    
    .info-label { 
        font-size: 0.75rem; 
        color: #f59e0b; 
        text-transform: uppercase; 
        letter-spacing: 1.5px; 
        margin-bottom: 10px;
        font-weight: 600;
    }
    
    .info-value { 
        font-size: 1.4rem; 
        font-weight: 700; 
        color: #fafafa; 
        margin-bottom: 6px;
        line-height: 1.3;
    }
    
    .info-desc { 
        font-size: 0.9rem; 
        color: #a1a1aa;
        line-height: 1.5;
    }
    
    /* Concept Box - Enhanced */
    .concept-box {
        background: linear-gradient(135deg, #042f2e 0%, #134e4a 100%);
        border: 1px solid #0d9488;
        border-radius: 16px;
        padding: 24px;
        margin: 18px 0;
        box-shadow: 0 4px 12px rgba(13, 148, 136, 0.15);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .concept-box::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(34, 211, 238, 0.1), transparent);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .concept-box:hover {
        border-color: #22d3ee;
        box-shadow: 0 8px 24px rgba(34, 211, 238, 0.2);
        transform: translateY(-2px);
    }
    
    .concept-title {
        font-weight: 700;
        color: #22d3ee;
        font-size: 1rem;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 10px;
        position: relative;
        z-index: 1;
    }
    
    .concept-text { 
        color: #99f6e4; 
        font-size: 0.95rem; 
        line-height: 1.8;
        position: relative;
        z-index: 1;
    }
    
    /* Movie Item - Enhanced */
    .movie-item {
        background: linear-gradient(145deg, #27272a 0%, #1f1f23 100%);
        border: 1px solid #3f3f46;
        border-radius: 14px;
        padding: 18px 24px;
        margin: 10px 0;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        cursor: pointer;
        position: relative;
    }
    
    .movie-item::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 0;
        background: linear-gradient(90deg, rgba(34, 211, 238, 0.1), transparent);
        transition: width 0.3s ease;
    }
    
    .movie-item:hover {
        border-color: #22d3ee;
        transform: translateX(6px);
        box-shadow: 0 4px 12px rgba(34, 211, 238, 0.15), 0 2px 6px rgba(0,0,0,0.1);
    }
    
    .movie-item:hover::before {
        width: 4px;
    }
    
    /* Streamlit header styling */
    header[data-testid="stHeader"] {
        background: #09090b !important;
        border-bottom: 1px solid #27272a;
    }
    
    /* Loading Screen */
    .loading-screen {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(180deg, #09090b 0%, #0c0c0e 50%, #09090b 100%);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        animation: fadeOut 0.5s ease-out 1.5s forwards;
    }
    
    @keyframes fadeOut {
        to { opacity: 0; visibility: hidden; }
    }
    
    .loading-logo {
        font-size: 4rem;
        font-weight: 700;
        color: #fafafa;
        letter-spacing: -2px;
        margin-bottom: 20px;
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    .loading-logo span { color: #22d3ee; }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(1.05); }
    }
    
    .loading-spinner {
        width: 50px;
        height: 50px;
        border: 4px solid #27272a;
        border-top: 4px solid #22d3ee;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Title bar - sticky at top */
    .title-bar {
        position: sticky;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        background: linear-gradient(180deg, #09090b 0%, #0d0d0f 100%);
        padding: 20px 0;
        border-bottom: 1px solid #27272a;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        margin-bottom: 0;
    }
    
    .title-content {
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        max-width: 100%;
    }
    
    .title-logo {
        font-size: 2.5rem;
        font-weight: 700;
        color: #fafafa;
        letter-spacing: -1px;
        text-align: center;
    }
    
    .title-logo span { color: #22d3ee; }
    
    /* Tabs container - sticky below title */
    div[data-testid="stTabs"] > div:first-child {
        position: sticky !important;
        top: 80px !important;
        z-index: 999 !important;
        background: #09090b;
        padding: 12px 0;
        margin-bottom: 20px;
        border-bottom: 1px solid #27272a;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    
    /* Center tabs */
    .stTabs [data-baseweb="tab-list"] {
        margin: 0 auto;
        display: flex;
        justify-content: center;
    }
    
    /* Remove extra padding from main content */
    .main .block-container {
        padding-top: 20px !important;
    }
    
    /* Tabs styling - Enhanced */
    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(180deg, #1a1a1d 0%, #141416 100%);
        border-radius: 12px;
        padding: 10px 14px;
        gap: 10px;
        border: 1px solid #2a2a2e;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.05);
        margin: 0 auto;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #27272a;
        border-radius: 8px;
        color: #a1a1aa;
        font-weight: 600;
        font-size: 0.85rem;
        padding: 10px 18px;
        border: 1px solid transparent;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .stTabs [data-baseweb="tab"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.5s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #3f3f46;
        color: #fafafa;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    .stTabs [data-baseweb="tab"]:hover::before {
        left: 100%;
    }
    
    /* Tab 1: Dashboard - Cyan */
    .stTabs [data-baseweb="tab-list"] button:nth-child(1)[aria-selected="true"] {
        background: linear-gradient(135deg, #22d3ee, #0891b2) !important;
        color: #000 !important;
        border-color: #22d3ee !important;
    }
    
    /* Tab 2: Explorer - Blue */
    .stTabs [data-baseweb="tab-list"] button:nth-child(2)[aria-selected="true"] {
        background: linear-gradient(135deg, #60a5fa, #3b82f6) !important;
        color: #000 !important;
        border-color: #60a5fa !important;
    }
    
    /* Tab 3: Financial - Orange/Amber */
    .stTabs [data-baseweb="tab-list"] button:nth-child(3)[aria-selected="true"] {
        background: linear-gradient(135deg, #fbbf24, #f59e0b) !important;
        color: #000 !important;
        border-color: #fbbf24 !important;
    }
    
    /* Tab 4: Interactive - Green/Teal */
    .stTabs [data-baseweb="tab-list"] button:nth-child(4)[aria-selected="true"] {
        background: linear-gradient(135deg, #34d399, #10b981) !important;
        color: #000 !important;
        border-color: #34d399 !important;
    }
    
    /* Tab 5: Genres - Pink/Rose */
    .stTabs [data-baseweb="tab-list"] button:nth-child(5)[aria-selected="true"] {
        background: linear-gradient(135deg, #f472b6, #ec4899) !important;
        color: #000 !important;
        border-color: #f472b6 !important;
    }
    
    /* Tab 6: Concepts - Purple/Violet */
    .stTabs [data-baseweb="tab-list"] button:nth-child(6)[aria-selected="true"] {
        background: linear-gradient(135deg, #a855f7, #7c3aed) !important;
        color: #fff !important;
        border-color: #a855f7 !important;
    }
    
    /* Sidebar - Enhanced */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #18181b 0%, #09090b 100%);
        border-right: 1px solid #27272a;
        box-shadow: 2px 0 8px rgba(0,0,0,0.1);
    }
    
    /* Streamlit Widget Styling - Enhanced */
    /* Input fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        background: #27272a !important;
        border: 1px solid #3f3f46 !important;
        border-radius: 10px !important;
        color: #fafafa !important;
        padding: 10px 14px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #22d3ee !important;
        box-shadow: 0 0 0 3px rgba(34, 211, 238, 0.1) !important;
        outline: none !important;
    }
    
    /* Sliders */
    .stSlider > div > div {
        background: #27272a !important;
    }
    
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #22d3ee, #f59e0b) !important;
    }
    
    .stSlider > div > div > div > div {
        background: #22d3ee !important;
        box-shadow: 0 2px 8px rgba(34, 211, 238, 0.4) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #22d3ee, #0891b2) !important;
        color: #000 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px rgba(34, 211, 238, 0.2) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(34, 211, 238, 0.3) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Checkboxes */
    .stCheckbox > label {
        color: #a1a1aa !important;
        font-weight: 500 !important;
    }
    
    .stCheckbox > label > div {
        background: #27272a !important;
        border: 1px solid #3f3f46 !important;
    }
    
    /* Selectbox dropdown */
    [data-baseweb="select"] {
        background: #27272a !important;
        border: 1px solid #3f3f46 !important;
        border-radius: 10px !important;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] { 
        font-weight: 700 !important; 
        color: #22d3ee !important;
        font-size: 1.5rem !important;
    }
    
    [data-testid="stMetricLabel"] { 
        color: #a1a1aa !important;
        font-weight: 500 !important;
    }
    
    /* Divider enhancement */
    .divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #22d3ee, #f59e0b, transparent);
        margin: 40px 0;
        border-radius: 2px;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Better spacing for main content */
    .main .block-container {
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }
    
    /* Ensure proper alignment */
    .main {
        width: 100%;
        max-width: 100%;
    }
    
    /* Fix column alignment */
    [data-testid="column"] {
        width: 100% !important;
    }
    
    /* Improved scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #18181b;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #22d3ee, #0891b2);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #06b6d4, #0e7490);
    }
    
    /* Smooth transitions for all interactive elements */
    * {
        transition-property: background-color, border-color, color, fill, stroke, opacity, box-shadow, transform;
        transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
        transition-duration: 150ms;
    }
    
    /* Focus states for accessibility */
    button:focus-visible,
    input:focus-visible,
    select:focus-visible {
        outline: 2px solid #22d3ee;
        outline-offset: 2px;
    }
    
    /* Divider */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #f59e0b, transparent);
        margin: 30px 0;
    }
    
    /* Metric */
    [data-testid="stMetricValue"] { font-weight: 700 !important; color: #22d3ee !important; }
    [data-testid="stMetricLabel"] { color: #a1a1aa !important; }
    
    /* Cinema Spotlight Cards */
    .spotlight-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        padding: 20px 0;
        overflow-x: auto;
    }
    
    .cinema-card {
        position: relative;
        width: 280px;
        height: 200px;
        border-radius: 16px;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;
        flex-shrink: 0;
    }
    
    .cinema-card:hover {
        transform: scale(1.05) translateY(-8px);
        box-shadow: 0 25px 50px rgba(0,0,0,0.4);
    }
    
    .cinema-card.action { background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%); }
    .cinema-card.comedy { background: linear-gradient(135deg, #f59e0b 0%, #b45309 100%); }
    .cinema-card.drama { background: linear-gradient(135deg, #7c3aed 0%, #5b21b6 100%); }
    .cinema-card.scifi { background: linear-gradient(135deg, #0891b2 0%, #155e75 100%); }
    .cinema-card.horror { background: linear-gradient(135deg, #1f2937 0%, #111827 100%); }
    
    .cinema-screen {
        position: absolute;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: 200px;
        height: 100px;
        background: linear-gradient(180deg, #18181b 0%, #27272a 100%);
        border-radius: 8px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border: 2px solid rgba(255,255,255,0.1);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .cinema-logo {
        font-size: 0.65rem;
        color: #22d3ee;
        font-weight: 600;
        letter-spacing: 2px;
        margin-bottom: 5px;
    }
    
    .cinema-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #fafafa;
        text-align: center;
    }
    
    .cinema-badge {
        background: rgba(255,255,255,0.9);
        color: #18181b;
        font-size: 0.65rem;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 4px;
        margin-top: 8px;
        letter-spacing: 0.5px;
    }
    
    .cinema-seats {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 60px;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 3px;
        padding: 10px;
        background: linear-gradient(180deg, transparent, rgba(0,0,0,0.3));
    }
    
    .seat {
        width: 12px;
        height: 10px;
        background: rgba(34, 211, 238, 0.4);
        border-radius: 3px 3px 0 0;
    }
    
    .spotlight-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 30px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid #f59e0b;
    }
    
    .spotlight-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #fafafa;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .spotlight-more {
        font-size: 0.85rem;
        color: #f59e0b;
        font-weight: 500;
    }
    
    #MainMenu, footer, .stDeployButton { display: none; }
    </style>
""", unsafe_allow_html=True)

# ============================================
# LOAD DATA
# ============================================
@st.cache_data
def load_data():
    df = pd.read_csv("tmdb_movies_data.csv")
    df['profit'] = df['revenue'] - df['budget']
    df['roi'] = np.where(df['budget'] > 0, (df['profit'] / df['budget']) * 100, 0)
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df['year'] = df['release_date'].dt.year
    df['month'] = df['release_date'].dt.month
    df['decade'] = (df['year'] // 10 * 10).astype('Int64')
    df['is_profitable'] = df['profit'] > 0
    df['primary_genre'] = df['genres'].apply(lambda x: x.split('|')[0] if pd.notna(x) else 'Unknown')
    return df

df = load_data()

# Chart styling
def style_chart(fig, height=400):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(39,39,42,0.5)',
        font=dict(family='Plus Jakarta Sans', color='#a1a1aa', size=11),
        title_font=dict(family='Plus Jakarta Sans', color='#fafafa', size=14, weight=600),
        xaxis=dict(gridcolor='rgba(63,63,70,0.5)', linecolor='#3f3f46'),
        yaxis=dict(gridcolor='rgba(63,63,70,0.5)', linecolor='#3f3f46'),
        height=height,
        margin=dict(l=20, r=20, t=50, b=40),
        hoverlabel=dict(bgcolor='#27272a', font_size=12),
        legend=dict(bgcolor='rgba(0,0,0,0)')
    )
    return fig

# Color Blind Friendly Palette (Blue/Orange instead of Red/Green)
COLORS = ['#22d3ee', '#06b6d4', '#0891b2', '#f59e0b', '#d97706']
DIVERGING = [[0, '#7c3aed'], [0.5, '#52525b'], [1, '#f59e0b']]  # Purple to Orange

# ============================================
# SIDEBAR FILTERS
# ============================================
with st.sidebar:
    st.markdown("## 🎛️ Filters")
    st.markdown("---")
    
    # Year Range
    years = sorted(df['year'].dropna().unique())
    if len(years) == 0:
        # Fallback if no valid years found
        years = [2000, 2015]
        st.warning("⚠️ No valid years found in dataset. Using default range.")
    
    min_year = int(min(years))
    max_year = int(max(years))
    # Ensure default range is within valid years
    default_min = max(min_year, 2000) if min_year < 2000 else min_year
    default_max = max_year
    
    year_range = st.slider("📅 Year Range", min_year, max_year, (default_min, default_max))
    
    st.markdown("---")
    
    # Genre Multi-select
    all_genres = sorted(df['primary_genre'].unique())
    selected_genres = st.multiselect("🎭 Genres", all_genres)
    
    st.markdown("---")
    
    # Budget
    budget_range = st.slider("💰 Budget ($M)", 0, 300, (0, 300))
    
    st.markdown("---")
    
    # Rating
    min_rating = st.slider("⭐ Min Rating", 0.0, 10.0, 0.0, 0.5)
    
    st.markdown("---")
    
    # Quick Filters
    st.markdown("### ⚡ Quick Filters")
    only_profitable = st.checkbox("✅ Profitable Only")
    only_blockbusters = st.checkbox("🎬 Blockbusters (>$500M)")
    hidden_gems = st.checkbox("💎 Hidden Gems (Low budget, High rating)")

# Apply Filters
mask = (
    (df['year'] >= year_range[0]) & (df['year'] <= year_range[1]) &
    (df['budget'] >= budget_range[0] * 1e6) & (df['budget'] <= budget_range[1] * 1e6) &
    (df['vote_average'] >= min_rating)
)

if selected_genres:
    mask &= df['primary_genre'].isin(selected_genres)
if only_profitable:
    mask &= df['profit'] > 0
if only_blockbusters:
    mask &= df['revenue'] > 500_000_000
if hidden_gems:
    mask &= (df['budget'] < 20_000_000) & (df['vote_average'] >= 7.0)

filtered_df = df[mask]

# Sidebar Stats
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📊 Selection")
    st.metric("Movies", f"{len(filtered_df):,}")
    if len(filtered_df) > 0:
        st.metric("Total Revenue", f"${filtered_df['revenue'].sum()/1e9:.1f}B")
        st.metric("Success Rate", f"{filtered_df['is_profitable'].mean()*100:.0f}%")

# ============================================
# LOADING SCREEN
# ============================================
st.markdown("""
<div class="loading-screen" id="loadingScreen">
    <div class="loading-logo">🎬 Cine<span>Metrics</span></div>
    <div class="loading-spinner"></div>
</div>
<script>
    setTimeout(function() {
        var loader = document.getElementById('loadingScreen');
        if (loader) loader.style.display = 'none';
    }, 2000);
</script>
""", unsafe_allow_html=True)

# ============================================
# FLOATING SHAPES (Live Background)
# ============================================
st.markdown("""
<div class="floating-shapes">
    <div class="shape"></div>
    <div class="shape"></div>
    <div class="shape"></div>
    <div class="shape"></div>
</div>
<script>
    // Ensure scrolling is enabled and alignment is correct
    (function() {
        // Enable scrolling
        document.documentElement.style.overflowY = 'auto';
        document.body.style.overflowY = 'auto';
        document.documentElement.style.overflowX = 'hidden';
        document.body.style.overflowX = 'hidden';
        
        // Fix app container
        var appContainer = document.querySelector('[data-testid="stAppViewContainer"]');
        if (appContainer) {
            appContainer.style.overflowY = 'auto';
            appContainer.style.overflowX = 'hidden';
            appContainer.style.height = 'auto';
        }
        
        // Ensure main content is properly aligned
        var mainContainer = document.querySelector('.main .block-container');
        if (mainContainer) {
            mainContainer.style.maxWidth = '100%';
            mainContainer.style.width = '100%';
        }
    })();
</script>
""", unsafe_allow_html=True)

# ============================================
# TITLE BAR (Fixed at top)
# ============================================
st.markdown("""
<div class="title-bar">
    <div class="title-content">
        <div class="title-logo">🎬 Cine<span>Metrics</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# MAIN TABS (Fixed at top, in line with Deploy)
# ============================================
tab1, tab6, tab3, tab2, tab4, tab_concepts = st.tabs([
    "📊 Dashboard", "🔍 Explorer", "💵 Financial", "🎮 Interactive", "🎭 Genres", "🎓 Concepts"
])

# ============================================
# TAB 1: DASHBOARD
# ============================================
with tab1:
    # Stats Row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Handle empty dataframe - use defaults for mean calculations
    avg_rating = filtered_df['vote_average'].mean() if len(filtered_df) > 0 else 0
    success_rate = filtered_df['is_profitable'].mean() * 100 if len(filtered_df) > 0 else 0
    
    stats = [
        ("🎬", f"{len(filtered_df):,}", "Movies"),
        ("💰", f"${filtered_df['revenue'].sum()/1e9:.1f}B", "Revenue"),
        ("📈", f"${filtered_df['profit'].sum()/1e9:.1f}B", "Profit"),
        ("⭐", f"{avg_rating:.1f}", "Avg Rating"),
        ("✅", f"{success_rate:.0f}%", "Success")
    ]

    for col, (icon, val, label) in zip([col1,col2,col3,col4,col5], stats):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">{icon}</div>
                <div class="stat-value">{val}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    # ============================================
    # GENRE PERFORMANCE OVERVIEW
    # ============================================
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: space-between; 
                margin: 25px 0 20px 0; padding-bottom: 12px; border-bottom: 1px solid #3f3f46;">
        <div style="font-size: 0.9rem; font-weight: 600; color: #a1a1aa; 
                    text-transform: uppercase; letter-spacing: 2px;">
            Genre Performance
        </div>
        <div style="font-size: 0.75rem; color: #52525b;">Top 5 by Revenue</div>
    </div>
    """, unsafe_allow_html=True)

    # Get top genres data
    genre_data = filtered_df.groupby('primary_genre').agg({
        'revenue': 'sum', 'original_title': 'count', 'vote_average': 'mean'
    }).reset_index()
    genre_data = genre_data.nlargest(5, 'revenue')

    # Display genre cards using Streamlit columns
    genre_cols = st.columns(5)

    # Calculate max revenue for percentage bar
    max_rev = genre_data['revenue'].max()

    for i, (_, row) in enumerate(genre_data.iterrows()):
        genre = row['primary_genre']
        movie_count = int(row['original_title'])
        revenue = row['revenue'] / 1e9
        rating = row['vote_average']
        rev_percent = (row['revenue'] / max_rev) * 100
        
        with genre_cols[i]:
            st.markdown(f"""
            <div style="background: linear-gradient(180deg, #1c1c1e 0%, #141416 100%); 
                        border: 1px solid #2a2a2e; border-radius: 12px; 
                        padding: 20px 16px; text-align: left; height: 200px;
                        position: relative; overflow: hidden;">
                <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px;
                            background: linear-gradient(90deg, #22d3ee, #f59e0b);"></div>
                <div style="font-size: 0.65rem; color: #52525b; text-transform: uppercase; 
                            letter-spacing: 1px; margin-bottom: 8px;">Genre</div>
                <div style="font-size: 1rem; font-weight: 600; color: #fafafa; 
                            margin-bottom: 16px; line-height: 1.2;">{genre}</div>
                <div style="margin-bottom: 12px;">
                    <div style="font-size: 1.5rem; font-weight: 700; color: #22d3ee;">${revenue:.1f}B</div>
                    <div style="font-size: 0.65rem; color: #52525b; margin-top: 2px;">Total Revenue</div>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <div>
                        <div style="font-size: 0.95rem; font-weight: 600; color: #fafafa;">{rating:.1f}</div>
                        <div style="font-size: 0.6rem; color: #52525b;">Avg Rating</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 0.95rem; font-weight: 600; color: #fafafa;">{movie_count:,}</div>
                        <div style="font-size: 0.6rem; color: #52525b;">Films</div>
                    </div>
                </div>
                <div style="background: #27272a; border-radius: 2px; height: 4px; margin-top: 12px;">
                    <div style="background: linear-gradient(90deg, #22d3ee, #f59e0b); 
                                height: 100%; width: {rev_percent:.0f}%; border-radius: 2px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Overview</div>', unsafe_allow_html=True)
    
    # Top Insights
    col1, col2, col3 = st.columns(3)
    
    if len(filtered_df) > 0:
        with col1:
            top = filtered_df.loc[filtered_df['revenue'].idxmax()]
            st.markdown(f"""
            <div class="info-card">
                <div class="info-label">🏆 Highest Grossing</div>
                <div class="info-value">{top['original_title']}</div>
                <div class="info-desc">${top['revenue']/1e9:.2f}B • {int(top['year']) if pd.notna(top['year']) else 'N/A'}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            rated = filtered_df[filtered_df['vote_count'] >= 500]
            if len(rated) > 0:
                best = rated.loc[rated['vote_average'].idxmax()]
                st.markdown(f"""
                <div class="info-card">
                    <div class="info-label">⭐ Top Rated</div>
                    <div class="info-value">{best['original_title']}</div>
                    <div class="info-desc">{best['vote_average']:.1f}/10 • {int(best['vote_count']):,} votes</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col3:
            profit_df = filtered_df[filtered_df['budget'] >= 1e6]
            if len(profit_df) > 0:
                best_roi = profit_df.loc[profit_df['roi'].idxmax()]
                st.markdown(f"""
                <div class="info-card">
                    <div class="info-label">💎 Best ROI</div>
                    <div class="info-value">{best_roi['original_title']}</div>
                    <div class="info-desc">{best_roi['roi']:.0f}% return • ${best_roi['budget']/1e6:.0f}M budget</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Charts Row 1
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        genre_rev = filtered_df.groupby('primary_genre')['revenue'].sum().nlargest(8).reset_index()
        fig = px.pie(genre_rev, values='revenue', names='primary_genre', hole=0.5,
                    title="Revenue by Genre", color_discrete_sequence=COLORS)
        style_chart(fig, 380)
        st.plotly_chart(fig, use_container_width=True)
    
    with chart_col2:
        yearly = filtered_df.groupby('year').agg({'revenue': 'sum', 'original_title': 'count'}).reset_index()
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=yearly['year'], y=yearly['original_title'], name='Movies', marker_color='#22d3ee'), secondary_y=False)
        fig.add_trace(go.Scatter(x=yearly['year'], y=yearly['revenue'], name='Revenue', line=dict(color='#f59e0b', width=3)), secondary_y=True)
        fig.update_layout(title="Movies & Revenue by Year")
        style_chart(fig, 380)
        st.plotly_chart(fig, use_container_width=True)
    
    # Charts Row 2 - New Visualizations
    st.markdown('<div class="section-title">📈 Advanced Analytics</div>', unsafe_allow_html=True)
    
    chart_col3, chart_col4 = st.columns(2)
    
    with chart_col3:
        # Correlation Heatmap
        numeric_cols = ['budget', 'revenue', 'profit', 'vote_average', 'popularity', 'vote_count', 'runtime']
        corr_data = filtered_df[numeric_cols].corr()
        fig = go.Figure(data=go.Heatmap(
            z=corr_data.values,
            x=corr_data.columns,
            y=corr_data.columns,
            colorscale='Teal',
            text=corr_data.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 10},
            colorbar=dict(title="Correlation")
        ))
        fig.update_layout(title="📊 Correlation Heatmap", height=400)
        style_chart(fig, 400)
        st.plotly_chart(fig, use_container_width=True)
    
    with chart_col4:
        # Box Plot - Revenue Distribution by Genre
        top_genres = filtered_df['primary_genre'].value_counts().head(8).index
        box_data = filtered_df[filtered_df['primary_genre'].isin(top_genres)]
        fig = px.box(box_data, x='primary_genre', y='revenue', 
                    title="Revenue Distribution by Genre",
                    color='primary_genre', color_discrete_sequence=COLORS)
        fig.update_yaxes(type="log")
        style_chart(fig, 400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Charts Row 3
    chart_col5, chart_col6 = st.columns(2)
    
    with chart_col5:
        # Month Release Heatmap
        month_data = filtered_df.groupby(['year', 'month']).agg({
            'revenue': 'sum',
            'original_title': 'count'
        }).reset_index()
        month_pivot = month_data.pivot(index='month', columns='year', values='revenue').fillna(0)
        fig = go.Figure(data=go.Heatmap(
            z=month_pivot.values,
            x=month_pivot.columns,
            y=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            colorscale='Viridis',
            colorbar=dict(title="Revenue ($)")
        ))
        fig.update_layout(title="📅 Release Month Heatmap (Revenue by Month & Year)", height=400)
        style_chart(fig, 400)
        st.plotly_chart(fig, use_container_width=True)
    
    with chart_col6:
        # Bubble Chart - Budget vs Revenue vs Rating
        bubble_data = filtered_df[(filtered_df['budget'] > 1e6) & (filtered_df['revenue'] > 0)].head(200)
        fig = px.scatter(bubble_data, x='budget', y='revenue', size='vote_count',
                        color='vote_average', hover_name='original_title',
                        color_continuous_scale='Teal',
                        title="Budget vs Revenue (Size = Votes, Color = Rating)",
                        labels={'budget': 'Budget ($)', 'revenue': 'Revenue ($)', 'vote_average': 'Rating'})
        style_chart(fig, 400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Charts Row 4
    chart_col7, chart_col8 = st.columns(2)
    
    with chart_col7:
        # Violin Plot - Rating Distribution by Genre
        top_genres_v = filtered_df['primary_genre'].value_counts().head(6).index
        violin_data = filtered_df[filtered_df['primary_genre'].isin(top_genres_v)]
        fig = px.violin(violin_data, x='primary_genre', y='vote_average',
                       color='primary_genre', color_discrete_sequence=COLORS,
                       title="Rating Distribution by Genre (Violin Plot)")
        style_chart(fig, 400)
        st.plotly_chart(fig, use_container_width=True)
    
    with chart_col8:
        # Sunburst Chart - Genre Hierarchy
        genre_decade = filtered_df.groupby(['primary_genre', 'decade']).agg({
            'revenue': 'sum',
            'original_title': 'count'
        }).reset_index()
        top_genres_s = genre_decade.groupby('primary_genre')['revenue'].sum().nlargest(6).index
        sunburst_data = genre_decade[genre_decade['primary_genre'].isin(top_genres_s)]
        fig = px.sunburst(sunburst_data, path=['primary_genre', 'decade'], values='revenue',
                         color='revenue', color_continuous_scale='Teal',
                         title="Genre & Decade Hierarchy (Sunburst)")
        style_chart(fig, 400)
        st.plotly_chart(fig, use_container_width=True)

# ============================================
# TAB 2: INTERACTIVE TOOLS
# ============================================
with tab2:
    st.markdown('<div class="section-title">🎮 Custom Chart Builder</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="concept-box">
        <div class="concept-title">🎯 Build Your Own Visualization</div>
        <div class="concept-text">Choose variables for each axis to explore relationships in the data.</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        x_var = st.selectbox("X-Axis", ['budget', 'popularity', 'vote_count', 'runtime', 'year'])
    with col2:
        y_var = st.selectbox("Y-Axis", ['revenue', 'profit', 'vote_average', 'roi', 'popularity'])
    with col3:
        color_var = st.selectbox("Color By", ['primary_genre', 'is_profitable', 'decade'])
    with col4:
        size_var = st.selectbox("Size By", ['popularity', 'vote_count', 'revenue', 'budget'])
    
    plot_df = filtered_df[(filtered_df[x_var] > 0) & (filtered_df[y_var] != 0)].head(400)
    fig = px.scatter(plot_df, x=x_var, y=y_var, color=color_var, size=size_var,
                    hover_name='original_title', hover_data=['year', 'director'],
                    title=f"{y_var.title()} vs {x_var.title()}", color_discrete_sequence=COLORS)
    style_chart(fig, 500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Movie Comparison Tool
    st.markdown('<div class="section-title">🔄 Movie Comparison</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="concept-box">
        <div class="concept-title">⚖️ Compare Two Movies Side-by-Side</div>
        <div class="concept-text">Select any two movies to see how they stack up against each other.</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    movie_list = filtered_df.nlargest(200, 'revenue')['original_title'].tolist() if len(filtered_df) > 0 else []
    
    if len(movie_list) > 0:
        with col1:
            movie1 = st.selectbox("🎬 First Movie", movie_list, key='m1')
        with col2:
            movie2 = st.selectbox("🎬 Second Movie", movie_list, index=min(1, len(movie_list)-1) if len(movie_list) > 1 else 0, key='m2')
    else:
        st.info("No movies available with current filters. Adjust filters to see movies.")
        movie1, movie2 = None, None
    
    if movie1 and movie2 and len(filtered_df) > 0:
        m1 = filtered_df[filtered_df['original_title'] == movie1].iloc[0]
        m2 = filtered_df[filtered_df['original_title'] == movie2].iloc[0]
        
        metrics = ['budget', 'revenue', 'profit', 'vote_average', 'popularity']
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name=movie1[:20], x=metrics, y=[m1[m] for m in metrics], marker_color='#22d3ee'))
        fig.add_trace(go.Bar(name=movie2[:20], x=metrics, y=[m2[m] for m in metrics], marker_color='#f59e0b'))
        fig.update_layout(barmode='group', title="Side-by-Side Comparison")
        style_chart(fig, 400)
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        for col, name, data in [(col1, movie1, m1), (col2, movie2, m2)]:
            with col:
                st.markdown(f"""
                <div class="info-card">
                    <div class="info-value">{name[:30]}</div>
                    <div class="info-desc">
                        📅 {int(data['year']) if pd.notna(data['year']) else 'N/A'} • 🎬 {data['director'] if pd.notna(data['director']) else 'Unknown'}<br>
                        💰 Budget: ${data['budget']/1e6:.0f}M • 📈 Revenue: ${data['revenue']/1e6:.0f}M<br>
                        ⭐ Rating: {data['vote_average']:.1f} • 🗳️ {int(data['vote_count']):,} votes
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Genre Drill-Down
    st.markdown('<div class="section-title">🔍 Genre Deep Dive</div>', unsafe_allow_html=True)
    
    genre_list = sorted(filtered_df['primary_genre'].unique()) if len(filtered_df) > 0 else []
    
    if len(genre_list) > 0:
        selected_genre = st.selectbox("Select a genre to explore", genre_list)
        
        genre_df = filtered_df[filtered_df['primary_genre'] == selected_genre]
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Movies", len(genre_df))
        col2.metric("Avg Revenue", f"${genre_df['revenue'].mean()/1e6:.0f}M" if len(genre_df) > 0 else "$0M")
        col3.metric("Avg Rating", f"{genre_df['vote_average'].mean():.1f}" if len(genre_df) > 0 else "0.0")
        col4.metric("Success Rate", f"{genre_df['is_profitable'].mean()*100:.0f}%" if len(genre_df) > 0 else "0%")
        
        st.dataframe(genre_df.nlargest(10, 'revenue')[['original_title', 'year', 'revenue', 'profit', 'vote_average']], use_container_width=True)
    else:
        st.info("No genres available with current filters.")
    
    # Additional Interactive Visualizations
    st.markdown('<div class="section-title">📊 Advanced Interactive Charts</div>', unsafe_allow_html=True)
    
    int_row1_col1, int_row1_col2 = st.columns(2)
    
    with int_row1_col1:
        # Density Contour Plot
        density_data = filtered_df[(filtered_df['budget'] > 1e6) & (filtered_df['revenue'] > 0)].head(500)
        fig = px.density_contour(density_data, x='budget', y='revenue',
                                color='vote_average',
                                title="Budget vs Revenue Density (Contour Plot)")
        fig.update_traces(contours_coloring="fill", contours_showlabels=True)
        style_chart(fig, 400)
        st.plotly_chart(fig, use_container_width=True)
    
    with int_row1_col2:
        # 3D Scatter Plot
        scatter_3d_data = filtered_df[(filtered_df['budget'] > 1e6) & (filtered_df['revenue'] > 0)].head(200)
        fig = px.scatter_3d(scatter_3d_data, x='budget', y='revenue', z='vote_average',
                           color='is_profitable',
                           color_discrete_map={True: '#f59e0b', False: '#7c3aed'},
                           hover_name='original_title',
                           title="3D: Budget vs Revenue vs Rating",
                           labels={'budget': 'Budget', 'revenue': 'Revenue', 'vote_average': 'Rating'})
        style_chart(fig, 400)
        st.plotly_chart(fig, use_container_width=True)
    
    int_row2_col1, int_row2_col2 = st.columns(2)
    
    with int_row2_col1:
        # Strip Plot - Rating Distribution
        strip_data = filtered_df[filtered_df['primary_genre'].isin(
            filtered_df['primary_genre'].value_counts().head(6).index
        )]
        fig = px.strip(strip_data, x='primary_genre', y='vote_average',
                      color='is_profitable',
                      color_discrete_map={True: '#f59e0b', False: '#7c3aed'},
                      title="Rating Distribution by Genre (Strip Plot)")
        style_chart(fig, 400)
        st.plotly_chart(fig, use_container_width=True)
    
    with int_row2_col2:
        # Area Chart - Revenue Trends by Genre
        area_data = filtered_df.groupby(['year', 'primary_genre'])['revenue'].sum().reset_index()
        top_genres_area = area_data.groupby('primary_genre')['revenue'].sum().nlargest(5).index
        area_filtered = area_data[area_data['primary_genre'].isin(top_genres_area)]
        fig = px.area(area_filtered, x='year', y='revenue', color='primary_genre',
                     title="Revenue Trends by Genre (Area Chart)",
                     color_discrete_sequence=COLORS)
        style_chart(fig, 400)
        st.plotly_chart(fig, use_container_width=True)

# ============================================
# TAB 3: FINANCIAL
# ============================================
with tab3:
    st.markdown('<div class="section-title">💵 Financial Analysis</div>', unsafe_allow_html=True)
    
    fin_col1, fin_col2 = st.columns(2)
    
    with fin_col1:
        top_profit = filtered_df.nlargest(10, 'profit')
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=top_profit['original_title'], x=top_profit['profit'], orientation='h',
            marker=dict(color=top_profit['profit'], colorscale='Teal'),
            text=[f"${x/1e9:.2f}B" if x >= 1e9 else f"${x/1e6:.0f}M" for x in top_profit['profit']],
            textposition='inside'
        ))
        fig.update_layout(title="🏆 Most Profitable", yaxis={'categoryorder': 'total ascending'})
        style_chart(fig, 450)
        st.plotly_chart(fig, use_container_width=True)
    
    with fin_col2:
        flops = filtered_df[filtered_df['budget'] > 1e7].nsmallest(10, 'profit')
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=flops['original_title'], x=flops['profit'], orientation='h',
            marker_color='#7c3aed',
            text=[f"-${abs(x)/1e6:.0f}M" for x in flops['profit']],
            textposition='inside', textfont=dict(color='white')
        ))
        fig.update_layout(title="📉 Biggest Flops", yaxis={'categoryorder': 'total descending'})
        style_chart(fig, 450)
        st.plotly_chart(fig, use_container_width=True)
    
    # Budget vs Revenue
    st.markdown('<div class="section-title">💰 Budget vs Revenue</div>', unsafe_allow_html=True)
    
    scatter_data = filtered_df[(filtered_df['budget'] > 1e6) & (filtered_df['revenue'] > 0)]
    scatter = scatter_data.sample(min(400, len(scatter_data))) if len(scatter_data) > 0 else scatter_data
    fig = px.scatter(scatter, x='budget', y='revenue', color='is_profitable',
                    color_discrete_map={True: '#f59e0b', False: '#7c3aed'},
                    hover_name='original_title', size='popularity',
                    title="Each dot is a movie • Orange = Profit, Purple = Loss")
    if len(scatter) > 0:
        fig.add_trace(go.Scatter(x=[0, scatter['budget'].max()], y=[0, scatter['budget'].max()],
                                mode='lines', name='Break-even', line=dict(dash='dash', color='#71717a')))
    style_chart(fig, 500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Additional Financial Visualizations
    st.markdown('<div class="section-title">📊 Financial Deep Dive</div>', unsafe_allow_html=True)
    
    fin_row1_col1, fin_row1_col2 = st.columns(2)
    
    with fin_row1_col1:
        # ROI Distribution Histogram
        roi_data = filtered_df[(filtered_df['budget'] > 1e6) & (filtered_df['roi'].notna())]
        fig = px.histogram(roi_data, x='roi', nbins=50, 
                          title="ROI Distribution",
                          labels={'roi': 'ROI (%)', 'count': 'Number of Movies'},
                          color_discrete_sequence=['#22d3ee'])
        fig.add_vline(x=0, line_dash="dash", line_color="#71717a", annotation_text="Break-even")
        style_chart(fig, 400)
        st.plotly_chart(fig, use_container_width=True)
    
    with fin_row1_col2:
        # Profit/Loss by Decade
        decade_profit = filtered_df.groupby('decade').agg({
            'profit': 'sum',
            'original_title': 'count'
        }).reset_index()
        fig = go.Figure()
        colors = ['#f59e0b' if x >= 0 else '#7c3aed' for x in decade_profit['profit']]
        fig.add_trace(go.Bar(
            x=decade_profit['decade'],
            y=decade_profit['profit'],
            marker_color=colors,
            text=[f"${x/1e9:.1f}B" if abs(x) >= 1e9 else f"${x/1e6:.0f}M" for x in decade_profit['profit']],
            textposition='outside'
        ))
        fig.update_layout(title="Total Profit by Decade", yaxis_title="Profit ($)")
        fig.add_hline(y=0, line_dash="dash", line_color="#71717a")
        style_chart(fig, 400)
        st.plotly_chart(fig, use_container_width=True)
    
    fin_row2_col1, fin_row2_col2 = st.columns(2)
    
    with fin_row2_col1:
        # Budget Efficiency (Revenue per Budget Dollar)
        efficiency = filtered_df[(filtered_df['budget'] > 1e6) & (filtered_df['revenue'] > 0)].copy()
        if len(efficiency) > 0:
            efficiency['efficiency'] = efficiency['revenue'] / efficiency['budget']
            top_eff = efficiency.nlargest(15, 'efficiency')
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=top_eff['original_title'],
                x=top_eff['efficiency'],
                orientation='h',
                marker_color='#10b981',
                text=[f"{x:.1f}x" for x in top_eff['efficiency']],
                textposition='inside'
            ))
            fig.update_layout(title="💰 Most Budget-Efficient Movies (Revenue per $)", 
                            yaxis={'categoryorder': 'total ascending'})
            style_chart(fig, 450)
            st.plotly_chart(fig, use_container_width=True)
    
    with fin_row2_col2:
        # Cumulative Revenue Over Time
        yearly_cum = filtered_df.groupby('year').agg({'revenue': 'sum'}).reset_index()
        yearly_cum = yearly_cum.sort_values('year')
        yearly_cum['cumulative'] = yearly_cum['revenue'].cumsum()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=yearly_cum['year'],
            y=yearly_cum['cumulative'],
            mode='lines+markers',
            fill='tozeroy',
            fillcolor='rgba(34, 211, 238, 0.2)',
            line=dict(color='#22d3ee', width=3),
            name='Cumulative Revenue'
        ))
        fig.update_layout(title="📈 Cumulative Revenue Over Time",
                          yaxis_title="Cumulative Revenue ($)")
        style_chart(fig, 400)
        st.plotly_chart(fig, use_container_width=True)

# ============================================
# TAB 4: GENRES
# ============================================
with tab4:
    st.markdown('<div class="section-title">🎭 Genre Analysis</div>', unsafe_allow_html=True)
    
    genre_stats = filtered_df.groupby('primary_genre').agg({
        'revenue': ['sum', 'mean'], 'profit': 'mean', 'vote_average': 'mean',
        'is_profitable': 'mean', 'original_title': 'count'
    }).reset_index()
    genre_stats.columns = ['Genre', 'Total Rev', 'Avg Rev', 'Avg Profit', 'Avg Rating', 'Success', 'Count']

    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.treemap(genre_stats, path=['Genre'], values='Total Rev', color='Avg Rating',
                        color_continuous_scale='Teal', title="Market Share (size = revenue, color = rating)")
        style_chart(fig, 400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        top_g = genre_stats.nlargest(8, 'Count')
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=top_g['Avg Rating'], theta=top_g['Genre'], fill='toself',
            fillcolor='rgba(34, 211, 238, 0.3)', line=dict(color='#22d3ee', width=2)
        ))
        fig.update_layout(title="Genre Quality Radar",
                         polar=dict(radialaxis=dict(range=[5, 8], gridcolor='#3f3f46'), bgcolor='#27272a'))
        style_chart(fig, 400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Additional Genre Visualizations
    st.markdown('<div class="section-title">🎨 Genre Analytics</div>', unsafe_allow_html=True)
    
    genre_row1_col1, genre_row1_col2 = st.columns(2)
    
    with genre_row1_col1:
        # Genre Performance Matrix (Heatmap)
        genre_matrix = filtered_df.groupby(['primary_genre', 'decade']).agg({
            'revenue': 'mean',
            'vote_average': 'mean'
        }).reset_index()
        top_genres_m = genre_matrix.groupby('primary_genre')['revenue'].sum().nlargest(8).index
        matrix_data = genre_matrix[genre_matrix['primary_genre'].isin(top_genres_m)]
        matrix_pivot = matrix_data.pivot(index='primary_genre', columns='decade', values='revenue').fillna(0)
        fig = go.Figure(data=go.Heatmap(
            z=matrix_pivot.values,
            x=matrix_pivot.columns,
            y=matrix_pivot.index,
            colorscale='Teal',
            colorbar=dict(title="Avg Revenue ($)")
        ))
        fig.update_layout(title="Genre Performance by Decade (Heatmap)", height=400)
        style_chart(fig, 400)
        st.plotly_chart(fig, use_container_width=True)
    
    with genre_row1_col2:
        # Stacked Bar - Genre Revenue Over Time
        genre_year = filtered_df.groupby(['year', 'primary_genre'])['revenue'].sum().reset_index()
        top_genres_sb = genre_year.groupby('primary_genre')['revenue'].sum().nlargest(6).index
        stacked_data = genre_year[genre_year['primary_genre'].isin(top_genres_sb)]
        fig = px.bar(stacked_data, x='year', y='revenue', color='primary_genre',
                    title="Genre Revenue Over Time (Stacked)",
                    color_discrete_sequence=COLORS)
        style_chart(fig, 400)
        st.plotly_chart(fig, use_container_width=True)
    
    genre_row2_col1, genre_row2_col2 = st.columns(2)
    
    with genre_row2_col1:
        # Parallel Coordinates - Multi-dimensional Genre Comparison
        top_genres_pc = genre_stats.nlargest(8, 'Total Rev')
        fig = go.Figure(data=go.Parcoords(
            line=dict(color=top_genres_pc['Avg Rating'],
                     colorscale='Teal',
                     showscale=True,
                     colorbar=dict(title="Rating")),
            dimensions=list([
                dict(label='Total Revenue', values=top_genres_pc['Total Rev']),
                dict(label='Avg Revenue', values=top_genres_pc['Avg Rev']),
                dict(label='Avg Profit', values=top_genres_pc['Avg Profit']),
                dict(label='Avg Rating', values=top_genres_pc['Avg Rating']),
                dict(label='Success Rate', values=top_genres_pc['Success']),
                dict(label='Count', values=top_genres_pc['Count'])
            ])
        ))
        fig.update_layout(title="Multi-Dimensional Genre Comparison (Parallel Coordinates)")
        style_chart(fig, 400)
        st.plotly_chart(fig, use_container_width=True)
    
    with genre_row2_col2:
        # Funnel Chart - Genre Success Funnel
        funnel_data = genre_stats.nlargest(10, 'Total Rev')
        fig = go.Figure(go.Funnel(
            y=funnel_data['Genre'],
            x=funnel_data['Total Rev'],
            textposition="inside",
            textinfo="value+percent initial",
            marker=dict(color=funnel_data['Avg Rating'],
                       colorscale='Teal',
                       line=dict(color='#27272a', width=2))
        ))
        fig.update_layout(title="Genre Revenue Funnel (Top 10)")
        style_chart(fig, 400)
        st.plotly_chart(fig, use_container_width=True)

# ============================================
# TAB 5: VISUALIZATION CONCEPTS
# ============================================
with tab_concepts:
    st.markdown('<div class="section-title">🎓 Data Visualization Concepts</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="concept-box">
        <div class="concept-title">📚 About This Dashboard</div>
        <div class="concept-text">
            This dashboard demonstrates key principles of effective data visualization,
            applied to real movie data from TMDB.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Concept 1: Chart Types
    st.markdown("### 📊 1. Choosing the Right Chart Type")
    st.markdown("""
    <div class="concept-box">
        <div class="concept-text">
            • <b>Bar Charts</b> → Compare categories<br>
            • <b>Scatter Plots</b> → Show relationships between variables<br>
            • <b>Line Charts</b> → Display trends over time<br>
            • <b>Pie/Donut</b> → Part-to-whole relationships
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption("📊 Bar: Compare categories")
        fig = px.bar(filtered_df.groupby('primary_genre')['revenue'].sum().nlargest(5).reset_index(),
                    x='primary_genre', y='revenue', color_discrete_sequence=['#22d3ee'])
        style_chart(fig, 220)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.caption("📈 Scatter: Relationships")
        scatter_subset = filtered_df[(filtered_df['budget']>0)&(filtered_df['revenue']>0)]
        s = scatter_subset.sample(min(80, len(scatter_subset))) if len(scatter_subset) > 0 else scatter_subset
        fig = px.scatter(s, x='budget', y='revenue', color_discrete_sequence=['#f59e0b'])
        style_chart(fig, 220)
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        st.caption("📉 Line: Trends over time")
        y = filtered_df.groupby('year')['revenue'].sum().reset_index()
        fig = px.line(y, x='year', y='revenue', color_discrete_sequence=['#22d3ee'])
        style_chart(fig, 220)
        st.plotly_chart(fig, use_container_width=True)
    
    # Concept 2: Color
    st.markdown("### 🎨 2. Strategic Use of Colour")
    st.markdown("""
    <div class="concept-box">
        <div class="concept-text">
            • <b>Sequential</b> → Low to high (single hue gradient)<br>
            • <b>Diverging</b> → Two extremes meeting at midpoint (profit/loss)<br>
            • <b>Categorical</b> → Distinct categories
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    color_col1, color_col2 = st.columns(2)
    with color_col1:
        st.caption("Sequential: Revenue (low → high)")
        top = filtered_df.nlargest(5, 'revenue')
        fig = px.bar(top, y='original_title', x='revenue', orientation='h',
                    color='revenue', color_continuous_scale='Teal')
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        style_chart(fig, 250)
        st.plotly_chart(fig, use_container_width=True)
    
    with color_col2:
        st.caption("Diverging: Profit (orange) vs Loss (purple)")
        sample = pd.concat([filtered_df[filtered_df['budget']>1e7].nlargest(3,'profit'),
                          filtered_df[filtered_df['budget']>1e7].nsmallest(3,'profit')])
        fig = px.bar(sample, y='original_title', x='profit', orientation='h',
                    color='profit', color_continuous_scale=DIVERGING)
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        style_chart(fig, 250)
        st.plotly_chart(fig, use_container_width=True)
    
    # Concept 3: Interactivity
    st.markdown("### 🖱️ 3. Interactive Exploration")
    st.markdown("""
    <div class="concept-box">
        <div class="concept-text">
            • <b>Filters</b> → Sidebar controls to slice data<br>
            • <b>Hover tooltips</b> → Details on demand<br>
            • <b>Custom controls</b> → User-driven views
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("👆 Try the **Interactive tab** to build your own charts!")
    
    # Concept 4: Annotation
    st.markdown("### ✏️ 4. Annotations & Context")
    st.markdown("""
    <div class="concept-box">
        <div class="concept-text">
            • <b>Titles</b> → What the chart shows<br>
            • <b>Reference lines</b> → Benchmarks and averages<br>
            • <b>Callouts</b> → Highlight key points
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    yearly = filtered_df.groupby('year')['revenue'].mean().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=yearly['year'], y=yearly['revenue'], mode='lines+markers',
                            line=dict(color='#22d3ee', width=2)))
    avg = yearly['revenue'].mean()
    fig.add_hline(y=avg, line_dash="dash", line_color="#71717a", annotation_text=f"Average: ${avg/1e6:.0f}M")
    peak = yearly.loc[yearly['revenue'].idxmax()]
    fig.add_annotation(x=peak['year'], y=peak['revenue'], text="Peak Year ↑", showarrow=True, arrowhead=2, arrowcolor='#f59e0b')
    fig.update_layout(title="Average Revenue by Year (Annotated)")
    style_chart(fig, 350)
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# TAB 6: EXPLORER
# ============================================
with tab6:
    st.markdown('<div class="section-title">🔍 Movie Explorer</div>', unsafe_allow_html=True)
    
    search_col1, search_col2, search_col3 = st.columns([2, 1, 1])
    with search_col1:
        search = st.text_input("🔍 Search", placeholder="Enter movie title...")
    with search_col2:
        sort_by = st.selectbox("Sort by", ['revenue', 'profit', 'vote_average', 'popularity', 'year'])
    with search_col3:
        sort_order = st.selectbox("Order", ['Descending', 'Ascending'])
    
    results = filtered_df.copy()
    if search:
        results = results[results['original_title'].str.contains(search, case=False, na=False)]
    results = results.sort_values(sort_by, ascending=(sort_order == 'Ascending'))
    
    st.markdown(f"**{len(results):,} movies found**")
    
    for _, row in results.head(15).iterrows():
        with st.expander(f"🎬 {row['original_title']} ({int(row['year']) if pd.notna(row['year']) else 'N/A'})"):
            col1, col2, col3 = st.columns([2,1,1])
            with col1:
                st.write(f"**Director:** {row['director']}")
                st.write(f"**Genre:** {row['genres']}")
                if pd.notna(row['tagline']):
                    st.write(f"*\"{row['tagline']}\"*")
            with col2:
                st.metric("Revenue", f"${row['revenue']/1e6:.0f}M")
                st.metric("Budget", f"${row['budget']/1e6:.0f}M")
            with col3:
                st.metric("Rating", f"{row['vote_average']:.1f}")
                profit_delta = "Profitable" if row['profit'] >= 0 else "Loss"
                delta_color = "normal" if row['profit'] >= 0 else "inverse"
                st.metric("Profit", f"${row['profit']/1e6:.0f}M", delta=profit_delta, delta_color=delta_color)
    
    st.markdown("---")
    st.dataframe(results[['original_title','year','primary_genre','director','budget','revenue','profit','vote_average']].head(100), use_container_width=True, height=400)
    st.download_button("📥 Download CSV", results.to_csv(index=False), "movies.csv", "text/csv")

# ============================================
# FOOTER
# ============================================
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align:center; padding:20px; color:#71717a;">
    <div style="font-weight:600; color:#fafafa; font-size:1.2rem;">CineMetrics</div>
    <div style="font-size:0.85rem; margin-top:5px;">ITD112 Data Visualization Project • {len(df):,} Movies</div>
</div>
""", unsafe_allow_html=True)
