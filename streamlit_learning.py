import streamlit as st

# 1. 建立網頁標題 (替代了 HTML 的 <h1>)
st.title("這是我的第一個網頁")

# 2. 顯示一般文字 (替代了 HTML 的 <p>)
st.write("哈囉！這是一個由 Streamlit 生成的極簡網頁。")

# 3. 建立一個互動按鈕 (替代了 JS 的事件監聽)
if st.button("點我看看"):
    st.success("你點擊了按鈕！這行字是動態出現的。")