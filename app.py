import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="TCS 입문형 스캔",
    page_icon="⏳",
    layout="centered"
)

# -----------------------------
# 1. 더미 문항 데이터
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
        "tags": ["OVERPLAN", "DELAY"]
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
    {
        "id": "Q11",
        "text": "무엇을 해야 할지 알지만, 시작하기 전에 마음이 먼저 지쳐버릴 때가 있다.",
        "tags": ["BURNOUT", "DELAY"]
    },
    {
        "id": "Q12",
        "text": "일을 잘하고 싶다는 마음 때문에 오히려 시작이 늦어질 때가 있다.",
        "tags": ["OVERPLAN", "AVOID"]
    },
    {
        "id": "Q13",
        "text": "작업을 시작해도 중간에 흐름을 잃고 다시 돌아오기 어려울 때가 있다.",
        "tags": ["INTRUSION", "BURNOUT"]
    },
    {
        "id": "Q14",
        "text": "오늘의 선택이 장기 목표와 이어져 있다는 감각이 약해질 때가 있다.",
        "tags": ["ANCHOR_GAP", "BURNOUT"]
    },
    {
        "id": "Q15",
        "text": "실패할 것 같다는 생각 때문에 시작 전에 머뭇거릴 때가 있다.",
        "tags": ["AVOID", "SHAME_LOOP"]
    },
]

tag_labels = {
    "DELAY": "시작 지연",
    "AVOID": "회피",
    "INTRUSION": "외부자극 이탈",
    "SHAME_LOOP": "자책 반복",
    "ANCHOR_GAP": "목표-행동 불일치",
    "OVERPLAN": "과잉 준비",
    "BURNOUT": "에너지 저하"
}

