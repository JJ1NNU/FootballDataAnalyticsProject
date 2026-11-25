// Build the editable Word report from notebook outputs (outputs/report_data.json + outputs/*.png).
// Every number in the report is read from the notebook's saved outputs, so report == notebook.
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
  AlignmentType, WidthType, ShadingType, BorderStyle, HeadingLevel, LevelFormat,
  PageBreak, Footer, PageNumber,
} = require("docx");

const OUT = path.join(__dirname, "outputs");
const D = JSON.parse(fs.readFileSync(path.join(OUT, "report_data.json"), "utf8"));
const FONT = "Malgun Gothic";

// ---------- helpers ----------
const f = (x, d = 3) => (x === null || x === undefined || Number.isNaN(x) ? "–" : Number(x).toFixed(d));
const pct = (x, d = 1) => f(x, d) + "%";
const row = (tbl, key, val) => D[tbl].find((r) => r[key] === val);

const P = (text, opts = {}) => new Paragraph({
  spacing: { after: 100, line: 300 }, ...opts,
  children: (Array.isArray(text) ? text : [text]).map((t) => (typeof t === "string" ? new TextRun(t) : t)),
});
const B = (t) => new TextRun({ text: t, bold: true });
const H1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(t)] });
const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(t)] });
const bullet = (text, level = 0) => new Paragraph({
  numbering: { reference: "bullets", level }, spacing: { after: 60, line: 290 },
  children: (Array.isArray(text) ? text : [text]).map((t) => (typeof t === "string" ? new TextRun(t) : t)),
});
const caption = (t) => new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { before: 60, after: 200 },
  children: [new TextRun({ text: t, size: 18, italics: true, color: "444444" })],
});

const TABLE_W = 9638; // A4 width - 2 x 2.0cm margins (DXA)
const border = { style: BorderStyle.SINGLE, size: 4, color: "999999" };
const borders = { top: border, bottom: border, left: border, right: border };
function table(headers, rows, weights, opts = {}) {
  const fs_ = opts.size || 16;
  const tot = weights.reduce((a, b) => a + b, 0);
  const widths = weights.map((w) => Math.floor((w / tot) * TABLE_W));
  widths[widths.length - 1] += TABLE_W - widths.reduce((a, b) => a + b, 0);
  const cell = (t, i, head, hl) => new TableCell({
    borders, width: { size: widths[i], type: WidthType.DXA },
    shading: head ? { fill: "DCE6F2", type: ShadingType.CLEAR } : hl ? { fill: "FFF4CC", type: ShadingType.CLEAR } : undefined,
    margins: { top: 40, bottom: 40, left: 70, right: 70 },
    children: [new Paragraph({
      alignment: i === 0 || (opts.leftCols || []).includes(i) ? AlignmentType.LEFT : AlignmentType.RIGHT,
      children: [new TextRun({ text: String(t), size: fs_, bold: head })],
    })],
  });
  return new Table({
    width: { size: TABLE_W, type: WidthType.DXA }, columnWidths: widths,
    rows: [
      new TableRow({ tableHeader: true, children: headers.map((h, i) => cell(h, i, true)) }),
      ...rows.map((r, ri) => new TableRow({ children: r.map((t, i) => cell(t, i, false, (opts.highlight || []).includes(ri))) })),
    ],
  });
}
function image(file, widthPx) {
  const buf = fs.readFileSync(path.join(OUT, file));
  const w = buf.readUInt32BE(16), h = buf.readUInt32BE(20); // PNG IHDR
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new ImageRun({ type: "png", data: buf, transformation: { width: widthPx, height: Math.round((widthPx * h) / w) } })],
  });
}

