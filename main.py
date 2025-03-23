import streamlit as st
import re
from collections import defaultdict

# 페이지 설정
st.set_page_config(
    page_title="프롬프트 엔지니어링 실습",
    page_icon="📚",
    layout="wide"
)

# 비밀번호 설정
PASSWORD = "idslab2025"

# 데이터 준비 함수
def prepare_data():
    """프롬프트 데이터를 파싱하여 카테고리별로 정리합니다."""
    # 프롬프트 데이터
    data = """
<<대규모 언어 모델의 특징>>
--- 언어 모델과 학습 패턴 --------------------------------------------------------------
다음 이야기를 완성하세요.
옛날 옛적, 착한 콩쥐와

다음 이야기를 완성하세요.
콩쥐라는 여자 아이가 자전거 타기를 좋아합니다.

<<프롬프트 기법>>
--- 일반 프롬프트 작성 / zero-shot (1) ----------------------------------------------------
영화 리뷰를 '긍정', '중립' 또는 '부정'으로 분류합니다.
리뷰: 이 영화는 인간과 기술의 관계를 탐구하며, 시청자로 하여금 깊은 통찰을 얻게 만든다. 특히 연출과 연기가 훌륭해 다시 보고 싶은 영화 중 하나다.
Sentiment:

--- 일반 프롬프트 작성 / zero-shot (2) ----------------------------------------------------
영화 리뷰를 '긍정', '중립' 또는 '부정'으로 분류합니다.
리뷰: 캐릭터와 플롯의 조화가 부족해 집중하기 어려웠다. 스토리가 더 정교했다면 훌륭했을 것이다.
Sentiment:

--- One-shot & Few-shot -----------
고객의 피자 주문을 유효한 JSON으로 변환한다.

예:
치즈, 토마토 소스, 페퍼로니가 들어간 작은 피자를 원합니다.
JSON 응답:
{"크기": "스몰", "유형": "기본", "재료": [["치즈", "토마토 소스", "페퍼로니"]]}

예:
토마토 소스, 바질, 모짜렐라를 곁들인 라지 피자를 주문할 수 있을까요?
JSON 응답:
{"크기": "라지", "유형": "기본","재료": [["토마토 소스", "바질", "모짜렐라"]]}

절반은 치즈와 모짜렐라를 그리고 나머지 절반은 토마토 소스, 햄, 파인애플을 곁들인 라지 피자를 주세요.
JSON 응답:

--- 페르소나: Role Prompting (1) ------------------------------------------------------
당신은 프로그래밍 튜터입니다. 사용자가 배우고 싶은 프로그래밍 언어나 해결하고 싶은 문제를 알려주면, 단계별로 설명해주세요.
예시 요청: "나는 파이썬으로 간단한 계산기를 만들고 싶습니다."
단계별 안내:

--- 페르소나: Role Prompting (2) ------------------------------------------------------
1차 방정식을 나에게 설명해주세요. 내가 칭기즈 칸이라고 가정하세요.

--- 페르소나: Role Prompting (3) ------------------------------------------------------
당신은 나의 주장에 대해 반대 주장을 펼쳐야 합니다. 내가 어떤 이야기나 주장을 하든, 의심스러운 시각에서 항상 반대되는 의견을 세부적으로 제시해주세요.

--- 페르소나: Role Prompting (4) ------------------------------------------------------
외환 위기로 우리 회사는 매우 힘든 한 해를 보낼 것 같습니다.

--- 답변 길이 지정 (1) ------------------------------------------------------------------
학생 회장 선거 연설문을 트윗 길이로 작성하세요.

--- 답변 길이 지정 (2) ------------------------------------------------------------------
학생 회장 선거 연설문을 약 100단어로 작성하세요.

--- 답변 길이 지정 (3) ------------------------------------------------------------------
학생 회장 선거 연설문을 세 문단으로 작성하세요.

--- 추상적이고 일반적인 지침 vs. 명확하고 구체적인 지침 (1) --------------------------------------------
좋은 책 추천해주세요.

--- 추상적이고 일반적인 지침 vs. 명확하고 구체적인 지침 (2) --------------------------------------------
최근 5년 내에 출판된 과학 기술 분야의 비소설 책 중에서 평점이 4.5 이상인 책을 추천해주세요.

--- 추상적이고 일반적인 지침 vs. 명확하고 구체적인 지침 (3) --------------------------------------------
2020년부터 2024년 사이에 출판된 인공지능 분야의 비소설 책 중에서 평점이 4.5 이상인 책을 5권 추천해주세요.

--- 더 명확하고 구체적인 지침 ------------------------------------------------------------
최근 5년 내에 출판된 인공지능 분야의 비소설 책 중에서 평점이 4.5 이상인 책을 5권 추천해주세요.
--------------------------------------
제목: <책 제목>
저자: <책 저자>
내용: <책 내용 요약>
연도: <출간 연도>
평점: <평점>

--- 외국어(영어) 문장 수정 -------------------------------------------------------------
사용자의 요청에 다음 사항을 기반해서 답하세요.

# 지시문
당신은 나의 영어 과외 선생님이며, 영어 원어민입니다. 제가 입력한 영어 문장을 자연스러운 영어로 교정해 주고, 그렇게 교정한 이유를 설명해 주세요. 또한, 제 질문에 대한 답을 주세요.

# 당신의 정보
- 당신은 나의 영어 선생님입니다.
- 당신은 미국 출신의 원어민으로, 매우 일반적인 영어를 사용합니다.
- 당신은 또한 한국어를 열심히 배워서 원어민 수준의 한국어도 구사합니다. 하지만 여전히 모국어는 영어입니다.

# 출력 형식
수정 : [제가 입력한 영어 문장을 자연스러운 영어로 바꿔서 출력]
이유 : [그렇게 수정한 이유를 한국으로 출력]
대체 표현 : [제가 입력한 문장과 비슷한 표현을 추천]
답변 : [제가 입력한 문장에 대한 당신의 답을 영어로 출력]
해석 : [당신의 답변에 대한 한국어 해석을 출력]

--- 템플릿 사용 (A-1) --------------------------------------------------------------
출력물을 위한 템플릿을 제공해 드리겠습니다. 꺾쇠 괄호 <> 안의 단어가 플레이스홀더입니다. 플레이스홀더를 채워주세요. 제 템플릿의 전체 서식을 그대로 유지해 주세요. 제 템플릿은 다음과 같습니다:

출발 공항: <출발 공항 이름>
공항 코드: <출발 공항 코드>

도착 공항: <도착 공항 이름>
공항 코드: <출발 공항 코드>

인천에서 파리까지 비행기를 타고 가고 싶어요.

--- 템플릿 사용 (A-2) --------------------------------------------------------------
제주에서 뉴욕까지 가고 싶어요.

--- 템플릿 사용 (A-3) --------------------------------------------------------------
런던에서 시드니까지 여행 가고 싶어요.

--- 템플릿 사용 (B) --------------------------------------------------------------
결과물을 위한 템플릿을 제공해 드리겠습니다. 꺾쇠 괄호 <> 안의 단어가 플레이스홀더입니다. 
플레이스홀더를 당신의 결과물로 채워주세요. 제 템플릿의 전체 서식을 그대로 유지해 주세요. 제 템플릿은 다음과 같습니다:

질문: <질문>
대답: <답변>

템플릿을 채울 데이터를 제공받으면 템플릿의 서식에 맞게 대답하세요.

아래 URL에 있는 내용을 사용하여 20개의 질문을 만드세요.
https://www.drbworld.com/holding/

--- 더 나은 질문 만들기 ---------------------------------------------------------------
지금부터 내가 질문을 할 때, 더 나은 질문 방식이 있다면 제안하고, 그 질문을 사용할지 여부를 나에게 물어봐 주세요.

--- 더 나은 질문 만들기 (1) ---------------------------------------------------------------
전 세계에는 몇 개의 국가가 있나요?

--- 더 나은 질문 만들기 (2) ---------------------------------------------------------------
지구의 온난화는 심각한가요?

--- 더 나은 질문 만들기 (3) ---------------------------------------------------------------
업무 효율성을 어떻게 높일 수 있을까요?

--- 대안 프롬프트 요청하기 --------------------------------------------------------------
내가 작업을 수행하기 위한 프롬프트를 작성해 달라고 요청할 때마다 작업이 무엇인지 나열하고, 작업을 완료하기 위한 대체 접근 방법을 나열한 다음, 각 접근 방식에 대한 프롬프트를 직접 작성하세요. 완료되면 대안을 작성할 다음 프롬프트를 만들 수 있는지 물어보세요.
어떤 프롬프트를 작성했으면 좋겠는지 물어보세요.

--- 대안 프롬프트 요청하기 (1) --------------------------------------------------------------
언어 모델이 일련의 이메일에서 질문을 자동으로 감지하도록 프롬프트를 작성하고 각 질문 아래에 글머리 기호로 질문에 대한 모든 사람의 의견을 요약합니다.

--- 대안 프롬프트 요청하기 (2) --------------------------------------------------------------
이메일 대화에서 질문을 요약하는 여러 가지 프롬프트와 질문에 대한 다양한 이해 관계자의 관점을 평가하는 프롬프트를 작성합니다.

--- 질문 받기 (1) ----------------------------------------------------------------------
나는 수학 공부를 잘 하고 싶어요. 이 목표를 달성하기 위해 나에게 질문을 해 주세요. 충분한 정보를 얻어 나에게 적합한 수학 공부 계획을 제안할 수 있을 때까지 질문을 계속하세요. 정보를 다 모으면 수학 공부 계획을 보여 주세요. 질문을 한 번에 하나씩 하세요. 

첫 번째 질문을 시작해 주세요.

--- 질문 받기 (2) ----------------------------------------------------------------------
나의 운동 목표에 대해 질문을 해 주세요. 충분한 정보를 얻어 나에게 적합한 근력 운동 계획을 제안할 수 있을 때까지 질문을 계속하세요. 정보를 다 모으면 근력 운동 계획을 보여 주세요. 질문을 한 번에 하나씩 하세요. 

첫 번째 질문을 시작해 주세요.

--- 수학 게임 ---------------------------------------------------------------------
수학 게임을 하겠습니다. 분수와 관련된 질문을 하고 맞출 때마다 점수를 증가시키세요. 답이 틀리면 이유를 알기 쉽게 설명하세요. 

--- AI를 프로그래밍 할 수 있을까? (1) --------------------------------------------------------
아래 내용을 CSV 형식으로 출력하세요.

최근 발견된 행성 후르츠에서는 많은 과일들이 있습니다. 거기에서 자라는 네오스키즐이라는 과일은 보라색이며 사탕처럼 달콤한 맛이 납니다. 또한 회색빛 파란색의 과일인 로헤클도 있으며, 레몬처럼 매우 시큼합니다. 파운잇은 밝은 녹색이며 단맛보다는 짭짤한 맛이 납니다. 네온 핑크색의 루프노바도 풍부하며, 솜사탕처럼 맛이 납니다. 마지막으로, 옅은 오렌지색을 띠는 글로울이라는 과일은 신맛과 쓴맛이 매우 강하며 산성이고 부식성이 있습니다.

--- AI를 프로그래밍 할 수 있을까? (2) --------------------------------------------------------
아래 내용을 CSV 형식으로 출력하세요.
제 이름은 홍길동입니다. 저는 현재 프롬프트 엔지니어링 수업을 듣고 있습니다.

--- AI를 프로그래밍 할 수 있을까? (3) --------------------------------------------------------
아래 내용을 CSV 형식으로 출력하세요. 컬럼을 이름, 역할, 수업으로 합니다.
제 이름은 홍길동입니다. 저는 현재 프롬프트 엔지니어링 수업을 듣고 있습니다.

--- AI를 프로그래밍 할 수 있을까? (4) --------------------------------------------------------
내가 입력하는 내용 외에도, 내가 요청한 CSV 형식에 맞는 추가 예시를 생성하세요.
제 이름은 홍길동입니다. 저는 현재 인공지능 특강을 듣고 있습니다.

--- 여행 계획 (A) --------------------------------------------------------------
여행 계획 애플리케이션을 만들려고 합니다. 저는 제 여행에 관해 설명하고 당신은 제가 지나갈 장소에서 할 수 있는 흥미로운 일을 나열합니다. 각 장소에서 며칠 동안 머무를 것인지 알려드리고 가능한 여정을 나열하겠습니다.
제 경로를 설명하기 위해 속기 표기법를 사용하겠습니다.
'뉴욕,3->파리,2'는 뉴욕에서 파리로 이동하고 뉴욕에서 3일, 파리에서 2일을 머문다는 뜻입니다.

--- 여행 계획 (A-1) --------------------------------------------------------------
서울,0->오사카,2->교토,1

--- 여행 계획 (A-2) --------------------------------------------------------------
런던,2->파리,4->로마,5->마드리드,3

--- 여행 계획 (B) --------------------------------------------------------------
기능을 추가하려고 합니다. 출발지와 도착지를 알려주면 출발지와 도착지 사이에 경유할 장소를 포함한 전체 경유지 목록을 제공합니다.

--- 여행 계획 (B-1) --------------------------------------------------------------
뉴욕,0->…->…->시카고,3

--- 여행 계획 (B-2) --------------------------------------------------------------
런던,1->…->프라하,2

--- 개요 확장하기 -------------------------------------------------------------------
개요 확장자 역할을 하세요. 제가 입력한 내용을 바탕으로 글머리 번호 개요를 생성한 다음, 어떤 글머리 번호를 확장할지 물어봅니다. 제가 선택한 글머리 번호에 대한 새로운 개요를 만듭니다. 마지막에는 다음에 확장할 글머리 기호를 물어보세요.

지구 온난화의 위험성

--- 액션 메뉴 만들기 -----------------------------------------------------------------
내가 입력한 내용을 바탕으로 글머리 번호 개요를 생성한 다음, 어떤 글머리 번호를 확장할지 물어봅니다. 내가 선택한 글머리 번호에 대한 새로운 개요를 만듭니다. 내가 "<글머리 번호> 글쓰기"라고 입력하면, 선택한 글머리 번호 <글머리 번호>에 대한 내용을 작성합니다. 최소한 3단락 이상의 내용을 작성합니다. 내가 "<글머리 번호>"만 입력하면, 해당 글머리 기호를 확장합니다. 마지막에는 다음 작업을 물어보세요.

지구 온난화의 위험성

--- 사실 확인 ---------------------------------------------------------------------
내가 입력한 내용을 바탕으로 글머리 번호 개요를 생성한 다음, 어떤 글머리 번호를 확장할지 물어봅니다. 내가 선택한 글머리 번호에 대한 새로운 개요를 만듭니다. 내가 "<글머리 번호> 글쓰기"라고 입력하면, 선택한 글머리 번호 <글머리 번호>에 대한 내용을 작성합니다. 최소한 3단락 이상의 내용을 작성합니다. 내가 "<글머리 번호>"만 입력하면, 해당 글머리 기호를 확장합니다. 텍스트를 출력할 때마다 결과물에 포함할 사실 세트 생성합니다. 사실 세트는 결과물의 끝에 삽입해야 합니다. 사실 세트는 사실 중 하나라도 틀릴 경우 결과물의 진실성을 약화시킬 수 있는 근본적인 사실이어야 합니다. 마지막에는 다음 작업을 물어보세요.

지구 온난화의 위험성

--- 역 프롬프트 --------------------------------------------------------------------
https://singjupost.com/steve-jobs-how-to-live-before-you-die-2005-speech-full-transcript/
이 글을 읽고 이러한 글을 만들 수 있는 프롬프트를 작성해주세요.

--- 대안 접근 방식 요청하기 ----------------------------------------------------------
지금부터 같은 작업을 수행할 수 있는 다른 방법이 있다면 가장 좋은 대안을 나열하세요. 대안을 비교하고 대조한 다음 어떤 방법을 사용할지 물어보세요.

데이터에 결측치(missing value)가 있어서 분석이나 모델링 전에 처리해야 해요.

--- 시멘틱 필터링 -------------------------------------------------------------------
다음 내용을 필터링하여 개인 식별이 가능한 정보 또는 개인을 재식별하는 데 사용될 수 있는 정보를 제거합니다. 정보를 제거한 후 최소한의 수정으로 내용을 자연스럽게 만듭니다.

강감찬은 서울특별시 강남구 테헤란로에 위치한 한 회사에서 근무하고 있으며, 연락처는 010-1234-5678이다. 회사 내에서 중요한 역할을 맡고 있어 업무상 다양한 프로젝트를 이끌고 있다. 이순신은 부산광역시 해운대구에 거주하며, 현재 창업을 준비하고 있다. 그와 연락하려면 010-9876-5432로 연락할 수 있다. 또한, 유관순은 대전광역시 서구 둔산동에서 중소기업을 운영하고 있으며, 개인 이메일 주소로는 yoo.gwansoon@example.com이 사용된다. 이 세 사람은 최근 진행된 공동 프로젝트에서 협업하며 각자의 전문성을 발휘하여 성공적으로 업무를 마무리했다.

--- 사고의 나무: Tree of Thoughts (ToT) ㅡ 1 단계 ---------------
1 단계:
{인간의 화성 이주}와 관련된 문제가 있습니다. 이 문제를 해결할 수 있는 세 가지 방법을 생각해 주세요.
또한, {지구와 화성 사이의 거리가 매우 멀기 때문에 정기적인 재보급이 어렵다}도 함께 고려해 주세요.
대답:

--- 사고의 나무: Tree of Thoughts (ToT) ㅡ 2 단계 ---------------
2 단계:
제안한 세 가지 해결 방법이 얼마나 좋은지 평가해 봅니다. 각 방법의 좋은 점과 아쉬운 점, 처음 시작할 때 얼마나 힘든지, 실제로 해내는 것이 어려운지, 문제가 생길 가능성이 있는지, 그리고 어떤 결과가 나올지를 생각합니다. 이런 점들을 바탕으로 각 방법이 성공할 가능성과 믿을 만한 정도를 계산합니다.
{세 가지 해결책}
대답:

--- 사고의 나무: Tree of Thoughts (ToT) - 3 단계 ---------------
3단계: 
각 해결책에 대해 사고 과정을 더욱 깊이 고민해 주세요. 잠재적인 시나리오, 실행 전략, 필요한 협력 관계나 자원, 예상되는 장애물을 극복할 수 있는 방법을 생각해 보시기 바랍니다. 또한, 예상치 못한 결과가 발생할 가능성과 그에 대한 대응 방법도 함께 고려해 주세요.
{검토 결과}
대답: 

--- 사고의 나무: Tree of Thoughts (ToT) - 4 단계 ---------------
4단계: 
평가와 시나리오를 바탕으로 실현 가능성이 높은 순서대로 해결책의 우선순위를 정해 주세요. 각 순위를 결정한 근거를 제시하고, 각 해결책에 대한 최종적인 의견이나 추가로 고려해야 할 사항을 제안해 주세요.
{깊은 사고 과정}
대답: 

--- 코드 프롬프트: 코드 작성 ------------------------------------------------------------
아래 내용을 파이썬 코드로 작성한다.

<내용>
주어진 판매 데이터를 기반으로 월별 매출 추세를 분석하고, 향후 6개월간의 매출을 예측하는 파이썬 코드를 작성하시오. 이를 위해 다음을 수행합니다.
1. CSV 파일에서 데이터를 불러오고, 월별로 집계된 매출 데이터를 생성합니다.
2. Pandas 및 Matplotlib 라이브러리를 사용해 월별 매출 추세를 시각화합니다.
3. ARIMA 또는 Prophet 모델을 사용해 향후 6개월간 매출을 예측하는 코드를 작성합니다.
4. 각 단계에 대한 설명과 함께 결과물을 시각화하여 출력합니다.
</내용>

--- Reason and Act (ReAct) ----------------------------------------------------
주어진 질문에 답하십시오. 당신은 검색에 접근할 수 있습니다.

다음 형식을 사용합니다.
Question : 답변해야 하는 입력 질문
Thought : 당신은 무엇을 해야 할지 항상 생각해야 합니다.
Action : 구체적으로 검색합니다.
Action Input : 검색 키워드를 알려주세요.
Observation : 액션(action)을 수행 한 결과를 요약하세요.
... (이 Thought/Action/Action Input/Observation을 최소한 2회 이상 반복 해야 합니다.)
Thought : 나는 이제 최종 답을 알고 있습니다.
Final Answer : 원래 입력 질문에 대한 최종 답변

한국에서 유명한 대학 마인크래프트 서버가 있다던데, 그 서버에 대한 소개를 보고서 형태로 작성해주세요. Web Pilot을 이용하세요.

<<텍스트 프롬프트: 챗봇>>
--- 영어 회화 챗봇 ------------------------------------------------------------------
당신은 영어 회화 파트너입니다. 사용자가 대화 연습을 원하는 주제나 상황을 알려주면, 그에 맞는 영어 대화를 시작해주세요. 영어로 말한 뒤 영어의 뜻을 괄호 안에 적어주세요. 만일 사용자의 영어가 부적절하거나 더 나은 표현이 있다면 어떻게 영어로 표현하는지 가르쳐주세요. 그리고 사용자가 영어로 대답을 못하고 한국어로 대답하면 그 대답을 어떻게 영어로 할 수 있는지 알려주세요. 당신의 모든 설명은 한국어로 하세요.

--- 영어 단어 공부 챗봇 ---------------------------------------------------------------
당신은 영어 단어를 재미있고 효과적으로 배울 수 있도록 도와주는 친근하고 격려하는 영어 선생님입니다. 

# 지침
1. 먼저 사용자 정보를 파악합니다.
- **나이**: 연령에 따라 이야기의 난이도와 주제를 조정합니다.
- **어휘 수준**: 초급, 중급, 고급에 따라 사용하는 단어의 난이도를 맞춥니다.
- **관심사**: 동물, 모험, 판타지, 스포츠 등 사용자가 좋아하는 주제를 반영합니다.
2. 사용자의 수준에 맞는 영어 단어 하나를 선택한 후 사용자에게 해당 영어 단어의 뜻을 물어봅니다.
- 사용자의 답이 틀리면 해당 단어의 **뜻**과 **발음**을 간단히 설명합니다.
- 사용자의 정답이 맞다면 칭찬을 하고 해당 단어의 **뜻**과 **발음**을 간단히 설명합니다.
3. 해당 단어의 뜻을 설명한 후, 이 단어와 관련이 있는 문장과 재미있는 짧은 이야기를 알려줍니다.
- 해당 단어를 포함한 문장 3개를 만들어 보여주고, 그 뜻을 설명합니다.
- 그 다음, 해당 단어와 관련된 재미 있는 이야기를 3-5 문장으로 만들어 보여줍니다.
4. 마지막 단계로 해당 단어가 어떤 상황에서 사용할 수 있는지 퀴즈를 통해 사용자에게 물어봅니다.
- 사용자의 대답에 따라 적절하게 대답하세요.
5. (2), (3), (4) 단계를 마치면 새로운 단어를 공부할지 물어봅니다.
당신의 모든 설명은 한국어로 하세요.

--- 한식당 챗봇 --------------------------------------------------------------------
당신은 한식당을 위한 자동 주문봇입니다. 먼저 고객에게 인사를 한 뒤 메뉴를 보여줍니다. 음식 메뉴는 다음과 같습니다.
[메인 메뉴]
- 불고기 15,000원
- 비빔밥 10,000원
- 김치찌개 8,000원
- 해물파전 12,000원
- 잡채 9,000원
[추가 옵션]
- 계란 1,000원
- 두부 1,500원
- 고기 3,000원
- 해산물 4,000원
- 고추장 500원
- 김치 1,000원
[음료]
- 콜라 / 사이다  2,000원
고객으로부터 주문을 받으면 먼저 주문한 음식이 메뉴에 있는지 확인합니다.  메뉴에 있는 음식이면, 주문 내역을 고객에게 요약하고, 고객이 추가로 주문할 것이 있는지 최종 확인합니다. 메뉴에서 항목을 구별할 수 있도록 모든 옵션 및 추가 사항 등을 명확히 해야 합니다. 
최종 확인 시, 고객이 주문한 메뉴와 해당 메뉴의 가격을 다시 확인하여  오류가 없는지 검토하세요. 메뉴 가격이나 최종 합계 계산이 틀렸다면 수정 후 총 합계를 고객에게 알려줍니다.
최종 주문을 확인 한 후 고객에게 픽업인지 배달인지 묻습니다. 배달인 경우 주소를 묻습니다. 마지막으로 결제를 진행합니다. 결제 방식으로는 현금 결제, 신용카드 결제, 모바일 결제가 있습니다. 이 중 고객이 원하는 결제 방식으로 결제를 처리합니다. 대화식이고 친근한 스타일로 간단하게 대답합니다.

<<이미지 프롬프트>>
--- 이미지 인식 (1) --------------------------------------------------------------------
이미지를 보이는 대로 설명하세요.

--- 이미지 인식 (2) --------------------------------------------------------------------
이 식물은 어떤 종류인가요? 한 단락으로 설명하세요.

--- 이미지 인식 (3) --------------------------------------------------------------------
이 개 품종은 무엇인가요? 한 단락에 글머리 기호로 설명하세요.

--- 이미지 인식 (4) --------------------------------------------------------------------
이 개 품종은 무엇인가요? 한 단락에 글머리 기호로 설명하세요.

--- 이 이미지에 어떤 문제가 있나요? ----------------------------------------------------
이게 무슨 문제인가요? 좋은 숫자는 무엇이어야 하나요?

--- 영수증 분석 --------------------------------------------------------------------
영수증에 표시된 총 청구 금액은 얼마인가요?

--- 영수증 분석 (2) --------------------------------------------------------------------
모든 영수증의 총 청구 금액은 얼마인가요?

--- 영수증 분석 (3) --------------------------------------------------------------------
생선회는 총 몇 개 구입했나요?
생선회 총 청구 금액은 얼마인가요?
구입한 쇠고기의 총 금액은 얼마인가요?
어떤 야채를 구입했나요? 금액은 얼마인가요?
세금은 총 얼마인가요?

--- 영양 분석 ---------------------------------------------------------------------
다이어트 중이에요. 어떤 음료를 마셔야 할까요?

쉽게 비교할 수 있도록 두 음료의 영양 성분을 JSON 형식으로 만드세요.

--- 다이어그램 분석 및 코드 생성 ----------------------------------------------------------
이 다이어그램의 흐름을 텍스트로 요약한 다음, 흐름을 구현하는 파이썬 프로그램을 작성하세요.

--- 데이터 변환 ----------------------------------------------------------------------
차트를 Markdown 테이블로 변환합니다.

차트를 HTML 테이블로 변환합니다.

--- 냉장고 음식으로 요리하기 -------------------------------------------------------------
냉장고에는 무엇이 있나요? 어떤 종류의 음식을 만들 수 있나요? 냉장고에 있는 재료만을 기준으로 두 가지 예를 보여주세요.

냉장고에 바나나가 있나요? 어디에 있나요?

--- 수학 문제 채점 ------------------------------------------------------------------
학생의 수학 숙제에서 각 답을 주의 깊게 확인하고, 먼저 계산을 한 다음, 결과를 학생의 답과 비교하고, 각 답에 정답 또는 오답을 표시한 다음, 마지막으로 모든 문제에 대한 총점을 반환하세요.

<<동영상 프롬프트>>
--- 동영상 이해 --------------------------------------------------------------------
이 동영상에 대한 설명을 주세요.

이 동영상에 대한 설명을 주세요.
    """
    
    # 카테고리와 프롬프트 제목, 내용을 분리
    categories = defaultdict(list)
    current_category = None
    
    lines = data.strip().split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        # 카테고리 추출
        category_match = re.match(r'<<(.+)>>', line)
        if category_match:
            current_category = category_match.group(1).strip()
            i += 1
            continue
        
        # 프롬프트 제목 추출 (패턴: --- 뒤에 제목과 구분선)
        title_match = re.match(r'--- (.+?) -+', line)
        if title_match and current_category:
            title = title_match.group(1).strip()
            content_lines = [line]  # 제목 라인 포함
            j = i + 1
            # 다음 프롬프트 제목 또는 카테고리 라인까지 내용 수집
            while j < len(lines):
                next_line = lines[j]
                if re.match(r'--- .+? -+', next_line) or re.match(r'<<.+>>', next_line):
                    break
                content_lines.append(next_line)
                j += 1
            content = '\n'.join(content_lines)
            categories[current_category].append({
                'title': title,
                'content': content
            })
            i = j
        else:
            i += 1
    
    return categories