# -----------------------------
# 2. 리포트 템플릿
# -----------------------------
reports = {
    "TYPE_A": {
        "name": "미루기-자책 반복형",
        "summary": "시작 지연과 자책 반복 신호가 함께 나타났습니다.",
        "interpretation": "이 패턴은 해야 할 일을 모르는 상태라기보다, 중요한 일을 앞둔 순간 부담이 커지고 그 부담을 피하려는 선택이 반복되는 흐름에 가깝습니다. 이후 미뤘다는 자책이 다시 실행력을 낮추면서 다음 시작을 더 어렵게 만들 수 있습니다.",
        "actions": [
            "오늘은 목표 전체를 끝내려 하지 말고, 작업 파일을 열고 3분만 시작해보세요.",
            "작업을 끝내는 것이 아니라 ‘시작 흔적’을 남기는 것을 목표로 해보세요.",
            "자책 문장을 줄이고, 다음 행동 하나만 정리해보세요."
        ]
    },
    "TYPE_B": {
        "name": "외부자극 이탈형",
        "summary": "외부 알림과 자극에 의해 실행 흐름이 끊기는 신호가 나타났습니다.",
        "interpretation": "이 패턴은 의지가 약해서라기보다, 집중이 형성되기 전에 외부 자극이 시간의 방향을 바꾸는 흐름에 가깝습니다. 중요한 것은 더 오래 버티는 것이 아니라, 시작 전 자극을 줄이는 환경을 만드는 것입니다.",
        "actions": [
            "20분 동안 알림을 끄고 한 가지 작업 화면만 열어두세요.",
            "작업 전 스마트폰을 손이 닿지 않는 곳에 두세요.",
            "작업 시작 전 사용할 앱과 닫을 앱을 먼저 정하세요."
        ]
    },
    "TYPE_C": {
        "name": "회피성 시작지연형",
        "summary": "중요한 일을 앞두고 회피와 시작 지연이 함께 나타나는 흐름이 보입니다.",
        "interpretation": "이 패턴은 일이 중요할수록 부담이 커지고, 그 부담을 낮추기 위해 다른 일을 먼저 선택하는 구조에 가깝습니다. 작업의 크기를 줄이지 않으면 시작 자체가 계속 무거워질 수 있습니다.",
        "actions": [
            "가장 중요한 작업을 5분 단위로 쪼개보세요.",
            "완성 목표가 아니라 첫 행동 목표를 정하세요.",
            "‘오늘 끝내기’ 대신 ‘오늘 시작하기’로 기준을 낮춰보세요."
        ]
    },
    "TYPE_D": {
        "name": "목표혼선형",
        "summary": "목표와 실제 오늘의 행동 사이에 간극이 나타나는 흐름이 보입니다.",
        "interpretation": "이 패턴은 목표가 없는 것이 아니라, 목표가 오늘의 첫 행동으로 충분히 번역되지 않은 상태에 가깝습니다. 큰 방향보다 지금 바로 시작할 수 있는 한 가지 행동을 정하는 것이 중요합니다.",
        "actions": [
            "오늘의 목표를 하나만 고르세요.",
            "그 목표를 위한 첫 행동을 10분 안에 끝낼 수 있는 형태로 줄이세요.",
            "하루가 끝나기 전 ‘내일 첫 행동’을 한 줄로 적어두세요."
        ]
    },
    "TYPE_E": {
        "name": "과잉준비-시작지연형",
        "summary": "준비와 계획이 오히려 시작을 늦추는 흐름이 나타났습니다.",
        "interpretation": "이 패턴은 무계획이라기보다, 잘하고 싶다는 마음이 강해져 시작 전 준비 단계가 길어지는 구조에 가깝습니다. 계획은 실행을 돕기 위한 것이지만, 어느 순간 실행을 미루는 안전지대가 될 수 있습니다.",
        "actions": [
            "계획을 더 세우기 전에 바로 실행할 수 있는 3분짜리 행동을 하나 정하세요.",
            "완벽한 준비 기준을 낮추고, 초안부터 만들어보세요.",
            "오늘은 계획 문서가 아니라 결과물의 흔적을 하나 남겨보세요."
        ]
    },
    "TYPE_F": {
        "name": "에너지저하-흐름상실형",
        "summary": "실행 의지는 있지만 에너지 저하로 흐름이 쉽게 끊기는 신호가 나타났습니다.",
        "interpretation": "이 패턴은 목표 의식이 없어서가 아니라, 시작과 유지에 필요한 에너지가 충분히 회복되지 않은 상태에 가깝습니다. 이 경우 더 강한 압박보다 회복 가능한 작은 리듬을 만드는 것이 중요합니다.",
        "actions": [
            "오늘은 긴 작업보다 10분 안에 끝나는 작은 단위 하나만 정하세요.",
            "작업 전 몸의 피로도를 먼저 확인하고, 무리한 계획을 줄이세요.",
            "실행 실패를 의지 부족으로 해석하지 말고, 회복 조건을 먼저 점검하세요."
        ]
    },
    "TYPE_G": {
        "name": "자기압박-회피형",
        "summary": "잘해야 한다는 압박이 회피와 지연으로 이어지는 흐름이 나타났습니다.",
        "interpretation": "이 패턴은 게으름보다는 자기 기준이 높아질수록 시작의 부담이 커지는 구조에 가깝습니다. 실패 가능성을 줄이려는 마음이 오히려 첫 행동을 늦출 수 있습니다.",
        "actions": [
            "오늘의 기준을 ‘잘하기’가 아니라 ‘작게 제출하기’로 바꿔보세요.",
            "실패해도 괜찮은 초안 하나를 먼저 만들어보세요.",
            "평가받을 결과물이 아니라 연습용 결과물을 만든다고 생각해보세요."
        ]
    },
    "TYPE_H": {
        "name": "분산형 실행흔들림형",
        "summary": "하나의 원인보다 여러 실행 흔들림이 분산되어 나타났습니다.",
        "interpretation": "현재 응답에서는 하나의 원인이 압도적으로 강하다기보다, 상황에 따라 시작 지연, 회피, 외부 자극, 목표 혼선이 번갈아 나타날 가능성이 있습니다. 이 경우 먼저 반복되는 시간대와 환경을 확인하는 것이 좋습니다.",
        "actions": [
            "오늘 하루 중 가장 자주 흐름이 끊기는 시간대를 기록해보세요.",
            "그 시간대에 반복되는 자극이나 감정을 하나만 적어보세요.",
            "내일 같은 시간대에 사용할 작은 방어 규칙을 정해보세요."
        ]
    },
    "TYPE_I": {
        "name": "비교적 안정형",
        "summary": "현재 응답에서는 특정 실행 이탈 신호가 강하게 나타나지 않았습니다.",
        "interpretation": "현재 흐름은 비교적 안정적으로 보입니다. 다만 특정 상황이나 피로가 누적될 때 외부 자극, 목표 혼선, 시작 지연이 나타날 수 있으므로 자신의 약한 조건을 미리 확인하는 것이 좋습니다.",
        "actions": [
            "현재 잘 유지되는 실행 조건을 한 가지 기록해보세요.",
            "흐름이 무너지는 상황이 있다면 시간대와 환경을 함께 적어보세요.",
            "좋은 흐름이 생긴 날의 첫 행동을 반복 가능한 규칙으로 만들어보세요."
        ]
    }
}