// ---------- numbers used in the text ----------
const S_C = row("q1_per90_summary", "player", "Cruyff");
const S_R = row("q1_per90_summary", "player", "Ronaldinho");
const CI_C = row("q1_per90_ci", "player", "Cruyff");
const CI_R = row("q1_per90_ci", "player", "Ronaldinho");
const cat = (p, c) => D.q1_category.find((r) => r._idx === p && r.category === c);
const RS_C = row("q1_rank_summary", "player", "Cruyff");
const RS_R = row("q1_rank_summary", "player", "Ronaldinho");
const pgC = D.q1_cruyff_per_game;
const best = pgC.reduce((a, b) => (b.vaep_per90 > a.vaep_per90 ? b : a));
const worst = pgC.reduce((a, b) => (b.vaep_per90 < a.vaep_per90 ? b : a));
const top3 = [...pgC].sort((a, b) => b.vaep - a.vaep).slice(0, 3).reduce((s, r) => s + r.vaep, 0) / pgC.reduce((s, r) => s + r.vaep, 0);
const wc = D.q1_wc1974_combined_rank;
const dist = (k) => D.q2_distribution.find((r) => r._idx === k);
const DC = dist("Cruyff games (all actions)"), DR = dist("Ronaldinho games (all actions)");
const DCo = dist("Cruyff (own actions)"), DRo = dist("Ronaldinho (own actions)");
const lab = (k) => D.q2_label_rates.find((r) => r._idx === k);
const met = (ds, l) => D.q2_metrics.find((r) => r.dataset === ds && r.label === l);
const MCs = met("Cruyff", "scores"), MCc = met("Cruyff", "concedes");
const MRs = met("Ronaldinho", "scores"), MRc = met("Ronaldinho", "concedes");
const MWs = met("WC2018 test (meta)", "scores"), MWc = met("WC2018 test (meta)", "concedes");
const scene = D.q3_scene;
const shot = scene[scene.length - 1], cross = scene[scene.length - 2];
const sceneNL = scene.filter((r) => r.player_name !== "Jair Ventura Filho");
const buildup = sceneNL.slice(0, -2).reduce((s, r) => s + r.vaep_value, 0);

// ---------- document body ----------
const body = [];

// Title block
body.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 },
  children: [new TextRun({ text: "축구 데이터 분석 과제 3", size: 24, color: "555555" })] }));
body.push(new Paragraph({ heading: HeadingLevel.TITLE, alignment: AlignmentType.CENTER,
  children: [new TextRun("VAEP로 레전드 평가하기: 요한 크루이프")] }));
body.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
  children: [new TextRun({ text: "비교 대상: 2004/05~2007/08 바르셀로나의 호나우지뉴", size: 22 })] }));
body.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 300 },
  children: [new TextRun({ text: "학번: ____________        이름: ____________", size: 22 })] }));

// 0. 데이터와 방법
body.push(H1("0. 데이터와 방법"));
body.push(bullet([B("파이프라인: "), "9주차 실습 노트북(Week 9, 1-run-spadl-vaep.ipynb)의 StatsBombLoader → SPADL 변환 → 특징·라벨 생성(nb_prev_actions=3, 라벨 기준 10개 행동) → VAEP 공식 계산을 그대로 사용했다. 득점·실점 모델은 조교가 제공한 pickle(vaep_models.pkl: 2020년대 분데스리가·라리가·리그1 127경기로 학습한 XGBoost)을 다시 학습하지 않고 적용했다."]));
body.push(bullet([B("크루이프 경기: "), `오픈 데이터에서 크루이프(Johan Cruyff, player_id 39713)가 출전한 경기는 ${pgC.length}경기다. 과제 안내문은 11경기로 적었지만, 1974 월드컵 네덜란드 7경기 중 우루과이전·불가리아전이 오픈 데이터에 없어 실제로는 유러피언컵 결승 3경기, 1974 월드컵 5경기, 1974 레알 마드리드 0-5 바르셀로나, 1978 코파 델 레이 결승으로 10경기다.`]));
body.push(bullet([B("호나우지뉴 경기: "), `2004/05~2007/08 라리가 오픈 데이터 77경기 중 호나우지뉴(Ronaldo de Assis Moreira)가 출전한 ${S_R.games}경기, 총 ${S_R.minutes}분이다.`]));
body.push(bullet([B("행동 종류 구분: "), "패스 = pass·cross·throw_in·freekick(short/crossed)·corner(short/crossed)·goalkick, 드리블 = dribble(공 운반)·take_on(돌파), 슛 = shot·shot_freekick·shot_penalty, 수비 행동 = tackle·interception·clearance·keeper_*, 그 밖의 행동(foul·bad_touch)은 기타로 묶었다."]));
body.push(bullet([B("출전 시간: "), "StatsBombLoader가 주는 경기별 minutes_played를 썼다. 표의 모든 숫자는 제출 노트북 출력(outputs/*.csv)과 같은 값이다."]));

// 문제 1
body.push(H1("문제 1. 재현"));
body.push(H2("1-1. 경기별 출전 시간, 행동 수, VAEP 합계, 공격·수비 가치"));
body.push(table(
  ["날짜", "대회", "경기", "출전(분)", "행동 수", "VAEP", "공격", "수비", "90분당"],
  pgC.map((r) => [r.date, r.competition.replace("Champions League", "European Cup"), r.match, r.minutes, r.actions, f(r.vaep), f(r.offensive), f(r.defensive), f(r.vaep_per90)]),
  [11, 17, 25, 7, 7, 8, 8, 8, 8], { leftCols: [1, 2] }));
