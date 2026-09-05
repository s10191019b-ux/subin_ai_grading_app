import streamlit as st

# ==========================================
# [Session State 초기화]
# ==========================================
if "incorrect_notes" not in st.session_state:
    st.session_state.incorrect_notes = {}

# ==========================================
# [채점 및 피드백 로직] - 유연한 의미 기반 평가
# ==========================================

def evaluate_meaning(user_text, concepts, bad_concepts=[]):
    """학생 답안의 의미 포함 여부 평가"""
    text = user_text.strip().replace(" ", "")
    if not text:
        return False
    # 부정적인 오개념 표현이 포함되어 있으면 False
    if any(bad in text for bad in bad_concepts):
        return False
    # 제시된 의미 개념군 중 하나라도 맞으면 True
    return any(concept in text for concept in concepts)


def grade_set1_q1(ans1, ans2, ans3):
    score = 0
    feedback = {}
    
    # (1) 과제 특성 (의미 확장)
    easy_concepts = ["쉬운", "쉬움", "부담없는", "친숙한", "노력이들지않는", "난이도가낮은", "단순한"]
    if evaluate_meaning(ans1, easy_concepts):
        score += 1
        feedback["(1) 과제 특성"] = {"pass": True, "comment": "과제의 난이도(쉬움/친숙함)를 올바르게 파악했습니다."}
    else:
        score += 0
        feedback["(1) 과제 특성"] = {
            "pass": False,
            "comment": "과제의 난이도가 상대적으로 '쉽거나 친숙한 과제'라는 점이 드러나지 않았습니다.",
            "guide": "'비교적 쉬운 과제' 또는 '친숙하고 좋아하는 과목'처럼 과제의 부담이 적다는 의미를 포함해 보세요.",
            "user_ans": ans1
        }
        
    # (2) 학습 환경 및 방법 (의미 확장)
    alone_concepts = ["혼자", "차분하게", "독자적", "개인", "스스로", "자율적", "방해받지않는"]
    bad_alone = ["함께", "모임", "같이", "여럿이"]
    if evaluate_meaning(ans2, alone_concepts, bad_alone):
        score += 1
        feedback["(2) 학습 환경"] = {"pass": True, "comment": "타인의 자극을 줄이고 '혼자 집중하는 환경'을 잘 제시했습니다."}
    else:
        score += 0
        feedback["(2) 학습 환경"] = {
            "pass": False,
            "comment": "타인과 함께하는 방식이 아닌 '차분히 혼자 집중하는 방식'이 표현되어야 합니다.",
            "guide": "'혼자 집중하는 시간을 갖는다' 또는 '독자적인 공간에서 차분히 공부한다'는 방향으로 수정해 보세요.",
            "user_ans": ans2
        }

    # (3) 현상 명칭
    if "사회적억제" in ans3.strip().replace(" ", ""):
        score += 1
        feedback["(3) 심리 현상"] = {"pass": True, "comment": "정확한 개념 명칭('사회적 억제')을 잘 작성했습니다."}
    else:
        score += 0
        feedback["(3) 심리 현상"] = {
            "pass": False,
            "comment": "'사회적 촉진'과 대비되는 정확한 용어 표기가 필요합니다.",
            "guide": "지문에서 설명한 타인의 존재가 수행을 방해하는 현상인 '사회적 억제'를 정확히 적어보세요.",
            "user_ans": ans3
        }

    return score, 3, feedback


def grade_set1_q2(ans1, ans2, method1, method2):
    score = 0
    feedback = {}
    
    # 방법 중복 여부
    same_method = (method1 == method2)
    
    # 문항 (1) 검증 (쉬운 과제 / 사회적 촉진 관련 내용)
    m1_pass = False
    if method1 == "예시" and evaluate_meaning(ans1, ["예를들어", "예컨대", "경우", "도서관", "커피숍", "모임", "함께"]):
        m1_pass = True
    elif method1 == "정의" and evaluate_meaning(ans1, ["사회적촉진", "이란", "뜻한다", "의미한다"]):
        m1_pass = True
    elif method1 in ["비교", "대조"] and evaluate_meaning(ans1, ["함께", "같이", "달리", "반면", "효과적"]):
        m1_pass = True

    if m1_pass and not same_method:
        score += 1.5
        feedback["(1) 문장 작성"] = {"pass": True, "comment": f"선택한 '{method1}'의 특성과 지문의 내용이 잘 들어맞습니다."}
    else:
        feedback["(1) 문장 작성"] = {
            "pass": False,
            "comment": f"선택한 설명 방법('{method1}')의 구조적 특성이나 '쉬운 과제는 함께할 때 효율적'이라는 내용이 부족합니다.",
            "guide": f"'{method1}'의 표현 방식을 활용하여 쉬운 과제를 할 때 커피숍이나 공부 모임을 활용한다는 내용을 완성해 보세요.",
            "user_ans": ans1
        }

    # 문항 (2) 검증 (어려운 과제 / 사회적 억제 관련 내용)
    m2_pass = False
    if method2 == "대조" and evaluate_meaning(ans2, ["반면", "달리", "와는르게", "아니라", "혼자"]):
        m2_pass = True
    elif method2 == "인과" and evaluate_meaning(ans2, ["때문에", "하므로", "따라서", "원인", "결과", "혼자"]):
        m2_pass = True
    elif method2 == "예시" and evaluate_meaning(ans2, ["예를들어", "경우", "어려운", "복잡한"]):
        m2_pass = True

    # 오개념 검증 (어려운 과제에 함께한다는 결론 제출 시 실패)
    if evaluate_meaning(ans2, ["어려운과제도함께", "어려울때도모임"]):
        m2_pass = False

    if m2_pass and not same_method:
        score += 1.5
        feedback["(2) 문장 작성"] = {"pass": True, "comment": f"선택한 '{method2}'의 특성을 살려 어려운 과제의 학습법을 잘 설명했습니다."}
    else:
        feedback["(2) 문장 작성"] = {
            "pass": False,
            "comment": f"'{method2}' 방법의 특성을 살리면서 '어려운 과제는 혼자 집중해야 한다'는 결론이 명확해야 합니다.",
            "guide": f"'{method2}' 표현 문형을 사용해 지나치게 어렵거나 복잡한 과제는 혼자 차분히 집중해야 학습 효과가 오른다는 방향으로 작성해 보세요.",
            "user_ans": ans2
        }

    return score, 3.0, feedback

