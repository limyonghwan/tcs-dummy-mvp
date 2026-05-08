import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="TCS 입문형 스캔",
    page_icon="⏳",
    layout="centered"
)

# -----------------------------
# 더미 문항 데이터
# 실제 TCS 문항이 아니라 시연용 샘플 문항
# -----------------------------
questions = [
    {
        "id": "Q1",
        "text": "해야 할 일을 알고 있어도 바로 시작하지 못할 때가 있다.",
        "tags": ["DELAY"]
    },
    {
        "id": "Q2",
        "text": "중요한 일을 앞두면 덜 중요한 일을 먼저 처리할 때가 있다.",
        "tags": ["DELAY", "AVOID"]
    },
    {
        "id": "Q3",
        "text": "외부 알림이나 자극 때문에 작업 흐름이 자주 끊긴다.",
        "tags": ["INTRUSION"]
    },
    {
        "id": "Q4",
        "text": "미룬 뒤 자책이 커져 다시 시작하기 어려워질 때가 있다.",
        "tags": ["SHAME_LOOP"]
    },
    {
        "id": "Q5",
        "text": "목표는 분명하지만 오늘 무엇부터 해야 할지 흐려질 때가 있다.",
        "tags": ["ANCHOR_GAP"]
    },
    {
        "id": "Q6",
        "text": "일을 시작하기 전에 준비나 계획을 너무 오래 붙잡을 때가 있다.",
        "tags": ["DELAY", "AVOID"]
    },
    {
        "id": "Q7",
        "text": "중요한 일을 하려 할수록 부담이 커져 다른 자극을 찾게 된다.",
        "tags": ["AVOID", "INTRUSION"]
    },
    {
        "id": "Q8",
        "text": "하루가 끝난 뒤 시간을 제대로 쓰지 못했다는 느낌이 자주 남는다.",
        "tags": ["SHAME_LOOP", "ANCHOR_GAP"]
    },
    {
        "id": "Q9",
        "text": "해야 할 일보다 당장 편한 선택을 먼저 하게 될 때가 있다.",
        "tags": ["AVOID"]
    },
    {
        "id": "Q10",
        "text": "중요한 목표가 있어도 실제 하루의 선택은 그 목표와 어긋날 때가 있다.",
        "tags": ["ANCHOR_GAP"]
    },
]

tag_labels = {
    "DELAY": "시작 지연",
    "AVOID": "회피",
    "INTRUSION": "외부자극 이탈",
    "SHAME_LOOP": "자책 반복",
    "ANCHOR_GAP": "목표-행동 불일치"
}