# -----------------------------
# 3. 계산 함수
# -----------------------------
def get_strength(score):
    if score >= 8:
        return "강함"
    if score >= 5.5:
        return "중간"
    if score >= 3:
        return "약함"
    return "낮음"


def calculate_result(answers):
    tag_totals = {tag: 0 for tag in tag_labels}
    tag_counts = {tag: 0 for tag in tag_labels}

    for q in questions:
        score = answers[q["id"]]
        for tag in q["tags"]:
            tag_totals[tag] += score
            tag_counts[tag] += 1

    # 태그별 문항 수가 다르므로 평균 점수로 보정
    tag_scores = {}
    for tag in tag_labels:
        if tag_counts[tag] == 0:
            tag_scores[tag] = 0
        else:
            tag_scores[tag] = round(tag_totals[tag] / tag_counts[tag], 2)

    sorted_tags = sorted(tag_scores.items(), key=lambda x: x[1], reverse=True)
    top_tags = [sorted_tags[0][0], sorted_tags[1][0], sorted_tags[2][0]]

    result_type = decide_type(tag_scores, top_tags)

    return tag_scores, top_tags, result_type


def decide_type(tag_scores, top_tags):
    top1, top2, top3 = top_tags
    top_set = set(top_tags[:2])
    max_score = tag_scores[top1]
    score_gap = tag_scores[top1] - tag_scores[top3]

    # 전체 신호가 낮은 경우
    if max_score < 4:
        return "TYPE_I"

    # 상위 3개가 촘촘하면 분산형
    if score_gap < 1.0 and max_score < 8:
        return "TYPE_H"

    if {"DELAY", "SHAME_LOOP"}.issubset(top_set):
        return "TYPE_A"

    if {"INTRUSION", "ANCHOR_GAP"}.issubset(top_set):
        return "TYPE_B"

    if {"DELAY", "AVOID"}.issubset(top_set):
        return "TYPE_C"

    if {"OVERPLAN", "DELAY"}.issubset(top_set) or {"OVERPLAN", "AVOID"}.issubset(top_set):
        return "TYPE_E"

    if {"BURNOUT", "DELAY"}.issubset(top_set) or {"BURNOUT", "ANCHOR_GAP"}.issubset(top_set):
        return "TYPE_F"

    if {"AVOID", "SHAME_LOOP"}.issubset(top_set):
        return "TYPE_G"

    if "ANCHOR_GAP" in top_set:
        return "TYPE_D"

    return "TYPE_H"


# -----------------------------
# 4. 화면
# -----------------------------
st.title("TCS 입문형 스캔")
st.caption("Time Choice Structure · 초기 데모 버전")

st.write(
    "계획은 세우지만 실행에서 반복적으로 이탈한다면, "
    "당신의 시간 선택 구조가 어디서 흔들리는지 가볍게 확인해보세요."
)

st.warning(
    "**주의 사항**\n\n"
    "이 버전은 TCS 검사 초기 데모 버전입니다.\n\n"
    "실제 검사 단계의 전체 문항과 해석은 최종 버전과는 많이 다를 수 있습니다."
)

st.divider()

with st.form("scan_form"):
    st.subheader("문항 응답")
    st.write("각 문항에 대해 0점에서 10점 사이로 응답해주세요.")

    answers = {}

