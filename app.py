import streamlit as st
from streamlit_sortables import sort_items
import random

# 웹사이트 제목과 아이콘 설정
st.set_page_config(page_title="국어 지문 순서 맞추기", page_icon="📖")

st.title("🧩 국어 지문 드래그 앤 드롭 퀴즈")
st.write("문장을 마우스로 끌어서 원래 순서대로 맞춰보세요!")

# 1. 지문 입력창 (선생님이 수업 전에 수정하거나 학생들이 직접 입력)
st.subheader("1. 지문을 입력하세요")
default_text = "지금까지 살펴본 것처럼 카이로스의 시간은 상황이나 사람에 따라 속도가 다르게 느껴질 수 있다. 하지만 이것은 어디까지나 개인의 느낌일 뿐이다. 실제로 시간이 고무줄처럼 늘었다가 줄어들 수는 없기 때문이다. 따라서 이러한 느낌은 ‘심리적인 상대성’이라고 표현하는 것이 더 적절하다. 재미있는 사실은 이러한 카이로스의 시간만큼은 온전히 우리가 결정할 수 있다는 점이다. 매일 모든 사람에게 똑같이 주어지는 24시간, 우리는 이 시간을 어떻게 보내야 할까?"
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
