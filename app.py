import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh

# 1. 強制設定為全寬模式，這是解決「非全螢幕」的關鍵
st.set_page_config(layout="wide", page_title="Vibe Dashboard")

# 2. 核心心跳
st_autorefresh(interval=1000, key="vibe_clock")

# 3. 注入 CSS：除了配色與字體，我們還要拔掉邊距 (Padding)
st.markdown("""
    <style>
    /* 拔掉所有預設的邊距與空白 */
    header, footer {visibility: hidden;}
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    .main-container {
        background-color: #101f30; /* 你的暗石灰色 */
        height: 100vh;
        width: 100vw; /* 確保寬度佔滿 100% 視窗 */
        display: flex;
        justify-content: center;
        gap: 200px;
        align-items: center;
        color: #FFFFFF;
        text-align: center;
        position: fixed; /* 固定位置，防止捲動 */
        top: 0;
        left: 0;
    }
    
    .city-label {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 30px;
        font-weight: 300;
        color: #A9A9A9;
        letter-spacing: 5px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    
    .time-display {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 110px;
        font-weight: 450;
        letter-spacing: -2px;
        /* 強制數字等寬，防止秒針跳動時字體晃動 */
        font-variant-numeric: tabular-nums; 
        margin: 0;
    }
    
    .date-display {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 25px;
        font-weight: 300;
        color: #7A7A7A;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. 邏輯層
tz_taipei = pytz.timezone('Asia/Taipei')
tz_belgium = pytz.timezone('Europe/Brussels')

now_tp = datetime.datetime.now(tz_taipei)
now_be = datetime.datetime.now(tz_belgium)

# 5. 渲染層
st.markdown(f"""
    <div class="main-container">
        <div>
            <div class="city-label">Belgium</div>
            <div class="time-display">{now_be.strftime("%H:%M:%S")}</div>
            <div class="date-display">{now_be.strftime("%Y / %m / %d")}</div>
        </div>
        <div>
            <div class="city-label">Taipei</div>
            <div class="time-display">{now_tp.strftime("%H:%M:%S")}</div>
            <div class="date-display">{now_tp.strftime("%Y / %m / %d")}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)