body.push(caption("표 1. 크루이프 경기별 VAEP (European Cup = 오픈 데이터의 Champions League 1970/71~1972/73)"));

// Ronaldinho season summary
const seasons = {};
for (const r of D.q1_ronaldinho_per_game) {
  const s = r.competition.slice(-9);
  seasons[s] = seasons[s] || { games: 0, minutes: 0, actions: 0, vaep: 0, off: 0, def: 0 };
  const x = seasons[s]; x.games++; x.minutes += r.minutes; x.actions += r.actions; x.vaep += r.vaep; x.off += r.offensive; x.def += r.defensive;
}
const seasonRows = Object.entries(seasons).map(([s, x]) => [s, x.games, x.minutes, x.actions, f(x.vaep), f(x.off), f(x.def), f((x.vaep * 90) / x.minutes)]);
seasonRows.push(["합계", S_R.games, S_R.minutes, S_R.actions, f(S_R.vaep), f(S_R.offensive), f(S_R.defensive), f(S_R.vaep_per90)]);
body.push(table(["시즌", "경기", "출전(분)", "행동 수", "VAEP", "공격", "수비", "90분당"], seasonRows, [14, 8, 10, 10, 10, 10, 10, 10], { highlight: [seasonRows.length - 1] }));
body.push(caption("표 2. 호나우지뉴 시즌별 요약 (경기별 전체 표는 부록 A)"));

body.push(H2("1-2. 90분당 VAEP와 행동 종류별 기여 비중"));
body.push(table(
  ["선수", "경기", "출전(분)", "행동 수", "VAEP 합", "90분당 VAEP", "95% 구간*", "90분당 공격", "90분당 수비"],
  [[`크루이프`, S_C.games, S_C.minutes, S_C.actions, f(S_C.vaep), f(S_C.vaep_per90), `[${f(CI_C.ci_low)}, ${f(CI_C.ci_high)}]`, f(S_C.offensive_per90), f(S_C.defensive_per90)],
   [`호나우지뉴`, S_R.games, S_R.minutes, S_R.actions, f(S_R.vaep), f(S_R.vaep_per90), `[${f(CI_R.ci_low)}, ${f(CI_R.ci_high)}]`, f(S_R.offensive_per90), f(S_R.defensive_per90)]],
  [12, 7, 9, 9, 10, 11, 16, 11, 11]));
body.push(caption("표 3. 90분당 VAEP (*경기를 단위로 1,000번 부트스트랩한 95% 구간)"));
const cats = ["Pass", "Dribble", "Shot", "Defensive", "Other"], catK = { Pass: "패스", Dribble: "드리블", Shot: "슛", Defensive: "수비 행동", Other: "기타" };
body.push(table(
  ["행동 종류", "크루이프 행동 수(비율)", "크루이프 90분당", "크루이프 VAEP 비중", "호나우지뉴 행동 수(비율)", "호나우지뉴 90분당", "호나우지뉴 VAEP 비중"],
  cats.map((c) => { const a = cat("Cruyff", c), b = cat("Ronaldinho", c);
    return [catK[c], `${a.actions} (${pct(a["share_of_actions_%"])})`, f(a.vaep_per90), pct(a["share_of_vaep_%"]), `${b.actions} (${pct(b["share_of_actions_%"])})`, f(b.vaep_per90), pct(b["share_of_vaep_%"])]; }),
  [12, 16, 12, 13, 16, 13, 14]));
body.push(caption("표 4. 행동 종류별 기여 (VAEP 비중 = 그 종류의 VAEP 합 ÷ 전체 VAEP 합. 기타가 음수라 나머지 비중의 합은 100%를 넘는다)"));
body.push(image("q1_category.png", 560));
body.push(caption("그림 1. 행동 종류별 90분당 VAEP (막대 위 숫자는 VAEP 비중)"));
body.push(P([`크루이프의 90분당 VAEP는 ${f(S_C.vaep_per90)}로 호나우지뉴(${f(S_R.vaep_per90)})보다 높다. 두 선수 모두 값의 거의 전부가 공격 가치에서 나오고, 90분당 수비 가치는 0에 가깝거나 약간 음수다. `,
  `크루이프의 값은 경기마다 크게 달라 ${best.match}(${best.date.slice(0, 4)})의 ${f(best.vaep_per90)}부터 ${worst.match}(${worst.date.slice(0, 4)})의 ${f(worst.vaep_per90)}까지 퍼져 있다. VAEP 합이 큰 세 경기가 전체의 ${pct(100 * top3)}를 차지한다. 그래서 부트스트랩 95% 구간 [${f(CI_C.ci_low)}, ${f(CI_C.ci_high)}]은 호나우지뉴의 구간 [${f(CI_R.ci_low)}, ${f(CI_R.ci_high)}]과 겹친다.`]));
