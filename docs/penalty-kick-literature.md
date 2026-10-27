# 페널티킥 선행연구 조사

> 작성일: 2026-10-27 · 관련 문서: [`data-sources-and-topics.md`](./data-sources-and-topics.md), [`literature-review-and-gaps.md`](./literature-review-and-gaps.md)

페널티킥은 **조건이 거의 통제된 1:1 게임**이라서 경제학(게임이론), 심리학(압박·초킹), 지각-운동 과학(시선), 통계학(실력 vs 운), 컴퓨터 비전(방향 예측)이 모두 모이는 주제입니다. 연구 흐름을 8갈래로 정리하고, 마지막에 연구 공백과 프로젝트 아이디어를 붙였습니다.

---

## 1. 게임이론: 프로 선수들은 혼합전략 균형을 따르는가

| 연구 | 데이터 | 핵심 결과 |
|---|---|---|
| Chiappori, Levitt & Groseclose 2002 (*AER*) | 프랑스·이탈리아 리그 | 키커와 골키퍼의 선택이 혼합전략 내시 균형의 예측과 대체로 일치 |
| **Palacios-Huerta 2003** (*Review of Economic Studies*) | 프로 PK 약 1,400개 | 약한 쪽 성공률 81.1% vs 강한 쪽 82.7%. **방향별 성공률이 같고(균형 조건), 선택 순서도 무작위와 구분되지 않음** → 실제 현장에서 미니맥스를 검증한 대표 사례 |
| Palacios-Huerta 2014, *Beautiful Game Theory* (책) | | 위 결과를 확장. 첼시가 2008 챔스 결승에서 쓴 분석 자료 일화가 유명 |
| Adversarial risk analysis 계열 등 | | 집계 데이터는 선수 간 실력 차이를 섞어 버린다는 방법론 비판. 균형 대신 상대 모델링 접근을 제안 |
| **Bransen, Janssen & Davis 2025**, *Stop Guessing: Optimizing Goalkeeper Policies* (arXiv 2505.24629) | 전문가가 키커·골키퍼 전략을 주석한 대규모 PK | 선수 비의존 시뮬레이션 프레임워크로 **골키퍼 개인 능력을 반영한 최적 정책**을 탐색. 키커와 골키퍼의 선택을 상호의존적으로 모델링. 스스로 밝힌 한계: 선수별 표본이 작음 |

## 2. 골키퍼 행동 편향 (Action bias) 논쟁

| 연구 | 주장 |
|---|---|
| **Bar-Eli et al. 2007** (*J. Economic Psychology*) | 이스라엘 등 PK 286개. 슈팅의 약 29%가 가운데로 오는데 골키퍼는 6%만 가운데에 남음. 가만히 있다 실점하면 더 비난받기 때문에 **움직이려는 편향**이 생긴다는 해석 |
| 반박 연구 (같은 데이터 + 분데스리가) | 가운데를 선택지로 제대로 넣어 계산하면 **골키퍼는 최적에 놀랍도록 가깝게 행동**한다 → 다이빙은 실수가 아니라 합리적인 경험칙 |
| 2023 리뷰 (*Asian J. Sport & Exercise Psychology*) | 논쟁 정리: 가운데에 남는 것이 실증 분포상 좋은 전략이라는 주장과 반론이 공존 |
| "가운데를 노려라" (The Conversation 등) | 가운데 슛의 성공률이 높다는 대중 분석. 다만 실패하면 더 비난받기 때문에 키커에게도 사회적 비용이 있음 |

## 3. 승부차기 순서: 선축 이점은 있는가

