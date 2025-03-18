import streamlit as st
import pandas as pd
import os
import ast
import time
import bcrypt

# --- 커스텀 CSS 추가 ---
st.markdown(
    """
    <style>
    /* Google Fonts: Orbitron (미래지향적 느낌) */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

    /* .stApp 배경 설정: 코인이 바둑판식으로 배열된 이미지 */
    .stApp {
        background: url('https://global-assets.benzinga.com/kr/2025/02/16222019/1739712018-Cryptocurrency-Photo-by-SvetlanaParnikov.jpeg') repeat !important;
        background-size: 150px 150px !important;
    }
    
    /* 기본 텍스트 스타일 */
    html, body, [class*="css"] {
        color: #ffffff;
        font-family: 'Orbitron', sans-serif;
    }
    
    /* 헤더 이미지 스타일 */
    .header-img {
        width: 100%;
        max-height: 300px;
        object-fit: cover;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    /* 타이틀 스타일: 빨간색, 굵은 글씨 */
    .title {
        text-align: center;
        color: #ffffff !important;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    /* 버튼 기본 스타일 */
    .stButton>button {
         color: #fff;
         font-weight: bold;
         border: none;
         border-radius: 8px;
         padding: 10px 20px;
         font-size: 16px;
         transition: transform 0.2s ease-in-out;
         box-shadow: 0px 4px 6px rgba(0,0,0,0.3);
    }
    /* 부여 버튼 (첫 번째 컬럼) */
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) .stButton > button {
         background-color: #00cc66 !important;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) .stButton > button:hover {
         background-color: #00e673 !important;
         transform: scale(1.05);
    }
    /* 회수 버튼 (두 번째 컬럼) */
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton > button {
         background-color: #cc3300 !important;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton > button:hover {
         background-color: #ff1a1a !important;
         transform: scale(1.05);
    }
    
    /* 체크박스 스타일 */
    .stCheckbox label {
         font-size: 16px;
         font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- 헤더: 움직이는 비트코인 GIF 추가 ---
st.markdown(
    '<div style="text-align:center;">'
    '<img class="header-img" src="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExemVldTNsMGVpMjZzdjhzc3hnbzl0d2szYjNoNXY2ZGt4ZXVtNncyciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/30VBSGB7QW1RJpNcHO/giphy.gif" alt="Bitcoin GIF">'
    '</div>',
    unsafe_allow_html=True
)

# --- 타이틀 ---
st.markdown('<h1 class="title">세진코인 관리 시스템</h1>', unsafe_allow_html=True)

# CSV 파일 경로
data_file = "students_points.csv"

# 관리자 암호 해시를 환경 변수에서 읽어옵니다.
ADMIN_PASSWORD_HASH = os.environ.get("ADMIN_PASSWORD_HASH")
if not ADMIN_PASSWORD_HASH:
    st.error("관리자 암호 해시가 환경 변수에 설정되어 있지 않습니다.")

def check_admin_password(input_password):
    """입력한 암호의 bcrypt 해시가 저장된 해시와 일치하는지 확인"""
    if not ADMIN_PASSWORD_HASH:
        return False
    return bcrypt.checkpw(input_password.encode('utf-8'),
                          ADMIN_PASSWORD_HASH.encode('utf-8'))

# 효과음 URL (무료 효과음 예시)
award_sound_url = "https://www.soundjay.com/buttons/button-1.wav"   # 부여 효과음
deduct_sound_url = "https://www.soundjay.com/buttons/button-2.wav"  # 회수 효과음

# CSV 파일 로드 함수
def load_data():
    if os.path.exists(data_file):
        return pd.read_csv(data_file)
    else:
        data = pd.DataFrame({
            "반": ["1반", "1반", "2반", "2반"],
            "학생": ["학생 A", "학생 B", "학생 C", "학생 D"],
            "세진코인": [0, 0, 0, 0],
            "기록": ["[]", "[]", "[]", "[]"]
        })
        data.to_csv(data_file, index=False)
        return data

# CSV 파일 저장 함수
def save_data(data):
    try:
        data.to_csv(data_file, index=False)
        print("[INFO] CSV 저장 완료!")
    except Exception as e:
        st.error(f"CSV 저장 오류: {e}")

# 이미지 URL
award_image = "https://cdnweb01.wikitree.co.kr/webdata/editor/202503/16/img_20250316172939_c39ea037.webp"
deduct_image = "https://i.ytimg.com/vi/4v8BOVlDI3Q/maxresdefault.jpg"

# 데이터 로드
data = load_data()

# 반 선택
selected_class = st.selectbox("반을 선택하세요:", data["반"].unique())
filtered_data = data[data["반"] == selected_class]

# 학생 선택
selected_student = st.selectbox("학생을 선택하세요:", filtered_data["학생"].tolist())
student_index = data[(data["반"] == selected_class) & (data["학생"] == selected_student)].index[0]

# 관리자 비밀번호 입력 (평문 입력 후 해시 비교)
password = st.text_input("관리자 비밀번호를 입력하세요:", type="password")

# 관리자 암호 확인 후 기능 사용
if password and check_admin_password(password):
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"{selected_student}에게 세진코인 부여"):
            data.at[student_inde