body.push(P([`행동 종류별로 보면 크루이프는 드리블(${pct(cat("Cruyff", "Dribble")["share_of_vaep_%"])})과 슛(${pct(cat("Cruyff", "Shot")["share_of_vaep_%"])})이 가치의 대부분을 만들고 패스 비중은 ${pct(cat("Cruyff", "Pass")["share_of_vaep_%"])}에 그친다. 호나우지뉴는 패스(${pct(cat("Ronaldinho", "Pass")["share_of_vaep_%"])})와 슛(${pct(cat("Ronaldinho", "Shot")["share_of_vaep_%"])})이 비슷하게 크고 드리블은 ${pct(cat("Ronaldinho", "Dribble")["share_of_vaep_%"])}다. `,
  `두 선수 모두 슛은 행동의 ${pct(cat("Cruyff", "Shot")["share_of_actions_%"])}·${pct(cat("Ronaldinho", "Shot")["share_of_actions_%"])}에 불과하지만 가치의 40% 이상을 차지한다. 득점으로 끝난 슛은 행동 후 득점 확률이 1에 가깝게 예측되므로 큰 가치를 받기 때문이다.`]));

body.push(H2("1-3. 같은 경기에 뛴 동료·상대 중 90분당 VAEP 순위"));
body.push(P("각 경기에서 양 팀 출전 선수 중 10분 이상 뛴 선수만 대상으로 90분당 VAEP 순위를 매겼다(순위/대상 인원). 팀 내 순위는 같은 팀 선수 중 순위다."));
body.push(table(
  ["날짜", "경기", "90분당 VAEP", "전체 순위", "팀 내 순위", "그 경기 1위 (90분당)"],
  D.q1_cruyff_rank.map((r) => [r.date, r.match, f(r.vaep_per90), r.rank_all, r.rank_in_team, `${r.top_player} ${f(r.top_per90)}`]),
  [11, 25, 11, 9, 9, 35], { leftCols: [1, 5] }));
body.push(caption("표 5. 크루이프의 경기별 90분당 VAEP 순위 (출전 10분 이상)"));
body.push(table(
  ["선수", "경기", "순위 중앙값", "순위 평균", "1위 경기", "3위 이내 경기", "평균 백분위"],
  [RS_C, RS_R].map((r) => [r.player === "Cruyff" ? "크루이프" : "호나우지뉴", r.games, f(r.median_rank, 1), f(r.mean_rank, 2), r.rank1_games, r.top3_games, pct(r["mean_percentile_%"])]),
  [14, 10, 14, 14, 12, 16, 14]));
body.push(caption("표 6. 경기별 순위 요약 (백분위 = 1 − (순위−1)/(인원−1), 호나우지뉴 경기별 순위는 부록 A)"));
body.push(P([`크루이프는 10경기 중 ${RS_C.rank1_games}경기에서 그 경기 1위, ${RS_C.top3_games}경기에서 3위 이내였고 순위 중앙값은 ${f(RS_C.median_rank, 0)}위다. 호나우지뉴는 ${RS_R.games}경기 중 ${RS_R.rank1_games}경기에서 1위, ${RS_R.top3_games}경기에서 3위 이내였고 순위 중앙값은 ${f(RS_R.median_rank, 0)}위다. `,
  `같은 경기 안의 순위는 시대마다 다른 데이터 특성(행동 수, 득점 빈도)을 어느 정도 상쇄하므로 90분당 VAEP 절댓값보다 비교에 덜 위험한 지표다. 다만 크루이프는 1974 월드컵 결승(${D.q1_cruyff_rank.find((r) => r.match.includes("Germany") && r.match.includes("1-2")).rank_all})과 동독전(${D.q1_cruyff_rank.find((r) => r.match.includes("German DR")).rank_all})에서는 중하위권이었다. `,
  `부록 B에 1974 월드컵 네덜란드 5경기를 합산한 순위(합산 출전 50분 이상 ${wc.length}명)를 붙였으며, 크루이프는 90분당 ${f(wc[0].vaep_per90)}로 1위다.`]));