# 비밀번호 확인
def check_password():
    """
    사용자가 입력한 비밀번호를 확인합니다.
    정확한 비밀번호가 입력되면 True를 반환합니다.
    """
    if 'password_verified' not in st.session_state:
        st.session_state.password_verified = False
    
    if st.session_state.password_verified:
        return True
    
    # 웹사이트 제목과 설명 추가
    st.title("실습 프롬프트")
    st.markdown("프롬프트 엔지니어링 학습을 위한 실습 프롬프트")
    
    password_input = st.text_input(
        "비밀번호를 입력하세요:", 
        type="password",
        help="프롬프트 모음을 보기 위한 비밀번호를 입력하세요."
    )
    
    if password_input == PASSWORD:
        st.session_state.password_verified = True
        return True
    elif password_input:
        st.error("비밀번호가 일치하지 않습니다.")
    
    return False

# 프롬프트 표시
def display_prompts():
    """
    카테고리와 프롬프트를 표시합니다.
    """
    # 데이터 준비
    categories = prepare_data()
    
    # 사이드바 설정
    st.sidebar.title("목차")
    
    # 카테고리별 메뉴
    for category, prompts in categories.items():
        st.sidebar.subheader(category)
        for prompt in prompts:
            title = prompt['title']
            # 링크의 앵커를 고유하게 만들기 위해 카테고리도 포함
            anchor = f"{category.replace(' ', '-')}-{title.replace(' ', '-')}"
            st.sidebar.markdown(f"- [{title}](#{anchor})")
    
    # 메인 콘텐츠
    st.title("실습 프롬프트")
    st.markdown("---")
    
    # 카테고리별 프롬프트 표시
    for category, prompts in categories.items():
        st.header(category)
        for prompt in prompts:
            title = prompt['title']
            content = prompt['content']
            
            # 고유한 앵커 생성
            anchor = f"{category.replace(' ', '-')}-{title.replace(' ', '-')}"
            
            # 제목 라인을 제외한 나머지 내용 추출
            content_lines = content.split('\n')
            actual_content = '\n'.join(content_lines[1:]).strip()
            
            # 앵커 포인트 추가
            st.markdown(f"<a name='{anchor}'></a>", unsafe_allow_html=True)
            st.subheader(title)
            st.markdown("```\n" + actual_content + "\n```")
            st.markdown("---")

# 메인 애플리케이션
def main():
    """
    애플리케이션의 메인 기능입니다.
    """
    if check_password():
        display_prompts()

if __name__ == "__main__":
    main()
