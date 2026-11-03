// Builds docs/slides/gk_corner_proposal.pptx (proposal talk, 12 slides + appendix).
// Usage: NODE_PATH=<dir with pptxgenjs> node docs/slides/build_deck.js
// Layout and text only; dashed boxes marked "직접 넣기" are for material to add by hand.
const path = require("path");
const pptxgen = require("pptxgenjs");

const FIG = path.join(__dirname, "figures");
const OUT = path.join(__dirname, "gk_corner_proposal.pptx");
const FONT = "Malgun Gothic";
const INK = "22262B", MUTED = "5A6169", RED = "C0392B", BLUE = "1F5FA8", LIGHT = "F3F5F7", LINE = "8A9199";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
pres.title = "골키퍼를 올릴 것인가";
pres.theme = { headFontFace: FONT, bodyFontFace: FONT };

const W = 13.33, M = 0.6;

function title(slide, text, sub) {
  slide.addText(text, { x: M, y: 0.35, w: W - 2 * M, h: 0.9, fontFace: FONT, fontSize: 30, bold: true, color: INK, margin: 0, isTextBox: true });
  if (sub) slide.addText(sub, { x: M, y: 1.2, w: W - 2 * M, h: 0.5, fontFace: FONT, fontSize: 16, color: MUTED, margin: 0, isTextBox: true });
}

function text(slide, t, o) {
  slide.addText(t, Object.assign({ fontFace: FONT, fontSize: 16, color: INK, margin: 0, valign: "top", isTextBox: true }, o));
}

function placeholder(slide, label, o) {
  slide.addShape(pres.shapes.RECTANGLE, Object.assign({ fill: { color: LIGHT }, line: { color: LINE, width: 1.25, dashType: "dash" } }, o));
  slide.addText("직접 넣기\n" + label, { x: o.x + 0.2, y: o.y + 0.2, w: o.w - 0.4, h: o.h - 0.4, fontFace: FONT, fontSize: 14, color: MUTED, align: "center", valign: "middle", margin: 0, isTextBox: true });
}

function box(slide, head, body, o, color) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, Object.assign({ fill: { color: "FFFFFF" }, line: { color: color || LINE, width: 1.5 }, rectRadius: 0.08 }, o));
  slide.addText([
    { text: head, options: { fontSize: 17, bold: true, color: color || INK, breakLine: true } },
    { text: body, options: { fontSize: 14, color: MUTED } },
  ], { x: o.x + 0.2, y: o.y + 0.15, w: o.w - 0.4, h: o.h - 0.3, fontFace: FONT, valign: "middle", margin: 0, isTextBox: true });
}