// 문제 2
body.push(H1("문제 2. 검증"));
body.push(H2("2-1. 경기당 행동 수와 행동 종류 분포"));
const distRows = [["Cruyff games (all actions)", "크루이프 10경기 (양 팀 전체)"], ["Ronaldinho games (all actions)", `호나우지뉴 ${S_R.games}경기 (양 팀 전체)`], ["Cruyff (own actions)", "크루이프 본인"], ["Ronaldinho (own actions)", "호나우지뉴 본인"]]
  .map(([k, name]) => { const r = dist(k); return [name, f(r.actions_per_game, 1), r.actions_per90 ? f(r.actions_per90, 1) : "–", pct(r["pass_%"]), pct(r["pass_success_%"]), pct(r["carry(dribble)_%"]), pct(r["take_on_%"], 2), pct(r["take_on_success_%"]), pct(r["shot_%"], 2), pct(r["defensive_%"])]; });
body.push(table(["데이터", "경기당 행동", "90분당 행동", "패스 비율", "패스 성공률", "운반 비율", "돌파 비율", "돌파 성공률", "슛 비율", "수비 비율"], distRows, [24, 9, 9, 8, 9, 8, 8, 9, 8, 8], { size: 15 }));
body.push(caption("표 7. 행동 수와 종류 분포 (돌파 = take_on, 운반 = dribble)"));
body.push(image("q2_actions_per_game.png", 400));
body.push(caption("그림 2. 경기당 SPADL 행동 수 (양 팀 합계)"));
body.push(H2("2-2. 행동 10개 안에 득점/실점이 나온 비율"));
const lr = [["Cruyff games", "크루이프 10경기"], ["Ronaldinho games", `호나우지뉴 ${S_R.games}경기`], ["Model train (meta)", "모델 학습 데이터 (2020년대)"], ["WC2018 test (meta)", "2018 월드컵 테스트"]]
  .map(([k, n]) => { const r = lab(k); return [n, r.n_actions ? r.n_actions : "–", pct(r["P(scores)_%"], 3), pct(r["P(concedes)_%"], 3), r.goals_per_game ? f(r.goals_per_game, 2) : "–"]; });
body.push(table(["데이터", "행동 수", "10개 안 득점 비율", "10개 안 실점 비율", "경기당 골"], lr, [30, 14, 18, 18, 14]));
body.push(caption("표 8. 라벨 비율 (lab.scores / lab.concedes). 학습·테스트 값은 제공 모델 meta에 기록된 값"));
body.push(H2("2-3. 제공 모델의 AUC와 Brier score"));
const mrow = (r, n) => [n, r.label === "scores" ? "득점" : "실점", r.n_pos ?? "–", pct(100 * r.base_rate, 3), r.mean_pred ? pct(100 * r.mean_pred, 3) : "–", f(r.auc), r.auc_95ci || "–", f(r.brier_score, 4), r.brier_95ci || "–", f(r.BSS)];
body.push(table(["데이터", "모델", "양성 수", "실제 비율", "평균 예측", "AUC", "AUC 95% 구간", "Brier", "Brier 95% 구간", "BSS"],
  [mrow(MCs, "크루이프"), mrow(MRs, "호나우지뉴"), mrow(MWs, "WC2018"), mrow(MCc, "크루이프"), mrow(MRc, "호나우지뉴"), mrow(MWc, "WC2018")],
  [12, 7, 8, 10, 10, 8, 14, 9, 14, 8], { size: 15 }));