| 연구 | 표본 | 결과 |
|---|---|---|
| **Apesteguia & Palacios-Huerta 2010** (*AER*) | 129회 | 먼저 차는 팀 승률 60.5%, **21%p 우위** → 큰 반향, IFAB의 **ABBA 방식 시범 도입**(2017)의 근거 |
| **Kocher, Lenz & Sutter 2012** (*Management Science*) | 540회 | **유의한 선축 이점 없음** (53.4%) |
| Palacios-Huerta 2014 | 1,001회 | 60.6% (이점 재확인) |
| Da Silva et al. 2018 | | 59.5% (유의) |
| Arrondel et al. 2019 | 프랑스 252회 | 이점 없음 |
| van Ours & van Tuijl (네덜란드 컵) | | 이점 있음. 후축 팀이 받는 심리적 압박으로 설명 |
| **Vandebroek, McCann & Vroom 2018**, *A comparison of penalty shootout designs* (arXiv 1806.01114) | 시뮬레이션 | 효과가 작으면 **500회 정도로는 검출력이 부족** → 결과가 엇갈리는 원인. ABBA 등 대안 방식의 공정성 비교 |
| 순서 계산법·도박사의 오류 연구 | | "직전 키커가 실축하면 다음 키커도?" 같은 순서 의존성 |

→ 아직 결론이 나지 않았습니다. 표본을 크게 모으면(전 세계 컵대회, 청소년·여자 대회, **2026 월드컵** 추가) 다시 검증할 여지가 있습니다.

## 4. 심리: 압박, 초킹, 회피 행동

| 연구 | 핵심 |
|---|---|
| **Jordet & Hartman 2008** (*J. Sport & Exercise Psychology*) | 월드컵·유로·챔스 승부차기 36회, 359킥. **"실축하면 패배"인 킥**에서 키커가 골키퍼에게 등을 돌리고 서두르는 **회피 행동**을 보이고, 성공률이 낮음 |
| Jordet 2007~2009 연구들 | 국가 지위가 높을수록(스타가 많을수록) 승부차기 성적이 나쁨. 개인 성공 후 세리머니 같은 행동이 팀 결과와 관련 |
| Jordet (2026 월드컵 AP 인터뷰) | **휘슬 직후 바로 출발한 키커가 2~5초 기다린 키커보다 더 많이 실축** |
| Jordet, *Pressure: Lessons from the Psychology of the Penalty Shootout* (책) | 대중서 정리 |
| 약 5만 개 유럽 PK 연구 (PMC11627389) | **승부차기 성공률은 일반 PK보다 낮고, 전담 키커도 마찬가지** → 원인은 골키퍼가 아니라 키커 수행 저하 |
| Wilson, Wood & Vine 2009 (Exeter) | **불안한 키커는 골키퍼를 더 오래 응시**하고, 그 결과 슛이 골키퍼 쪽으로 몰림 (주의 통제 이론) |

## 5. 지각-운동: 키커 전략과 시선

| 연구 | 핵심 |
|---|---|
| **van der Kamp 2006**; **Noël & van der Kamp 2012** | **골키퍼 의존 전략**(골키퍼가 먼저 움직이는 걸 보고 반대로 차기) vs **골키퍼 비의존 전략**(미리 정한 방향으로 차기). 비의존 전략이 더 정확한 킥 제어와 관련 |
| **Wood & Wilson 2010** (*A moving goalkeeper distracts penalty takers*) | 아이트래커를 쓴 실험. **팔을 흔드는 골키퍼**는 키커의 시선을 끌어 정확도를 떨어뜨림 |
| Wood & Wilson (중앙 응시 연구) | 시선이 가운데에 머물면 구석을 노려도 슛이 중앙으로 몰림 |
| Furley et al. 2016/2018 (*Frontiers*) | 실험실 결과가 **실제 승부차기**에서도 나타나는지 검증 |
| Masters, van der Kamp & Jackson 2007 (*Psychological Science*) | 골키퍼가 **중앙에서 몇 cm만 비켜 서도** 키커가 무의식적으로 넓은 쪽으로 차는 경향 (이번 검색에서 원문은 재확인하지 못함) |

## 6. 골키퍼 능력·규정 변화

