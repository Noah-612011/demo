import streamlit as st
from gtts import gTTS
from io import BytesIO
import base64
import streamlit.components.v1 as components
import json
from groq import Groq
def bong_bong_bay():
    st.balloons()
   
st.set_page_config(page_title="Trợ lý Lịch sử 4.0", layout="centered")
if "page" not in st.session_state:
    st.session_state.page = "ask"
if "show_bubble" not in st.session_state:
    st.session_state.show_bubble = False
st.image("https://c2nguyencongtru.chauduc-brvt.edu.vn/upload/62990/20251215/logo_thcs_nguyencongtru_34a39.png", width=120)

# ====== DÙNG API KEY TỪ STREAMLIT SECRETS ======
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def tra_loi_AI_lich_su(cau_hoi: str):
    prompt = (
        "Bạn là trợ lý chuyên về lịch sử. "
        "Hãy trả lời ngắn gọn, chính xác và không nói lan man.\n"
        f"Câu hỏi: {cau_hoi}\nTrả lời:"
    )
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant" ,
            messages=[
                {"role": "user", "content":
         prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"AI gặp lỗi: {e}"
def tom_tat_3_y(cau_tra_loi: str):
    prompt = (
        "Hãy tóm tắt nội dung lịch sử sau thành 3 ý ngắn gọn, "
        "mỗi ý 1 dòng, không lan man:\n"
        f"{cau_tra_loi}"
    )
    try:
        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
              messages=[
                {"role": "user", "content":
         prompt}
            ]
        )
        return res.choices[0].message.content
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
    "thành tựu", "xu thế", "điện biên phủ", "cột mốc quan trọng", "tóm tắt"

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
        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
           messages=[
                {"role": "user", "content":
         prompt}
            ]
        )

        text = res.choices[0].message.content.strip()

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
    font-weight: 600;
    border: none;
    cursor: pointer;
    box-shadow: 0 6px 0 #4b2e1f;
    animation: pulse 2.5s infinite;
}

/* Hover = chơi */
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 0 #3a2216;
}

/* ===== TRỢ LÝ ĐANG PHÂN TÍCH ===== */
.analysis-box {
    margin-top: 12px;
    padding: 14px 18px;
    background-color: #f3ead7;
    border-left: 6px solid #7a5536;
    border-radius: 14px;
    font-style: italic;
    color: #4b2e1f;
    font-weight: 500;
    animation: fadePulse 1.6s infinite;
}

@keyframes fadePulse {
    0% { opacity: 0.6; }
    50% { opacity: 1; }
    100% { opacity: 0.6; }
}

/* Click = nhấn */
.stButton > button:active {
    transform: translateY(4px);
    box-shadow: 0 2px 0 #3a2216;
}

/* Nhịp thở */
@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.02); }
    100% { transform: scale(1); }
}

/* ===== THẺ TRẢ LỜI – NHƯ THẺ HỌC ===== */
.stAlert, .stInfo {
    background-color: #fff8e9;
    border-radius: 22px;
    padding: 18px;
    margin-top: 14px;
    box-shadow: 0 10px 18px rgba(0,0,0,0.12);
    border-left: 8px solid #6b4a2d;
    animation: pop 0.35s ease;
}

/* Thẻ ghi nhớ */
.stInfo {
    border-left-color: #3f6b4f;
    background-color: #eef5ef;
}

/* Thẻ bật ra */
@keyframes pop {
    from {
        transform: scale(0.95);
        opacity: 0;
    }
    to {
        transform: scale(1);
        opacity: 1;
    }
}

/* ===== AUDIO ===== */
audio {
    margin-top: 12px;
    border-radius: 14px;
}

/* ===== CHI TIẾT NHÍ NHẢNH ===== */
label {
    font-weight: 600;
}