// S1 표지 + 투표
let s = pres.addSlide(); s.background = { color: "111418" };
text(s, "95분, 1골 뒤진 코너킥.\n골키퍼를 올리시겠습니까?", { x: M, y: 2.0, w: W - 2 * M, h: 2.2, fontSize: 44, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
text(s, "골키퍼를 올릴 것인가 — 경기 막판 코너킥 골키퍼 공격 가담의 효용과 최적 정책", { x: M, y: 5.2, w: W - 2 * M, h: 0.5, fontSize: 16, color: "C9CED4", align: "center" });
text(s, "[팀명] · [발표자] · 2026.[  ].[  ]", { x: M, y: 5.8, w: W - 2 * M, h: 0.4, fontSize: 14, color: "8A9199", align: "center" });
s.addNotes("청중에게 손을 들게 한다: 올린다 / 안 올린다. 결과를 대략 기억해 두었다가 마지막 슬라이드에서 언급한다.\n'감독들은 매주 이 결정을 내리는데, 축구에서는 아직 아무도 이걸 데이터로 답한 적이 없습니다. 오늘은 그 답을 어떻게 찾을지 말씀드리겠습니다.'");

// S2 같은 선택, 정반대 결과
s = pres.addSlide();
title(s, "같은 선택, 정반대 결과");
placeholder(s, "영상 ① 알리송 95분 헤더 결승골\n웨스트브롬 1-2 리버풀 (2021.05.16)\nyoutube.com/watch?v=CFXkwCtEzDQ (NBC Sports)\n10~15초로 자른 로컬 클립 권장", { x: M, y: 1.5, w: 5.8, h: 3.6 });
placeholder(s, "영상 ② 조지아 골키퍼 가담 → 90+7분 빈 골문 실점\n튀르키예 3-1 조지아 (유로 2024)\nyoutube.com/watch?v=f7JinPLrBOg (FOX Soccer)\n10~15초로 자른 로컬 클립 권장", { x: W - M - 5.8, y: 1.5, w: 5.8, h: 3.6 });
text(s, "무승부 → 승리  (+2점)", { x: M, y: 5.35, w: 5.8, h: 0.6, fontSize: 24, bold: true, color: BLUE, align: "center" });
text(s, "1골 차 패배 → 2골 차 패배", { x: W - M - 5.8, y: 5.35, w: 5.8, h: 0.6, fontSize: 24, bold: true, color: RED, align: "center" });
text(s, "영상 출처: NBC Sports, FOX Soccer (YouTube 공식 채널)", { x: M, y: 6.8, w: W - 2 * M, h: 0.3, fontSize: 10, color: MUTED });
s.addNotes("영상을 하나씩 순서대로 튼다(동시 재생 금지). 각 영상이 끝난 뒤 아래 한 줄이 나타나도록 애니메이션.\n① 1-1 동점, 95분 코너. 리버풀 골키퍼 알리송이 올라가 헤더로 결승골.\n② 1-2로 뒤진 추가시간. 조지아 골키퍼가 코너에 올라갔고, 클리어된 공이 그대로 역습이 되어 빈 골문에 실점.\n'결과만 보면 둘 다 그럴 수 있는 일입니다. 우리가 묻는 건 평균적으로 이득인가, 그리고 언제 이득인가입니다.'");

// S3 하키는 답했고 축구는 아직
s = pres.addSlide();
title(s, "하키는 답했고, 축구는 아직이다");
placeholder(s, "아이스하키에서 골리를 빼고\n빈 골문으로 경기하는 장면 사진 1장\n(출처 표기, 저작권 문제 시 아이콘으로 대체)", { x: M, y: 1.5, w: 5.4, h: 4.6 });
box(s, "아이스하키", "골리를 빼고 공격수를 넣는 전략을 오래 연구\n→ '감독들은 너무 늦게, 너무 드물게 뺀다'", { x: 6.5, y: 1.6, w: 6.2, h: 1.8 }, BLUE);
box(s, "축구", "블로그 분석 1편(ASA, 2018)\n그마저 핵심 숫자는 하키에서 빌려 와 가정", { x: 6.5, y: 3.7, w: 6.2, h: 1.8 }, RED);
text(s, "→ 우리는 그 숫자를 직접 잰다", { x: 6.5, y: 5.75, w: 6.2, h: 0.5, fontSize: 20, bold: true });
s.addNotes("하키 연구(Beaudoin & Swartz 2010, The American Statistician)는 경기 시뮬레이터로 최적 시점을 계산했고, 이후 NHL 팀들이 실제로 더 일찍 골리를 빼기 시작했다.\n축구에서는 American Soccer Analysis(2018) 블로그가 '역습 위험이 2배면 이득, 4배면 손해'까지 계산했지만, 골키퍼가 언제 골문을 비웠는지 데이터가 없어 그 배수를 하키에서 빌려 가정했다.\n'그 배수를 아무도 측정하지 않았습니다. 우리는 그걸 잽니다.'");

// S4 60건
s = pres.addSlide();
title(s, "왜 아무도 못 했나: 코너킥 58,115개 중 60건");
s.addImage({ path: path.join(FIG, "s4_corners_dots.png"), x: M, y: 1.45, w: 8.4, h: 5.55, altText: "회색 점 58,115개(코너킥) 중 빨간 점 60개(골키퍼 가담 추정)" });
text(s, [
  { text: "회색 점 하나 = 코너킥 하나", options: { fontSize: 16, color: MUTED, breakLine: true } },
  { text: "빨간 점 = 골키퍼가 올라간 코너", options: { fontSize: 16, color: RED, breakLine: true } },
  { text: " ", options: { fontSize: 12, breakLine: true } },
  { text: "득점 1 · 실점 5", options: { fontSize: 32, bold: true, color: INK, breakLine: true } },
  { text: " ", options: { fontSize: 12, breakLine: true } },
  { text: "→ 직접 비교로는 결론 불가", options: { fontSize: 20, bold: true, color: INK } },
], { x: 9.3, y: 2.2, w: 3.5, h: 4.0 });
text(s, "공개 데이터 5,902경기(StatsBomb + Wyscout). 빨간 점의 위치는 무작위 배치", { x: M, y: 7.0, w: 8.4, h: 0.3, fontSize: 10, color: MUTED });
s.addNotes("'골키퍼가 실제로 올라간 코너는 이만큼밖에 없고, 그중 골은 단 하나입니다. 올렸을 때와 안 올렸을 때를 직접 비교하면 아무 결론도 낼 수 없습니다. 그래서 질문을 쪼갰습니다.'\n(질문 대비: 60건은 세 가지 방법으로 자동 탐지 — 부록 A1)");

// S5 쪼개기
s = pres.addSlide();
title(s, "아이디어: 드문 사건을 흔한 사건으로 쪼갠다", "골키퍼가 올라간 장면은 60개뿐이지만, 각 부품은 수천~수만 번씩 일어난다");
box(s, "① 골키퍼 1명이 더해지면 골 확률이 얼마나 오르나", "코너킥 수만 개 + 선수 위치 스냅사진 2,468장", { x: M, y: 2.0, w: 5.9, h: 1.5 }, BLUE);
box(s, "② 골문이 비면 역습 실점이 몇 배가 되나", "코너 후 역습 수만 건 + 골키퍼가 골문을 비운 슈팅 212개 + 트래킹으로 잰 역습 속도", { x: W - M - 5.9, y: 2.0, w: 5.9, h: 1.5 }, RED);
box(s, "③ 남은 시간 동안 골이 날 확률", "약 5,900경기의 득점 시각 (남은 시간 · 점수차 · 홈/원정 · 리그/토너먼트)", { x: M, y: 3.85, w: W - 2 * M, h: 1.2 });
s.addShape(pres.shapes.DOWN_ARROW, { x: W / 2 - 0.3, y: 5.15, w: 0.6, h: 0.45, fill: { color: LINE }, line: { color: LINE } });
box(s, "④ 종료 휘슬부터 거꾸로 계산해서 '올릴까, 말까' 판정", "실제 사례 60건은 학습에 쓰지 않고, 결과가 말이 되는지 점검하는 데만 사용", { x: M, y: 5.7, w: W - 2 * M, h: 1.2 }, INK);
s.addNotes("클릭마다 블록이 하나씩 나타나도록 애니메이션(①→②→③→④).\n'골키퍼가 올라간 장면 자체는 드물지만, 그걸 이루는 부품은 흔합니다. 박스에 공격수가 몇 명이냐는 코너마다 다르고, 골키퍼가 골문을 비운 채 슈팅을 맞는 장면은 스위핑·1대1 등에서도 나옵니다.'\n하키 연구도 같은 방식(부품 확률 + 시뮬레이터)이었다고 한 문장.\n실제 사례 60건은 '역습 슈팅 장면에서 골키퍼가 멀리 있음'으로 찾은 것처럼 실점 쪽으로 치우친 경우가 있어서, 학습에 넣지 않는 편이 안전하다.");

// S6 스냅사진
s = pres.addSlide();
title(s, "데이터: 그 순간의 스냅사진");
s.addImage({ path: path.join(FIG, "s6_360_frame.png"), x: M, y: 1.35, w: 4.5, h: 5.85, altText: "월드컵 2022 덴마크–호주 93분 코너킥 순간 선수 위치. 덴마크 골키퍼가 상대 6야드 박스 앞에 있음" });
text(s, "월드컵 2022 덴마크–호주, 93분 코너킥 순간\n화면에 보이는 모든 선수의 위치 (회색 영역 = 카메라에 잡힌 범위)", { x: 5.6, y: 1.6, w: 7.1, h: 1.0, fontSize: 16, color: MUTED });
text(s, "이런 장면이 코너킥 2,468개에 있다", { x: 5.6, y: 2.9, w: 7.1, h: 0.6, fontSize: 24, bold: true });
s.addTable([
  [{ text: "데이터", options: { bold: true } }, { text: "규모", options: { bold: true } }, { text: "쓰임", options: { bold: true } }],
  ["StatsBomb", "3,961경기 · 코너 38,799", "코너 결과, 역습, 슈팅"],
  ["  └ 스냅사진(360)", "코너 2,468", "박스 배치, 골키퍼 위치"],
  ["Wyscout", "1,941경기 · 코너 19,316", "교차 검증"],
  ["트래킹(Sportec·SkillCorner)", "27경기 · 코너 156", "역습 속도, 골키퍼 위치"],
], { x: 5.6, y: 3.7, w: 7.1, colW: [2.5, 2.3, 2.3], fontFace: FONT, fontSize: 12, color: INK, border: { type: "solid", color: "D5DAE0", pt: 0.75 }, fill: { color: "FFFFFF" }, rowH: 0.42 });
text(s, "모두 공개 데이터, 수집·정제 완료", { x: 5.6, y: 6.75, w: 7.1, h: 0.4, fontSize: 14, color: MUTED });
s.addNotes("'이런 스냅사진에서 골키퍼가 어디 있었는지, 박스에 몇 명이 있었는지를 직접 셉니다. 이 장면에서는 덴마크 골키퍼가 상대 골문 바로 앞에 와 있습니다.'\n이 그림이 다음 슬라이드의 '선수 한 명 더 넣어 보기'를 이해하는 기반.\n데이터 정제 이야기는 하지 않는다(질문 시 부록 A3).");

// S7 보이는 것 / 안 보이는 것
s = pres.addSlide();
title(s, "이미 보이는 것, 아직 안 보이는 것");
text(s, "막판엔 역습 실점 위험 약 2.6배", { x: M, y: 1.4, w: 5.9, h: 0.5, fontSize: 20, bold: true, color: RED });
s.addImage({ path: path.join(FIG, "s7_concede_rate.png"), x: M, y: 1.95, w: 5.6, h: 4.3, altText: "코너 후 60초 안 실점률: 전체 0.69%, 85분 이후 지고 있을 때 1.81%, 95% 신뢰구간" });
text(s, "1명 더 넣은 효과? 단순 비교로는 구분 불가", { x: 6.85, y: 1.4, w: 5.9, h: 0.5, fontSize: 20, bold: true, color: BLUE });
s.addImage({ path: path.join(FIG, "s7_attackers_xg.png"), x: 6.85, y: 1.95, w: 5.6, h: 4.3, altText: "박스 안 공격 인원 4~7명별 코너 기대득점과 95% 신뢰구간, 구간이 서로 겹침" });
text(s, "오차막대 = 95% 신뢰구간 · StatsBomb 공개 데이터(오른쪽은 스냅사진이 있는 코너, 짧은 코너 제외)", { x: M, y: 6.6, w: W - 2 * M, h: 0.3, fontSize: 10, color: MUTED });
s.addNotes("왼쪽은 이미 확인된 사실: 코너 후 60초 안 실점률이 전체 0.69%에서 85분 이후 지고 있을 때 1.81%로, 신뢰구간이 겹치지 않는다.\n오른쪽은 아직 모르는 것: 박스 인원이 많을수록 조금 오르는 것처럼 보이지만 구간이 다 겹친다. 박스에 몇 명을 넣느냐는 상황마다 달라서(지고 있을수록 많이 넣고, 상대도 더 많이 막음) 단순 평균으로는 효과가 묻힌다.\n'그래서 장면 전체를 읽는 신경망으로 같은 장면에 선수 한 명만 더 넣어 보고, 그 답을 통계적 인과 추정으로 교차 검증합니다.'");

// S8 냅킨 계산
s = pres.addSlide();
title(s, "손으로 풀어 보기: 마지막 코너라면?");
text(s, "리그 경기 · 1골 뒤진 채 마지막 코너킥", { x: M, y: 1.45, w: W - 2 * M, h: 0.5, fontSize: 18, color: MUTED });
box(s, "올렸다가 골", "무승부 → +1점", { x: M, y: 2.15, w: 5.9, h: 1.4 }, BLUE);
box(s, "올렸다가 실점", "어차피 패배 → 0점 손해", { x: W - M - 5.9, y: 2.15, w: 5.9, h: 1.4 }, RED);
text(s, "→ 잃을 게 없다. 무조건 올린다", { x: M, y: 3.8, w: W - 2 * M, h: 0.7, fontSize: 30, bold: true, align: "center" });
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: M, y: 4.85, w: W - 2 * M, h: 1.8, fill: { color: LIGHT }, line: { color: LIGHT }, rectRadius: 0.1 });
text(s, [
  { text: "그럼 종료 5분 전이라면?", options: { fontSize: 26, bold: true, color: INK, breakLine: true } },
  { text: "실점하면 남은 시간에 동점을 만들 기회까지 사라진다. 토너먼트라면 동점에도 연장전이 있다.", options: { fontSize: 16, color: MUTED, breakLine: true } },
  { text: "진짜 질문 = 언제부터 손해인가", options: { fontSize: 20, bold: true, color: RED } },
], { x: M + 0.3, y: 5.0, w: W - 2 * M - 0.6, h: 1.55, valign: "middle" });
s.addNotes("한 줄씩 나타나게 애니메이션. 청중이 스스로 계산하게 잠깐 멈춘다.\n'1골 뒤진 채 끝나면 추가 실점을 해도 승점은 어차피 0점입니다. 그러니 마지막 코너는 올리는 게 당연합니다. ASA 분석도 같은 결론이었습니다.'\n'문제는 시간이 남아 있을 때입니다. 실점하면 남은 시간 동안 동점을 만들 가능성까지 같이 잃습니다. 토너먼트라면 동점에서도 연장전이 있어서 계산이 또 달라집니다. 그래서 진짜 질문은 언제부터 손해인가입니다.'");

