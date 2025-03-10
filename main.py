import streamlit as st
import pandas as pd
import os
import ast

# CSV 파일 경로
data_file = "students_points.csv"

# CSV 파일 로드 함수
def load_data():
    if os.path.exists(data_file):
        data = pd.read_csv(data_file)
    else:
        data = pd.DataFrame(columns=["반", "학생", "세진코인", "기록"])

    # 새로운 학생 명단 반영 (기존 데이터 유지)
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
        save_data(data)  # 데이터 저장

    return data

# CSV 파일 저장 함수
def save_data(data):
    data.to_csv(data_file, index=False)

# 데이터 로드
data = load_data()

# 페이지 제목
st.title("세진코인")

# 반 선택
selected_class = st.selectbox("반을 선택하세요:", data["반"].unique())
filtered_data = data[data["반"] == selected_class]

# 학생 선택
selected_student = st.selectbox("학생을 선택하세요:", filtered_data["학생"].tolist())
student_index = data[(data["반"] == selected_class) & (data["학생"] == selected_student)].index[0]

# 세진코인 부여 기능 (비밀번호 확인 추가)
password = st.text_input("비밀번호를 입력하세요:", type="password")
correct_password = "tpwls6212"  # 비밀번호 설정

if password == correct_password:
    col1, col2 = st.columns(2)

    with col1:
        if st.button(f"{selected_student}에게 세진코인 부여"):
            data.at[student_index, "세진코인"] += 1
            record_list = ast.literal_eval(data.at[student_index, "기록"])
            record_list.append(1)
            data.at[student_index, "기록"] = str(record_list)

            save_data(data)  
            data = load_data()  # 변경된 데이터 다시 불러오기
            st.success(f"{selected_student}에게 상점이 부여되었습니다.")

    with col2:
        if st.button(f"{selected_student}에게 세진코인 회수"):
            data.at[student_index, "세진코인"] -= 1
            record_list = ast.literal_eval(data.at[student_index, "기록"])
            record_list.append(-1)
            data.at[student_index, "기록"] = str(record_list)

            save_data(data)  
            data = load_data()  # 변경된 데이터 다시 불러오기
            st.error(f"{selected_student}에게 벌점이 부여되었습니다.")

    # 선택한 학생만 업데이트된 데이터 표시
    st.subheader(f"{selected_student}의 업데이트된 세진코인")
    updated_student_data = data.loc[[student_index], ["반", "학생", "세진코인", "기록"]]
    st.dataframe(updated_student_data)
else:
    st.warning("올바른 비밀번호를 입력하세요.")
