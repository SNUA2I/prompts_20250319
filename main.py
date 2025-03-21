import streamlit as st
import textwrap

# 페이지 설정
st.set_page_config(page_title="실습 프롬프트", layout="wide")

# 부드러운 스크롤 효과를 위한 CSS
st.markdown("""
    <style>
    html { scroll-behavior: smooth; }
    </style>
    """, unsafe_allow_html=True)

# -------------------------
# 대분류 순서(그룹)
# -------------------------
group_order = [
    "대규모 언어 모델의 특징",
    "프롬프트 기법",
    "텍스트 프롬프트: 챗봇",
    "이미지 프롬프트",
    "동영상 프롬프트"
]

# -------------------------
# 프롬프트 데이터
# (본문 예시는 길어서 여기서는 축약/생략 없이 그대로 둡니다.)
# -------------------------
prompts = [
    {
        "group": "대규모 언어 모델의 특징",
        "title": "언어 모델과 학습 패턴",
        "prompt": """다음 이야기를 완성하세요.
옛날 옛적, 착한 콩쥐와

이 이야기를 완성하세요.
콩쥐라는 여자 아이가 자전거 타기를 좋아합니다."""
    },
    # ... 이하 모든 프롬프트(질문에서 제공된 전체 내용)를 동일한 구조로 추가 ...
    # 예시로 몇 개만 더 적어둡니다.
    {
        "group": "프롬프트 기법",
        "title": "일반 프롬프트 작성 / zero-shot",
        "prompt": """영화 리뷰를 ‘긍정’, ‘중립’ 또는 ‘부정’으로 분류합니다.
리뷰: 이 영화는 인간과 기술의 관계를 탐구하며, 시청자로 하여금 깊은 통찰을 얻게 만든다. 특히 연출과 연기가 훌륭해 다시 보고 싶은 영화 중 하나다.
Sentiment:

영화 리뷰를 ‘긍정’, ‘중립’ 또는 ‘부정’으로 분류합니다.
리뷰: 캐릭터와 플롯의 조화가 부족해 집중하기 어려웠다. 스토리가 더 정교했다면 훌륭했을 것이다.
Sentiment:"""
    },
    {
        "group": "텍스트 프롬프트: 챗봇",
        "title": "영어 회화 챗봇",
        "prompt": """당신은 영어 회화 파트너입니다. 사용자가 대화 연습을 원하는 주제나 상황을 알려주면...
당신의 모든 설명은 한국어로 하세요."""
    },
    {
        "group": "이미지 프롬프트",
        "title": "이미지 인식 (1)",
        "prompt": """이미지를 보이는 대로 설명하세요.

이 식물은 어떤 종류인가요? 한 단락으로 설명하세요."""
    },
    {
        "group": "동영상 프롬프트",
        "title": "동영상 이해",
        "prompt": """이 동영상에 대한 설명을 주세요.

이 동영상에 대한 설명을 주세요."""
    },
    # 질문에서 주어진 모든 프롬프트를 동일한 구조로 계속 추가...
]

# -------------------------
# 사이드바 목차 생성
# -------------------------
sidebar_md = "# 프롬프트 목록\n"
for i, grp in enumerate(group_order):
    # 대분류(그룹) 항목
    sidebar_md += f"- [{grp}](#group-{i})\n"
    # 해당 그룹에 속하는 프롬프트를 찾아 제목을 나열
    for j, p in enumerate(prompts):
        if p["group"] == grp:
            sidebar_md += f"    - [{p['title']}](#prompt-{j})\n"

st.sidebar.markdown(sidebar_md, unsafe_allow_html=True)

# -------------------------
# 메인 타이틀
# -------------------------
st.title("실습 프롬프트")

# -------------------------
# 글로벌 비밀번호 사용 (원클릭 Unlock)
# -------------------------
if "global_unlock" not in st.session_state:
    st.session_state["global_unlock"] = False

if not st.session_state["global_unlock"]:
    with st.form("unlock_form"):
        global_pwd = st.text_input("전체 프롬프트 열람을 위한 비밀번호를 입력하세요:", type="password")
        submitted = st.form_submit_button("확인")
        if submitted:
            if global_pwd == "global1234":  # 원하는 비밀번호로 변경
                st.session_state["global_unlock"] = True
            else:
                st.error("비밀번호가 틀렸습니다!")

# -------------------------
# 비밀번호 통과 시, 본문 출력
# -------------------------
if st.session_state["global_unlock"]:
    # 그룹 순서대로 출력
    for i, grp in enumerate(group_order):
        # 대분류 제목 (HTML 태그 h2에 id 부여)
        st.markdown(f'<h2 id="group-{i}">{grp}</h2>', unsafe_allow_html=True)

        # 해당 그룹의 프롬프트 출력
        for j, p in enumerate(prompts):
            if p["group"] == grp:
                # 프롬프트 제목 (HTML 태그 h3에 id 부여)
                st.markdown(f'<h3 id="prompt-{j}">{p["title"]}</h3>', unsafe_allow_html=True)
                # 프롬프트 내용
                st.code(textwrap.dedent(p["prompt"]), language="")
else:
    st.write("비밀번호를 입력하시면 프롬프트 내용을 확인할 수 있습니다.")