// S9 권장 지도
s = pres.addSlide();
title(s, "우리가 내놓을 것: 골키퍼 가담 권장 지도", "각 칸 = 그 상황에서 골키퍼를 올렸을 때 이득일 확률");
const mins = ["80′", "85′", "88′", "90′", "92′", "95′+"], diffs = ["0 (동점)", "−1", "−2"];
function grid(x0, label) {
  text(s, label, { x: x0, y: 2.0, w: 5.8, h: 0.4, fontSize: 18, bold: true });
  const cw = 0.78, ch = 0.75, gx = x0 + 1.1, gy = 2.55;
  diffs.forEach((d, r) => {
    text(s, d, { x: x0, y: gy + r * ch + 0.22, w: 1.0, h: 0.35, fontSize: 13, color: MUTED });
    mins.forEach((m, c) => {
      const filled = label.startsWith("리그") && d === "−1" && m === "95′+";
      s.addShape(pres.shapes.RECTANGLE, { x: gx + c * cw, y: gy + r * ch, w: cw - 0.06, h: ch - 0.06, fill: { color: filled ? BLUE : "FFFFFF" }, line: { color: "C5CBD2", width: 0.75 } });
      if (filled) text(s, "GO", { x: gx + c * cw, y: gy + r * ch + 0.2, w: cw - 0.06, h: 0.3, fontSize: 12, bold: true, color: "FFFFFF", align: "center" });
    });
  });
  mins.forEach((m, c) => text(s, m, { x: gx + c * cw, y: gy + 3 * ch + 0.05, w: cw - 0.06, h: 0.3, fontSize: 12, color: MUTED, align: "center" }));
  text(s, "남은 시간 →", { x: gx, y: gy + 3 * ch + 0.38, w: 4.6, h: 0.3, fontSize: 12, color: MUTED });
}
grid(M, "리그 (기대 승점)");
grid(6.9, "토너먼트 녹아웃 (진출 확률)");
text(s, "파랑 = 올려라 · 빨강 = 유지 · 회색 = 판단 유보    |    지금 칠한 칸은 앞에서 손으로 계산한 한 칸뿐 — 나머지를 채우는 것이 목표", { x: M, y: 6.25, w: W - 2 * M, h: 0.4, fontSize: 13, color: MUTED });
text(s, "+ 감독들의 실제 선택을 이 지도 위에 찍어, '하키처럼 너무 늦고 드문가?'를 확인", { x: M, y: 6.7, w: W - 2 * M, h: 0.4, fontSize: 14, bold: true });
s.addNotes("'각 칸에는 그 상황에서 골키퍼를 올렸을 때 이득일 확률이 들어갑니다. 지금 칠한 칸은 방금 손으로 계산한 리그 · 1골 열세 · 마지막 코너 한 칸뿐입니다.'\n예상(가설): 1골 뒤질 때 마지막 몇 분부터 파랑. 동점 · 토너먼트는 빨강 쪽.\n부산물: ① ASA가 가정한 '역습 위험 배수'를 실측값으로 대체 ② 실제 감독들의 선택(골키퍼 가담 사례, 가담하지 않은 막판 열세 코너 약 1,700개)을 지도 위에 찍어 보수성을 확인.");