reports = {
    "TYPE_A": {
        "name": "미루기-자책 반복형",
        "summary": "시작 지연과 자책 반복 신호가 함께 나타났습니다.",
        "interpretation": (
            "이 패턴은 해야 할 일을 모르는 상태라기보다, 중요한 일을 앞둔 순간 부담이 커지고 "
            "그 부담을 피하려는 선택이 반복되는 흐름에 가깝습니다. 이후 미뤘다는 자책이 다시 실행력을 낮추면서 "
            "다음 시작을 더 어렵게 만들 수 있습니다."
        ),
        "actions": [
            "오늘은 목표 전체를 끝내려 하지 말고, 작업 파일을 열고 3분만 시작해보세요.",
            "작업을 끝내는 것이 아니라 ‘시작 흔적’을 남기는 것을 목표로 해보세요.",
            "자책 문장을 줄이고, 다음 행동 하나만 정리해보세요."
        ]
    },
    "TYPE_B": {
        "name": "외부자극 이탈형",
        "summary": "외부 알림과 자극에 의해 실행 흐름이 끊기는 신호가 나타났습니다.",
        "interpretation": (
            "이 패턴은 의지가 약해서라기보다, 집중이 형성되기 전에 외부 자극이 시간의 방향을 바꾸는 흐름에 가깝습니다. "
            "중요한 것은 더 오래 버티는 것이 아니라, 시작 전 자극을 줄이는 환경을 만드는 것입니다."
        ),
        "actions": [
            "20분 동안 알림을 끄고 한 가지 작업 화면만 열어두세요.",
            "작업 전 스마트폰을 손이 닿지 않는 곳에 두세요.",
            "작업 시작 전 사용할 앱과 닫을 앱을 먼저 정하세요."
        ]
    },
    "TYPE_C": {
        "name": "회피성 시작지연형",
        "summary": "중요한 일을 앞두고 회피와 시작 지연이 함께 나타나는 흐름이 보입니다.",
        "interpretation": (
            "이 패턴은 일이 중요할수록 부담이 커지고, 그 부담을 낮추기 위해 다른 일을 먼저 선택하는 구조에 가깝습니다. "
            "작업의 크기를 줄이지 않으면 시작 자체가 계속 무거워질 수 있습니다."
        ),
        "actions": [
            "가장 중요한 작업을 5분 단위로 쪼개보세요.",
            "완성 목표가 아니라 첫 행동 목표를 정하세요.",
            "‘오늘 끝내기’ 대신 ‘오늘 시작하기’로 기준을 낮춰보세요."
        ]
    },
    "TYPE_D": {
        "name": "목표혼선형",
        "summary": "목표와 실제 오늘의 행동 사이에 간극이 나타나는 흐름이 보입니다.",
        "interpretation": (
            "이 패턴은 목표가 없는 것이 아니라, 목표가 오늘의 첫 행동으로 충분히 번역되지 않은 상태에 가깝습니다. "
            "큰 방향보다 지금 바로 시작할 수 있는 한 가지 행동을 정하는 것이 중요합니다."
        ),
        "actions": [
            "오늘의 목표를 하나만 고르세요.",
            "그 목표를 위한 첫 행동을 10분 안에 끝낼 수 있는 형태로 줄이세요.",
            "하루가 끝나기 전 ‘내일 첫 행동’을 한 줄로 적어두세요."
        ]
    },
    "TYPE_E": {
        "name": "일반 실행 흔들림형",
        "summary": "특정 신호가 압도적으로 높다기보다 여러 실행 흔들림이 분산되어 나타났습니다.",
        "interpretation": (
            "현재 응답에서는 하나의 원인이 강하게 고정되어 있다기보다, 상황에 따라 시작 지연, 회피, 외부 자극, 목표 혼선이 "
            "번갈아 나타날 가능성이 있습니다. 이 경우 가장 먼저 확인할 것은 ‘내가 가장 자주 무너지는 시간대’입니다."
        ),
        "actions": [
            "오늘 하루 중 가장 자주 흐름이 끊기는 시간대를 기록해보세요.",
            "그 시간대에 반복되는 자극이나 감정을 하나만 적어보세요.",
            "내일 같은 시간대에 사용할 작은 방어 규칙을 정해보세요."
        ]
    }
}


def decide_type(top_tags):
    tag_set = set(top_tags)

    if {"DELAY", "SHAME_LOOP"}.issubset(tag_set):
        return "TYPE_A"

    if {"INTRUSION", "ANCHOR_GAP"}.issubset(tag_set):
        return "TYPE_B"

    if {"DELAY", "AVOID"}.issubset(tag_set):
        return "TYPE_C"

    if "ANCHOR_GAP" in tag_set:
        return "TYPE_D"

    return "TYPE_E"


def calculate_result(answers):
    tag_scores = {
        "DELAY": 0,
        "AVOID": 0,
        "INTRUSION": 0,
        "SHAME_LOOP": 0,
        "ANCHOR_GAP": 0
    }

    for q in questions:
        score = answers[q["id"]]
        for tag in q["tags"]:
            tag_scores[tag] += score

    sorted_tags = sorted(tag_scores.items(), key=lambda x: x[1], reverse=True)
    top_tags = [sorted_tags[0][0], sorted_tags[1][0]]
    result_type = decide_type(top_tags)

    return tag_scores, top_tags, result_type


# -----------------------------
# 화면
# -----------------------------
st.title("TCS 입문형 스캔")
st.caption("Time Choice Structure · 더미 MVP 테스트 버전")

st.write(
    "계획은 세우지만 실행에서 반복적으로 이탈한다면, "
    "당신의 시간 선택 구조가 어디서 흔들리는지 가볍게 확인해보세요."
)