| 연구 | 핵심 |
|---|---|
| **Bornkamp et al. 2009** (분데스리가, 계층적 베이즈) | 골키퍼 개인 PK 선방 능력 차이는 **통계적으로 거의 검출되지 않음** |
| 챔스·유로파 2018~2022 PK 103개 연구 (*Motricidade* 2024) | 평균 선방률 22.3%(골키퍼별 9.8~38.8%), 선방에 영향을 주는 요인을 탐색 |
| **2019 규정 변경**(골키퍼는 킥 순간 한 발만 골라인에 있으면 됨) — 운동학 연구 (*Scientific Reports* 2022, PMC9630263) | 골키퍼 6명 실험: 새 규정에서 **더 멀리, 더 빠르게 다이빙**. 다만 **실제 경기 선방률에 미친 효과를 분리한 연구는 찾지 못함** |
| 현행 Law 14 (2025/26, 2026/27) | 침범(encroachment) 처벌 조건 등 세부 규정 |

## 7. 통계: 실력인가 운인가

| 연구 | 핵심 |
|---|---|
| **Hanck & Arnold 2023** (*AStA Advances in Statistical Analysis*) | 분데스리가 1963~2021 키커 순위를 계층적 베이즈로 산출. 키커당 표본이 작아 **빈도주의 추정은 신뢰하기 어렵고 축소(shrinkage)가 필수** |
| American Soccer Analysis 2021, *Priors and Penalties* | 경험적 베이즈로 키커 랭킹. DB 선수의 73%는 PK 경험이 0 |
| **Deb 2026** (*J. Sports Analytics*, *Skill or chance?*) | 승부차기에서 지속적인 개인 효과는 작음. **실력 비중의 사후 추정치가 0에 가까움** → 승부차기는 대부분 운 |
| Harvard Sports Analysis, *How likely are keeper penalties?* | 골키퍼가 PK를 차는 경우 분석 |

## 8. 머신러닝·컴퓨터 비전: 방향 예측

| 연구 | 데이터 | 결과 |
|---|---|---|
| Pose + 기보 분석 결합 연구 (*Frontiers* 2022, PMC8964455) | OpenPose로 PK 영상 34개의 신체 각도 측정 | 자세 기반 PK 전략 분석의 초기 사례 |
| Salazar & Alatrista-Salas 2024 (ICMLT) | 분할 + 3D 자세 | 딥러닝 모델 3종 비교 |
| **Freire-Obregón et al.** (LNCS) | 수작업 주석 PK 영상 약 1,010개 | 킥 이전 움직임으로 좌/우 예측 **최대 63.9%**, 실제 골키퍼의 판단보다 높음 |
| *Predicting Soccer PK Direction Using Human Action Recognition* (arXiv 2507.12617) | 트래킹 + 행동 인식 임베딩 | 3클래스 정확도 약 52%. 인간 골키퍼 기준선보다 높다고 주장 |
| **Ranasinghe & Ranasinghe 2025** (arXiv 2509.26088, LNCS 2026) | PK 755개 | RGB(MobileNetV2) + 키포인트(Attention LSTM) 이중 분기, **89%** (공개 여부 불명, 데이터 구성이 불명확) |
| 학생·석사 프로젝트(GitHub: KickSense, MobileNetV3+GRU, YOLOv7-Pose+LSTM) | | 재현 가능한 출발 코드 |

→ **정확도 52%부터 89%까지 편차가 크고, 데이터셋·분할·클래스 정의가 제각각이며, 공개 벤치마크가 없습니다.** 이 분야의 가장 큰 약점입니다.

---

## 9. 페널티킥 데이터 구하는 법

