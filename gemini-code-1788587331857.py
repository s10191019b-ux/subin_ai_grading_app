import streamlit as st
import re

# ==========================================
# [채점 엔진] 모듈별 채점 함수
# ==========================================

def grade_set1_q1(ans1, ans2, ans3):
    """ 세트 1 - 문항 1 채점 로직 """
    score = 0
    feedback = []
    
    # (1) 과제 특성
    kw1 = ["쉬운", "쉬운 과제", "난이도가 낮은", "친숙한", "노력이 들지 않는", "큰 노력이 필요 없는"]
    if any(k in ans1 for k in kw1):
        score += 1
        feedback.append("(1) 정답: 과제 난이도가 올바르게 기술되었습니다.")
    else:
        feedback.append("(1) 오답: '쉬운 과제' 또는 '친숙한 과목' 등 과제 난이도 특성이 포함되어야 합니다.")
        
    # (2) 방법
    kw2 = ["혼자", "차분하게", "독자적으로", "혼자서"]
    if any(k in ans2 for k in kw2) and not any(bad in ans2 for bad in ["함께", "모임", "같이"]):
        score += 1
        feedback.append("(2) 정답: '혼자 집중하는 환경'이 올바르게 제시되었습니다.")
    else:
        feedback.append("(2) 오답: 타인과의 협동이 아닌 '혼자 집중하는 방식'이 명시되어야 합니다.")
        
    # (3) 현상 (단어 정답)
    if "사회적 억제" in ans3.replace(" ", ""):
        score += 1
        feedback.append("(3) 정답: '사회적 억제' 용어가 정확히 표기되었습니다.")
    else:
        feedback.append("(3) 오답: '사회적 억제'라는 정확한 명칭이 작성되어야 합니다.")
        
    return score, 3, feedback


def grade_set1_q2(ans1, ans2, method1, method2):
    """ 세트 1 - 문항 2 채점 로직 """
    score = 0
    feedback = []
    
    # 1. 서로 다른 설명 방법 사용 여부
    if method1 == method2:
        feedback.append("⚠️ [감점] (1)과 (2)에 동일한 설명 방법이 선택되었습니다. 서로 다른 방법을 사용해야 합니다.")
    
    # 2. 문항 (1) 검증 (지문 기반 내용 + 설명 방법 특성)
    pass_1 = False
    if method1 in ["예시", "비교", "대조"]:
        if any(k in ans1 for k in ["쉬운", "친숙한", "도서관", "커피숍", "모임", "함께"]):
            pass_1 = True
    elif method1 == "정의":
        if any(k in ans1 for k in ["사회적 촉진", "사회적 억제", "이란", " 뜻한다", "의미한다"]):
            pass_1 = True
            
    if pass_1:
        score += 1.5
        feedback.append(f"(1) 정답: 선택한 '{method1}' 방법의 특성과 지문 내용이 잘 반영되었습니다.")
    else:
        feedback.append(f"(1) 오답: '{method1}' 방법의 특성 또는 지문의 쉬운 과제/사회적 촉진 내용이 드러나지 않습니다.")

    # 3. 문항 (2) 검증
    pass_2 = False
    if method2 in ["대조", "인과", "예시"]:
        if any(k in ans2 for k in ["어려운", "복잡한", "혼자", "차분하게", "집중"]):
            pass_2 = True
            
    # 오개념 검증 (결론 방향성 검증: 어려운 과제에 '함께하기'를 적용하면 오답)
    if any(bad in ans2 for bad in ["어려운 과제도 함께", "모임을 만들어 해결"]):
        pass_2 = False
        feedback.append("⚠️ [오개념 감지] 어려운 과제에는 '혼자 집중하는 환경'을 결론으로 내놓아야 합니다.")

    if pass_2:
        score += 1.5
        feedback.append(f"(2) 정답: 선택한 '{method2}' 방법의 특성과 어려운 과제 학습 전략이 명확합니다.")
    else:
        feedback.append(f"(2) 오답: '{method2}' 방법의 특성이나 '어려운 과제는 혼자 집중해야 한다'는 결론이 부족합니다.")

    return score, 3.0, feedback


def grade_set1_q3(v_ans, v_eff, a_ans, a_eff):
    """ 세트 1 - 문항 3 채점 로직 (영상 연출) """
    score = 0
    feedback = []
    
    # (1) 시각 요소 및 효과
    # 연출: 혼자/개인 공간
    v_ok = any(k in v_ans for k in ["혼자", "개인", "독서실", "방", "클로즈업", "고민", "몰두"])
    # 효과: 타인 자극 차단 / 집중
    v_eff_ok = any(k in v_eff for k in ["자극", "차단", "집중", "차분", "억제"])
    
    if v_ok and v_eff_ok:
        score += 2
        feedback.append("(1) 시각 요소 정답: '혼자 있는 연출'과 '외부 자극 차단/집중 효과'가 지문 근거와 함께 잘 작성되었습니다.")
    else:
        feedback.append("(1) 시각 요소 오답/부분점수: 혼자 공부하는 시각 연출 및 '자극 차단/집중' 효과 서술을 보완하세요.")

    # (2) 청각 요소 및 효과
    # 연출: 정적/고요함/잔잔함
    a_ok = any(k in a_ans for k in ["고요", "적막", "정적", "잔잔", "소음 없는", "초침"])
    # 오개념 차단 (경쾌한 소리 사용 시 오답)
    if any(bad in a_ans for bad in ["경쾌한", "빠른", "왁자지껄"]):
        a_ok = False
        
    # 효과: 몰입/차분함
    a_eff_ok = any(k in a_eff for k in ["몰입", "차분", "집중", "분위기"])
    
    if a_ok and a_eff_ok:
        score += 2
        feedback.append("(2) 청각 요소 정답: 고요한 청각 연출과 '차분한 몰입 분위기 형성' 효과가 적절합니다.")
    else:
        feedback.append("(2) 청각 요소 오답: 정적/고요함을 주는 청각 요소 및 차분한 집중 분위기 효과가 드러나야 합니다.")

    return score, 4.0, feedback


