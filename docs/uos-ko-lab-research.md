# 서울시립대 고상기 교수 연구실(CIDA) 축구 연구 정리와 주제 연결

> 작성일: 2026-10-29 · 출처: 연구실 홈페이지 [cida.uos.ac.kr/publication.html](https://cida.uos.ac.kr/publication.html), arXiv, Hudl, MIT Sloan
> 관련 문서: [`data-sources-and-topics.md`](./data-sources-and-topics.md) · [`literature-review-and-gaps.md`](./literature-review-and-gaps.md) · [`penalty-kick-literature.md`](./penalty-kick-literature.md) · [`cognitive-bias-literature.md`](./cognitive-bias-literature.md)

연구실 홈페이지에 정리된 축구 관련 논문은 **국제학회·저널 14편 + 국내학회 7편**입니다. 주요 공저자는 이민호, 조건희, 홍미루, 김현성(KAIST·핏투게더), 최한준, Pascal Bauer(DFB)입니다. 연구실 소개의 Sports Data Analytics 분야는 **선수 경기력 평가, 다중 에이전트 궤적 추론, 포메이션 분석, 전략 최적화**를 다룹니다.

---

## 1. 논문 목록 (주제별)

### 1-1. 선수 가치 평가 (Player valuation)

| 논문 | 학회 | 핵심 | 데이터 |
|---|---|---|---|
| **exPress**: *Contextual Valuation of Individual Players Within Pressing Situations in Soccer* (이민호, 조건희, 홍미루, Bauer, 고상기) | **MIT Sloan SAC 2025** | 압박 상황에서 **선수 위치와 공간 역학**으로 압박 효과를 평가. **Expected Pressing Value(xP)** 제안. 여러 베이스라인 중 XGBoost가 최고 성능. 선수 위치 조정이 압박 전략과 **압박 저항(press resistance)** 을 어떻게 개선하는지 전술적 시사점 제시 | **이벤트 + 360 데이터** (StatsBomb 360 형식) |
| *Contextual Evaluation of Individual Contributions from Pressing Situations in Football* (같은 저자) | MLSA 2025 (Springer CCIS 2833) | exPress의 정식 출판판 | 동일 |
| **Valuing La Pausa**: *Quantifying Optimal Pass Timing Beyond Speed* (같은 저자) | **MIT Sloan SAC 2026, 결선 진출(200편+ 중 상위 7편)** | 패스의 **타이밍**(서두르지 않고 기다리는 판단)을 가치화. 공간적 판단과 시간적 판단을 결합한 지표. 시간적 판단을 넣으면 팀 경기당 승점과의 상관이 유의하게 높아진다는 보고 | (초록 원문 미확인) |
| **ScoutGPT / EventGPT**: *Capturing Player Impact from Team Action Sequences: A GPT-Based Framework for Transfer Fit* (이민호, 홍미루, 조건희, 소재희, Bauer, 고상기; arXiv 2512.17266) | **Hudl Performance Insights 2025** (런던 발표) | 팀 액션 시퀀스를 GPT로 학습. **학습된 선수 임베딩을 다른 팀의 이벤트 시퀀스에 넣어** 그 선수가 새 팀·전술에서 어떻게 행동하고 어떤 가치를 낼지 시뮬레이션 → **이적 적합도**. 다음 이벤트 예측에서 시퀀스 베이스라인보다 우수 | **EPL 5시즌 이벤트 데이터** |
| *Modeling Matches as Language: A Generative Transformer Approach for Counterfactual Player Valuation in Football* (홍미루, 이민호, 조건희, 조혁제, 김현성, Bauer, 고상기; arXiv 2603.15212) | **ECML PKDD 2026** (Applied Data Science) | 경기 이벤트를 토큰으로 보는 NanoGPT 기반 Transformer + 몬테카를로 시뮬레이션으로 **가상 라인업·이적의 반사실 결과**를 추정. 선수 이적 시뮬레이션이 공격 전진과 득점확률을 측정 가능하게 바꿈 | **K리그 이벤트 데이터** |
| 공간 행동 가치 기반 축구 라인업 최적화 (정송윤, 조건희, 고상기) | 한국컴퓨터종합학술대회(KCC) 2026 | 공간적 행동 가치로 최적 라인업 탐색 | |
| 딥러닝 기반 축구 경기 플레이 가치 평가 알고리즘 (조건희, 고상기) | KCC 2023 | 플레이 가치 평가 | |
| 딥러닝 기반 패스 의도 예측 알고리즘 (조건희, 강민구, 고상기) | KCC 2024 | 패스 의도(누구에게 주려 했나) 예측 | |
| 3D 공 궤적과 문맥 정보를 이용한 크로스 결과 예측 (홍미루, 이민호, 고상기) | KCC 2026 | 크로스 성공 예측 | |

### 1-2. 궤적 추론·복원 (Trajectory inference / imputation)

| 논문 | 학회 | 핵심 |
|---|---|---|
| ***Imputing Multi-Agent Trajectories from Event and Snapshot Data in Soccer*** (조건희, 홍미루, 이민호, 최한준, Bauer, 고상기) | **CIKM 2025** | **이벤트 + 360 스냅샷만으로 모든 이벤트 시점의 22명 위치를 예측.** 공간·시간 어텐션. 13경기에서 **평균 위치 오차 5.84m**. 복원한 위치로 **Pitch Control**(원래 트래킹이 필요한 과제)까지 계산해 검증 |
| 이벤트 및 스냅샷 데이터를 이용한 선수 위치 예측 모델 (조건희, 홍미루, 고상기) | KCC 2025 | 위 연구의 국내판 |
| *Trajectory Imputation in Multi-Agent Sports with Derivative-Accumulating Self-Ensemble* (최한준, 김현성 외) | **ECML PKDD 2025** | 결측 궤적 복원, 미분 누적 자기앙상블 |
| *Ball Trajectory Inference from Multi-Agent Sports Contexts Using Set Transformer and Hierarchical Bi-LSTM* (김현성 외) | **KDD 2023** | 선수 궤적만으로 **공 궤적 추론**. 점유자를 먼저 추정하는 계층 구조 |
| ***PathCRF**: Ball-Free Soccer Event Detection via Possession Path Inference from Player Trajectories* (김현성, 이건희, 서상우, 고상기, 윤진성, 박찬영; arXiv 2602.12080) | **KDD 2026** | **공 데이터 없이 선수 트래킹만으로 이벤트(볼 컨트롤·패스) 검출.** 선수를 노드로 한 동적 그래프에서 시점마다 점유 엣지를 고르고 CRF + Viterbi로 디코딩. 코드 공개 표시 |

### 1-3. 트래킹·포메이션·선수 표현

| 논문 | 학회 | 핵심 |
|---|---|---|
| ***SoccerCPD**: Formation and role change-point detection* (김현성 외) | **KDD 2022** | 경기 중 **포메이션과 선수 역할이 바뀌는 시점** 자동 탐지 |
| 국면 인지형 온라인 포메이션 변화점 탐지 (조혁제, 홍미루, 고상기) | KCC 2026 | SoccerCPD의 실시간·국면별 확장 |
| ***6MapNet**: Representing Soccer Players from Tracking Data by a Triplet Network* (김현성 외) | MLSA 2021 | 트래킹 기반 **선수 표현 학습**(삼중항 네트워크) → 비슷한 역할·스타일 선수 찾기 |
| *Contextual Sprint Classification in Soccer Based on Deep Learning* (김현성, 조건희, 윤진성, 고상기) | IT4PSS @ IJCAI 2024 | 스프린트를 **전술 문맥에 따라 분류**(침투, 커버 등) |
| *Cost-Efficient and Bias-Robust Sports Player Tracking by Integrating GPS and Video* | MLSA 2022 | GPS + 영상 결합 추적 |
| *A Deep Learning Approach for Fatigue Prediction Using GPS Data and RPE* | IEEE Access 2022 | GPS·주관적 운동강도로 피로 예측 |
| 딥러닝 기반 축구 영상 좌표 추적 알고리즘 | KSC 2021 | 영상 → 좌표 |

### 1-4. 연구실 외부지만 같은 계열 (김현성: KAIST·핏투게더)
- **DEFCON** (arXiv 2512.10355, 2025): 수비 기여 평가. 결론에서 **역할 탐지(SoccerCPD) 결합, 공수 통합 평가**를 향후 과제로 명시
- **ELASTIC** (MLSA 2025): 이벤트-트래킹 동기화

---

## 2. 연구실 연구의 흐름 (한눈에)

```
이벤트 + 360 스냅샷 ──► 궤적 복원 (CIKM'25) ──► 트래킹 수준 분석 (Pitch Control 등)
        │                                               │
        ├──► 압박 가치 exPress (Sloan'25) ──► 패스 타이밍 La Pausa (Sloan'26)
        │
        └──► 이벤트 = 언어 (ScoutGPT, HPI'25 → ECML PKDD'26) ──► 이적 적합도 · 반사실 가치 · 라인업 최적화

트래킹만 ──► 공 궤적 추론 (KDD'23) ──► 공 없는 이벤트 검출 PathCRF (KDD'26)
        └──► 포메이션·역할 변화 SoccerCPD (KDD'22) · 선수 표현 6MapNet · 스프린트 분류
```

연구실의 일관된 관심사는 두 가지로 보입니다.
1. **비싼 데이터 없이 싼 데이터로**: 이벤트 → 트래킹 복원, 트래킹 → 공·이벤트 복원
2. **문맥을 반영한 선수 가치**: 압박, 타이밍, 이적 적합도를 반사실적으로 평가

---

## 3. 지금까지의 추천 주제와 연결 (조정)

이 연구들과 **겹치는지**, **확장할 수 있는지**를 기준으로 추천을 다시 정리했습니다. 교수님 연구실의 코드·모델을 출발점으로 쓸 수 있다면 8주 안에 끝낼 가능성이 크게 높아집니다.

| 기존 아이디어 | 연구실 연구와의 관계 | 조정 |
|---|---|---|
| (2차 1순위) 압박 조건부 빌드업 가치 & 센터백 발밑 | **exPress가 압박하는 쪽의 xP를 같은 360 데이터로 이미 계산**하고, 응용으로 "압박 저항"을 언급. **La Pausa가 패스 타이밍**을 다룸 | ⚠️ 부분 중복. 대신 **"exPress의 거울상: 압박받는 쪽의 탈압박 가치"** 로 명시적으로 확장하면 가장 자연스러움. xP 모델을 그대로 받아 "압박 성공 기대확률 대비 실제로 벗어난 정도"를 선수 지표로 만들고, 빌드업 효과의 인과 분석(RQ1)을 추가 기여로 둠. **La Pausa와 겹치지 않도록 타이밍이 아닌 공간·선택 측면에 집중** |
| (2차 2순위) 중계 트래킹 결측에 대한 오프더볼 지표 강건성 | 연구실의 **궤적 복원(CIKM'25, ECML'25)** 은 Pitch Control까지만 검증 | ✅ **직접 확장.** "복원한 궤적으로 계산한 **선수 단위 지표**(exPress xP, OBSO, Pressing Intensity)의 순위가 원본과 얼마나 일치하는가"는 연구실 논문이 다루지 않은 다음 단계. 1순위로 올릴 만함 |
| (2차 3순위) 조직 영향력·리더십 | ScoutGPT의 "선수 임베딩 교체" 반사실과 같은 아이디어 | ✅ ScoutGPT식 **"이 선수를 평균 선수 임베딩으로 바꾸면 팀 시퀀스가 어떻게 바뀌나"** 로 구현하면 트래킹 없이 이벤트 데이터만으로 가능 |
| (1차) 포지션 전환 / 멀티포지션 | **6MapNet**(선수 표현), **SoccerCPD**(역할 탐지), **ScoutGPT**(새 환경 시뮬레이션) | ✅ **"ScoutGPT로 포지션 전환 시뮬레이션"**: 선수 임베딩을 다른 역할 슬롯에 넣어 가치 변화를 예측하고, 실제 전환 사례(Transfermarkt)로 검증. 연구실은 "팀 이적"만 다뤘고 **"포지션 이적"은 미개척** |
| (1차) 특정 팀에 선수 추천 | ScoutGPT가 정확히 이 주제 | ⚠️ 그대로 하면 중복. 공개 데이터(StatsBomb 2015/16 빅5)로 **재현 + 검증 방법론(실제 이적 후 성과로 사후 검증)** 을 기여로 삼는 방향은 가능 |
| (인지편향 B1) 평점의 운 보상 | 연구실의 가치 모델(플레이 가치 평가, exPress)을 **객관 기준선**으로 쓸 수 있음 | ✅ 겹치지 않음. 연구실 모델 = 객관 가치, 언론·앱 평점 = 주관 평가로 놓고 차이를 편향으로 분석 |
| (인지편향 B3) 수비 예방 기여 저평가 | DEFCON(김현성) 결론과 일치 | ✅ DEFCON·exPress 지표를 받아 시장가치·평점과 비교 |
| (페널티킥) | 연구실에 페널티킥 연구 없음 | 독립 주제 |
| 비전(트래핑·스캐닝) | 연구실은 영상 → 좌표(2021) 정도 | 독립 주제, 위험 높음 |
| 오프더볼 런 평가 | **스프린트 문맥 분류(IJCAI'24)** 가 런 유형을 분류 | ✅ 분류된 런에 가치(OBSO, 공간 생성)를 붙이는 확장 |

---

## 4. 최종 추천 (연구실 연구 반영)

### ⭐ 1순위: "복원된 궤적으로 선수를 평가해도 되는가? — 이벤트·스냅샷 기반 궤적 복원의 하위 지표 신뢰도 검증과 개선"

- **배경**: 연구실은 이벤트 + 360만으로 전원 위치를 복원했고(CIKM'25, 오차 5.84m), Pitch Control로 검증했습니다. 하지만 **선수 평가 지표(xP, OBSO, DEFCON류)에 그대로 써도 순위가 유지되는지**는 아직 보고되지 않았습니다. 이 질문이 풀려야 트래킹이 없는 대다수 리그(K리그 하위 리그 포함)에서 오프더볼 평가를 쓸 수 있습니다.
- **데이터**: Sportec 7경기 + PFF 월드컵 2022(정답 트래킹). 여기서 "이벤트 + 360 형태의 스냅샷"을 **인위적으로 만들어** 복원 → 원본과 비교합니다. SkillCorner(실제 중계 결측)에도 적용합니다.
- **방법**
  1. 연구실 방식의 복원 모델(공간·시간 어텐션)을 재현하거나, 공개 코드가 있으면 사용합니다.
  2. 원본 vs 복원 궤적에서 **선수 단위 지표**를 각각 계산합니다(Pitch Control 기반 OBSO, Pressing Intensity, exPress xP).
  3. 순위 상관, 상위 k명 일치율, 지표별 민감도를 측정합니다. "어떤 지표가 복원 오차에 강건한가"를 정리합니다.
  4. **개선**: 하위 지표 손실을 직접 학습 목표에 넣는 **과업 인지(task-aware) 복원**이나 불확실성 전파(여러 샘플을 생성한 뒤 지표의 분포 계산)를 제안합니다.
- **장점**: 정답이 있어서 평가가 깔끔하고, 딥러닝 비중이 높습니다. **연구실의 최신 연구를 그대로 확장**합니다.

### 2순위: "탈압박의 가치 — exPress의 거울상으로 본 센터백·골키퍼 빌드업 지표와 빌드업의 인과 효과"
- exPress의 xP(압박 성공 기대)를 받아, **압박받는 선수가 기대보다 얼마나 잘 벗어났는가**를 선수 지표로 정의합니다.
- 팀 수준에서는 "같은 압박 강도에서 짧은 빌드업 vs 롱볼"의 기대가치 차이를 인과적으로 추정합니다.
- La Pausa(타이밍)와 구분해 **공간·선택** 측면에 집중합니다.
- 데이터: StatsBomb 360(exPress와 같은 형식), 2015/16 빅5(`under_pressure` 표시).

### 3순위: "포지션 이적 시뮬레이션 — 생성형 이벤트 모델로 찾는 멀티포지션의 조건"
- ScoutGPT의 "선수 임베딩 교체"를 **팀이 아니라 역할 슬롯**에 적용합니다. 예: 풀백을 윙 슬롯에 넣으면?
- 실제 포지션 전환 사례로 사후 검증합니다. 6MapNet식 역할 표현과도 비교합니다.
- 데이터: StatsBomb 2015/16 빅5 + 레버쿠젠 23/24 등 시즌 단위 이벤트, Transfermarkt 포지션 이력.

### 4순위: "평점은 운을 얼마나 보상하는가" (인지편향 B1)
- 연구실 가치 모델을 객관 기준선으로, 앱·언론 평점을 주관 평가로 놓고 결과 편향과 운의 과잉보상을 측정합니다. 겹침이 없는 독립 주제입니다.

> **교수님 면담 때 확인할 것**: ① 연구실 모델(CIKM'25 복원, exPress, ScoutGPT)의 코드·체크포인트를 학부 프로젝트에서 쓸 수 있는지 ② 연구실이 쓰는 데이터(EPL 5시즌, K리그 이벤트)에 접근할 수 있는지, 아니면 공개 데이터로만 해야 하는지 ③ 진행 중인 연구실 프로젝트와 겹치는지.

---

## 참고 링크
- 연구실 논문 목록: https://cida.uos.ac.kr/publication.html · 연구실 홈: https://cida.uos.ac.kr/
- exPress (Sloan 2025): https://www.sloansportsconference.com/research-papers/contextual-valuation-of-individual-players-within-pressing-situations-in-football · 연구실 소식: https://cida.uos.ac.kr/2025/05/10/mit-sloan-2025.html · MLSA 출판판: https://researchr.org/publication/LeeJHBK25
- ScoutGPT / Transfer Fit: https://arxiv.org/abs/2512.17266 · Hudl PDF: https://static.hudl.com/craft/performance-insights-research-stage/2025/Capturing-Player-Impact-From-Team-Action-Sequences-Minho-Lee_2025-12-03-151414_edbt.pdf · Hudl 블로그: https://www.hudl.com/blog/hpi-25-minho-lee
- Modeling Matches as Language: https://arxiv.org/abs/2603.15212
- 궤적 복원 (CIKM 2025): https://pure.uos.ac.kr/en/publications/imputing-multi-agent-trajectories-from-event-and-snapshot-data-in/
- PathCRF: https://arxiv.org/abs/2602.12080
- 공 궤적 추론: https://arxiv.org/abs/2306.08206 · SoccerCPD: https://arxiv.org/abs/2206.10926
- DEFCON: https://arxiv.org/abs/2512.10355
- 고상기 교수 프로필: https://pure.uos.ac.kr/en/persons/sang-ki-ko/ · Google Scholar: https://scholar.google.com/citations?hl=en&user=byYGU_AAAAAJ
