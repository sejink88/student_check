import streamlit as st
import pandas as pd
import os

# CSV 파일 경로
data_file = "students_points.csv"

# CSV 파일 로드 함수
def load_data():
    if os.path.exists(data_file):
        return pd.read_csv(data_file)
    else:
        data = pd.DataFrame({
            "학생": ["학생 A", "학생 B", "학생 C", "학생 D"],
            "상벌점": [0, 0, 0, 0],
            "기록": ["[]", "[]", "[]", "[]"]
        })
        data.to_csv(data_file, index=False)
        return data

# CSV 파일 저장 함수
def save_data(data):
    data.to_csv(data_file, index=False)

# 데이터 로드
data = load_data()

# 페이지 제목
st.title("학생 상벌점 관리")

# 학생 목록 표시
st.subheader("학생 목록")
st.dataframe(data)

# 학생 선택
selected_student = st.selectbox("학생을 선택하세요:", data["학생"].tolist())

# 선택한 학생의 현재 점수 가져오기
student_index = data[data["학생"] == selected_student].index[0]

# 상벌점 부여 기능
col1, col2 = st.columns(2)

with col1:
    if st.button(f"{selected_student}에게 상점 부여"):
        data.at[student_index, "상벌점"] += 1
        record_list = eval(data.at[student_index, "기록"])
        record_list.append(1)
        data.at[student_index, "기록"] = str(record_list)
        save_data(data)
        st.success(f"{selected_student}에게 상점이 부여되었습니다.")

with col2:
    if st.button(f"{selected_student}에게 벌점 부여"):
        data.at[student_index, "상벌점"] -= 1
        record_list = eval(data.at[student_index, "기록"])
        record_list.append(-1)
        data.at[student_index, "기록"] = str(record_list)
        save_data(data)
        st.error(f"{selected_student}에게 벌점이 부여되었습니다.")

# 업데이트된 데이터 표시
st.subheader("업데이트된 상벌점")
st.dataframe(data)