body.push(caption("표 9. 모델 성능 (95% 구간은 경기 단위 부트스트랩 1,000회, BSS = 1 − Brier / [기저율×(1−기저율)])"));
body.push(image("q2_calibration.png", 560));
body.push(caption("그림 3. 신뢰도 곡선: 예측 확률 구간별 실제 비율 (점선이 완벽한 보정)"));
body.push(P([B("무엇이 다른가. "),
  `① 크루이프 경기는 경기당 행동이 ${f(DC.actions_per_game, 0)}개로 호나우지뉴 경기(${f(DR.actions_per_game, 0)}개)보다 적고 패스 성공률이 낮다(${pct(DC["pass_success_%"])} vs ${pct(DR["pass_success_%"])}). 패스 비율은 거의 같고, 돌파(${pct(DC["take_on_%"], 2)} vs ${pct(DR["take_on_%"], 2)})와 슛(${pct(DC["shot_%"], 2)} vs ${pct(DR["shot_%"], 2)}) 비율은 크루이프 경기가 조금 높다. 선수 본인만 보면 크루이프는 돌파 비율(${pct(DCo["take_on_%"], 2)})과 돌파 성공률(${pct(DCo["take_on_success_%"])})이 호나우지뉴(${pct(DRo["take_on_%"], 2)}, ${pct(DRo["take_on_success_%"])})보다 높고, 패스 성공률(${pct(DCo["pass_success_%"])} vs ${pct(DRo["pass_success_%"])})과 슛 비율은 낮다. `,
  `② 행동 10개 안 득점 비율은 ${pct(lab("Cruyff games")["P(scores)_%"], 2)}와 ${pct(lab("Ronaldinho games")["P(scores)_%"], 2)}, 실점 비율은 ${pct(lab("Cruyff games")["P(concedes)_%"], 2)}와 ${pct(lab("Ronaldinho games")["P(concedes)_%"], 2)}로 학습 데이터와 비슷하다. 라벨 기저율은 시대 차이가 거의 없다. `,
  `③ 득점 모델 AUC는 크루이프 경기 ${f(MCs.auc)}, 호나우지뉴 경기 ${f(MRs.auc)}, 2018 월드컵 ${f(MWs.auc)} 순이다. 크루이프 경기에서 변별력이 가장 낮지만 BSS는 ${f(MCs.BSS)}로 호나우지뉴(${f(MRs.BSS)})와 비슷하고, 평균 예측(${pct(100 * MCs.mean_pred, 2)})도 실제 비율(${pct(100 * MCs.base_rate, 2)})에 가깝다. 반면 실점 모델은 크루이프 경기의 양성이 ${MCc.n_pos}개뿐이라 AUC 95% 구간이 ${MCc.auc_95ci}로 매우 넓고, BSS가 ${f(MCc.BSS)}로 기저율만 예측하는 것보다 못하다. 따라서 크루이프의 수비 가치(실점 확률 변화)는 믿을 근거가 약하다.`]));

body.push(H2("2-4. 주장 분류"));
body.push(table(["주장", "분류"], [
  ["① 이 모델의 득점 확률 예측은 배정 선수의 경기에서도 잘 맞는다.", "직접 검증 가능"],
  ["② 90분당 VAEP가 비교 대상보다 높으므로 배정 선수가 더 좋은 선수다.", "현재 데이터로는 불가"],
  ["③ 이 패스의 VAEP +0.03은 그 패스가 실제로 만든 가치와 같다.", "현재 데이터로는 불가"],
], [75, 25], { leftCols: [1] }));
body.push(caption("표 10. 주장 분류"));
body.push(P([B("① 직접 검증 가능. "), `크루이프 경기에도 '행동 10개 안에 득점했는가'라는 실제 라벨이 있으므로 예측 확률과 바로 비교할 수 있다. 실제로 AUC ${f(MCs.auc)}(95% 구간 ${MCs.auc_95ci}), Brier ${f(MCs.brier_score, 4)}, BSS ${f(MCs.BSS)}를 계산했다. 결과는 '잘 맞는다'에 가깝지만 2018 월드컵(${f(MWs.auc)})보다 변별력이 낮고, 신뢰도 곡선에서 예측 확률 5~10% 구간이 실제보다 높게 예측된다. 득점 라벨 양성이 ${MCs.n_pos}개라 구간이 넓다는 점도 함께 적어야 한다.`]));
body.push(P([B("② 현재 데이터로는 불가. "), `'90분당 VAEP가 높다'는 계산할 수 있지만 '더 좋은 선수'에는 정답 라벨이 없어 어떤 데이터로도 직접 맞춰 볼 수 없다. 게다가 이 비교에는 차이를 만드는 다른 원인이 섞여 있다. 크루이프는 결승·월드컵 위주 10경기(${S_C.minutes}분), 호나우지뉴는 라리가 ${S_R.games}경기(${S_R.minutes}분)이고, 두 시대의 데이터 분포(표 7)가 다르며, 모델은 2020년대 리그로 학습했다. 90분당 값의 95% 구간도 서로 겹친다(표 3). VAEP는 온 볼 행동만 평가하므로 공간 창출·압박 같은 오프 더 볼 기여도 빠진다. 따라서 숫자는 주장 ②의 결론을 뒷받침하지 못한다.`]));
body.push(P([B("③ 현재 데이터로는 불가. "), "한 패스가 '실제로 만든 가치'는 그 패스를 하지 않았을 때와의 차이(반사실)인데, 이는 관측되지 않는다. 한 번의 패스 뒤에는 득점했다/안 했다는 0/1 결과만 남으므로 +0.03 같은 연속값을 개별 행동 단위로 채점할 수 없다. 간접적으로 확인할 수 있는 것은 '비슷한 상황에서 득점 확률 예측이 평균적으로 맞는가'(그림 3의 보정) 정도이며, 이는 평균 수준의 정합성일 뿐 그 패스 하나의 가치가 +0.03이라는 증거가 아니다."]));

