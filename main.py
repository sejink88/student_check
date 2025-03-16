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

    /* 전체 배경: 코인이 바둑판식으로 배열된 이미지 적용 */
    html, body, [class*="css"]  {
        background: url('https://cdn.pixabay.com/photo/2013/07/13/10/46/coins-157845_1280.png') repeat;
        background-size: 150px 150px;  /* 이미지 크기를 조절 (원하는 크기로 변경 가능) */
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
         background-color: #00cc66 !imp
