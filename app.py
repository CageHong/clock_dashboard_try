import streamlit as st
import datetime
import pytz
import os
import random
import base64
import pandas_market_calendars as mcal
from streamlit_autorefresh import st_autorefresh

# --- 1. 初始化設定 ---
st.set_page_config(layout="wide", page_title="Vibe Dashboard")

# 優化：雲端建議設為 2000ms (2秒)，避免多人同時在線時記憶體崩潰
st_autorefresh(interval=2000, key="vibe_clock")

IMAGE_DIR = "vibe_images"
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# --- 2. 工具函數 ---

@st.cache_data(ttl=60, show_spinner=False)
def get_base64_img(file_path):
    """加入快取與 TTL，避免每秒重複讀取硬碟導致崩潰"""
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

def get_vibe_bg(minute_seed):
    """局部隨機實例，確保多人同時切換時互不干擾"""
    valid_extensions = ('.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG')
    if not os.path.exists(IMAGE_DIR): return None
    files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(valid_extensions)]
    if not files: return None
    
    local_random = random.Random(minute_seed)
    return os.path.join(IMAGE_DIR, local_random.choice(files))

def check_market_status(exchange_code):
    """股市狀態判斷"""
    try:
        calendar = mcal.get_calendar(exchange_code)
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        schedule = calendar.schedule(start_date=now_utc - datetime.timedelta(days=1), 
                                     end_date=now_utc + datetime.timedelta(days=1))
        is_open = calendar.open_at_time(schedule, now_utc)
        return ("MARKET OPEN", "status-open") if is_open else ("MARKET CLOSED", "status-closed")
    except:
        return ("MARKET CLOSED", "status-closed")

# --- 3. 數據準備 ---

# 優先讀取開關狀態
vibe_mode = st.toggle("DAY MODE", value=True)

# 時區設定
tz_be, tz_tp, tz_us = pytz.timezone('Europe/Brussels'), pytz.timezone('Asia/Taipei'), pytz.timezone('America/New_York')
now_be = datetime.datetime.now(tz_be)
now_tp = datetime.datetime.now(tz_tp)
now_us = datetime.datetime.now(tz_us)

# 核心背景邏輯：強化 Night Mode 的權重
img_path = get_vibe_bg(now_be.minute)
if vibe_mode and img_path:
    b64 = get_base64_img(img_path)
    if b64:
        bg_style = f"""
            background-image: linear-gradient(rgba(16, 31, 48, 0.3), rgba(16, 31, 48, 0.75)), 
                              url('data:image/jpeg;base64,{b64}') !important;
            background-size: cover !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
        """
    else:
        bg_style = "background-image: none !important; background-color: #101f30 !important;"
else:
    bg_style = "background-image: none !important; background-color: #101f30 !important;"

# 獲取股市狀態
tp_stat, tp_class = check_market_status('XTAI')
us_stat, us_class = check_market_status('NYSE')

# --- 4. CSS 樣式注入 ---
st.markdown(f"""
    <style>
    header, [data-testid="stHeader"], footer {{ visibility: hidden; height: 0; }}
    
    .stApp {{
        {bg_style}
        color: white;
        transition: background 1.0s ease-in-out;
    }}

    .stToggle {{ transform: translateX(15vw); margin-top: 20px; margin-bottom: 10px; }}
    div[data-baseweb="toggle"] > div {{ background-color: #444 !important; }}
    div[data-baseweb="toggle"][aria-checked="true"] > div:first-child {{ background-color: #AAA !important; }}
    .stToggle label p {{ color: #AAA !important; font-size: 14px; letter-spacing: 1px; }}

    .dashboard-grid {{
        display: grid;
        grid-template-columns: repeat(6, 25vw);
        grid-template-rows: repeat(3, 33.33vh);
        height: 75vh; width: 100vw;
    }}
    .be-zone {{ 
        grid-column: 1/3; grid-row: 1/3;
        background: rgba(255,255,255,0.03);
        padding-left: 5vw; display: flex;
        flex-direction: column; justify-content: center;
        border-radius: 20px; margin: 10px; 
    }}
    .tp-zone, .us-zone {{ 
        background: rgba(255,255,255,0.02);
        padding-left: 3vw; display: flex;
        flex-direction: column; justify-content: center;
        border-radius: 20px; margin: 10px; overflow: hidden; 
    }}
    .tp-zone {{ grid-column: 1/2; grid-row: 3/4; }}
    .us-zone {{ grid-column: 2/3; grid-row: 3/4; }}

    .city-label {{ font-size: 42px; color: #CCC; }}
    .small-city-label {{ font-size: 26px; color: #AAA; }}
    .be-time {{ font-size: 100px; font-weight: 500; font-variant-numeric: tabular-nums; }}
    .ampm {{ font-size: 50px; margin-left: 20px}}
    .be-date {{ font-size: 42px; font-weight: 450; color: #AAA; margin-right: 20px; }}
    .be-day {{ font-size: 42px; font-weight: 450; color: #BBB; }} 
    .small-time {{ font-size: 45px; font-variant-numeric: tabular-nums; }}
    .small-ampm {{ font-size: 30px; margin-left: 5px}}

    .market-status {{ font-size: 14px; font-weight: bold; margin-top: 10px; letter-spacing: 1px; }}
    .status-open {{ color: #00AA90 !important; }}
    .status-closed {{ color: #888 !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. HTML 渲染 (12小時制) ---
be_time_main = now_be.strftime("%I:%M")
be_ampm = now_be.strftime("%p")
tp_ampm = now_tp.strftime("%p")
us_ampm = now_us.strftime("%p")

be_html = f'''
<div class="be-zone">
    <div class="city-label">Belgium</div>
    <div class="be-time">{be_time_main}<span class="ampm">{be_ampm}</span></div>
    <div class="info-line">
        <span class="be-date">{now_be.strftime("%Y-%m-%d")}</span>
        <span class="be-day">{now_be.strftime("%A")}</span>
    </div>
</div>'''

tp_html = f'''
<div class="tp-zone">
    <div class="small-city-label">Taiwan</div>
    <div class="small-time">{now_tp.strftime("%I:%M")}\
        <span class="small-ampm">{tp_ampm}</span></div>
    <div class="market-status {tp_class}">{tp_stat}</div>
</div>'''

us_html = f'''
<div class="us-zone">
    <div class="small-city-label">New York</div>
    <div class="small-time">{now_us.strftime("%I:%M")}\
        <span class="small-ampm">{us_ampm}</span></div>
    <div class="market-status {us_class}">{us_stat}</div>
</div>'''

st.markdown(f'<div class="dashboard-grid">{be_html}{tp_html}{us_html}</div>', unsafe_allow_html=True)