for idx, q in enumerate(questions, start=1):
    answers[q["id"]] = st.slider(
        f"{idx}. {q['text']}",
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
    report = st.session_state["report"]

    strength_words = {}

    for tag in top_tags:
        strength = get_strength(tag_scores[tag])

        if strength == "강함":
            strength_words[tag] = "강하게 나타남"
        elif strength == "중간":
            strength_words[tag] = "중간 이상으로 나타남"
        elif strength == "약함":
            strength_words[tag] = "약하게 나타남"
        else:
            strength_words[tag] = "낮게 나타남"

    primary_tag = top_tags[0]
    secondary_tag = top_tags[1]
    third_tag = top_tags[2]

    primary_label = tag_labels[primary_tag]
    secondary_label = tag_labels[secondary_tag]
    third_label = tag_labels[third_tag]

    pair_key = tuple(top_tags[:2])

    flow_patterns = {
        ("DELAY", "SHAME_LOOP"): (
            "현재 응답 흐름에서는 시작이 늦어지고, 늦어진 시간에 대한 자책이 다시 다음 시작을 무겁게 만드는 흐름이 보입니다. "
            "해야 할 일을 모르는 것이 아니라, 시작 전의 부담과 시작 후의 자책이 서로 이어지며 시간을 붙잡는 구조에 가깝습니다."
        ),
        ("SHAME_LOOP", "DELAY"): (
            "현재 응답 흐름에서는 자책이 먼저 크게 남고, 그 감정이 다음 시작을 더 늦추는 흐름이 보입니다. "
            "이 경우 중요한 것은 더 강하게 몰아붙이는 것이 아니라, 자책이 시작을 막기 전에 첫 행동을 작게 만드는 것입니다."
        ),
        ("DELAY", "AVOID"): (
            "현재 응답 흐름에서는 중요한 일을 앞둔 순간 첫 행동이 늦어지고, 부담을 낮추기 위해 다른 선택으로 돌아서는 흐름이 보입니다. "
            "일을 하기 싫다기보다, 시작 직전의 압력이 다른 선택을 끌어당기는 구조에 가깝습니다."
        ),
        ("AVOID", "DELAY"): (
            "현재 응답 흐름에서는 부담을 피하려는 선택이 먼저 나타나고, 그 결과 시작이 뒤로 밀리는 흐름이 보입니다. "
            "이 경우 시간은 사라진다기보다, 당장의 편안함을 선택하는 쪽으로 방향을 바꾸는 모습에 가깝습니다."
        ),
        ("INTRUSION", "ANCHOR_GAP"): (
            "현재 응답 흐름에서는 목표의 방향은 존재하지만, 외부 자극이 오늘의 선택을 다른 곳으로 끌고 가는 모습이 보입니다. "
            "집중력이 없는 것이 아니라, 시간의 방향이 외부 신호에 의해 자주 재배치되는 흐름에 가깝습니다."
        ),
        ("ANCHOR_GAP", "INTRUSION"): (
            "현재 응답 흐름에서는 장기 목표와 오늘의 선택 사이에 간극이 생기고, 그 틈으로 외부 자극이 쉽게 들어오는 모습이 보입니다. "
            "큰 목표는 있지만 그것이 오늘의 첫 행동으로 충분히 고정되지 않은 상태에 가깝습니다."
        ),
        ("OVERPLAN", "DELAY"): (
            "현재 응답 흐름에서는 준비와 정리가 길어지면서 첫 행동이 뒤로 밀리는 흐름이 보입니다. "
            "무계획이 문제가 아니라, 더 잘하고 싶다는 마음이 실행 이전의 준비 단계에 오래 머무르게 하는 구조에 가깝습니다."
        ),
        ("DELAY", "OVERPLAN"): (
            "현재 응답 흐름에서는 시작이 늦어지는 과정에서 계획과 준비가 안전한 머무름의 공간처럼 작동하는 모습이 보입니다. "
            "계획은 필요하지만, 어느 순간 실행을 미루는 이유가 될 수 있습니다."
        ),
        ("BURNOUT", "DELAY"): (
            "현재 응답 흐름에서는 해야 한다는 인식은 있지만, 에너지 저하로 인해 시작선 앞에서 멈추는 모습이 보입니다. "
            "이 경우 더 강한 의지보다 회복 가능한 작은 실행 리듬이 먼저 필요할 수 있습니다."
        ),
        ("DELAY", "BURNOUT"): (
            "현재 응답 흐름에서는 시작이 늦어지는 이유가 단순한 회피라기보다, 실행을 지속할 에너지가 충분히 올라오지 않는 상태와 연결되어 보입니다. "
            "작업의 크기를 줄이고 회복 조건을 함께 확인하는 것이 중요합니다."
        ),
        ("AVOID", "SHAME_LOOP"): (
            "현재 응답 흐름에서는 부담을 피하려는 선택이 뒤늦은 자책과 연결되는 모습이 보입니다. "
            "당장의 회피는 마음을 잠시 가볍게 하지만, 시간이 지난 뒤 다시 자신을 압박하는 방향으로 돌아올 수 있습니다."
        ),
        ("SHAME_LOOP", "AVOID"): (
            "현재 응답 흐름에서는 자책이 쌓이면서 다음 선택에서 다시 회피가 강화되는 모습이 보입니다. "
            "이 경우 자책을 줄이는 것이 단순한 위로가 아니라, 다음 실행을 가능하게 만드는 조건이 됩니다."
        ),
    }

    flow_text = flow_patterns.get(
        pair_key,
        (
            f"현재 응답 흐름에서는 {primary_label} 신호가 가장 먼저 드러나고, "
            f"그 뒤에 {secondary_label} 신호가 겹쳐지는 모습이 보입니다. "
            f"여기에 {third_label} 신호가 보조적으로 붙으면서, 오늘의 시간 선택이 한 방향으로 고정되기보다 "
            "상황에 따라 흔들리는 흐름으로 읽힙니다."
        )
    )

    st.divider()
    st.subheader("결과 리포트")
    st.markdown(f"## {report['name']}")
    st.write(report["summary"])

    st.markdown("### 주요 신호")
    for idx, tag in enumerate(top_tags, start=1):
        st.write(
            f"{idx}순위 신호: **{tag_labels[tag]}** / {strength_words[tag]}"
        )

    st.markdown("### 해석")
    st.write(report["interpretation"])

    st.markdown("### 오늘의 실행 규칙")
    for idx, action in enumerate(report["actions"], start=1):
        st.success(f"{idx}. {action}")

    st.markdown("### 선택 결과 계산 추정도")

    with st.expander("내 응답이 어떤 시간 선택 흐름으로 읽혔는지 보기"):
        st.caption(
            "이 영역은 내부 계산표가 아니라, 현재 응답 흐름을 사람이 읽을 수 있는 문장으로 바꾼 참고 해석입니다."
        )

        st.write(f"가장 먼저 드러난 선택 흐름은 **{primary_label}**입니다.")
        st.write(f"그다음으로 겹쳐진 흐름은 **{secondary_label}**입니다.")
        st.write(f"보조적으로 함께 감지된 흐름은 **{third_label}**입니다.")

        st.info(flow_text)

        st.write(
            "즉, 이 결과는 단순히 점수를 합산한 결론이라기보다, "
            "당신이 해야 할 일 앞에서 어떤 식으로 시간을 선택하고, 어디서 방향이 흔들리며, "
            "어떤 감정이나 자극이 그 선택에 영향을 주는지를 문장으로 추정한 것입니다."
        )

    st.markdown("### 결과 읽는 법")
    st.info(
        "이 결과는 현재 응답에서 가장 두드러진 시간 선택 신호를 바탕으로 만든 입문형 리포트입니다. "
        "정식 진단에서는 더 많은 문항과 검증 문항을 통해 우선순위 충돌, 회피 반응, 스트레스 반응, "
        "자기보고 신뢰도 등을 함께 확인할 수 있습니다."
    )

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
[TCS 초기 데모 테스트 피드백]
테스트 일시: {datetime.now().strftime("%Y-%m-%d %H:%M")}
결과 유형: {report["name"]}
1순위 신호: {primary_label} / {strength_words[primary_tag]}
2순위 신호: {secondary_label} / {strength_words[secondary_tag]}
3순위 신호: {third_label} / {strength_words[third_tag]}

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
