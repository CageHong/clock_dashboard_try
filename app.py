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

# 10秒刷新一次
st_autorefresh(interval=10000, key="vibe_clock")

IMAGE_DIR = "vibe_images"
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# --- 2. 工具函數 ---

@st.cache_data(ttl=3600, show_spinner=False)
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
        return ("MARKET OPEN", "status-open") if calendar.open_at_time(schedule, now_utc) else ("MARKET CLOSED", "status-closed")
    except:
        return ("MARKET CLOSED", "status-closed")

# --- 3. 數據準備 ---
tz_be, tz_tp, tz_us = pytz.timezone('Europe/Brussels'), pytz.timezone('Asia/Taipei'), pytz.timezone('America/New_York')
now_be, now_tp, now_us = datetime.datetime.now(tz_be), datetime.datetime.now(tz_tp), datetime.datetime.now(tz_us)

tp_diff = f"{int((now_tp.utcoffset() - now_be.utcoffset()).total_seconds() / 3600):+d}"
us_diff = f"{int((now_us.utcoffset() - now_be.utcoffset()).total_seconds() / 3600):+d}"

with st.sidebar:
    st.markdown("### DASHBOARD SETTINGS")
    vibe_mode = st.toggle("DAY MODE", value=True)
    st.markdown("---")
    components.html("""
        <button id="fs-btn" style="width:100%; background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15); color:#DDD; padding:12px; border-radius:10px; cursor:pointer; font-family:sans-serif;">▶ PRESENT MODE</button>
        <script>
            const btn = document.getElementById('fs-btn');
            btn.onclick = () => {
                const doc = window.parent.document.documentElement;
                if (!window.parent.document.fullscreenElement) doc.requestFullscreen();
                else window.parent.document.exitFullscreen();
            };
        </script>""", height=70)

img_path = get_vibe_bg(now_be.minute)
b64 = get_base64_img(img_path) if vibe_mode and img_path else None

# --- 4. CSS 樣式注入 (精確控制字體與背景) ---
st.markdown(f"""
<style>
    /* 1. 引入字體並精確限制範圍，避免破壞 Streamlit 圖示 */
    @import url('https://fonts.cdnfonts.com/css/helvetica-neue-55');
    
    html, body, [data-testid="stAppViewContainer"],\
            .dashboard-grid, .be-zone, .tp-zone, .us-zone {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
    }}

    /* 2. 背景優化：鎖定底色防止切換時閃白 */
    .stApp {{
        background-color: #101f30 !important;
        background-image: linear-gradient(rgba(16, 31, 48, 0.6), rgba(16, 31, 48, 0.75)),
                          url('data:image/jpeg;base64,{b64}') !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        transition: background-image 2s ease-in-out !important;
    }}

    /* 3. 修正側邊欄按鈕 (防止文字取代圖示) */
    [data-testid="stSidebarCollapsedControl"] {{
        background: rgba(255,255,255,0.1) !important;
        border-radius: 50% !important;
        color: white !important;
        width: 40px !important;
        height: 40px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        top: 20px !important;
    }}
    /* 強制圖示字體回歸 */
    [data-testid="stSidebarCollapsedControl"] span {{
        font-family: "Source Sans Pro", sans-serif !important;
    }}

    /* 4. 佈局設定 */
    header[data-testid="stHeader"] {{ background: transparent !important; }}
    [data-testid="stAppViewMenu"], [data-testid="stAppDeployButton"]\
        {{ display: none !important; }}
    
    .block-container {{
        padding: 0rem !important;
        margin-top: -60px !important;
        max-width: 100vw !important;
        height: 100vh !important;
    }}

    .dashboard-grid {{
        display: grid;
        grid-template-columns: repeat(6, 25vw);
        grid-template-rows: repeat(3, 33.33vh);
        height: 100vh; width: 100vw;
    }}

    .be-zone, .tp-zone, .us-zone {{
        display: flex; flex-direction: column; justify-content: center;
        border-radius: 20px; margin: 15px;
    }}
    .be-zone {{ grid-column: 1/3; grid-row: 1/3;\
        background: rgba(255, 255, 255, 0.1); padding-left: 5vw; }}
    .tp-zone {{ grid-column: 1/2; grid-row: 3/4;\
        background: rgba(255, 255, 255, 0.06); padding-left: 3vw; }}
    .us-zone {{ grid-column: 2/3; grid-row: 3/4;\
        background: rgba(255, 255, 255, 0.06); padding-left: 3vw; }}

    /* 字體粗細調優 */
    .be-time {{ font-size: 120px; font-weight: 500; font-variant-numeric: tabular-nums;\
        letter-spacing: -1px; }}
    .ampm {{ font-size: 50px; margin-left: 15px; color: rgba(255,255,255,0.5);\
        font-weight: 300; }}
    .small-time {{ font-size: 45px; font-variant-numeric: tabular-nums;\
        font-weight: 400; }}
    .status-open {{ color: #00AA90 !important; font-weight: 400; font-size: 14px;\
    margin-top: 10px; }}
    .status-closed {{ color: #888 !important; font-weight: 400; font-size: 14px;\
    margin-top: 10px; }}
</style>
""", unsafe_allow_html=True)

# --- 5. 畫面渲染 ---
tp_stat, tp_class = check_market_status('XTAI')
us_stat, us_class = check_market_status('NYSE')

st.markdown(f'''
<div class="dashboard-grid">
    <div class="be-zone">
        <div style="font-size:40px; color:#CCC; font-weight:300;">Belgium</div>
        <div class="be-time">{now_be.strftime("%I:%M")}<span \
            class="ampm">{now_be.strftime("%p")}</span></div>
        <div style="font-size:35px; color:#AAA;">{now_be.strftime("%B %d, %Y")} \
            <span style="color:#BBB;">{now_be.strftime("%A")}</span></div>
    </div>
    <div class="tp-zone">
        <div style="font-size:26px; color:#AAA; display:flex; align-items:baseline;\
        ">Taiwan<span style="font-size:15px; color:rgba(255,255,255,0.25); \
            margin-left:12px;">{tp_diff}</span></div>
        <div class="small-time">{now_tp.strftime("%I:%M")}\
            <span style="font-size:30px; margin-left:5px; color:rgba(255,255,255,0.2);\
                ">{now_tp.strftime("%p")}</span></div>
        <div class="{tp_class}">{tp_stat}</div>
    </div>
    <div class="us-zone">
        <div style="font-size:26px; color:#AAA; display:flex; align-items:baseline;\
        ">New York<span style="font-size:15px; color:rgba(255,255,255,0.25); \
            margin-left:12px;">{us_diff}</span></div>
        <div class="small-time">{now_us.strftime("%I:%M")}\
            <span style="font-size:30px; margin-left:5px; color:rgba(255,255,255,0.2);\
                ">{now_us.strftime("%p")}</span></div>
        <div class="{us_class}">{us_stat}</div>
    </div>
</div>
''', unsafe_allow_html=True)