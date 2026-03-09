import streamlit as st
import datetime
import pytz
import os
import random
import base64
import pandas_market_calendars as mcal
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components

# --- 1. 初始化設定 ---
st.set_page_config(layout="wide", page_title="Vibe Dashboard")

# 10秒刷新一次：平衡效能與即時性
st_autorefresh(interval=10000, key="vibe_clock")

IMAGE_DIR = "vibe_images"
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# --- 2. 工具函數 ---

@st.cache_data(ttl=60, show_spinner=False)
def get_base64_img(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

def get_vibe_bg(minute_seed):
    valid_extensions = ('.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG')
    if not os.path.exists(IMAGE_DIR): return None
    files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(valid_extensions)]
    if not files: return None
    
    local_random = random.Random(minute_seed)
    return os.path.join(IMAGE_DIR, local_random.choice(files))

def check_market_status(exchange_code):
    try:
        calendar = mcal.get_calendar(exchange_code)
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        schedule = calendar.schedule(start_date=now_utc - datetime.timedelta(days=1), 
                                     end_date=now_utc + datetime.timedelta(days=1))
        is_open = calendar.open_at_time(schedule, now_utc)
        return ("MARKET OPEN", "status-open") if is_open else ("MARKET CLOSED",\
                                                               "status-closed")
    except:
        return ("MARKET CLOSED", "status-closed")

# --- 3. 數據準備與側邊欄控制 ---

with st.sidebar:
    st.markdown("### DASHBOARD SETTINGS")
    vibe_mode = st.toggle("DAY MODE", value=True)
    st.markdown("---")
    
    # 強化版全螢幕按鈕：純 HTML 確保穿透 Iframe 安全機制
    components.html(
        """
        <button id="fs-btn" style="
            width: 100%; background: rgba(255,255,255,0.08); 
            border: 1px solid rgba(255,255,255,0.15); 
            color: #DDD; padding: 12px; border-radius: 10px; 
            cursor: pointer; font-size: 14px; letter-spacing: 1.5px;
            transition: 0.3s; font-family: sans-serif;
        " onmouseover="this.style.background='rgba(255,255,255,0.15)';\
            this.style.color='white'" 
           onmouseout="this.style.background='rgba(255,255,255,0.08)';\
            this.style.color='#DDD'">
            ▶ PRESENT MODE
        </button>
        <script>
        const btn = document.getElementById('fs-btn');
        btn.onclick = function() {
            const doc = window.parent.document.documentElement;
            const fullDoc = window.parent.document;
            if (!fullDoc.fullscreenElement) {
                if (doc.requestFullscreen) doc.requestFullscreen();
                else if (doc.webkitRequestFullscreen) doc.webkitRequestFullscreen();
                else if (doc.msRequestFullscreen) doc.msRequestFullscreen();
            } else {
                if (fullDoc.exitFullscreen) fullDoc.exitFullscreen();
            }
        };
        </script>
        """,
        height=70,
    )

# 時區設定
tz_be, tz_tp, tz_us = pytz.timezone('Europe/Brussels'), \
                      pytz.timezone('Asia/Taipei'), pytz.timezone('America/New_York')
now_be, now_tp, now_us = datetime.datetime.now(tz_be), \
                         datetime.datetime.now(tz_tp), datetime.datetime.now(tz_us)
# 計算相對於比利時的小時差
tp_diff = f"{int((now_tp.utcoffset() - now_be.utcoffset()).total_seconds() / 3600):+d}"
us_diff = f"{int((now_us.utcoffset() - now_be.utcoffset()).total_seconds() / 3600):+d}"

# 背景圖片邏輯
img_path = get_vibe_bg(now_be.minute)
b64 = get_base64_img(img_path) if vibe_mode and img_path else None
if b64:
    bg_style = f"""
        background-image: linear-gradient(rgba(16, 31, 48, 0.3), rgba(16, 31, 48, 0.75)), 
                          url('data:image/jpeg;base64,{b64}') !important;
        background-size: cover !important;
        background-position: center !important;
    """
else:
    bg_style = "background-image: none !important; background-color: #101f30 !important;"

tp_stat, tp_class = check_market_status('XTAI')
us_stat, us_class = check_market_status('NYSE')

