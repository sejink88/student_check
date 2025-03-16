import streamlit as st
import pandas as pd
import os
import ast
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

# 🔹 Google Drive API 인증 설정
SCOPES = ["https://www.googleapis.com/auth/drive.file"]
SERVICE_ACCOUNT_FILE = "your_service_account.json"  # ✅ 서비스 계정 JSON 키 파일 (위치 확인 필요)

# Google Drive API 서비스 생성
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
drive_service = build("drive", "v3", credentials=credentials)

# 🔹 Google Drive에 CSV 저장 함수
def save_to_google_drive(local_file, drive_folder_id):
    """Google Drive에 CSV 파일 업로드"""
    file_metadata = {
        "name": os.path.basename(local_file),
        "parents": ["1L7weXiTriUbfiwhN03LFRhn3IRU4c3Y2"],  # ✅ Google Drive 폴더 ID 입력
    }
    media = MediaFileUpload(local_file, mimetype="text/csv")
    
    file = drive_service.files().create(
        body=file_metadata, media_body=media, fields="id"
    ).execute()
    
    print(f"[INFO] Google Drive에 저장됨: {file.get('id')}")

# 🔹 CSV 파일 경로
data_file = "students_points.csv"

# 관리자 비밀번호
ADMIN_PASSWORD = "wjddusdlcjswo"

# 🔹 CSV 파일 로드 함수
def load_data():
    if os.path.exists(data_file):
        return pd.read_csv(data_file)
    else:
        data = pd.DataFrame({
            "반": ["1반", "1반", "2반", "2반"],
            "학생": ["학생 A", "학생 B", "학생 C", "학생 D"],
            "상벌점": [0, 0, 0, 0],
            "기록": ["[]", "[]", "[]", "[]"]
        })
        data.to_csv(data_file, index=False)
        return data

# 🔹 CSV 파일 저장 함수 (Google Drive 연동 포함)
def save_data(data):
    """로컬에 CSV 저장 후 Google Drive에 업로드"""
    data.to_csv(data_file, index=False)
    print("[INFO] 로컬에 CSV 저장 완료!")

    # Google Drive에 저장 (폴더 ID 입력 필요)
    drive_folder_id = "1L7weXiTriUbfiwhN03LFRhn3IRU4c3Y2"  # ✅ Google Drive 폴더 ID 입력
    save_to_google_drive(data_file, drive_folder_id)

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

# 비밀번호 입력
password = st.text_input("비밀번호를 입력하세요:", type="password")

# 상벌점 부여 기능
col1, col2 = st.columns(2)

if password == ADMIN_PASSWORD:
    with col1:
        if st.button(f"{selected_student}에게 세진코인 부여"):
            data.at[student_index, "상벌점"] += 1
            record_list = ast.literal_eval(data.at[student_index, "기록"])
            record_list.append(1)
            data.at[student_index, "기록"] = str(record_list)
            save_data(data)  # 🔹 Google Drive에 저장
            st.success(f"{selected_student}에게 세진코인이 부여되었습니다.")

    with col2:
        if st.button(f"{selected_student}에게 세진코인 회수"):
            data.at[student_index, "상벌점"] -= 1
            record_list = ast.literal_eval(data.at[student_index, "기록"])
            record_list.append(-1)
            data.at[student_index, "기록"] = str(record_list)
            save_data(data)  # 🔹 Google Drive에 저장
            st.error(f"{selected_student}에게 세진코인이 사용되었습니다.")
else:
    st.warning("올바른 비밀번호를 입력해야 상벌점을 부여할 수 있습니다.")

# 업데이트된 데이터 표시
st.subheader("업데이트된 상벌점")
st.dataframe(data)

