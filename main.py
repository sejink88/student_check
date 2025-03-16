import streamlit as st
import pandas as pd
import os
import ast

# --- 커스텀 CSS 추가 ---
st.markdown(
    """
    <style>
    /* 전체 배경색 및 폰트 설정 */
    body {
        background-color: #1E1E2F;
        color: #FFFFFF;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* 헤더 스타일 */
    .header {
        text-align: center;
        padding: 20px;
    }
    
    /* 버튼 스타일 */
    .stButton>button {
        background-color: #FF6F61;
        color: white;
        font-size: 18px;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #FF8A75;
    }
    
    /* 체크박스 스타일 (예시) */
    .stCheckbox label {
        font-size: 16px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- 헤더 이미지 및 타이틀 ---
st.markdown('<div class="header"><img src="https://images.unsplash.com/photo-1593642532973-d31b6557fa68?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60" alt="Cool Banner" width="100%"></div>', unsafe_allow_html=True)
st.title("세진코인 관리 시스템")
st.markdown("<h3 style='text-align: center; color: #FF6F61;'>멋진 중학생들을 위한 세진코인 관리 앱</h3>", unsafe_allow_html=True)

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
    with col2:
        if st.button(f"{selected_student}에게 세진코인 회수"):
            data.at[student_index, "세진코인"] -= 1
            record_list = ast.literal_eval(data.at[student_index, "기록"])
            record_list.append(-1)
            data.at[student_index, "기록"] = str(record_list)
            save_data(data)
            st.error(f"{selected_student}에게 세진코인이 사용되었습니다.")
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