# --- 4. CSS 樣式注入 (Helvetica Neue + 置頂 + 淨化版) ---
st.markdown(f"""
    <style>
    /* 1. 全域字體設定：優先調用 Helvetica Neue 並優化渲染 */
    html, body, [class*="css"], .stApp, div, span, p {{
        font-family: "Helvetica Neue", Helvetica, Arial, "PingFang TC", 
                     "Microsoft JhengHei", sans-serif !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }}

    /* 2. 透明化 Header 並隱藏 Deploy 與 三個點選單 */
    header[data-testid="stHeader"] {{
        background: transparent !important;
    }}
    [data-testid="stAppViewMenu"], [data-testid="stAppDeployButton"] {{
        display: none !important;
    }}
    
    /* 3. 側邊欄喚回按鈕美化：隱身模式 */
    [data-testid="stSidebarCollapsedControl"] {{
        color: white !important;
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 50%;
        margin-top: 65px; 
        opacity: 0.3;
        transition: 0.4s ease;
    }}
    [data-testid="stSidebarCollapsedControl"]:hover {{ 
        opacity: 1; 
        background: rgba(255, 255, 255, 0.2) !important;
    }}

    /* 4. 核心置頂佈局 (向上平移 60px 蓋住原 Header 區域) */
    .block-container {{
        padding: 0rem !important;
        margin-top: -60px !important; 
        max-width: 100vw !important;
        height: 100vh !important;
    }}
    
    footer {{ visibility: hidden; }}
    .stApp {{
        {bg_style}
        color: white;
        transition: background 1.5s ease-in-out;
    }}

    /* 5. Grid 佈局：回歸你最喜歡的 25vw 比例 */
    .dashboard-grid {{
        display: grid;
        grid-template-columns: repeat(6, 25vw);
        grid-template-rows: repeat(3, 33.33vh);
        height: 100vh;
        width: 100vw;
        margin: 0 !important;
    }}
    
    .be-zone {{ 
        grid-column: 1/3; grid-row: 1/3;
        background: rgba(255, 255, 255, 0.03);
        padding-left: 5vw; display: flex;
        flex-direction: column; justify-content: center;
        border-radius: 20px; margin: 15px; 
    }}
    .tp-zone, .us-zone {{ 
        background: rgba(255, 255, 255, 0.02);
        padding-left: 3vw; display: flex;
        flex-direction: column; justify-content: center;
        border-radius: 20px; margin: 15px; overflow: hidden; 
    }}
    .tp-zone {{ grid-column: 1/2; grid-row: 3/4; }}
    .us-zone {{ grid-column: 2/3; grid-row: 3/4; }}

    /* 6. 文字細節：Helvetica Neue 的字距微調 */
    .city-label {{ 
        font-size: 50px; 
        color: #DDD; 
        letter-spacing: -1px; 
    }}
    .small-city-label {{
        font-size: 26px;
        color: #AAA;
        display: flex;
        align-items: baseline;
        letter-spacing: 0.5px;
    }}

    .diff-tag {{
        font-size: 15px;
        font-weight: 400;
        color: rgba(255, 255, 255, 0.4);
        margin-left: 12px;
        letter-spacing: 1px;
    }}

    .be-time {{ 
        font-size: 120px; 
        font-weight: 500; 
        font-variant-numeric: tabular-nums; 
        letter-spacing: -2px; 
    }}
    .ampm {{ 
        font-size: 50px; 
        margin-left: 20px; 
        color: rgba(255, 255, 255, 0.3); 
    }}
    .be-date {{ font-size: 42px; font-weight: 450; color: #AAA; margin-right: 20px; }}
    .be-day {{ font-size: 42px; font-weight: 450; color: #BBB; }} 
    
    .small-time {{ 
        font-size: 45px; 
        font-variant-numeric: tabular-nums; 
        letter-spacing: -1px; 
    }}
    .small-ampm {{ 
        font-size: 30px; 
        margin-left: 5px; 
        color: rgba(255, 255, 255, 0.5); 
    }}

    .market-status {{ 
        font-size: 14px; 
        font-weight: 600; 
        margin-top: 10px;
        letter-spacing: 1.5px; 
        text-transform: uppercase;
    }}
    .status-open {{ color: #00AA90 !important; }}
    .status-closed {{ color: #888 !important; }}

    /* 7. 側邊欄組件美化 */
    div[data-baseweb="toggle"] > div {{ background-color: rgba(255,255,255,0.1) !important; }}
    div[data-baseweb="toggle"][aria-checked="true"] > div {{ background-color: #AAA !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. HTML 渲染 ---
be_html = f'''
<div class="be-zone">
    <div class="city-label">Belgium</div>
    <div class="be-time">{now_be.strftime("%I:%M")}\
        <span class="ampm">{now_be.strftime("%p")}</span></div>
    <div class="info-line">
        <span class="be-date">{now_be.strftime("%B %d, %Y")}</span>
        <span class="be-day">{now_be.strftime("%A")}</span>
    </div>
</div>'''

tp_html = f'''
<div class="tp-zone">
    <div class="small-city-label">Taiwan\
        <span class="diff-tag">{tp_diff}</span></div>
    <div class="small-time">{now_tp.strftime("%I:%M")}\
        <span class="small-ampm">{now_tp.strftime("%p")}</span></div>
    <div class="market-status {tp_class}">{tp_stat}</div>
</div>'''

us_html = f'''
<div class="us-zone">
    <div class="small-city-label">New York\
        <span class="diff-tag">{us_diff}</span></div>
    <div class="small-time">{now_us.strftime("%I:%M")}\
        <span class="small-ampm">{now_us.strftime("%p")}</span></div>
    <div class="market-status {us_class}">{us_stat}</div>
</div>'''

st.markdown(f'<div class="dashboard-grid">{be_html}{tp_html}{us_html}</div>',\
            unsafe_allow_html=True)