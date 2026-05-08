import streamlit as st
from streamlit_sortables import sort_items
import random

# --- 1. 기본 설정 ---
# 웹사이트 제목, 아이콘, 레이아웃 설정
st.set_page_config(page_title="국어 지문 순서 맞추기", page_icon="📖", layout="wide")

# --- 2. 제목 및 안내 문구 ---
st.title("🧩 국어 지문 드래그 앤 드롭 퀴즈")
st.info("지문을 입력한 후, 섞여 있는 문장을 마우스로 끌어서 원래 순서대로 배열해 보세요!", icon="💡")

# --- 3. 사이드바 설정 (색상 선택, 새로 섞기) ---
with st.sidebar:
    st.header("⚙️ 설정")
    # 색상 선택 도구 (컬러 피커)
    selected_color = st.color_picker("문장 색상 선택", "#FF4B4B")
    
    # '새로 섞기' 버튼
    if st.button("🔄 새로 섞기", use_container_width=True):
        # 'sentences_data'를 삭제하여 문장을 다시 섞도록 함
        if 'sentences_data' in st.session_state:
            del st.session_state['sentences_data']
        # 'text_input_area'의 내용도 초기화될 수 있으므로, 키를 함께 관리
        if 'text_input_area' in st.session_state:
            del st.session_state['text_input_area']
        st.rerun()

st.divider()

# --- 4. 지문 입력 ---
st.subheader("1. 지문을 입력하세요")
default_text = "지금까지 살펴본 것처럼 카이로스의 시간은 상황이나 사람에 따라 속도가 다르게 느껴질 수 있다. 하지만 이것은 어디까지나 개인의 느낌일 뿐이다. 실제로 시간이 고무줄처럼 늘었다가 줄어들 수는 없기 때문이다. 따라서 이러한 느낌은 ‘심리적인 상대성’이라고 표현하는 것이 더 적절하다. 재미있는 사실은 이러한 카이로스의 시간만큼은 온전히 우리가 결정할 수 있다는 점이다. 매일 모든 사람에게 똑같이 주어지는 24시간, 우리는 이 시간을 어떻게 보내야 할까?"
text_input = st.text_area(
    "교과서 지문을 복사해서 넣어주세요:",
    default_text,
    height=150,
    key="text_input_area" # 입력창의 상태를 유지하기 위한 고유 키
)

# --- 5. 문장 처리 및 섞기 로직 ---
# 지문이 입력되었을 때만 아래 로직 실행
if text_input:
    # 지문이 바뀌었거나, 섞인 데이터가 없으면 새로 생성
    if 'sentences_data' not in st.session_state or st.session_state.get('current_text') != text_input:
        st.session_state.current_text = text_input # 현재 지문을 기록
        
        # 원본 문장 순서 저장 (정답 비교용, 마침표 제거)
        original_sentences = [s.strip() for s in text_input.split('.') if s.strip()]
        
        # 섞을 문장 데이터 생성
        shuffled_sentences = original_sentences[:]
        random.shuffle(shuffled_sentences)
        
        # session_state에 원본과 섞인 순서 모두 저장
        st.session_state.sentences_data = {
            'original': original_sentences,
            'shuffled': shuffled_sentences
        }

    # --- 6. 드래그 앤 드롭 화면 구성 ---
    st.subheader("2. 문장을 끌어서 순서를 바꾸세요")

    # 화면에 표시될 아이템 생성 (색상 적용된 HTML 태그 포함)
    items_to_display = [
        {
            'label': f'<p style="color:{selected_color}; font-size: 16px; margin: 5px 0;">{sentence}.</p>',
            'original_sentence': sentence # HTML 태그가 없는 원본 문장 (정답 비교용)
        }
        for sentence in st.session_state.sentences_data['shuffled']
    ]

    # sort_items에 고유한 key를 부여하여 안정성 향상
    sorted_result_data = sort_items(items_to_display, key='sortable_list', direction='vertical')

    st.divider()

    # --- 7. 정답 확인 로직 ---
    if st.button("✅ 정답 확인하기", use_container_width=True):
        # 사용자가 정렬한 결과에서 순수한 문장 텍스트만 추출
        user_sorted_sentences = [item['original_sentence'] for item in sorted_result_data]
        
        # 정답(원본 순서)과 사용자 정렬 순서 비교
        if user_sorted_sentences == st.session_state.sentences_data['original']:
            st.balloons()
            st.success("🎉 우와! 완벽한 정답입니다. 문장의 흐름을 아주 잘 파악했네요!")
        else:
            st.error("아쉽지만, 아직 순서가 맞지 않아요. 아래 '원문 정답'과 비교하며 다시 한번 생각해볼까요?")
            # 틀렸을 경우 정답 공개
            st.subheader("✨ 원문 정답")
            original_text_display = "\n".join(
                [f"**{i+1}.** {s}." for i, s in enumerate(st.session_state.sentences_data['original'])]
            )
            st.markdown(original_text_display)
