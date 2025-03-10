import streamlit as st
import pandas as pd
import os
import ast

# CSV 파일 경로
data_file = "students_points.csv"

# CSV 파일 로드 함수
def load_data():
    """CSV 파일을 로드하고, 학생 데이터를 업데이트하는 함수"""
    if os.path.exists(data_file):
        data = pd.read_csv(data_file)
    else:
        data = pd.DataFrame(columns=["반", "학생", "세진코인", "기록"])

    class_students = {
        "1반": ["김성호", "김재영", "김정원", "김준희"],
        "2반": ["강태연", "고연우", "김건우"],
        "3반": ["강성철", "강정웅", "권승우"],
        "4반": ["강범준", "고태윤", "김성훈"],
        "5반": ["김도현", "김범찬", "김세훈"]
    }

    existing_students = set(zip(data["반"], data["학생"]))
    new_entries = []

    for class_name, students in class_students.items():
        for student in students:
            if (class_name, student) not in existing_students:
                new_entries.append([class_name, student, 0, "[]"])

    if new_entries:
        new_data = pd.DataFrame(new_entries, columns=["반", "학생", "세진코인", "기록"])
        data = pd.concat([data, new_data], ignore_index=True)
        save_data(data)

    return data

# CSV 파일 저장 함수
def save_data(data):
    """현재 데이터를 CSV 파일에 저장하는 함수"""
    data.to_csv(data_file, index=False)

# 세션 상태에서 데이터 로드
if "data" not in st.session_state:
    st.session_state["data"] = load_data()

data = st.session_state["data"]

# 페이지 제목
st.title("세진코인 관리 시스템")

# 반 선택
selected_class = st.selectbox("반을 선택하세요:", data["반"].unique())
filtered_data = data[data["반"] == selected_class]

# 학생 선택
selected_student = st.selectbox("학생을 선택하세요:", filtered_data["학생"].tolist())
student_index = data[(data["반"] == selected_class) & (data["학생"] == selected_student)].index[0]

# 세진코인 부여 기능 (비밀번호 확인 추가)
password = st.text_input("비밀번호를 입력하세요:", type="password")
correct_password = "sejin2025"

if password == correct_password:
    col1, col2 = st.columns(2)

    with col1:
        if st.button(f"{selected_student}에게 세진코인 부여"):
            data.at[student_index, "세진코인"] += 1
            record_list = ast.literal_eval(data.at[student_index, "기록"])
            record_list.append(1)
            data.at[student_index, "기록"] = str(record_list)

            # 데이터 저장 후 세션 상태 업데이트
            save_data(data)
            st.session_state["data"] = data

            st.success(f"{selected_student}에게 세진코인이 부여되었습니다.")

    with col2:
        if st.button(f"{selected_student}에게 세진코인 회수"):
            data.at[student_index, "세진코인"] -= 1
            record_list = ast.literal_eval(data.at[student_index, "기록"])
            record_list.append(-1)
            data.at[student_index, "기록"] = str(record_list)

            # 데이터 저장 후 세션 상태 업데이트
            save_data(data)
            st.session_state["data"] = data

            st.error(f"{selected_student}에게 세진코인이 회수되었습니다.")

    # 선택한 학생의 업데이트된 데이터 표시
    st.subheader(f"{selected_student}의 업데이트된 세진코인")
    updated_student_data = data.loc[[student_index], ["반", "학생", "세진코인", "기록"]]
    st.dataframe(updated_student_data)
else:
    st.warning("올바른 비밀번호를 입력하세요.")