// 문제 3
body.push(H1("문제 3. 시각화: 1974 월드컵 네덜란드 2-0 브라질, 크루이프 발리골"));
body.push(P("1974년 7월 3일 2차 조별리그 브라질전 후반, 네덜란드 진영의 프리킥부터 크롤의 왼발 크로스와 크루이프의 발리 슛까지 12개 행동이다. scores·concedes는 행동 직후 상태에서 예측한 10개 행동 안 득점·실점 확률이다."));
body.push(table(["#", "시간", "선수", "행동", "결과", "P(득점)", "P(실점)", "공격 가치", "수비 가치", "VAEP"],
  scene.map((r, i) => [i + 1, r.time, r.player_name, r.type_name, r.result_name, f(r.scores), f(r.concedes), f(r.offensive_value), f(r.defensive_value), f(r.vaep_value)]),
  [4, 9, 20, 14, 8, 9, 9, 9, 9, 9], { leftCols: [2, 3, 4], highlight: [scene.length - 2, scene.length - 1], size: 15 }));
body.push(caption("표 11. 대표 장면의 행동별 득점·실점 확률과 VAEP (#1은 브라질 자이르징요의 파울)"));
body.push(image("q3_scene.png", 620));
body.push(caption("그림 4. matplotsoccer로 그린 대표 장면 (Week 9 plot_actions 함수 사용)"));
body.push(P([B("가장 큰 가치를 받은 행동: "), `크루이프의 발리 슛(VAEP ${f(shot.vaep_value)})이다. 크롤의 크로스 직후 득점 확률이 ${f(cross.scores)}였고, 골이 들어간 슛은 득점 확률이 ${f(shot.scores)}로 예측되므로 그 차이가 그대로 슛의 가치가 된다. 두 번째는 크롤의 크로스(${f(cross.vaep_value)})이고, 그 앞의 빌드업 행동 9개는 모두 합해도 ${f(buildup)}에 그친다.`]));
body.push(P([B("전부 크루이프에게 귀속해도 되는가: "), "전부 귀속하기는 어렵다. 이유는 다음과 같다."]));
body.push(bullet(["VAEP는 '공헌'이 아니라 '확률이 바뀐 시점'으로 가치를 나눈다. 크로스가 들어온 시점의 득점 확률(0.385)을 넘는 나머지는 모두 마지막 행동인 슛이 받는다. 같은 골이라도 마무리가 어려울수록 슛이 더 많이 받고, 쉬운 탭인이면 크로스가 더 많이 받는다."]));
body.push(bullet(["크루이프가 공 없이 슛 위치까지 들어간 움직임, 크롤의 오버래핑, 다른 선수들이 수비수를 끌어낸 움직임은 SPADL 행동이 아니어서 가치를 받지 못한다. 크롤의 크로스 가치 0.361 안에는 크루이프의 침투 움직임 덕분에 생긴 몫도 섞여 있다."]));
body.push(bullet(["골 여부라는 결과가 슛의 가치를 결정하므로 골키퍼의 실수나 운도 슛을 한 선수에게 들어간다. 같은 슛이 골대를 맞았다면 크루이프의 VAEP는 음수가 될 수도 있다."]));
body.push(P(`따라서 ${f(shot.vaep_value)}는 '크루이프가 결정적 마무리를 했다'는 측정으로는 의미가 있지만, 이 공격 전체의 가치를 그에게 돌리는 근거는 아니다. 크롤의 크로스와 오프 더 볼 움직임까지 포함해 장면 단위로 나눠 보는 것이 맞다.`));

// 문제 4
body.push(H1("문제 4. 결론"));
body.push(P([B("결론: 레전드의 90분당 VAEP는 GOAT 논쟁의 '결정적 근거'로는 쓸 수 없고, 아래 단서를 모두 붙인 '보조 근거'로만 쓸 수 있다. "),
  `크루이프의 ${f(S_C.vaep_per90)}는 '이 10경기에서, 2020년대 리그로 학습한 모델이 보기에 온 볼 공격 기여가 컸다'는 뜻이지 '호나우지뉴(${f(S_R.vaep_per90)})보다 위대하다'는 뜻이 아니다.`]));
