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
        # 새로운 학생 명단 반영
        students_data = {
            "반": [],
            "학생": [],
            "상벌점": [],
            "기록": []
        }

        class_students = {
            "1반": ["김성호", "김재영", "김정원", "김준희", "박민우", "박성하", "박주찬", "박준성", "박필규", "박현우", 
                  "반도완", "배준우", "서명교", "윤선빈", "이운찬", "이은규", "장우석", "장재익", "전영현", "전은호", 
                  "전준석", "조선우", "차서혁", "최성찬", "최수안", "최준혁", "허진웅", "황지환"],
            "2반": ["강태연", "고연우", "김건우", "김지용", "김태윤", "박성준", "박정우", "박진형", "방성준", "송상민", 
                  "오교선", "오수민", "원준영", "윤온유", "윤준원", "이동연", "이민우", "이서후", "이석민", "이승학", 
                  "장주노", "조동은", "지준우", "최재혁", "한유담", "한윤서", "홍정재"],
            "3반": ["강성철", "강정웅", "권승우", "금민서", "김동현", "김란우", "김민석", "김민성", "김민준", "김성현",
                  "김장환", "김재원", "김태훈", "김하람", "Lim Kirill", "민현홍", "박지우", "손정혁", "오성민", "유태환", 
                  "이연동", "이준호", "임건우", "임용진", "전찬호", "전홍균", "정영도", "허현준"],
            "4반": ["강범준", "고태윤", "김성훈", "김수환", "김시후", "김태현", "김형준", "박재형", "박중원", "박지우", 
                  "송지환", "신명진", "신정우", "양하랑", "연정우", "오대희", "오은교", "유진호", "윤재석", "이서준", 
                  "이충환", "정지호", "조은찬", "지준서", "최승원", "최찬홍", "최현서"],
            "5반": ["김도현", "김범찬", "김세훈", "김승도", "김신율", "김종호", "김태건", "김한결", "김현수", "백인성", 
                  "안현준", "엄우성", "엄준원", "이원준", "이제범", "이준우", "이태민", "이태영", "임강현", "임서후", 
                  "장승혁", "정원영", "정현재", "지한규", "최종원", "최지원", "한상묵"]
        }

        for class_name, students in class_students.items():
            for student in students:
                students_data["반"].append(class_name)
                students_data["학생"].append(student)
                students_data["상벌점"].append(0)
                students_data["기록"].append("[]")

        data = pd.DataFrame(students_data)
        data.to_csv(data_file, index=False)
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

# 상벌점 부여 기능 (비밀번호 확인 추가)
password = st.text_input("비밀번호를 입력하세요:", type="password")
correct_password = "sejin2025"  # 비밀번호 설정

if password == correct_password:
    col1, col2 = st.columns(2)

    with col1:
        if st.button(f"{selected_student}에게 세진코인 부여"):
            data.at[student_index, "상벌점"] += 1
            record_list = eval(data.at[student_index, "기록"])
            record_list.append(1)
            data.at[student_index, "기록"] = str(record_list)
            save_data(data)
            st.success(f"{selected_student}에게 상점이 부여되었습니다.")

    with col2:
        if st.button(f"{selected_student}에게 세진코인 회수"):
            data.at[student_index, "상벌점"] -= 1
            record_list = eval(data.at[student_index, "기록"])
            record_list.append(-1)
            data.at[student_index, "기록"] = str(record_list)
            save_data(data)
            st.error(f"{selected_student}에게 벌점이 부여되었습니다.")

    # 선택한 학생만 업데이트된 데이터 표시
    st.subheader(f"{selected_student}의 업데이트된 상벌점")
    updated_student_data = data.loc[[student_index], ["반", "학생", "상벌점", "기록"]]
    st.dataframe(updated_student_data)
else:
    st.warning("올바른 비밀번호를 입력하세요.")
