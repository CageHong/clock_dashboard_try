import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide")
st_autorefresh(interval=1000, key="vibe_clock")

# 1. CSS 空間定義
st.markdown("""
    <style>
    header, footer {visibility: hidden;}
    .stApp { background-color: #101f30; color: white; }
    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(4, 25vw);
        grid-template-rows: repeat(3, 33.33vh);
        height: 100vh; width: 100vw;
    }
    .be-zone { grid-column: 1/3; grid-row: 1/3; background: rgba(255,255,255,0.03); padding-left: 5vw; display: flex; flex-direction: column; justify-content: center; }
    .tp-zone { grid-column: 3/4; grid-row: 1/2; background: rgba(255,255,255,0.02); padding-left: 3vw; display: flex; flex-direction: column; justify-content: center; overflow: hidden; }
    .us-zone { grid-column: 4/5; grid-row: 1/2; background: rgba(255,255,255,0.01); padding-left: 3vw; display: flex; flex-direction: column; justify-content: center; overflow: hidden; }
    .city-label { font-size: 14px; color: #888; }
    .be-time { font-size: 110px; font-weight: 600; }
    .small-time { font-size: 45px; }
    .status-open { color: #4CAF50; }
    .status-closed { color: #F44336; }
    </style>
""", unsafe_allow_html=True)

# 2. 數據準備
tz_be, tz_tp, tz_us = pytz.timezone('Europe/Brussels'), pytz.timezone('Asia/Taipei'), pytz.timezone('America/New_York')
now_be, now_tp, now_us = datetime.datetime.now(tz_be), datetime.datetime.now(tz_tp), datetime.datetime.now(tz_us)

# 3. 渲染 (避開所有大括號嵌套衝突)
be_html = f'<div class="be-zone"><div class="city-label">Brussels</div><div class="be-time">{now_be.strftime("%H:%M:%S")}</div></div>'
tp_html = f'<div class="tp-zone"><div class="city-label">Taipei</div><div class="small-time">{now_tp.strftime("%H:%M")}</div></div>'
us_html = f'<div class="us-zone"><div class="city-label">New York</div><div class="small-time">{now_us.strftime("%H:%M")}</div></div>'

st.markdown(f'<div class="dashboard-grid">{be_html}{tp_html}{us_html}</div>', unsafe_allow_html=True)