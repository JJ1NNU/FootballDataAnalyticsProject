"""Revise the proposal deck: keep slides 1-2 of the user's edited file as they are,
replace everything from slide 3 on.

Usage: python3 docs/slides/revise_deck.py <user_edited.pptx> [out.pptx]
"""
import os, sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "figures")
FONT = "Malgun Gothic"
INK, MUTED, RED, BLUE, LIGHT, LINE = "22262B", "5A6169", "C0392B", "1F5FA8", "F3F5F7", "C5CBD2"
W, M = 13.333, 0.6


def rgb(h):
    return RGBColor.from_string(h)


def drop_slides_from(prs, keep):
    ids = prs.slides._sldIdLst
    for sld in list(ids)[keep:]:
        prs.part.drop_rel(sld.rId)
        ids.remove(sld)


def new_slide(prs, dark=False):
    s = prs.slides.add_slide(prs.slide_layouts[0])
    for ph in list(s.placeholders):
        ph._element.getparent().remove(ph._element)
    if dark:
        s.background.fill.solid(); s.background.fill.fore_color.rgb = rgb("111418")
    return s


def text(s, runs, x, y, w, h, size=16, color=INK, bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    """runs: str, or list of paragraphs; a paragraph is str or (str, {size,color,bold}) or a list of such runs."""
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    paras = runs if isinstance(runs, list) else [runs]
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        items = para if isinstance(para, list) else [para]
        for it in items:
            t, o = (it, {}) if isinstance(it, str) else it
            r = p.add_run(); r.text = t
            f = r.font; f.name = FONT; f.size = Pt(o.get("size", size)); f.bold = o.get("bold", bold)
            f.color.rgb = rgb(o.get("color", color))
        if "space" in (items[-1][1] if not isinstance(items[-1], str) else {}):
            p.space_after = Pt(items[-1][1]["space"])
    return tb


def title(s, t, sub=None):
    text(s, t, M, 0.35, W - 2 * M, 0.8, size=28, bold=True)
    if sub:
        text(s, sub, M, 1.1, W - 2 * M, 0.45, size=16, color=MUTED)


def rect(s, x, y, w, h, fill="FFFFFF", line=LINE, rounded=True, width=1.25):
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    if rounded:
        sh.adjustments[0] = 0.06
    sh.fill.solid(); sh.fill.fore_color.rgb = rgb(fill)
    if line:
        sh.line.color.rgb = rgb(line); sh.line.width = Pt(width)
    else:
        sh.line.fill.background()
    sh.shadow.inherit = False
    sh.text_frame.text = ""
    return sh


def card(s, head, body, x, y, w, h, color=INK, head_size=17, body_size=14):
    rect(s, x, y, w, h, line=color)
    text(s, [(head, {"size": head_size, "bold": True, "color": color, "space": 4}), (body, {"size": body_size, "color": MUTED})],
         x + 0.2, y + 0.15, w - 0.4, h - 0.3, anchor=MSO_ANCHOR.MIDDLE)


def arrow_down(s, x, y):
    a = s.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(x), Inches(y), Inches(0.5), Inches(0.4))
    a.fill.solid(); a.fill.fore_color.rgb = rgb("8A9199"); a.line.fill.background(); a.shadow.inherit = False


def table(s, rows, x, y, w, col_w, size=12, row_h=0.5, head_fill="EEF1F4"):
    t = s.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y), Inches(w), Inches(row_h * len(rows))).table
    for j, cw in enumerate(col_w):
        t.columns[j].width = Inches(cw)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = t.cell(i, j); c.text = ""
            c.fill.solid(); c.fill.fore_color.rgb = rgb(head_fill if i == 0 else "FFFFFF")
            c.margin_left = c.margin_right = Inches(0.08); c.margin_top = c.margin_bottom = Inches(0.05)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = c.text_frame.paragraphs[0]; r = p.add_run(); r.text = val
            r.font.name = FONT; r.font.size = Pt(size); r.font.bold = (i == 0 or j == 0)
            r.font.color.rgb = rgb(INK)
    return t


