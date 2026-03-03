import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh

# 1. 頁面配置
st.set_page_config(layout="wide", page_title="Vibe Dashboard")
st_autorefresh(interval=1000, key="vibe_clock")

# 2. 注入靠左、上下排列、半透明底版的 CSS
st.markdown("""
    <style>
    header, footer {visibility: hidden;}
    .block-container { padding: 0 !important; max-width: 100% !important; }
    .stApp { background-color: #373C38; }
    
    /* 建立靠左的容器 */
    .side-container {
        position: fixed;
        top: 50px;
        left: 40px;
        display: flex;
        flex-direction: column; /* 上下排列 */
        gap: 20px;
    }
    
    /* 半透明底版樣式 */
    .glass-card {
        background: rgba(255, 255, 255, 0.05); /* 半透明白 */
        backdrop-filter: blur(10px); /* 磨砂玻璃效果 */
        padding: 30px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        width: 380px;
        text-align: left; /* 文字靠左 */
    }
    
    .time-display {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 70px; /* 稍微縮小以適應側邊欄 */
        font-weight: 600;
        letter-spacing: -2px;
        font-variant-numeric: tabular-nums;
        line-height: 1;
    }
    .time-be { color: #FFFFFF; }
    .time-tp { color: #A9A9A9; }
    .city-label { font-size: 14px; color: #888; letter-spacing: 4px; text-transform: uppercase; margin-bottom: 8px; }
    .date-display { font-size: 16px; color: #666; margin-top: 8px; }
    
    /* 輸入框定位 */
    .stTextInput { position: fixed; bottom: 40px; left: 40px; width: 380px; }
    input { background-color: rgba(255,255,255,0.05) !important; color: white !important; border: 1px solid #444 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. 邏輯層 (時區與記憶)
if 'todo' not in st.session_state: st.session_state.todo = ""

tz_tp, tz_be = pytz.timezone('Asia/Taipei'), pytz.timezone('Europe/Brussels')
now_tp, now_be = datetime.datetime.now(tz_tp), datetime.datetime.now(tz_be)

# 4. 渲染側邊上下排列的時鐘
st.markdown(f"""
    <div class="side-container">
        <div class="glass-card">
            <div class="city-label">Brussels</div>
            <div class="time-display time-be">{now_be.strftime("%H:%M:%S")}</div>
            <div class="date-display">{now_be.strftime("%A, %b %d")}</div>
        </div>
        <div class="glass-card">
            <div class="city-label">Taipei</div>
            <div class="time-display time-tp">{now_tp.strftime("%H:%M:%S")}</div>
            <div class="date-display">{now_tp.strftime("%A, %b %d")}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 5. 記憶功能輸入框
st.session_state.todo = st.text_input("", value=st.session_state.todo, placeholder="Research Notes / TAZ Observations...")