| 소스 | 내용 | 비고 |
|---|---|---|
| **StatsBomb Open Data** | PK(`shot.type = Penalty`)와 승부차기(`period = 5`)에 **골문 내 도착 좌표(y, z)**, 골키퍼 위치 프리즈프레임, 사용한 발, 결과가 있음 | 방향과 높이를 정확히 얻을 수 있는 거의 유일한 공개 소스. 월드컵·유로·코파 승부차기 포함 |
| **Transfermarkt** | 선수별 커리어 PK 기록(성공/실축/선방, 상대 골키퍼, 경기), 골키퍼별 PK 선방 기록 | 수만 건 규모. 방향 정보는 없음. 크롤링 시 요청 간격 필요 |
| Wikipedia | 주요 대회 승부차기 순서·결과 | 선축 이점 연구용 |
| Kaggle | 월드컵 PK 9구역 데이터, EPL 2016/17 PK 103개(방향 + 골키퍼 방향, CC0) 등 | 소규모 |
| 영상 | YouTube 하이라이트, SoccerNet(PK 장면 일부) | 비전 연구용. 저작권 주의 |
| Understat / FotMob | PK 여부 표시가 있는 슈팅 데이터 | |

---

## 10. 연구 공백과 프로젝트 아이디어

| # | 공백 | 프로젝트 아이디어 | 참신성 | 도전성 | 현실성 |
|---|---|---|---|---|---|
| P1 | 비전 방향 예측에 **공개 벤치마크가 없고**, "언제부터 예측 가능해지는가"를 묻지 않음 | **키커 '가독성(readability)' 지표**: 공을 차기 t초 전 프레임까지만 보고 방향을 예측하는 모델을 학습하고, **정확도가 우연 수준을 넘는 시점**을 키커별로 측정. 늦게 읽힐수록 좋은 키커인지(디셉션), 골키퍼 의존 전략과 관련 있는지 검증 | ★★★ | ★★★ | ★★ (영상 수백 개를 직접 라벨링해야 함) |
| P2 | 2019 한 발 규정, VAR 침범 판정이 **실제 선방률에 미친 효과를 분리한 연구가 없음** | Transfermarkt 리그별 PK 수만 건으로 **단절 시계열(ITS) / 이중차분(DiD)**. 규정 적용 시점이 리그·대회별로 다른 점을 활용 | ★★ | ★★ | ★★★ |
| P3 | 선축 이점 논쟁이 **검출력 부족**으로 미해결 | 전 세계 승부차기를 최대한 모아(Wikipedia·Transfermarkt, 2026 월드컵 포함) 검출력 분석부터 수행. 리그 수준·성별·시대별 이질성을 함께 검증 | ★★ | ★★ | ★★★ |
| P4 | 압박을 "실축하면 패배" 같은 **이진 변수**로만 정의 | 실시간 승리확률 모델로 **킥의 레버리지**(성공/실패 시 승리확률 차이)를 연속 변수로 정의하고, 계층적 베이즈로 "압박에 강한 키커"를 축소 추정. 2차 문서의 "재미/서스펜스" 주제와 모델 공유 가능 | ★★★ | ★★ | ★★★ |
| P5 | 게임이론 검증이 집계 위주이고 **개인별 균형 이탈 탐지**는 드묾 | StatsBomb의 방향 데이터 + 키커별 계층 모델로 "예측 가능한 키커"(특정 방향 편향, 직전 킥 따라하기)를 찾고, 골키퍼가 이를 활용했는지 측정 | ★★ | ★★ | ★★ (키커별 표본 부족) |
| P6 | 골키퍼 PK 능력이 **검출되지 않는다**는 결과(2009) 이후 업데이트 부족 | 방향 선택 정확도(맞는 쪽으로 다이빙)와 선방(다이빙 거리·타이밍)을 분리해 **"읽기 능력" vs "도달 능력"** 으로 분해 | ★★ | ★★ | ★★ |

### 추천 조합
- **딥러닝 비중을 원하면 P1**: 비전(자세 추정 + 시계열) + 시간별 예측가능성 분석이 들어가서 1차 문서에서 생각하셨던 "순간적인 능력을 비전으로 수치화하기"와 바로 이어집니다. 라벨링 부담이 있으니 키커 20~30명 × 10킥 이상으로 범위를 좁히세요.
- **현실성을 원하면 P2 + P4**: 데이터 크롤링만으로 가능하고, 인과 추론과 베이즈 모델로 도전성을 확보할 수 있습니다.
- 페널티킥은 단독 주제로도 충분하지만, **메인 주제(빌드업·오프더볼)의 부록**으로 넣기에는 결이 다릅니다. 하나를 고르시길 권합니다.