# ==========================================
# [Streamlit UI Main]
# ==========================================

st.set_page_config(page_title="서논술형 자동 채점 & 복습 시스템", layout="wide")

st.title("📝 국어과 서·논술형 답안 채점 및 맞춤 피드백 시스템")
st.caption("2회고사 대비 모의 문항 연습 및 오답 피드백")

# 메인 탭 구성
main_tab1, main_tab2 = st.tabs(["✍️ 문항 풀이 및 채점", "📖 오답 노트 & 맞춤 피드백"])

with main_tab1:
    selected_set = st.selectbox("채점할 문항 세트를 선택하세요", ["실전 적용-1 (학습 환경)"])
    
    if selected_set == "실전 적용-1 (학습 환경)":
        st.header("📌 [실전 적용-1] 과제 난이도에 따른 학습 환경")
        
        q_tab1, q_tab2 = st.tabs(["[서·논술형 1]", "[서·논술형 2]"])
        
        # [서·논술형 1]
        with q_tab1:
            st.subheader("요약 표 채우기")
            a1 = st.text_input("(1) 과제의 특성:", placeholder="예: 비교적 쉬운 과제, 부담 없는 학습 내용 등")
            a2 = st.text_input("(2) 효율적인 환경 및 방법:", placeholder="예: 차분하게 혼자 집중하는 시간을 가짐")
            a3 = st.text_input("(3) 관련된 심리 현상:", placeholder="예: 사회적 억제")
            
            if st.button("서·논술형 1 채점하기"):
                score, max_score, fb = grade_set1_q1(a1, a2, a3)
                st.metric("획득 점수", f"{score} / {max_score} 점")
                
                # 결과 기록 및 출력
                for q_name, result in fb.items():
                    if result["pass"]:
                        st.success(f"**{q_name}**: {result['comment']}")
                    else:
                        st.error(f"**{q_name}**: {result['comment']}")
                        # 오답 노트 세션에 저장
                        st.session_state.incorrect_notes[f"[세트1-문항1] {q_name}"] = result

        # [서·논술형 2]
        with q_tab2:
            st.subheader("설명문 작성하기")
            st.info("주어진 첫 문장: 과제의 특성과 난이도에 따라 우리의 학습 효율을 높이는 방법은 다르게 적용되어야 한다.")
            
            col1, col2 = st.columns(2)
            with col1:
                m1 = st.selectbox("(1) 설명 방법 선택:", ["예시", "정의", "비교", "대조"])
                t1 = st.text_area("(1) 문장 작성:", placeholder="예: 예를 들어, 비교적 쉬운 과제는 모임을 통해 함께 공부하는 것이 효과적이다. (예시)")
            with col2:
                m2 = st.selectbox("(2) 설명 방법 선택:", ["대조", "인과", "예시"])
                t2 = st.text_area("(2) 문장 작성:", placeholder="예: 반면 지나치게 어려운 과제는 차분히 혼자 집중할 때 효율성이 높아진다. (대조)")

            if st.button("서·논술형 2 채점하기"):
                score, max_score, fb = grade_set1_q2(t1, t2, m1, m2)
                st.metric("획득 점수", f"{score} / {max_score} 점")
                
                for q_name, result in fb.items():
                    if result["pass"]:
                        st.success(f"**{q_name}**: {result['comment']}")
                    else:
                        st.error(f"**{q_name}**: {result['comment']}")
                        st.session_state.incorrect_notes[f"[세트1-문항2] {q_name}"] = result

# ==========================================
# [탭 2] 오답 노트 및 맞춤 피드백
# ==========================================
with main_tab2:
    st.header("📖 나만의 오답 노트 & 개별 피드백")
    st.caption("채점 과정에서 보완이 필요한 답안들을 모아 복습할 수 있는 공간입니다.")
    
    if not st.session_state.incorrect_notes:
        st.info("🎉 현재 보완이 필요한 오답이 없습니다! 문항을 풀고 채점을 진행해 보세요.")
    else:
        if st.button("오답 노트 초기화"):
            st.session_state.incorrect_notes = {}
            st.rerun()

        for title, item in list(st.session_state.incorrect_notes.items()):
            with st.expander(f"❌ {title}", expanded=True):
                st.write(f"**내가 작성한 답안:** `{item['user_ans'] if item['user_ans'] else '(미입력)'}`")
                st.warning(f"**피드백:** {item['comment']}")
                st.info(f"💡 **이렇게 수정해 보세요:** {item['guide']}")
