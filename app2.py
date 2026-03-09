import streamlit as st
import datetime
import pytz
import os
import random
import base64
import pandas_market_calendars as mcal
from streamlit_autorefresh import st_autorefresh

# --- 1. 初始化設定 ---
st.set_page_config(layout="wide")
st_autorefresh(interval=1000, key="vibe_clock")

IMAGE_DIR = "vibe_images"
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# --- 2. 工具函數 ---

# 圖片轉 Base64 供 CSS 使用
def get_base64_img(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# 每分鐘隨機挑選一張本地照片
def get_vibe_bg(minute_seed):
    files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not files: return None
    random.seed(minute_seed)
    return os.path.join(IMAGE_DIR, random.choice(files))

# 精確股市狀態判斷 (使用 pandas_market_calendars)
def check_market_status(exchange_code):
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

# 簡約開關：位於頁面最上方，預設靠左
vibe_mode = st.toggle("DAY MODE", value=True)

tz_be = pytz.timezone('Europe/Brussels')
tz_tp = pytz.timezone('Asia/Taipei')
tz_us = pytz.timezone('America/New_York')

now_be = datetime.datetime.now(tz_be)
now_tp = datetime.datetime.now(tz_tp)
now_us = datetime.datetime.now(tz_us)

# 背景圖片與 Vibe 模式邏輯
img_path = get_vibe_bg(now_be.minute)
if vibe_mode and img_path:
    b64 = get_base64_img(img_path)
    bg_css = f"background-image: linear-gradient(rgba(16, 31, 48, 0.3),\
        rgba(16, 31, 48, 0.75)), url('data:image/jpeg;base64,{b64}');\
            background-size: cover; background-position: center;"
else:
    bg_css = "background-color: #101f30;"

# 獲取股市狀態
tp_stat, tp_class = check_market_status('XTAI')
us_stat, us_class = check_market_status('NYSE')

# --- 4. CSS 樣式注入 (核心美化) ---
st.markdown(f"""
    <style>
    /* 1. 徹底隱藏 Header 與 Footer */
    header, [data-testid="stHeader"], footer {{ visibility: hidden; height: 0; }}
    
    /* 2. 背景與全域顏色 */
    .stApp {{
        {bg_css}
        color: white;
        transition: background 1.5s ease-in-out;
    }}

    /* 3. Switch 開關美化：靠左、去紅、灰白感 */
    .stToggle {{
        transform: translateX(15vw);
        margin-top: 20px;
        margin-bottom: 10px;
    }}
    /* 強制修改 Switch 軌道顏色 (關閉時深灰) */
    div[data-baseweb="toggle"] > div {{
        background-color: #444 !important;
    }}
    /* 強制修改 Switch 軌道顏色 (開啟時淺灰，取代紅色) */
    div[data-baseweb="toggle"][aria-checked="true"] > div:first-child {{
        background-color: #AAA !important;
    }}
    /* 修改 DAY MODE 文字顏色 */
    .stToggle label p {{
        color: #AAA !important;
        font-size: 14px;
        letter-spacing: 1px;
    }}

    /* 4. Dashboard Grid 佈局 */
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

    /* 5. 文字與狀態顏色 */
    .city-label {{ font-size: 42px; color: #CCC; }}
    .small-city-label {{ font-size: 20px; color: #AAA; }}
    .be-time {{ font-size: 110px; font-weight: 500; }}
    .be-date {{ font-size: 42px; font-weight: 450; color: #AAA; margin-right: 20px; }}
    .be-day {{ font-size: 42px; font-weight: 450; color: #BBB; }} 
    .small-time {{ font-size: 45px; }}

    .market-status {{ font-size: 14px; font-weight: bold; margin-top: 10px; letter-spacing: 1px; }}
    .status-open {{ color: #00AA90 !important; }}  /* 綠色開盤 */
    .status-closed {{ color: #888 !important; }} /* 灰色休市 */
    </style>
""", unsafe_allow_html=True)

# --- 5. HTML 渲染 ---
be_html = f'''
<div class="be-zone">
    <div class="city-label">Belgium</div>
    <div class="be-time">{now_be.strftime("%H:%M:%S")}</div>
    <div class="info-line">
        <span class="be-date">{now_be.strftime("%Y-%m-%d")}</span>
        <span class="be-day">{now_be.strftime("%A")[:3]}</span>
    </div>
</div>'''

tp_html = f'''
<div class="tp-zone">
    <div class="small-city-label">Taiwan</div>
    <div class="small-time">{now_tp.strftime("%H:%M")}</div>
    <div class="market-status {tp_class}">{tp_stat}</div>
</div>'''

us_html = f'''
<div class="us-zone">
    <div class="small-city-label">New York</div>
    <div class="small-time">{now_us.strftime("%H:%M")}</div>
    <div class="market-status {us_class}">{us_stat}</div>
</div>'''

st.markdown(f'<div class="dashboard-grid">{be_html}{tp_html}{us_html}</div>', unsafe_allow_html=True)