---

## 참고 링크

- Palacios-Huerta 균형 검증 해설: https://qz.com/228958/the-only-penalty-kick-strategy-is-not-having-a-strategy
- 골키퍼 의사결정 연구 (*Should I stay or should I go?*): https://lida.sport-iat.de/twm/Record/4019956?lng=en
- 2023 리뷰 (*Asian J. Sport & Exercise Psychology*): https://doaj.org/article/8e176597417e41d79021626a57cd94a2
- 가운데를 노려라 (The Conversation): https://theconversation.com/aim-for-the-middle-it-could-be-your-best-shot-for-a-goal-in-a-penalty-shootout-99679
- Bransen, Janssen & Davis 2025: https://arxiv.org/abs/2505.24629
- Vandebroek et al. 2018, Shootout designs: https://arxiv.org/abs/1806.01114
- Kocher, Lenz & Sutter (IZA DP 4846): https://www.iza.org/publications/dp4846
- Jordet & Hartman 2008: https://nih.brage.unit.no/nih-xmlui/handle/11250/170403
- 2026 월드컵 승부차기 압박 (AP): https://www.ksat.com/sports/2026/06/30/penalty-shootouts-at-the-world-cup-are-a-drama-of-inhumane-pressure/
- Gaze & keeper-dependent 전략 (*Frontiers* 2019): https://www.frontiersin.org/journals/sports-and-active-living/articles/10.3389/fspor.2019.00069/full
- Wood & Wilson 2010: https://hira.hope.ac.uk/id/eprint/348/
- Wilson et al., Anxiety & attentional control: https://ore.exeter.ac.uk/repository/handle/10036/3053
- Furley et al. 2016: https://www.dshs-koeln.de/fileadmin/redaktion/Institute/Kognitions-_und_Sportspielforschung/Publikationen/Paper/Furley_2016_Attention-towards-the-goalkeeper-and-distraction-during-penalty-shootouts.pdf
- 골키퍼 존재가 키커 시선에 주는 영향: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5790805/
- Hanck & Arnold 2023: https://link.springer.com/article/10.1007/s10182-021-00420-w
- ASA, Priors and Penalties: https://www.americansocceranalysis.com/home/2021/11/19/priors-and-penalties-finding-the-best-penalty-takers-with-bayes
- Bornkamp et al. 2009: https://ideas.repec.org/h/spr/sprchp/978-3-7908-2121-5_4.html
- Deb 2026, Skill or chance?: https://research.iimb.ac.in/fac_pubs/1829
- 약 5만 PK 승부차기 vs 일반 PK: https://pmc.ncbi.nlm.nih.gov/articles/PMC11627389/
- 2019 한 발 규정 운동학: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9630263/
- 골키퍼 PK 선방 요인 (*Motricidade*): https://revistas.rcaap.pt/motricidade/article/view/31429
- Law 14 (2026/27): https://www.thefa.com/-/media/files/thefaportal/governance-docs/laws-of-the-game/2026-27/law-14---the-penalty-kick.ashx
- Ranasinghe & Ranasinghe 2025: https://arxiv.org/abs/2509.26088
- PK 방향 예측 (행동 인식): https://arxiv.org/abs/2507.12617
- 자세 기반 PK 전략 분석: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8964455/
- Freire-Obregón et al.: https://accedacris.ulpgc.es/handle/10553/154924
- EPL 2016/17 PK 데이터 분석 (TDS): https://towardsdatascience.com/?p=608561
- 코드: https://github.com/ibrahimtariq1804/KickSense · https://github.com/Opaksbolu/Soccer-Penalty-Direction-Prediction · https://github.com/gabriellavinco/PenaltyKickPrediction