label::before {
    content: "🖋️ ";
}
</style>
""",  unsafe_allow_html=True)

# ======================
# 🔓 NÚT BẬT ÂM THANH
# ======================
if st.button("🔊 BẬT ÂM THANH (1 lần)"):
    js = """
    <script>
        try {
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            if (ctx.state === 'suspended') ctx.resume();
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            gain.gain.value = 0;
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start();
            osc.stop(ctx.currentTime + 0.05);
        } catch(e) {}
    </script>
    """
    components.html(js, height=0)
    st.session_state["audio_unlocked"] = True
    st.success("Âm thanh đã mở khoá!")


# ======================
# 📜 DỮ LIỆU LỊCH SỬ CƠ BẢN
# ======================
lich_su_data = {
    "trưng trắc": "Hai Bà Trưng khởi nghĩa chống quân Hán năm 40 sau Công Nguyên.",
    "ngô quyền": "Ngô Quyền đánh bại quân Nam Hán trên sông Bạch Đằng năm 938.",
    "lý thái tổ": "Năm 1010, Lý Thái Tổ dời đô về Thăng Long.",
    "trần hưng đạo": "Trần Hưng Đạo ba lần đánh bại quân Nguyên – Mông.",
    "lê lợi": "Lê Lợi lãnh đạo khởi nghĩa Lam Sơn và giành độc lập năm 1428."
}

def tra_loi_lich_su(cau_hoi: str):
    if not cau_hoi:
        return "Vui lòng nhập câu hỏi."
    cau_hoi = cau_hoi.lower()
    for key, value in lich_su_data.items():
        if key in cau_hoi:
            return value
    return None  # Không trả lời → dùng AI


# ======================
# 💬 GIAO DIỆN
# ======================
if st.session_state.page == "ask":
    cau_hoi = st.text_input("❓ Nhập câu hỏi lịch sử:")

    if st.button("📖 Trả lời"):
        st.session_state.da_tra_loi = True
        if not is_history_question(cau_hoi):
            st.error("❗ Tôi chỉ trả lời câu hỏi về lịch sử.")
            st.stop()
            
        with st.spinner("📜 Trợ lý đang tra cứu lịch sử..."):
        analysis_placeholder = st.empty()
        analysis_placeholder.markdown(
            '<div class="analysis-box">📜 Trợ lý lịch sử đang phân tích...</div>',
            unsafe_allow_html=True
        )

        tra_loi = tra_loi_lich_su(cau_hoi)
        if tra_loi is None:
            tra_loi = tra_loi_AI_lich_su(cau_hoi)

        analysis_placeholder.empty()
        st.success(tra_loi)

        # 📌 Ghi nhớ nhanh
        st.markdown("### 📌 Ghi nhớ nhanh")
        tom_tat = tom_tat_3_y(tra_loi)
        if tom_tat:
            st.info(tom_tat)

        # 🔊 TTS
        try:
            mp3_fp = BytesIO()
            gTTS(text=tra_loi, lang="vi").write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            audio_b64 = base64.b64encode(mp3_fp.read()).decode()
        except:
            audio_b64 = None

        if audio_b64:
            unlocked = "true" if st.session_state["audio_unlocked"] else "false"
            components.html(f"""
            <audio controls autoplay>
                <source src="data:audio/mp3;base64,{audio_b64}">
            </audio>
            """, height=120)

        st.session_state.noi_dung_on_tap = tra_loi

if st.session_state.get("da_tra_loi") and st.session_state.page == "ask":
    if st.button("🧠 Luyện tập kiến thức"):
        st.session_state.page = "quiz"
        st.rerun()
# ======================
# 📝 TRANG LUYỆN TẬP
# ======================
if st.session_state.page == "quiz":
    st.title("📝 Luyện tập nhanh")

    if st.session_state.get("show_bubble"):
        bong_bong_bay()
        st.session_state.show_bubble = False


    if "noi_dung_on_tap" not in st.session_state:
        st.warning("⚠️ Hãy hỏi bài trước khi luyện tập")
        if st.button("🔙 Quay lại"):
            st.session_state.page = "ask"
            st.rerun()
        st.stop()

    if "quiz_data" not in st.session_state:
        with st.spinner("🤖 AI đang tạo câu hỏi trắc nghiệm..."):
            st.session_state.quiz_data = tao_trac_nghiem_tu_AI(
                st.session_state.noi_dung_on_tap
            )
        st.session_state.user_answers = {}
        st.session_state.submitted = False
        st.rerun()

    st.divider()
    st.markdown("### ✏️ Trả lời các câu hỏi sau:")

    # ===== HIỂN THỊ CÂU HỎI =====
    for idx, q in enumerate(st.session_state.quiz_data):
        st.markdown(f"**Câu {idx+1}: {q['question']}**")

        choice = st.radio(
            "",
            options=list(q["options"].keys()),
            format_func=lambda x: f"{x}. {q['options'][x]}",
            key=f"q_{idx}",
            disabled=st.session_state.submitted
        )

        # Lưu đáp án
        st.session_state.user_answers[idx] = choice

        # ===== ĐÚNG / SAI =====
        is_correct = (
            st.session_state.submitted
            and st.session_state.user_answers.get(idx) == q["answer"]
        )

        is_wrong = (
            st.session_state.submitted
            and st.session_state.user_answers.get(idx) != q["answer"]
        )

        # ===== HIỂN THỊ SAU KHI NỘP =====
        if st.session_state.submitted:
            if is_correct:
                st.markdown(
                    "<div style='color:#2e7d32;font-weight:600'>✔ Đúng</div>",
                    unsafe_allow_html=True
                )
            elif is_wrong:
                st.markdown(
                    "<div style='color:#c62828;font-weight:600'>✖ Sai</div>",
                    unsafe_allow_html=True
                )

        st.divider()

         # ===== NỘP BÀI =====
    if not st.session_state.submitted:
        if st.button("✅ Nộp bài"):
            st.session_state.submitted = True
            st.session_state.show_bubble = True
            st.rerun()
    else:
        score = 0
        st.session_state.wrong_questions = []

        for idx, q in enumerate(st.session_state.quiz_data):
            if st.session_state.user_answers.get(idx) == q["answer"]:
                score += 10
            else:
                st.session_state.wrong_questions.append(q)


        # Hiển thị kết quả
        st.success(f"🎉 Bạn đúng {score // 10}/{len(st.session_state.quiz_data)} câu!")

        # Danh hiệu
        if score == len(st.session_state.quiz_data) * 10:
            st.success("🏆 DANH HIỆU: NHÀ SỬ HỌC NHÍ")
            st.balloons()
        elif score >= 20:
            st.info("🥈 DANH HIỆU: CHIẾN BINH LỊCH SỬ")
        else:
            st.warning("🥉 DANH HIỆU: TẬP SỰ LỊCH SỬ")

        # 📘 NÚT HỌC LẠI PHẦN SAI
        if st.session_state.wrong_questions:
            if st.button("📘 Học lại phần làm sai"):
                st.session_state.page = "review_wrong"
                st.rerun()

        # 🔙 QUAY LẠI
        if st.button("🔙 Quay lại hỏi bài"):
            st.session_state.page = "ask"
            st.session_state.da_tra_loi = False
            st.session_state.show_bubble = False

            for i in range(10):
                st.session_state.pop(f"q_{i}", None)

            st.session_state.pop("quiz_data", None)
            st.session_state.pop("user_answers", None)
            st.session_state.pop("wrong_questions", None)
            st.session_state.submitted = False
            st.rerun()

# ======================
# 📘 TRANG HỌC LẠI PHẦN SAI
# ======================
if st.session_state.page == "review_wrong":
    st.title("📘 Học lại phần làm sai")

    for idx, q in enumerate(st.session_state.wrong_questions):
        st.markdown(f"### ❌ Câu {idx+1}: {q['question']}")

        correct = q["answer"]
        st.success(f"✅ Đáp án đúng: {correct}. {q['options'][correct]}")
        giai_thich = tra_loi_AI_lich_su(
            f"Vì sao đáp án {correct} là đúng cho câu hỏi: {q['question']}?"
        )
        st.info("📌 Giải thích ngắn gọn: " + giai_thich)

    st.divider()

    if st.button("🔙 Quay lại làm bài mới"):
        st.session_state.page = "ask"
        st.session_state.pop("quiz_data", None)
        st.session_state.pop("user_answers", None)
        st.session_state.pop("wrong_questions", None)
        st.session_state.submitted = False
        st.rerun()
