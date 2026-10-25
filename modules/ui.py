import streamlit as st

def inject_css():
    st.markdown("""
    <style>
    .stApp { background: #f5f7fb; }
    [data-testid="stSidebar"] { background: #eef2f8; }
    .block-container { padding-top: 1.6rem; padding-bottom: 2.5rem; }
    div[data-testid="stMetric"] {
        background: white; border: 1px solid #e2e8f0; padding: 16px;
        border-radius: 14px; box-shadow: 0 2px 8px rgba(15,23,42,.04);
    }
    div.stButton > button, div.stDownloadButton > button {
        border-radius: 10px; font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

def render_status(status):
    s = str(status).lower()
    if "unsafe" in s or "critical" in s:
        st.error(f"Status: {status}")
    elif "review" in s or "uncertain" in s:
        st.warning(f"Status: {status}")
    else:
        st.success(f"Status: {status}")
