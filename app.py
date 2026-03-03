import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh

# 1. 頁面配置
st.set_page_config(layout="wide", page_title="Vibe Dashboard")
st_autorefresh(interval=1000, key="vibe_clock")

# 2. 注入左側 1/3 佈局與大日期 CSS
st.markdown("""
    <style>
    header, footer {visibility: hidden;}
    .block-container { padding: 0 !important; max-width: 100% !important; }
    .stApp { background-color: #373C38; }
    
    /* 左側 1/3 容器設定 */
    .side-panel {
        position: fixed;
        top: 0;
        left: 0;
        width: 33.33vw; /* 佔據左側 1/3 */
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding-left: 5vw;
        gap: 8vh; /* 調整上下兩塊的間距 */
        z-index: 100;
    }
    
    /* 單一城市區塊 (半透明底版) */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        padding: 40px;
        border-radius: 20px;
        border-left: 3px solid rgba(255, 255, 255, 0.2); /* 加強側邊線條感 */
        width: 80%;
    }
    
    .city-label { font-size: 14px; color: #888; letter-spacing: 6px; text-transform: uppercase; margin-bottom: 15px; }
    
    .time-display {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 85px; /* 時鐘大小 */
        font-weight: 600;
        letter-spacing: -3px;
        font-variant-numeric: tabular-nums;
        line-height: 1;
        margin-bottom: 10px;
    }
    .time-be { color: #FFFFFF; }
    .time-tp { color: #A9A9A9; }
    
    /* 放大日期與星期 */
    .date-display {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 28px; /* 放大日期 */
        font-weight: 300;
        color: rgba(255, 255, 255, 0.6);
    }
    .weekday-highlight {
        font-weight: 600;
        color: #FFFFFF;
        margin-right: 10px;
    }
    
    /* 輸入框：放在左下方 */
    .stTextInput { position: fixed; bottom: 40px; left: 5vw; width: 25vw; }
    input { background-color: rgba(255,255,255,0.05) !important; color: white !important; border: 1px solid #555 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. 邏輯層 (時區與記憶)
if 'todo' not in st.session_state: st.session_state.todo = ""

tz_tp, tz_be = pytz.timezone('Asia/Taipei'), pytz.timezone('Europe/Brussels')
now_tp, now_be = datetime.datetime.now(tz_tp), datetime.datetime.now(tz_be)

# 4. 渲染左側 1/3 佈局
st.markdown(f"""
    <div class="side-panel">
        <div class="glass-card">
            <div class="city-label">Belgium</div>
            <div class="time-display time-be">{now_be.strftime("%H:%M:%S")}</div>
            <div class="date-display">
                <span class="weekday-highlight">{now_be.strftime("%A")}</span>
                {now_be.strftime("%b %d")}
            </div>
        </div>
        
        <div class="glass-card">
            <div class="city-label">Taipei</div>
            <div class="time-display time-tp">{now_tp.strftime("%H:%M:%S")}</div>
            <div class="date-display">
                <span class="weekday-highlight">{now_tp.strftime("%A")}</span>
                {now_tp.strftime("%b %d")}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 5. 記憶功能輸入框
st.session_state.todo = st.text_input("", value=st.session_state.todo, placeholder="Research Notes...")