body.push(bullet([B("표본: "), `크루이프는 ${S_C.minutes}분(10경기), 그것도 결승·월드컵처럼 기록이 남은 경기만이다. 경기별 값이 ${f(worst.vaep_per90)}~${f(best.vaep_per90)}로 흩어져 있고 상위 3경기가 ${pct(100 * top3)}를 차지하며, 95% 구간 [${f(CI_C.ci_low)}, ${f(CI_C.ci_high)}]이 비교 대상과 겹친다. 숫자를 쓸 때는 구간과 경기 수를 함께 적어야 한다.`]));
body.push(bullet([B("데이터의 시대 차이: "), `1970년대 경기는 남아 있는 영상을 나중에 코딩한 데이터라 경기당 행동 수(${f(DC.actions_per_game, 0)} vs ${f(DR.actions_per_game, 0)})와 패스 성공률이 다르다. 같은 플레이라도 기록되는 방식이 다를 수 있다.`]));
body.push(bullet([B("모델의 외삽: "), `모델은 2020년대 리그로 학습했다. 득점 모델은 크루이프 경기에서도 쓸 만하지만(AUC ${f(MCs.auc)}) 현대 경기보다 변별력이 낮고, 실점 모델은 근거가 거의 없다(BSS ${f(MCc.BSS)}). 수비 가치는 비교에서 빼거나 따로 표시해야 한다.`]));
body.push(bullet([B("비교 맥락: "), "결승·월드컵 대 리그 경기, 상대 수준, 팀 전술(토털 풋볼과 2000년대 바르셀로나), 선수의 역할이 다르다. 시대 간 절댓값보다 같은 경기 안의 순위·백분위(표 6)처럼 시대 효과를 줄인 지표를 함께 제시해야 한다."]));
body.push(bullet([B("VAEP의 구조: "), "온 볼 행동만 평가하고, 골이 된 슛에 가치가 몰리며(문제 3), 수비·오프 더 볼 기여를 거의 잡지 못한다. 공격형 선수에게 유리한 척도라는 점을 밝혀야 한다."]));
body.push(new Paragraph({ spacing: { before: 200, after: 80 }, children: [B("행동 가치 모델 전반에 대한 생각")] }));
body.push(P(new TextRun({ text: "(직접 작성)", color: "888888", italics: true })));

// 부록
body.push(new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: true, children: [new TextRun("부록 A. 호나우지뉴 경기별 VAEP와 순위")] }));
const rankR = D.q1_ronaldinho_rank;
body.push(table(["날짜", "경기", "출전", "행동", "VAEP", "공격", "수비", "90분당", "전체 순위"],
  D.q1_ronaldinho_per_game.map((r, i) => [r.date, r.match, r.minutes, r.actions, f(r.vaep), f(r.offensive), f(r.defensive), f(r.vaep_per90), rankR[i].rank_all]),
  [11, 30, 7, 7, 8, 8, 8, 8, 9], { leftCols: [1], size: 14 }));
body.push(caption("표 A1. 호나우지뉴 경기별 VAEP와 90분당 VAEP 순위 (출전 10분 이상)"));
body.push(H1("부록 B. 1974 월드컵 네덜란드 5경기 통합 순위"));
body.push(table(["순위", "선수", "팀", "경기", "출전(분)", "VAEP", "90분당"],
  wc.slice(0, 10).map((r) => [r._idx, r.name, r.team, r.games, r.minutes, f(r.vaep_value), f(r.vaep_per90)]),
  [8, 28, 18, 9, 12, 12, 12], { leftCols: [1, 2], highlight: [0] }));
body.push(caption(`표 B1. 5경기 합산 90분당 VAEP 상위 10명 (합산 출전 50분 이상 ${wc.length}명 대상)`));

// ---------- document ----------
const doc = new Document({
  creator: "", title: "과제 3 - VAEP로 레전드 평가하기 (요한 크루이프)",
  styles: {
    default: { document: { run: { font: FONT, size: 21 } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal", next: "Normal", run: { font: FONT, size: 36, bold: true }, paragraph: { spacing: { before: 0, after: 120 }, keepNext: true } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: FONT, size: 28, bold: true, color: "1F3864" }, paragraph: { spacing: { before: 300, after: 140 }, keepNext: true, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: FONT, size: 23, bold: true, color: "2F5496" }, paragraph: { spacing: { before: 200, after: 100 }, keepNext: true, outlineLevel: 1 } },
    ],
  },
  numbering: { config: [{ reference: "bullets", levels: [
    { level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 400, hanging: 260 } } } },
    { level: 1, format: LevelFormat.BULLET, text: "–", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 800, hanging: 260 } } } },
  ] }] },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], size: 18 })] })] }) },
    children: body,
  }],
});
Packer.toBuffer(doc).then((buf) => {
  const out = path.join(__dirname, "assignment3_report_cruyff.docx");
  fs.writeFileSync(out, buf);
  console.log("wrote", out);
});
