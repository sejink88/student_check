import streamlit as st
import pandas as pd
import os
import ast

# --- 커스텀 CSS 추가 ---
st.markdown(
    """
    <style>
    /* Google Fonts: Orbitron (미래지향적 느낌) */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

    /* .stApp 배경 설정: 코인이 바둑판식으로 배열된 이미지 */
    .stApp {
        background: url('https://cdn.pixabay.com/photo/2013/07/13/10/46/coins-157845_1280.png') repeat !important;
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

    /* 타이틀 스타일 */
    .title {
        text-align: center;
        color: #ff4500;
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
    '<img class="header-img" src="https://media.giphy.com/media/13HgwGsXF0aiGY/giphy.gif" alt="Bitcoin GIF">'
    '</div>',
    unsafe_allow_html=True
)

# --- 타이틀 ---
st.markdown('<h1 class="title">세진코인 관리 시스템</h1>', unsafe_allow_html=True)

# CSV 파일 경로
data_file = "students_points.csv"

# 관리자 비밀번호
ADMIN_PASSWORD = "wjddusdlcjswo"

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

# CSV 파일 저장 함수 (로컬에만 저장)
def save_data(data):
    try:
        data.to_csv(data_file, index=False)
        print("[INFO] 로컬에 CSV 저장 완료!")
    except Exception:
        pass  # 오류 메시지 없이 무시

# 안정적인 이미지 URL 사용 예시
# 부여 시: 축하하는 파티 이미지
award_image = "data:image/jpeg;base64,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"
# 회수 시: 놀란 얼굴 이미지
deduct_image = "https://cdn.pixabay.com/photo/2016/11/29/04/17/emoticon-1869262_1280.png"

# 데이터 로드
data = load_data()

# 반 선택
selected_class = st.selectbox("반을 선택하세요:", data["반"].unique())
filtered_data = data[data["반"] == selected_class]

# 학생 선택
selected_student = st.selectbox("학생을 선택하세요:", filtered_data["학생"].tolist())
student_index = data[(data["반"] == selected_class) & (data["학생"] == selected_student)].index[0]

# 비밀번호 입력
password = st.text_input("비밀번호를 입력하세요:", type="password")

# 세진코인 부여 기능
col1, col2 = st.columns(2)

if password == ADMIN_PASSWORD:
    with col1:
        if st.button(f"{selected_student}에게 세진코인 부여"):
            data.at[student_index, "세진코인"] += 1
            record_list = ast.literal_eval(data.at[student_index, "기록"])
            record_list.append(1)
            data.at[student_index, "기록"] = str(record_list)
            save_data(data)
            st.success(f"{selected_student}에게 세진코인이 부여되었습니다.")
            # 부여 시 재미있는 그림 출력
            st.image(award_image, use_container_width=True)
    with col2:
        if st.button(f"{selected_student}에게 세진코인 회수"):
            data.at[student_index, "세진코인"] -= 1
            record_list = ast.literal_eval(data.at[student_index, "기록"])
            record_list.append(-1)
            data.at[student_index, "기록"] = str(record_list)
            save_data(data)
            st.error(f"{selected_student}에게 세진코인이 사용되었습니다.")
            # 회수 시 재미있는 그림 출력
            st.image(deduct_image, use_container_width=True)
else:
    st.warning("올바른 비밀번호를 입력해야 세진코인을 부여할 수 있습니다.")

# 기본: 선택한 학생의 업데이트된 데이터만 표시
updated_student_data = data.loc[[student_index]]
st.subheader(f"{selected_student}의 업데이트된 세진코인")
st.dataframe(updated_student_data)

# 전체 학생의 세진코인 현황은 체크박스를 클릭할 때만 표시
if st.checkbox("전체 학생 세진코인 현황 보기"):
    st.subheader("전체 학생 세진코인 현황")
    st.dataframe(data)
