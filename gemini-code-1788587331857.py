import streamlit as st

# ==========================================
# [Session State 기반 게임 데이터 초기화]
# ==========================================
if "user_xp" not in st.session_state:
    st.session_state.user_xp = 0
if "user_level" not in st.session_state:
    st.session_state.user_level = 1
if "user_hp" not in st.session_state:
    st.session_state.user_hp = 100
if "incorrect_notes" not in st.session_state:
    st.session_state.incorrect_notes = {}

# XP 및 레벨업 업데이트 함수
def add_xp(amount):
    st.session_state.user_xp += amount
    # 100 XP당 1 레벨업
    new_level = (st.session_state.user_xp // 100) + 1
    if new_level > st.session_state.user_level:
        st.session_state.user_level = new_level
        st.balloons()
        st.toast(f"🎉 LEVEL UP! 레벨 {st.session_state.user_level}이(가) 되었습니다!", icon="⚔️")

# ==========================================
# [채점 및 유연한 평가 로직]
# ==========================================
def evaluate_meaning(user_text, concepts, bad_concepts=[]):
    text = user_text.strip().replace(" ", "")
    if not text:
        return False
    if any(bad in text for bad in bad_concepts):
        return False
    return any(concept in text for concept in concepts)

def grade_set1_q1(ans1, ans2, ans3):
    score = 0
    feedback = {}
    
    # (1) 과제 특성
    easy_concepts = ["쉬운", "쉬움", "부담없는", "친숙한", "노력이들지않는", "난이도가낮은", "단순한"]
    if evaluate_meaning(ans1, easy_concepts):
        score += 1
        feedback["(1) 과제 특성"] = {"pass": True, "comment": "🎯 과제의 난이도 특성을 올바르게 분석했습니다."}
    else:
        feedback["(1) 과제 특성"] = {
            "pass": False,
            "comment": "🛡️ 과제가 상대적으로 '쉽거나 친숙하다'는 핵심 특성이 빠져있습니다.",
            "guide": "지문에서 다룬 '부담이 적거나 친숙한 과제'의 특성이 드러나도록 써보세요.",
            "user_ans": ans1
        }
        
    # (2) 학습 환경
    alone_concepts = ["혼자", "차분하게", "독자적", "개인", "스스로", "자율적", "방해받지않는"]
    bad_alone = ["함께", "모임", "같이", "여럿이"]
    if evaluate_meaning(ans2, alone_concepts, bad_alone):
        score += 1
        feedback["(2) 학습 환경"] = {"pass": True, "comment": "🎯 타인의 자극을 피하고 '혼자 집중하는 환경'을 잘 제시했습니다."}
    else:
        feedback["(2) 학습 환경"] = {
            "pass": False,
            "comment": "🛡️ 타인과 함께하는 방식이 아니라 '차분히 혼자 집중하는 방식'이 명시되어야 합니다.",
            "guide": "타인의 방해 없이 '혼자 집중하여 공부한다'는 결론으로 수정해 보세요.",
            "user_ans": ans2
        }

    # (3) 심리 현상 명칭
    if "사회적억제" in ans3.strip().replace(" ", ""):
        score += 1
        feedback["(3) 심리 현상"] = {"pass": True, "comment": "🎯 정확한 주문(용어)인 '사회적 억제'를 간파했습니다!"}
    else:
        feedback["(3) 심리 현상"] = {
            "pass": False,
            "comment": "🛡️ 정확한 심리학 용어 명칭이 필요합니다.",
            "guide": "지문에서 타인의 존재가 오히려 방해가 되는 현상으로 소개된 '사회적 억제'를 입력하세요.",
            "user_ans": ans3
        }

    return score, 3, feedback


def grade_set1_q2(ans1, ans2, method1, method2):
    score = 0
    feedback = {}
    same_method = (method1 == method2)
    
    # (1) 문항 검증
    m1_pass = False
    if method1 == "예시" and evaluate_meaning(ans1, ["예를들어", "예컨대", "경우", "도서관", "커피숍", "모임", "함께"]):
        m1_pass = True
    elif method1 == "정의" and evaluate_meaning(ans1, ["사회적촉진", "이란", "뜻한다", "의미한다"]):
        m1_pass = True
    elif method1 in ["비교", "대조"] and evaluate_meaning(ans1, ["함께", "같이", "달리", "반면", "효과적"]):
        m1_pass = True

    if m1_pass and not same_method:
        score += 1.5
        feedback["(1) 문장 작성"] = {"pass": True, "comment": f"🎯 스킬 '{method1}'의 특성과 학습 전략을 잘 결합했습니다."}
    else:
        feedback["(1) 문장 작성"] = {
            "pass": False,
            "comment": f"🛡️ 선택한 설명 기술('{method1}')의 문장 구조나 '쉬운 과제는 함께해야 한다'는 결론이 약합니다.",
            "guide": f"'{method1}' 기법을 활용하여 '쉬운 과제나 친숙한 과목은 모임 등을 통해 함께 공부할 때 효율적이다'라는 내용을 완성하세요.",
            "user_ans": ans1
        }

    # (2) 문항 검증
    m2_pass = False
    if method2 == "대조" and evaluate_meaning(ans2, ["반면", "달리", "와는르게", "아니라", "혼자"]):
        m2_pass = True
    elif method2 == "인과" and evaluate_meaning(ans2, ["때문에", "하므로", "따라서", "원인", "결과", "혼자"]):
        m2_pass = True
    elif method2 == "예시" and evaluate_meaning(ans2, ["예를들어", "경우", "어려운", "복잡한"]):
        m2_pass = True

    if evaluate_meaning(ans2, ["어려운과제도함께", "어려울때도모임"]):
        m2_pass = False

    if m2_pass and not same_method:
        score += 1.5
        feedback["(2) 문장 작성"] = {"pass": True, "comment": f"🎯 스킬 '{method2}'의 특성을 활용해 어려운 과제 전략을 명확히 설명했습니다."}
    else:
        feedback["(2) 문장 작성"] = {
            "pass": False,
            "comment": f"🛡️ '{method2}' 기술의 표현 방식과 '어려운 과제는 혼자 집중해야 한다'는 결론이 드러나야 합니다.",
            "guide": f"'{method2}' 표현 패턴을 적용하여, 지나치게 심도 있거나 어려운 과제는 혼자 집중할 때 효율성이 올라간다는 내용으로 작성해 보세요.",
            "user_ans": ans2
        }

    return score, 3.0, feedback


# ==========================================
# [UI & 게임 스테이지 구성]
# ==========================================
st.set_page_config(page_title="서논술형 던전 탐험대", layout="wide", page_icon="⚔️")

# 사이드바: 게임 대시보드
st.sidebar.title("⚔️ 탐험대 상태창")
st.sidebar.markdown(f"**LEVEL:** {st.session_state.user_level}")
st.sidebar.progress(st.session_state.user_xp % 100 / 100, text=f"XP: {st.session_state.user_xp} / {(st.session_state.user_level)*100}")
st.sidebar.metric("체력 (HP)", f"{st.session_state.user_hp} / 100")

if st.sidebar.button("🎮 게임 데이터 리셋"):
    st.session_state.user_xp = 0
    st.session_state.user_level = 1
    st.session_state.user_hp = 100
    st.session_state.incorrect_notes = {}
    st.rerun()

st.title("🏰 국어 서논술형 던전 탐험")
st.caption("텍스트 퀘스트를 수행하며 서논술형 표현력을 극대화하세요!")

main_tab1, main_tab2 = st.tabs(["⚔️ 퀘스트 수행 (문제 풀이)", "📜 오답 재훈련소 (맞춤 피드백)"])

# ----------------------------------------------------
# [탭 1] 퀘스트 수행
# ----------------------------------------------------
with main_tab1:
    st.header("STAGE 1. 효율적인 학습 환경의 비밀을 찾아라")
    
    q_tab1, q_tab2 = st.tabs(["[퀘스트 1] 요약 표 완성", "[퀘스트 2] 설명문 연계"])
    
    # [퀘스트 1]
    with q_tab1:
        st.subheader("📋 퀘스트 1: 요약 표의 빈칸을 채워라!")
        st.write("지문의 내용을 분석하여 빈칸 (1), (2), (3)에 들어갈 적절한 답을 입력하세요.")
        
        # 정답 유출 방지: placeholder에는 힌트성 예시를 완전히 제거함
        ans1 = st.text_input("(1) 과제의 특성:", placeholder="답안을 입력하세요...")
        ans2 = st.text_input("(2) 효율적인 환경 및 방법:", placeholder="답안을 입력하세요...")
        ans3 = st.text_input("(3) 관련된 심리 현상 명칭:", placeholder="답안을 입력하세요...")
        
        if st.button("⚔️ 퀘스트 1 제출 및 공격"):
            score, max_score, fb = grade_set1_q1(ans1, ans2, ans3)
            earned_xp = int(score * 20)
            add_xp(earned_xp)
            
            st.write(f"### 획득 경험치: +{earned_xp} XP (점수: {score}/{max_score})")
            
            for q_name, result in fb.items():
                if result["pass"]:
                    st.success(f"**{q_name}**: {result['comment']}")
                else:
                    st.error(f"**{q_name}**: {result['comment']}")
                    st.session_state.user_hp = max(0, st.session_state.user_hp - 10)
                    st.session_state.incorrect_notes[f"[ST1-Q1] {q_name}"] = result

    # [퀘스트 2]
    with q_tab2:
        st.subheader("✍️ 퀘스트 2: 설명문 작성 공격!")
        st.info("📜 주어진 첫 문장: 과제의 특성과 난이도에 따라 우리의 학습 효율을 높이는 방법은 다르게 적용되어야 한다.")
        
        col1, col2 = st.columns(2)
        with col1:
            m1 = st.selectbox("(1) 문장 사용 기술(설명 방법):", ["예시", "정의", "비교", "대조"])
            t1 = st.text_area("(1) 이어질 문장 작성:", placeholder="내용을 작성하고 끝에 (사용방법)을 표기하세요...")
        with col2:
            m2 = st.selectbox("(2) 문장 사용 기술(설명 방법):", ["대조", "인과", "예시"])
            t2 = st.text_area("(2) 이어질 문장 작성:", placeholder="내용을 작성하고 끝에 (사용방법)을 표기하세요...")

        if st.button("⚔️ 퀘스트 2 제출 및 공격"):
            score, max_score, fb = grade_set1_q2(t1, t2, m1, m2)
            earned_xp = int(score * 25)
            add_xp(earned_xp)
            
            st.write(f"### 획득 경험치: +{earned_xp} XP (점수: {score}/{max_score})")
            
            for q_name, result in fb.items():
                if result["pass"]:
                    st.success(f"**{q_name}**: {result['comment']}")
                else:
                    st.error(f"**{q_name}**: {result['comment']}")
                    st.session_state.user_hp = max(0, st.session_state.user_hp - 10)
                    st.session_state.incorrect_notes[f"[ST1-Q2] {q_name}"] = result

# ----------------------------------------------------
# [탭 2] 오답 재훈련소
# ----------------------------------------------------
with main_tab2:
    st.header("📜 오답 재훈련소 (피드백 & 복습)")
    st.caption("실패했던 퀘스트를 다시 분석하고 약점을 보완하세요.")
    
    if not st.session_state.incorrect_notes:
        st.info("🎉 완벽합니다! 현재 보완할 오답 퀘스트가 없습니다. 모든 던전을 클리어하세요!")
    else:
        for title, item in list(st.session_state.incorrect_notes.items()):
            with st.expander(f"⚠️ {title}", expanded=True):
                st.write(f"**작성했던 답안:** `{item['user_ans'] if item['user_ans'] else '(미입력)'}`")
                st.warning(f"**분석 피드백:** {item['comment']}")
                st.info(f"💡 **공격력 강화 가이드 (수정 방향):** {item['guide']}")
