import streamlit as st
import pandas as pd
import os
import json

# 관리자 비밀번호 설정
PASSWORD = "sejin2025"

# CSV 파일 경로
data_file = "students_points.csv"

# 학생 데이터
class_students = {
    "1반": ["김성호", "김재영", "김정원", "김준희", "박민우", "박성하", "박주찬", "박준성", "박필규", "박현우", 
          "반도완", "배준우", "서명교", "윤선빈", "이운찬", "이은규", "장우석", "장재익", "전영현", "전은호", 
          "전준석", "조선우", "차서혁", "최성찬", "최수안", "최준혁", "허진웅", "황지환"],
    "2반": ["강태연", "고연우", "김건우", "김지용", "김태윤", "박성준", "박정우", "박진형", "방성준", "송상민", 
          "오교선", "오수민", "원준영", "윤온유", "윤준원", "이동연", "이민우", "이서후", "이석민", "이승학", 
          "장주노", "조동은", "지준우", "최재혁", "한유담", "한윤서", "홍정재"]
}

def load_data():
    """기존 데이터를 유지하면서 새로운 학생만 추가"""
    if os.path.exists(data_file):
        # 기존 데이터 로드
        data = pd.read_csv(data_file)
    else:
        # 파일이 없으면 빈 데이터프레임 생성
        data = pd.DataFrame(columns=["반", "학생", "세진코인", "기록"])

    # 기존 데이터의 학생 목록 가져오기
    existing_students = set(zip(data["반"], data["학생"]))

    # 새롭게 추가할 학생 리스트
    new_entries = []

    for class_name, students in class_students.items():
        for student in students:
            if (class_name, student) not in existing_students:
                # 새로운 학생은 세진코인 0, 기록을 빈 리스트로 추가
                new_entries.append([class_name, student, 0, "[]"])

    # 새로운 학생만 추가
    if new_entries:
        new_data = pd.DataFrame(new_entries, columns=["반", "학생", "세진코인", "기록"])
        data = pd.concat([data, new_data], ignore_index=True)

    return data

def save_data(data):
    """데이터 변경 시 즉시 CSV 저장"""
    if not data.empty:
        data.to_csv(data_file, index=False)

# 데이터 로드
data = load_data()

# Streamlit UI 설정
st.title("세진코인 관리 시스템")

selected_class = st.selectbox("반을 선택하세요:", sorted(data["반"].unique()))
filtered_data = data[data["반"] == selected_class]

selected_student = st.selectbox("학생을 선택하세요:", sorted(filtered_data["학생"].tolist()))
student_index = data[(data["반"] == selected_class) & (data["학생"] == selected_student)].index[0]

password = st.text_input("비밀번호를 입력하세요:", type="password")

if password == PASSWORD:
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"{selected_student}에게 세진코인 추가"):
            data.at[student_index, "세진코인"] += 1
            record_list = json.loads(data.at[student_index, "기록"])
            record_list.append(1)
            data.at[student_index, "기록"] = json.dumps(record_list)
            save_data(data)  # 즉시 저장
            st.success(f"{selected_student}에게 1코인 추가됨.")
            st.experimental_rerun()

    with col2:
        if st.button(f"{selected_student}에게 세진코인 차감"):
            if data.at[student_index, "세진코인"] > 0:
                data.at[student_index, "세진코인"] -= 1
                record_list = json.loads(data.at[student_index, "기록"])
                record_list.append(-1)
                data.at[student_index, "기록"] = json.dumps(record_list)
                save_data(data)  # 즉시 저장
                st.error(f"{selected_student}에게 1코인 차감됨.")
                st.experimental_rerun()
            else:
                st.warning("세진코인이 부족합니다.")
    
    # 업데이트된 정보 표시
    st.subheader(f"{selected_student}의 정보")
    updated_student_data = data.loc[[student_index], ["반", "학생", "세진코인", "기록"]]
    st.dataframe(updated_student_data)
else:
    st.warning("올바른 비밀번호를 입력하세요.")
