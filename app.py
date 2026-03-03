import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh

# 1. 頁面配置
st.set_page_config(layout="wide", page_title="Vibe Dashboard")
st_autorefresh(interval=1000, key="vibe_clock")

# 2. 注入 CSS：修正層級與輸入框位置
st.markdown("""
    <style>
    header, footer {visibility: hidden;}
    .block-container { padding: 0 !important; max-width: 100% !important; }
    .stApp { background-color: #101f30; }
    
    /* 左側 1/3 容器 */
    .side-panel {
        position: fixed;
        top: 0;
        left: 0;
        width: 33.33vw;
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding-left: 5vw;
        gap: 5vh;
        z-index: 10; /* 降低層級確保輸入框可被點擊 */
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        padding: 40px;
        border-radius: 20px;
        width: 100%; /* 確保寬度填滿 1/3 內的 padding */
    }
    
    .city-label { font-size: 24px; color: #888; letter-spacing: 6px; text-transform: uppercase; margin-bottom: 10px; }
    
    .time-display {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 85px;
        font-weight: 450;
        letter-spacing: -3px;
        font-variant-numeric: tabular-nums;
        line-height: 1;
        margin-bottom: 10px;
    }
    .time-be { color: #FFFFFF; }
    .time-tp { color: #A9A9A9; }
    
    .date-display {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 28px;
        font-weight: 300;
        color: rgba(255, 255, 255, 0.6);
    }
    .weekday-highlight { font-weight: 600; color: #FFFFFF; margin-right: 10px; }
    
    /* 輸入框定位修改：將其移出 side-panel 的覆蓋範圍 */
    .stTextInput { 
        position: fixed; 
        bottom: 40px; 
        left: 40vw; /* 移到右側 2/3 的起始位置 */
        width: 30vw; 
        z-index: 100; /* 確保在最上層 */
    }
    input { 
        background-color: rgba(255,255,255,0.05) !important; 
        color: white !important; 
        border: 1px solid #555 !important; 
        padding: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 邏輯層 (時區與記憶)
if 'todo' not in st.session_state: st.session_state.todo = ""

tz_tp, tz_be = pytz.timezone('Asia/Taipei'), pytz.timezone('Europe/Brussels')
now_tp, now_be = datetime.datetime.now(tz_tp), datetime.datetime.now(tz_be)

# 4. 渲染 HTML (確保 div 標籤完全閉合)
st.markdown(f"""
    <div class="side-panel">
        <div class="glass-card">
            <div class="city-label">Belgium</div>
            <div class="time-display time-be">{now_be.strftime("%H:%M")}</div>
            <div class="date-display">
                <span class="weekday-highlight">{now_be.strftime("%A")}</span>
                {now_be.strftime("%b %d")}
            </div>
        </div>
        
        <div class="glass-card">
            <div class="city-label">Taipei</div>
            <div class="time-display time-tp">{now_tp.strftime("%H:%M")}</div>
            <div class="date-display">
                <span class="weekday-highlight">{now_tp.strftime("%A")}</span>
                {now_tp.strftime("%b %d")}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 5. 記憶功能輸入框
st.session_state.todo = st.text_input("", value=st.session_state.todo, placeholder="Research Notes...")