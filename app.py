import streamlit as st
from streamlit_sortables import sort_items
import random

# 웹사이트 제목과 아이콘 설정
st.set_page_config(page_title="국어 지문 순서 맞추기", page_icon="📖")

st.title("🧩 국어 지문 드래그 앤 드롭 퀴즈")
st.write("문장을 마우스로 끌어서 원래 순서대로 맞춰보세요!")

# 1. 지문 입력창 (선생님이 수업 전에 수정하거나 학생들이 직접 입력)
st.subheader("1. 지문을 입력하세요")
default_text = "다람쥐는 도토리를 좋아합니다. 겨울이 오기 전에 도토리를 숨깁니다. 하지만 가끔은 어디에 숨겼는지 잊어버리기도 합니다. 덕분에 싹이 터서 나무가 자라납니다."
text_input = st.text_area("교과서 지문을 복사해서 넣어주세요:", default_text, height=150)

# 2. 문장 나누기 및 초기 섞기 로직
# (새로고침 전까지는 섞인 순서가 유지되도록 설정합니다)
if 'shuffled_sentences' not in st.session_state or st.button("새로 섞기"):
    sentences = [s.strip() + "." for s in text_input.split('.') if s.strip()]
    random.shuffle(sentences)
    st.session_state.shuffled_sentences = sentences

st.divider()

# 3. 드래그 앤 드롭 화면
st.subheader("2. 문장을 끌어서 순서를 바꾸세요")
# 이 부분이 마우스로 문장을 움직이게 해주는 핵심 기능입니다.
sorted_items = sort_items(st.session_state.shuffled_sentences)

st.divider()

# 4. 정답 확인 버튼
if st.button("✅ 정답 확인하기"):
    # 원래 지문의 순서와 사용자가 정렬한 순서를 비교합니다.
    original_sentences = [s.strip() + "." for s in text_input.split('.') if s.strip()]
    
    if sorted_items == original_sentences:
        st.balloons() # 정답일 때 풍선 애니메이션
        st.success("우와! 정답입니다. 문장의 흐름을 아주 잘 파악했네요!")
    else:
        st.error("아직 순서가 맞지 않아요. 교과서를 다시 한번 천천히 읽어볼까요?")
