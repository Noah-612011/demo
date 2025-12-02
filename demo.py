import streamlit as st
from gpt4all import GPT4All

st.set_page_config(page_title="AI Lịch Sử", page_icon="📜")

# Load model GPT4All (tải lần đầu ~100MB)
model = GPT4All("ggml-gpt4all-j-v1.3-groovy.bin")

st.title("📜 Chat AI Lịch Sử")
st.write("Hỏi AI bất cứ điều gì về lịch sử, nó sẽ trả lời bạn!")

# Lưu lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input từ người dùng
user_input = st.text_input("Nhập câu hỏi lịch sử của bạn:")

if st.button("Gửi"):
    if user_input:
        # Prompt cố định để AI chỉ trả lời về lịch sử
        prompt = f"Bạn là chuyên gia lịch sử. Trả lời chi tiết, chỉ về lịch sử: {user_input}"
        response = model.generate(prompt)

        # Lưu lịch sử chat
        st.session_state.messages.append({"user": user_input, "ai": response})

        # Hiển thị chat
        for msg in st.session_state.messages:
            st.markdown(f"*Bạn:* {msg['user']}")
            st.markdown(f"*AI:* {msg['ai']}\n")
    else:
        st.warning("Nhập câu hỏi trước đã!")

# Nút xóa chat
if st.button("Xóa lịch sử chat"):
    st.session_state.messages = []
    st.success("Đã xóa lịch sử chat!")
