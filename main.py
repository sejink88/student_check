import streamlit as st
import pandas as pd

# 학생들의 이름과 초기 상벌점 정보
students = ['학생 A', '학생 B', '학생 C', '학생 D']
points = {'학생 A': 0, '학생 B': 0, '학생 C': 0, '학생 D': 0}

# 학생 데이터프레임
df = pd.DataFrame(list(points.items()), columns=['학생', '상벌점'])

# 페이지 제목
st.title("학생 상벌점 관리")

# 학생 목록 표시
st.subheader("학생 목록")
st.dataframe(df)

# 학생 선택
selected_student = st.selectbox("학생을 선택하세요:", students)

# 상벌점 부여 기능
col1, col2 = st.columns(2)

with col1:
    if st.button(f"{selected_student}에게 상점 부여"):
        points[selected_student] += 1
        st.success(f"{selected_student}에게 상점이 부여되었습니다.")

with col2:
    if st.button(f"{selected_student}에게 벌점 부여"):
        points[selected_student] -= 1
        st.error(f"{selected_student}에게 벌점이 부여되었습니다.")

# 업데이트된 데이터 표시
df = pd.DataFrame(list(points.items()), columns=['학생', '상벌점'])
st.subheader("업데이트된 상벌점")
st.dataframe(df)