// S10 신뢰도
s = pres.addSlide();
title(s, "얼마나 믿을 수 있나");
const lights = [
  ["2E8B57", "결론의 방향", "높음", "이득인 상황과 손해인 상황의 구분"],
  ["D4A017", "경계 시점", "±1~2분", "모형 가정에 따라 경계가 이동 (하키 연구 간에도 약 3분 vs 6분)"],
  [RED, "효과의 정확한 크기", "넓은 구간", "반사실은 직접 검증 불가 · 효과가 잡음 수준(앞 슬라이드 오른쪽)"],
];
lights.forEach(([c, h, lvl, why], i) => {
  const y = 1.6 + i * 1.5;
  s.addShape(pres.shapes.OVAL, { x: M, y: y + 0.15, w: 0.9, h: 0.9, fill: { color: c }, line: { color: c } });
  text(s, [{ text: h + "  ", options: { fontSize: 22, bold: true, color: INK } }, { text: lvl, options: { fontSize: 22, bold: true, color: c } }], { x: M + 1.2, y: y + 0.1, w: 10.5, h: 0.5 });
  text(s, why, { x: M + 1.2, y: y + 0.65, w: 10.5, h: 0.45, fontSize: 15, color: MUTED });
});
text(s, "→ 점 하나가 아니라 '이득일 확률'로 보고하고, 실제 사례 60건으로 결과가 터무니없지 않은지 점검한다", { x: M, y: 6.25, w: W - 2 * M, h: 0.6, fontSize: 17, bold: true });
s.addNotes("근거 수치: 막판 열세 코너 60초 실점률의 95% 신뢰구간이 1.28~2.56%로 2배 폭. 빈 골문 위험은 코너가 아닌 비슷한 상황(골키퍼가 20m 이상 떨어진 슈팅 212개)에서 빌려 온다.\n'경계에서 먼 상황, 예를 들어 70분 2골 차는 명백히 손해, 95분 1골 차는 명백히 이득으로 판정할 수 있습니다. 경계 근처는 1~2분 정도 불확실성을 감수해야 합니다.'\n나머지 한계(상대 반응, 데이터 대표성)는 질문이 오면 부록 A5로.");