# ==========================================
# [Streamlit UI] 사용자 인터페이스
# ==========================================

st.set_page_config(page_title="서논술형 자동 채점 시스템", layout="wide")

st.title("📝 국어과 서·논술형 답안 자동 채점 시스템")
st.caption("2회고사 대비 모의 문항 (다양한 설명 방법 및 매체의 복합양식성)")

# 세트 선택
selected_set = st.sidebar.selectbox("채점할 문항 세트를 선택하세요", ["실전 적용-1 (학습 환경)", "실전 적용-2 (정전기)", "실전 적용-3 (AI 미술)"])

if selected_set == "실전 적용-1 (학습 환경)":
    st.header("📌 [실전 적용-1] 과제 난이도에 따른 학습 환경")
    
    tab1, tab2, tab3 = st.tabs(["[서·논술형 1]", "[서·논술형 2]", "[서·논술형 3]"])
    
    # ----------------------------------------------------
    # [서·논술형 1]
    # ----------------------------------------------------
    with tab1:
        st.subheader("요약 표 채우기")
        st.write("지문 내용에 맞춰 빈칸 (1), (2), (3)에 들어갈 내용을 작성하세요.")
        
        a1 = st.text_input("(1) 과제의 특성:", placeholder="예: 비교적 쉬운 과제")
        a2 = st.text_input("(2) 효율적인 환경 및 방법:", placeholder="예: 차분하게 혼자 집중하는 시간을 가짐")
        a3 = st.text_input("(3) 관련된 심리 현상:", placeholder="예: 사회적 억제")
        
        if st.button("서·논술형 1 채점하기"):
            score, max_score, fb = grade_set1_q1(a1, a2, a3)
            st.metric("획득 점수", f"{score} / {max_score} 점")
            for f in fb:
                st.write(f)
                
    # ----------------------------------------------------
    # [서·논술형 2]
    # ----------------------------------------------------
    with tab2:
        st.subheader("설명문 작성하기")
        st.info("첫 문장: 과제의 특성과 난이도에 따라 우리의 학습 효율을 높이는 방법은 다르게 적용되어야 한다.")
        
        col1, col2 = st.columns(2)
        with col1:
            m1 = st.selectbox("(1) 문장 설명 방법 선택:", ["예시", "정의", "비교", "대조", "인과"])
            t1 = st.text_area("(1) 이어질 문장 작성:", placeholder="문장 끝에 (설명방법) 표기 권장")
        with col2:
            m2 = st.selectbox("(2) 문장 설명 방법 선택:", ["대조", "인과", "예시", "정의", "비교"])
            t2 = st.text_area("(2) 이어질 문장 작성:", placeholder="문장 끝에 (설명방법) 표기 권장")
            
        with st.expander("💡 선택지별 모범 답안 보기"):
            st.markdown("""
            * **[선택 A: 예시 + 대조]**
              * **(1)** 예를 들어, 비교적 쉬운 과제나 친숙한 과목을 공부할 때에는 커피숍이나 공부 모임 등 다른 사람들과 함께하는 환경이 효과적이다. **(예시)**
              * **(2)** 반면 지나치게 어렵거나 복잡한 과제는 다른 사람과 함께하기보다 차분하게 혼자 집중하여 연습할 때 학습 효율이 올라간다. **(대조)**
            * **[선택 B: 정의 + 예시]**
              * **(1)** 사회적 촉진이란 타인의 존재가 과제 수행을 촉진하는 현상을 의미한다. **(정의)**
              * **(2)** 비교적 쉬운 과제를 할 때 도서관이나 커피숍에서 다른 사람들과 함께 공부하는 것이 이에 해당한다. **(예시)**
            """)

        if st.button("서·논술형 2 채점하기"):
            score, max_score, fb = grade_set1_q2(t1, t2, m1, m2)
            st.metric("획득 점수", f"{score} / {max_score} 점")
            for f in fb:
                st.write(f)

    # ----------------------------------------------------
    # [서·논술형 3]
    # ----------------------------------------------------
    with tab3:
        st.subheader("영상 연출 기획안 (장면 2: 어려운 과제를 할 때)")
        
        v_ans = st.text_input("(1) 시각 요소(Ⓐ) 연출 계획:", placeholder="예: 차분한 독서실에서 혼자 공부에 몰두하는 모습")
        v_eff = st.text_input("   - 시각 요소의 효과:", placeholder="예: 외부 자극을 차단하고 혼자 집중해야 함을 전달함")
        
        a_ans = st.text_input("(2) 청각 요소(Ⓑ) 연출 계획:", placeholder="예: 소음이 거의 없는 고요한 정적이나 잔잔한 소리")
        a_eff = st.text_input("   - 청각 요소의 효과:", placeholder="예: 어려운 과제 수행 시 필요한 차분한 집중 분위기 형성")
        
        if st.button("서·논술형 3 채점하기"):
            score, max_score, fb = grade_set1_q3(v_ans, v_eff, a_ans, a_eff)
            st.metric("획득 점수", f"{score} / {max_score} 점")
            for f in fb:
                st.write(f)

else:
    st.info("나머지 세트(실전 적용-2, 3)도 위와 동일한 채점 구조로 확장 가능합니다. 모듈 구조가 적용되어 있습니다.")