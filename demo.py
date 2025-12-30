import streamlit as st
from gtts import gTTS
from io import BytesIO
import base64
import streamlit.components.v1 as components
import json
from openai import OpenAI
def bong_bong_bay():
    st.balloons()
   
st.set_page_config(page_title="Trợ lý Lịch sử 4.0", layout="centered")
if "page" not in st.session_state:
    st.session_state.page = "ask"
if "show_bubble" not in st.session_state:
    st.session_state.show_bubble = False

# ====== DÙNG API KEY TỪ STREAMLIT SECRETS ======
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def tra_loi_AI_lich_su(cau_hoi: str):
    prompt = (
        "Bạn là trợ lý chuyên về lịch sử. "
        "Hãy trả lời ngắn gọn, chính xác và không nói lan man.\n"
        f"Câu hỏi: {cau_hoi}\nTrả lời:"
    )
    try:
        completion = client.responses.create(
            model="gpt-4o-mini",
            input=prompt
        )
        return completion.output_text
    except Exception as e:
        return f"AI gặp lỗi: {e}"
def tom_tat_3_y(cau_tra_loi: str):
    prompt = (
        "Hãy tóm tắt nội dung lịch sử sau thành 3 ý ngắn gọn, "
        "mỗi ý 1 dòng, không lan man:\n"
        f"{cau_tra_loi}"
    )
    try:
        res = client.responses.create(
            model="gpt-4o-mini",
            input=prompt
        )
        return res.output_text
    except:
        return None
   
# ======================
# 🔍 TỪ KHÓA LỊCH SỬ
# ======================
history_keywords = [
    "lịch sử", "chiến tranh", "khởi nghĩa", "cách mạng",
    "triều đại", "vua", "thế chiến", "cổ đại", "trung đại",
    "hiện đại", "di tích", "danh lam", "quân", "trận",
    "đế quốc", "là ai", "bác hồ", "hồ chí minh", "nạn đói", "thế giới", 
    "kể tên", "thông tin", "phát xít", "dân chủ", "hậu quả", "mỹ la-tinh", 
    "kinh tế", "hiệp hội", "giặc đói", "chiến dịch", "phong trào", "thắng lợi", "trật tự","xã hội",
    "thành tựu", "xu thế", "điện biên phủ"

]

def is_history_question(question):
    q = question.lower()
    for kw in history_keywords:
        if kw in q:
            return True
    return False

def tao_trac_nghiem_tu_AI(noi_dung):
    prompt = f"""
    Dựa vào nội dung sau, hãy tạo 3 câu hỏi trắc nghiệm lịch sử.
    Mỗi câu có 4 đáp án A, B, C, D.
    Chỉ có 1 đáp án đúng.

    Chỉ trả về JSON, KHÔNG giải thích, KHÔNG thêm chữ.

    Định dạng:
    [
      {{
        "question": "...",
        "options": {{
          "A": "...",
          "B": "...",
          "C": "...",
          "D": "..."
        }},
        "answer": "A"
      }}
    ]

    Nội dung:
    {noi_dung}
    """

    try:
        res = client.responses.create(
            model="gpt-4o-mini",
            input=prompt
        )

        text = res.output_text.strip()

        # 👉 LẤY PHẦN JSON CHO CHẮC
        start = text.find("[")
        end = text.rfind("]") + 1
        json_text = text[start:end]

        return json.loads(json_text)

    except Exception as e:
        st.error("❌ Lỗi tạo câu hỏi trắc nghiệm")
        st.code(str(e))
        return []


# ======================
# ⚙️ CẤU HÌNH TRANG
# ======================

if "audio_unlocked" not in st.session_state:
    st.session_state["audio_unlocked"] = False

st.title("📚 TRỢ LÝ LỊCH SỬ 4.0")
st.write("👉 Bấm BẬT ÂM THANH (chỉ 1 lần), sau đó nhập câu hỏi rồi bấm Trả lời.")
st.write("📱 Trên IOS phải bấm ▶ để nghe.")
st.write("📱 Android/PC tự phát âm thanh.")

st.markdown("""
<style>
/* ===== NỀN GIẤY CỔ ===== */
.stApp {
    background: linear-gradient(180deg, #f6f1e7, #efe7d8);
    color: #2b2b2b;
    font-family: "Segoe UI", serif;
}
/* 🚫 TẮT MÀU CẢNH BÁO MẶC ĐỊNH CỦA RADIO */
div[role="radiogroup"] label {
    background: transparent !important;
    border: none !important;
}

/* Không đỏ khi chưa submit */
div[role="radiogroup"] input:checked + div {
    background-color: transparent !important;
    box-shadow: none !important;
}

/* Bỏ viền focus */
div[role="radiogroup"] input:focus + div {
    outline: none !important;
}

/* ===== TIÊU ĐỀ ===== */
h1 {
    color: #4b2e1f;
    text-align: center;
    letter-spacing: 1.5px;
    margin-bottom: 10px;
}

h2, h3 {
    color: #5c3b28;
}

/* ===== Ô NHẬP – MỀM NHƯ SỔ TAY (FIX CHỮ) ===== */
input[type="text"] {
    background-color: #fffdf8;
    border: 2px dashed #9c7a4a;
    border-radius: 18px;
    padding: 14px;
    font-size: 16px;

    color: #000000 !important;        /* 👈 chữ người dùng nhập */
    font-weight: 500;

    transition: all 0.25s ease;
}

/* Placeholder: Nhập câu hỏi lịch sử */
input[type="text"]::placeholder {
    color: #3b2f1c !important;        /* 👈 nâu đậm cổ */
    opacity: 1;                       /* 👈 BẮT BUỘC */
    font-style: italic;
}

/* Khi focus */
input[type="text"]:focus {
    outline: none;
    border-color: #6b4a2d;
    box-shadow: 0 0 0 3px rgba(107,74,45,0.15);
}

/* ===== NÚT – NHÚN NHẢY NHẸ ===== */
.stButton > button {
    background: linear-gradient(180deg, #7a5536, #5c3b28);
    color: white;
    border-radius: 20px;
    padding: 14px 30px;
    font-size: 16px;
    