// S11 일정
s = pres.addSlide();
title(s, "일정");
const steps = [
  ["완료", "데이터 수집 · 정제", "공개 데이터 5,902경기, 골키퍼 가담 후보 60건"],
  ["11/23", "중간 점검", "부품 모델 3개 완성 (코너 공격 · 역습 위험 · 남은 시간 득점)"],
  ["12/14", "권장 지도 완성", "의사결정 모델, 감독 행동 비교, 민감도 분석"],
  ["12/21", "최종 발표", "지도로 답하기"],
];
steps.forEach(([d, h, b], i) => {
  const x = M + i * 3.1;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 2.1, w: 2.85, h: 3.2, fill: { color: i === 0 ? "EAF1FA" : "FFFFFF" }, line: { color: i === 0 ? BLUE : LINE, width: 1.25 }, rectRadius: 0.08 });
  text(s, d, { x: x + 0.25, y: 2.35, w: 2.35, h: 0.6, fontSize: 26, bold: true, color: i === 0 ? BLUE : INK });
  text(s, h, { x: x + 0.25, y: 3.1, w: 2.35, h: 0.5, fontSize: 18, bold: true });
  text(s, b, { x: x + 0.25, y: 3.7, w: 2.35, h: 1.4, fontSize: 14, color: MUTED });
});
text(s, "중간 점검 대안: 신경망 결과와 통계적 추정이 어긋나면 더 보수적인 쪽을 채택", { x: M, y: 5.8, w: W - 2 * M, h: 0.5, fontSize: 15, color: MUTED });
s.addNotes("'데이터는 이미 다 모아 두었습니다.' 주 단위 세부 일정은 기획서에 있으므로 읽지 않는다.");

