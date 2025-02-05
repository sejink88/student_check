import streamlit as st
import pandas as pd

# 초기 상벌점 기록 (이 부분은 실시간으로 업데이트 되거나, CSV 파일로 로드하여 활용)
students = ['학생 A', '학생 B', '학생 C', '학생 D']
# 각 학생의 이름과 초기 상벌점 (0으로 시작)
points = {student: {'상벌점': 0, '기록': []} for student in students}

# 상벌점 기록 함수
def update_points(student, point_change):
    points[student]['상벌점'] += point_change
    points[student]['기록'].append(point_change)

# 페이지 제목
st.title("학생 상벌점 관리")

# 학생 목록 표시
st.subheader("학생 목록")
# 학생들의 상벌점과 기록을 출력
df = pd.DataFrame([(student, points[student]['상벌점'], points[student]['기록']) for student in students],
                  columns=['학생', '상벌점', '기록'])

st.dataframe(df)

# 학생 선택
selected_student = st.selectbox("학생을 선택하세요:", students)

# 상벌점 부여 기능
col1, col2 = st.columns(2)

with col1:
    if st.button(f"{selected_student}에게 상점 부여"):
        update_points(selected_student, 1)
        st.success(f"{selected_student}에게 상점이 부여되었습니다.")

with col2:
    if st.button(f"{selected_student}에게 벌점 부여"):
        update_points(selected_student, -1)
        st.error(f"{selected_student}에게 벌점이 부여되었습니다.")

# 업데이트된 데이터 표시
st.subheader("업데이트된 상벌점")
df = pd.DataFrame([(student, points[student]['상벌점'], points[student]['기록']) for student in students],
                  columns=['학생', '상벌점', '기록'])
st.dataframe(df)