st.info(
    "이 버전은 시장 반응과 리포트 흐름을 확인하기 위한 더미 MVP입니다. "
    "실제 TCS의 전체 문항, 가중치, 유형 판정표는 포함되어 있지 않습니다."
)

st.divider()

with st.form("scan_form"):
    st.subheader("문항 응답")
    st.write("각 문항에 대해 0점에서 10점 사이로 응답해주세요.")

    answers = {}

    for q in questions:
        answers[q["id"]] = st.slider(
            q["text"],
            min_value=0,
            max_value=10,
            value=5,
            step=1
        )

    submitted = st.form_submit_button("결과 보기")

if submitted:
    tag_scores, top_tags, result_type = calculate_result(answers)
    report = reports[result_type]

    st.session_state["result_ready"] = True
    st.session_state["tag_scores"] = tag_scores
    st.session_state["top_tags"] = top_tags
    st.session_state["result_type"] = result_type
    st.session_state["report"] = report
    st.session_state["answers"] = answers

if st.session_state.get("result_ready"):
    tag_scores = st.session_state["tag_scores"]
    top_tags = st.session_state["top_tags"]
    result_type = st.session_state["result_type"]
    report = st.session_state["report"]

    st.divider()
    st.subheader("결과 리포트")
    st.markdown(f"## {report['name']}")
    st.write(report["summary"])

    st.markdown("### 주요 신호")
    st.write(f"1순위 신호: **{tag_labels[top_tags[0]]}**")
    st.write(f"2순위 신호: **{tag_labels[top_tags[1]]}**")

    st.markdown("### 해석")
    st.write(report["interpretation"])

    st.markdown("### 오늘의 실행 규칙")
    for idx, action in enumerate(report["actions"], start=1):
        st.success(f"{idx}. {action}")

    st.markdown("### 다음 단계")
    st.info(
        "현재 결과는 입문형 스캔입니다. 정식 진단에서는 우선순위 충돌, 회피 반응, "
        "스트레스 반응, 자기보고 신뢰도 등을 함께 확인할 수 있습니다."
    )

    with st.expander("더미 계산 결과 보기"):
        st.write("태그별 점수")
        for tag, score in tag_scores.items():
            st.write(f"{tag_labels[tag]}: {score}")

    st.divider()
    st.subheader("테스트 피드백")

    st.write(
        "아래 질문에 답한 뒤, 생성된 피드백 요약을 복사해서 전달해주세요. "
        "현재 버전은 응답을 서버에 저장하지 않습니다."
    )

    with st.form("feedback_form"):
        fit_score = st.slider("1. 결과가 본인과 얼마나 맞는 것 같았나요?", 0, 10, 5)
        best_part = st.text_input("2. 어떤 부분이 가장 와닿았나요?")
        unclear_part = st.text_input("3. 애매하거나 안 맞는 문장이 있었나요?")
        want_more = st.radio("4. 결과를 보고 더 자세히 알고 싶다는 생각이 들었나요?", ["그렇다", "아니다", "잘 모르겠다"])
        want_full = st.radio("5. 정식 진단이 있다면 해볼 의향이 있나요?", ["그렇다", "아니다", "조건부로 있다"])
        paid_condition = st.text_area("6. 유료라면 어떤 조건에서 돈을 낼 것 같나요?")

        feedback_submitted = st.form_submit_button("피드백 요약 만들기")

    if feedback_submitted:
        feedback_text = f"""
[TCS 더미 MVP 테스트 피드백]
테스트 일시: {datetime.now().strftime("%Y-%m-%d %H:%M")}
결과 유형: {report["name"]}
1순위 신호: {tag_labels[top_tags[0]]}
2순위 신호: {tag_labels[top_tags[1]]}

1. 결과 공감도: {fit_score}/10
2. 가장 와닿은 부분: {best_part}
3. 애매하거나 안 맞는 문장: {unclear_part}
4. 더 자세히 알고 싶은가: {want_more}
5. 정식 진단 의향: {want_full}
6. 유료 결제 조건: {paid_condition}
"""
        st.markdown("### 복사용 피드백 요약")
        st.code(feedback_text, language="text")

        st.download_button(
            label="피드백 TXT 다운로드",
            data=feedback_text,
            file_name="tcs_feedback.txt",
            mime="text/plain"
        )