// S12 다시 질문
s = pres.addSlide(); s.background = { color: "111418" };
text(s, "95분, 1골 뒤진 코너킥.\n골키퍼를 올리시겠습니까?", { x: M, y: 1.6, w: W - 2 * M, h: 2.2, fontSize: 40, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
text(s, "그럼 90분이라면?", { x: M, y: 4.1, w: W - 2 * M, h: 0.9, fontSize: 40, bold: true, color: "F2B134", align: "center" });
text(s, "12월 21일, 지도로 답하겠습니다", { x: M, y: 5.5, w: W - 2 * M, h: 0.5, fontSize: 18, color: "C9CED4", align: "center" });
s.addNotes("처음 투표 결과를 언급: '대부분 올린다고 하셨는데, 앞에서 본 것처럼 그건 맞을 가능성이 높습니다. 그런데 90분이라면요?'\n→ Q&A.");

// 부록
s = pres.addSlide();
title(s, "부록: 질문 대비");
const apx = [
  ["A1", "골키퍼 가담 탐지 방법과 편향", "스냅사진 위치 · 골키퍼의 공 관여 · 역습 슈팅 시 골키퍼 위치 → 마지막 방법은 실점한 경우만 잡힘"],
  ["A2", "빈 골문 슈팅", "골키퍼가 골문에서 20~30m: 실제 득점이 기대득점의 1.64배 (n = 174)"],
  ["A3", "데이터 품질", "Wyscout 좌표 반전 이벤트, 스냅사진 골키퍼 라벨 오류, Sportec 결측 좌표 → 정제 완료"],
  ["A4", "모델 세부", "그래프 신경망(GATv2) + 좌우 반전 증강, 경기 단위 교차검증, 이중 기계학습(DML), 포아송 득점 모형, 부트스트랩"],
  ["A5", "한계 6가지", "반사실 검증 불가 · 효과 ≈ 잡음 · 대리 상황 · 상대 반응 · 모형 가정 · 데이터 대표성"],
  ["A6", "참고문헌", "Beaudoin & Swartz 2010 · Young(ASA) 2018 · Wang 외 2024(TacticAI) · Chernozhukov 외 2018 · Bassek 외 2025"],
];
apx.forEach(([k, h, b], i) => {
  const y = 1.45 + i * 0.93;
  text(s, k, { x: M, y, w: 0.7, h: 0.4, fontSize: 18, bold: true, color: BLUE });
  text(s, h, { x: M + 0.8, y, w: 3.4, h: 0.4, fontSize: 16, bold: true });
  text(s, b, { x: M + 4.3, y, w: W - 2 * M - 4.3, h: 0.8, fontSize: 13, color: MUTED });
});
s.addNotes("발표하지 않는 슬라이드. 질문이 나오면 해당 항목을 펼쳐 설명한다. 후보 60건 목록은 data/derived/gk_up_candidates.csv.");

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote", OUT));