NOTES_BODY = None  # body placeholder copied from an existing notes page (the notes master has none)


def notes(s, t):
    import copy
    ns = s.notes_slide
    if ns.notes_text_frame is None and NOTES_BODY is not None:
        ns.shapes._spTree.append(copy.deepcopy(NOTES_BODY))
    ns.notes_text_frame.text = t


def build(src, out):
    prs = Presentation(src)
    global NOTES_BODY
    first = prs.slides[0].notes_slide
    NOTES_BODY = next(sh._element for sh in first.placeholders if sh.placeholder_format.type == 2)  # BODY
    drop_slides_from(prs, 2)

    # 3 연구 질문과 선행연구
    s = new_slide(prs)
    title(s, "연구 질문: 몇 분, 몇 골 차부터 골키퍼 가담이 손해인가")
    text(s, "세부 질문", M, 1.55, 6.6, 0.45, size=18, bold=True)
    card(s, "① 득점 확률 증가", "골키퍼 1명 추가 시 코너킥 득점 확률 변화", M, 2.1, 6.6, 1.15, color=BLUE)
    card(s, "② 실점 확률 증가", "골문을 비운 상태의 역습 실점 확률 변화", M, 3.45, 6.6, 1.15, color=RED)
    card(s, "③ 판정", "남은 시간 · 점수차 · 대회 형태(리그/토너먼트)별 골키퍼 가담의 이득 여부", M, 4.8, 6.6, 1.15)
    rect(s, 7.6, 1.55, 5.13, 4.4, fill=LIGHT, line=None)
    text(s, [("선행연구", {"size": 18, "bold": True, "space": 10}),
             ("학술 연구 없음", {"size": 30, "bold": True, "color": RED, "space": 14}),
             ("블로그 분석 1편 (American Soccer Analysis, 2018)", {"size": 15, "bold": True, "space": 4}),
             ("역습 위험 2배 이하 → 이득, 4배 이상 → 손해라는 손익분기 계산", {"size": 14, "color": MUTED, "space": 4}),
             ("단, 역습 위험 배수는 측정 없이 가정", {"size": 14, "color": MUTED, "space": 14}),
             ("→ 본 프로젝트: 해당 수치의 데이터 기반 측정", {"size": 16, "bold": True})],
         7.9, 1.8, 4.6, 4.0)
    notes(s, "선행연구 조사 결과 학술 논문은 찾지 못했다. 유일한 정량 분석은 American Soccer Analysis(2018) 블로그로, 골키퍼가 언제 골문을 비웠는지 데이터가 없어 역습 위험 배수를 가정했다.\n"
             "말로 덧붙일 점: 1골 뒤진 채 리그 경기의 마지막 코너라면 실점해도 승점은 어차피 0점이므로 올리는 것이 당연하다. 시간이 남아 있으면 실점이 남은 시간의 동점 기회까지 없애므로, 진짜 질문은 '언제부터 손해인가'다.\n"
             "(질문 대비) 아이스하키에서는 골리를 빼는 전략을 시뮬레이터로 연구했고(Beaudoin & Swartz 2010), 이후 NHL 팀들이 더 일찍 골리를 빼기 시작했다. 본 프로젝트의 방법론적 전례.")

    # 4 데이터와 60건
    s = new_slide(prs)
    title(s, "공개 데이터 전체 탐색, 골키퍼 가담 후보 60건")
    funnel = [
        ("탐색 범위", "StatsBomb 공개 데이터 전체(80개 대회·시즌) + Wyscout 공개 데이터 + 트래킹 27경기", "5,902경기", 9.0),
        ("코너킥", "탐색 범위 내 모든 코너킥", "58,115개", 8.2),
        ("골키퍼 가담 후보", "80분 이후 · 동점 또는 열세 · 골키퍼 상대 진영 진입 (영상 검증 예정)", "60건", 7.4),
        ("결과", "후보 60건의 코너 직후 결과", "득점 1 · 실점 5", 6.6),
    ]
    for i, (h, b, n, w) in enumerate(funnel):
        y = 1.55 + i * 1.3
        rect(s, M, y, w, 1.1, fill="FFFFFF" if i < 3 else "FBEDEB", line=LINE if i < 3 else RED)
        text(s, [(h, {"size": 15, "bold": True, "space": 2}), (b, {"size": 12, "color": MUTED})], M + 0.25, y + 0.12, w - 3.2, 0.9, anchor=MSO_ANCHOR.MIDDLE)
        text(s, n, M + w - 2.95, y + 0.12, 2.75, 0.86, size=22, bold=True, color=RED if i >= 2 else INK, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
    rect(s, 10.0, 1.55, 2.73, 2.5, fill=LIGHT, line=None)
    text(s, [("골키퍼 가담 vs 비가담", {"size": 16, "bold": True, "space": 4}), ("직접 비교 불가", {"size": 24, "bold": True, "color": RED, "space": 8}),
             ("득점 1건으로는 득점 확률 추정 불가", {"size": 13, "color": MUTED})], 10.2, 1.75, 2.33, 2.1, anchor=MSO_ANCHOR.MIDDLE)
    notes(s, "접근 가능한 공개 데이터를 모두 모았다: StatsBomb 공개 데이터 80개 대회·시즌 전부, Wyscout 공개 데이터, Sportec·SkillCorner 트래킹.\n"
             "그 안의 코너킥 58,115개 중 골키퍼가 올라간 것으로 보이는 경우는 60건뿐이고, 득점은 1건, 실점은 5건이다. 60건은 자동 탐지된 후보로, 영상으로 확인할 예정이다.\n"
             "'이 정도로는 골키퍼를 올렸을 때와 안 올렸을 때를 직접 비교할 수 없습니다. 그래서 확률을 나누어 추정합니다.'\n"
             "(질문 대비) 탐지 방법: 스냅사진 속 골키퍼 위치, 골키퍼의 상대 진영 공 관여, 역습 슈팅 순간 골키퍼 위치. 마지막 방법은 실점한 경우만 잡히는 편향이 있어 학습에는 쓰지 않는다.")

    # 5 방법 구조
    s = new_slide(prs)
    title(s, "방법: 세 가지 확률 추정 후 비교")
    cw = (W - 2 * M - 0.6) / 3
    blocks = [("① 코너킥 득점 모델", "골키퍼 가담 시\n코너킥 득점 확률 증가분", BLUE),
              ("② 역습 실점 모델", "골키퍼 가담 시\n역습 실점 확률 증가분", RED),
              ("③ 남은 시간 득점 모델", "남은 시간 동안\n양 팀의 득점 확률", INK)]
    for i, (h, b, c) in enumerate(blocks):
        card(s, h, b, M + i * (cw + 0.3), 1.55, cw, 1.7, color=c, head_size=18, body_size=15)
    arrow_down(s, W / 2 - 0.25, 3.4)
    rect(s, M, 3.95, W - 2 * M, 2.0, line=INK, width=1.75)
    text(s, [("④ 판정 모델", {"size": 18, "bold": True, "space": 8}),
             [("득점 확률 증가 × 득점 시 이득", {"size": 17, "bold": True, "color": BLUE}), ("     vs     ", {"size": 17, "color": MUTED}),
              ("실점 확률 증가 × 실점 시 손해", {"size": 17, "bold": True, "color": RED})],
             ("남은 시간의 득점 가능성까지 반영, 경기 종료 시점부터 역산", {"size": 14, "color": MUTED, "space": 2}),
             ("출력: 상황(남은 시간 × 점수차 × 대회 형태)별 골키퍼 가담 이득 확률", {"size": 14, "color": MUTED})],
         M + 0.3, 4.1, W - 2 * M - 0.6, 1.75, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, "실제 가담 사례 60건: 학습 제외, 최종 결과 점검에만 사용", M, 6.2, W - 2 * M, 0.4, size=15, bold=True)
    notes(s, "골키퍼 가담 장면 자체는 60건뿐이지만, 이를 구성하는 세 확률은 각각 수천~수만 개 사례로 추정할 수 있다.\n"
             "①은 코너킥에서 공격수 한 명이 늘면 득점 확률이 얼마나 오르는지, ②는 골문이 비면 역습 실점 확률이 얼마나 오르는지, ③은 남은 시간 동안 골이 날 확률이다.\n"
             "④에서 세 값을 합쳐, 각 상황에서 골키퍼를 올렸을 때와 올리지 않았을 때 최종 기대 승점(리그) 또는 진출 확률(토너먼트)을 비교한다. 경기 종료 시점부터 거꾸로 계산하므로 '지금 실점하면 남은 시간에 만회할 기회가 사라진다'는 점이 자동으로 반영된다.\n"
             "실제 사례 60건은 일부가 실점 쪽으로 치우쳐 탐지되었기 때문에 학습에 쓰지 않는다.")

    # 6 모델별 입력·출력
    s = new_slide(prs)
    title(s, "모델별 입력 · 출력 · 추정 방법")
    rows = [
        ["모델", "입력 데이터", "출력", "골키퍼 가담 반영 방법", "검증"],
        ["① 코너킥 득점", "코너 순간 전체 선수 위치\n(스냅사진, 코너 2,468개)", "코너 직후 득점 기대값", "같은 장면에 공격수 1명 추가 시 예측값 차이", "박스 인원이 서로 다른 실제 코너 비교(인과 추정)"],
        ["② 역습 실점", "코너 실패 후 상대 공격(코너 58,115개)\n골키퍼가 골문에서 20m 이상 떨어진 슈팅(212개)\n트래킹 역습 속도(27경기)", "코너 직후 실점 확률", "상대 슈팅 확률 × 골키퍼 복귀 실패 확률 × 빈 골문 슈팅 득점 확률", "실제 막판 코너 실점률과 비교"],
        ["③ 남은 시간 득점", "약 5,900경기의 득점 · 퇴장 시각", "분 · 점수차별 득점 확률", "해당 없음(①②와 결합되는 공통 기반)", "실제 경기 결과 예측 정확도"],
    ]
    table(s, rows, M, 1.5, W - 2 * M, [1.7, 3.45, 1.9, 2.75, 2.33], size=12, row_h=1.0)
    text(s, "① 모델: 선수 간 관계를 반영하는 그래프 신경망 · ② 모델: 확률 3개를 각각 추정 후 곱셈 · ③ 모델: 시간대별 득점 빈도 모형", M, 6.2, W - 2 * M, 0.5, size=13, color=MUTED)
    notes(s, "① 핵심 아이디어: 코너 순간 선수 위치로 득점 기대값을 예측하는 모델을 만든 뒤, 같은 장면에 공격수 한 명(골키퍼)을 추가해 예측값이 얼마나 바뀌는지 본다. 이 값이 믿을 만한지는 실제로 박스 인원이 많았던 코너와 적었던 코너를, 상황을 통제한 채 비교하는 인과 추정 결과와 맞춰 확인한다.\n"
             "② 골키퍼가 올라갔다가 코너가 실패하면, 상대가 슈팅까지 갈 확률, 골키퍼가 제때 돌아오지 못할 확률, 빈 골문 슈팅이 들어갈 확률을 곱한다. 빈 골문 확률은 골키퍼가 골문에서 멀리 떨어져 있던 실제 슈팅 212개에서 추정한다.\n"
             "③ 남은 시간 동안 양 팀이 골을 넣을 확률. ①②의 값과 합쳐 판정 모델의 입력이 된다.\n"
             "(질문 대비) 모델 세부: 그래프 신경망(GATv2), 좌우 반전 데이터 증강, 경기 단위 교차검증, 이중 기계학습(DML), 포아송 득점 모형, 부트스트랩.")

    # 7 데이터 예시
    s = new_slide(prs)
    title(s, "입력 데이터 예시: 코너킥 순간 스냅사진")
    s.shapes.add_picture(os.path.join(FIG, "s6_360_frame.png"), Inches(M), Inches(1.3), height=Inches(5.9))
    items = [("스냅사진(StatsBomb 360)", "이벤트 순간 화면 안의 모든 선수 위치"),
             ("보유량", "코너킥 2,468개 — 골키퍼 가담 여부와 무관한 전체 코너"),
             ("예시 장면", "월드컵 2022 덴마크–호주 93분, 골키퍼가 올라간 드문 장면"),
             ("활용", "박스 안 공격 · 수비 인원, 골키퍼 위치 → 코너킥 득점 모델 입력"),
             ("골키퍼 가담 반영", "이 장면에 공격수 1명 추가 후 예측 득점 확률 변화 계산")]
    for i, (h, b) in enumerate(items):
        y = 1.55 + i * 1.0
        text(s, [(h, {"size": 16, "bold": True, "color": BLUE if i < 4 else RED, "space": 2}), (b, {"size": 14, "color": MUTED})], 5.6, y, 7.1, 0.9)
    notes(s, "스냅사진은 코너킥이 차지는 순간 화면에 보이는 모든 선수의 위치다. 회색 영역은 카메라에 잡힌 범위.\n"
             "2,468개는 골키퍼가 올라간 코너가 아니라, 스냅사진이 있는 코너킥 전체다. 이 예시는 골키퍼가 올라간 드문 장면을 골랐다.\n"
             "코너킥 득점 모델은 이런 장면을 입력으로 받아 득점 확률을 예측하고, 장면에 공격수 한 명을 더 넣었을 때의 예측 변화로 골키퍼 가담의 이득을 계산한다.")

    # 8 권장 지도 예시
    s = new_slide(prs)
    title(s, "최종 산출물: 골키퍼 가담 권장 지도", "칸 값 = 해당 상황에서 골키퍼 가담이 이득일 확률 (0~1)")
    tag = rect(s, 9.6, 0.45, 3.13, 0.55, fill="FBEDEB", line=RED)
    text(s, "예시 · 임의 값 (실제 결과 아님)", 9.7, 0.52, 2.93, 0.45, size=13, bold=True, color=RED, align=PP_ALIGN.CENTER)
    mins = ["80′", "85′", "88′", "90′", "92′", "95′+"]
    vals = {"0 (동점)": [.05, .05, .08, .10, .15, .25], "−1 (1골 열세)": [.10, .20, .35, .55, .75, .95], "−2 (2골 열세)": [.10, .15, .25, .35, .45, .55]}
    gx, gy, cw2, ch = M + 2.0, 2.0, 1.25, 1.0
    for r, (lab, row) in enumerate(vals.items()):
        text(s, lab, M, gy + r * ch + 0.32, 1.9, 0.4, size=14, color=MUTED)
        for c, v in enumerate(row):
            base = (255, 255, 255); tgt = (0x1F, 0x5F, 0xA8)
            col = "".join(f"{int(b + (t - b) * v):02X}" for b, t in zip(base, tgt))
            rect(s, gx + c * cw2, gy + r * ch, cw2 - 0.06, ch - 0.06, fill=col, line=LINE, rounded=False, width=0.75)
            text(s, f"{v:.2f}", gx + c * cw2, gy + r * ch + 0.3, cw2 - 0.06, 0.4, size=15, bold=True, color="FFFFFF" if v >= 0.5 else INK, align=PP_ALIGN.CENTER)
    for c, m in enumerate(mins):
        text(s, m, gx + c * cw2, gy + 3 * ch + 0.05, cw2 - 0.06, 0.35, size=13, color=MUTED, align=PP_ALIGN.CENTER)
    text(s, "경기 시간 →", gx, gy + 3 * ch + 0.4, 4, 0.35, size=13, color=MUTED)
    text(s, [("리그 경기 기준", {"size": 15, "bold": True, "space": 6}),
             ("토너먼트용 지도 별도 작성", {"size": 14, "color": MUTED, "space": 6}),
             ("실제 감독 선택을 지도 위에 표시해 권장과 비교", {"size": 14, "color": MUTED})],
         gx + 6 * cw2 + 0.3, 2.1, W - M - (gx + 6 * cw2 + 0.3), 2.6)
    notes(s, "이 표의 숫자는 형식을 보여 주기 위한 임의 값이다. 최종 발표에서는 실제 모델 결과로 채운다.\n"
             "읽는 법: 예를 들어 1골 뒤진 92분 코너에서 값이 0.75라면, 모델 불확실성을 고려했을 때 골키퍼를 올리는 쪽이 이득일 확률이 75%라는 뜻이다.\n"
             "같은 지도를 토너먼트(연장전·승부차기 반영)용으로도 만든다. 또한 실제 골키퍼 가담 사례와 가담하지 않은 막판 코너를 지도 위에 찍어, 감독들의 선택이 권장보다 보수적인지 확인한다.\n"
             "부산물: ASA(2018)가 가정한 역습 위험 배수의 실측값.")

    # 9 한계
    s = new_slide(prs)
    title(s, "본 실험의 한계와 대응")
    rows = [
        ["한계", "대응"],
        ["골키퍼 추가 효과: 실측이 아닌 모델 기반 추정", "실제 코너 간 박스 인원 차이를 이용한 인과 추정과 교차 검증"],
        ["골키퍼의 공중볼 · 마무리 능력: 일반 공격수와 차이", "능력 계수 범위 설정 후 민감도 분석"],
        ["빈 골문 실점 확률: 코너 외 상황(스위핑 · 1대1)에서 차용", "실제 가담 사례 60건의 실점 빈도와 비교 점검"],
        ["상대 팀의 대응 변화(수비 인원 증가 등): 데이터 부재로 미반영", "상대 대응 시나리오 별도 계산"],
        ["판정 경계: 득점 모델 가정(연장전 · 승부차기)에 따라 이동", "단일 값이 아닌 이득 확률로 결과 제시"],
        ["데이터 편중: 스냅사진 데이터의 국제대회 위주 구성", "대회 · 성별 구분 결과 제시"],
    ]
    table(s, rows, M, 1.5, W - 2 * M, [6.4, 5.73], size=14, row_h=0.7)
    notes(s, "앞의 모델별 표와 대응되는 한계다.\n"
             "가장 큰 한계는 첫째 줄: '같은 장면에 골키퍼만 더했다면'은 데이터에 없으므로 모델의 추정이다. 그래서 실제 코너들 사이의 박스 인원 차이로 같은 값을 따로 추정해 맞춰 본다.\n"
             "근거 수치(질문 대비): 막판 열세 코너 후 60초 실점률 1.81%, 95% 신뢰구간 1.28~2.56%로 폭이 2배. 빈 골문 슈팅 표본 212개.\n"
             "경계에서 먼 상황(예: 70분 2골 차, 95분 1골 차)은 높은 신뢰로 판정할 수 있고, 경계 근처는 1~2분 정도 불확실성이 남을 것으로 예상한다.")

    # 10 일정
    s = new_slide(prs)
    title(s, "일정")
    steps = [("완료", "데이터 수집 · 정제", "공개 데이터 5,902경기, 골키퍼 가담 후보 60건"),
             ("11/23", "중간 점검", "세 모델(코너킥 득점 · 역습 실점 · 남은 시간 득점) 완성"),
             ("12/14", "권장 지도 완성", "판정 모델, 감독 선택 비교, 민감도 분석"),
             ("12/21", "최종 발표", "권장 지도 기반 결론")]
    for i, (d, h, b) in enumerate(steps):
        x = M + i * 3.1
        rect(s, x, 2.0, 2.85, 3.2, fill="EAF1FA" if i == 0 else "FFFFFF", line=BLUE if i == 0 else LINE)
        text(s, [(d, {"size": 26, "bold": True, "color": BLUE if i == 0 else INK, "space": 10}), (h, {"size": 18, "bold": True, "space": 8}), (b, {"size": 14, "color": MUTED})],
             x + 0.25, 2.25, 2.35, 2.8)
    text(s, "중간 점검 대안: 그래프 신경망 결과와 인과 추정 결과 불일치 시 보수적 결과 채택", M, 5.7, W - 2 * M, 0.5, size=15, color=MUTED)
    notes(s, "데이터 수집과 정제는 이미 끝났다. 주 단위 세부 일정은 기획서 참고.")

    # 11 마무리
    s = new_slide(prs, dark=True)
    text(s, ["95분, 1골 뒤진 코너킥.", "골키퍼를 올리시겠습니까?"], M, 1.6, W - 2 * M, 2.2, size=40, bold=True, color="FFFFFF", align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, "그럼 90분이라면?", M, 4.1, W - 2 * M, 0.9, size=40, bold=True, color="F2B134", align=PP_ALIGN.CENTER)
    text(s, "12월 21일, 권장 지도로 답변", M, 5.5, W - 2 * M, 0.5, size=18, color="C9CED4", align=PP_ALIGN.CENTER)
    notes(s, "'95분이라면 아마 대부분 올린다고 답하실 겁니다. 앞에서 말씀드렸듯 그건 맞을 가능성이 높습니다. 그런데 90분이라면요?' → 최종 발표 예고 후 Q&A.")

    # 부록
    s = new_slide(prs)
    title(s, "부록: 질문 대비")
    apx = [("A1", "골키퍼 가담 탐지 방법과 편향", "스냅사진 속 골키퍼 위치 · 골키퍼의 상대 진영 공 관여 · 역습 슈팅 순간 골키퍼 위치. 마지막 방법은 실점한 경우만 탐지"),
           ("A2", "빈 골문 슈팅", "골키퍼가 골문에서 20~30m 떨어진 슈팅: 실제 득점이 기대득점의 1.64배 (n = 174)"),
           ("A3", "데이터 품질", "Wyscout 좌표 반전 이벤트, 스냅사진 골키퍼 라벨 오류, Sportec 결측 좌표 → 정제 완료"),
           ("A4", "모델 세부", "그래프 신경망(GATv2) + 좌우 반전 증강, 경기 단위 교차검증, 이중 기계학습(DML), 포아송 득점 모형, 부트스트랩"),
           ("A5", "동기 자료", "코너 후 60초 실점률: 전체 0.69% vs 85분 이후 열세 1.81% (95% 신뢰구간 1.28~2.56%)"),
           ("A6", "참고문헌", "Young(ASA) 2018 · Beaudoin & Swartz 2010 · Wang 외 2024(TacticAI) · Chernozhukov 외 2018 · Bassek 외 2025")]
    for i, (k, h, b) in enumerate(apx):
        y = 1.45 + i * 0.93
        text(s, k, M, y, 0.7, 0.4, size=18, bold=True, color=BLUE)
        text(s, h, M + 0.8, y, 3.4, 0.4, size=16, bold=True)
        text(s, b, M + 4.3, y, W - 2 * M - 4.3, 0.8, size=13, color=MUTED)
    notes(s, "발표하지 않는 슬라이드. 후보 60건 목록은 data/derived/gk_up_candidates.csv.")

    prs.save(out)
    print("saved", out, "slides:", len(prs.slides._sldIdLst))


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "gk_corner_proposal.pptx"))
