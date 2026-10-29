# 선행연구 조사 · 연구 공백 · 주제 추천 (2차)

> 작성일: 2026-10-27 · 1차 문서: [`data-sources-and-topics.md`](./data-sources-and-topics.md)
> 이 문서에서 다루는 것
> 1. 오프더볼(off-ball) 선수 분석 선행연구 정리
> 2. "수비수의 발밑(볼 플레잉 능력)" 수치화와 "빌드업이 실제로 중요한가"를 다룬 연구
> 3. 직접 찾은 연구 공백(gap)
> 4. 공백을 바탕으로 한 주제 추천 (1차 추천 수정 포함)

---

## ⚠️ 먼저 알아둘 점: 1차 추천 수정이 필요합니다

1차 문서의 1순위였던 "그림자 팀(Ghost)으로 수비 오프더볼 기여 측정"은 **2025년 말~2026년 사이에 연달아 논문이 나온 영역**이었습니다.

| 논문 | 시기 | 겹치는 부분 |
|---|---|---|
| Kim et al., **DEFCON** — *Better Prevent than Tackle* (arXiv 2512.10355) | 2025.12 | GAT로 공격 옵션별 성공확률·EPV·수비수 책임도를 추정하고, 수비수 개인에게 EPV 감소분을 분배합니다. 에레디비시 트래킹 사용 |
| Bischofberger et al., ***Blame is easier than praise*** (arXiv 2606.19931) | 2026.06 | **월드컵 2022 64경기**(우리가 쓰려던 PFF 데이터와 같은 대회)와 여자 분데스리가, 3. 리가를 사용합니다. 역할 조건부 기준선으로 수비 오프더볼 책임을 배분하고, 코드도 공개했습니다 |
| Groom et al. (arXiv 2601.00748) | 2026.01 | HMM으로 대인/지역방어 배정을 추론하고 **역할 조건부 ghosting**을 수행합니다(코너킥 한정) |
| Everett et al., GAT 기반 수비 영향 (IEEE DSAA) | 2025 | 수비수 어텐션을 제거했을 때 패스 성공확률이 어떻게 변하는지 측정합니다 |

즉, **"수비수의 오프더볼 기여를 반사실로 평가한다"는 아이디어 자체는 더 이상 새롭지 않습니다.** 대신 이 논문들이 **스스로 밝힌 한계와 향후 과제**가 좋은 출발점이 됩니다(3장 참고).

또한 이 분야 핵심 논문 다수가 **서울시립대(고상기 교수 연구실), KAIST, 핏투게더(Fitogether)** 쪽에서 나왔습니다. 김현성 등의 DEFCON·ELASTIC·SoccerCPD·공 궤적 추론, 이민호 등의 exPress가 그렇습니다. 수업 튜토리얼 저장소(`UOS-FootballDataAnalytics-Tutorial`)를 보면 같은 학교일 가능성이 높으니, **이 연구들을 확장하는 방향**이 지도교수님 입장에서도 가장 반가울 수 있습니다. 주제를 정하기 전에 교수님께 겹치는 부분이 있는지 한 번 확인하시길 권합니다.

---

## 1. 오프더볼 선수 분석 선행연구 정리

공을 가진 시간은 선수 1명당 경기에서 평균 2~3분에 불과합니다. 나머지 시간을 평가하려는 연구는 크게 7갈래로 나뉩니다.

### 1-1. 공간 가치 모델: "어디가 얼마나 가치 있는 공간인가"

| 연구 | 핵심 아이디어 | 의의 / 한계 |
|---|---|---|
| Spearman et al. 2017, *Physics-based modeling of pass probabilities* | 선수의 도달 시간을 물리 모델로 계산해 패스 성공확률을 구합니다 | Pitch control의 원형 |
| Fernández & Bornn 2018, ***Wide Open Spaces*** (Sloan) | 공간 점유(occupation)와 공간 생성(generation)을 정량화합니다. 오프더볼 움직임이 동료에게 만들어 준 공간을 측정 | 오프더볼 "공간 창출" 평가의 출발점 |
| Spearman 2018, ***Beyond Expected Goals*** (Sloan) — **OBSO** | Off-Ball Scoring Opportunity = (공이 그 지점에 갈 확률) × (그 지점을 내가 통제할 확률) × (그 지점에서의 득점확률) | 해석이 쉬워서 이후 수많은 확장이 나왔습니다 |
| Fernández, Bornn & Cervone 2019/2021, **EPV** (Sloan / *Machine Learning*) | 딥러닝으로 프레임마다 점유 기대가치를 계산하고, 패스·드리블·슈팅 확률과 조건부 가치로 분해합니다 | DEFCON 등 최근 연구의 뼈대 |
| Fernández & Bornn 2020, **SoccerMap** (ECML PKDD) | 피치 전체 확률 지도를 출력하는 완전 합성곱 신경망 | 시각적으로 해석하기 좋습니다 |
| Power et al. 2017, *Not all passes are created equal* (KDD) | 트래킹 기반 패스의 위험(risk)과 보상(reward) | |
| Bekkers 2025, **Pressing Intensity** (arXiv 2501.04712) | Pitch control의 도달 시간을 이용해 수비수-공격수 쌍마다 압박 확률 행렬을 만듭니다 | `unravelsports`에 구현돼 있어 바로 쓸 수 있습니다 |

### 1-2. 공격 오프더볼: 침투·런·공간 창출 평가

| 연구 | 핵심 아이디어 | 의의 / 한계 |
|---|---|---|
| Teranishi, Tsutsui, Takeda & Fujii 2023, **C-OBSO** (arXiv 2206.01899) | 실제 움직임과 궤적 예측 모델이 만든 **참조 움직임**의 OBSO 차이 = "동료를 위한 득점기회 창출" | **반사실 오프더볼 평가의 대표 사례.** 연봉과 유의한 양의 상관 |
| Wu & Swartz, *Evaluation of Off-the-Ball Actions in Soccer* (SFU) | 오프더볼 움직임 전후의 상태가치를 비교합니다 | |
| Llana, Burriel, Madrero & Fernández 2022, *Is it worth the effort?* (arXiv 2204.02313) | 고강도 런을 점유가치 모델과 연결해 **"헛뛴 런" vs "가치 있는 런"** 을 구분합니다 | 피지컬 지표에 전술 문맥을 부여 |
| Yeung & Fujii 2024, Iwashita et al. 2024, Kono & Fujii 2024 | OBSO를 다른 스포츠·이벤트 데이터 환경으로 확장 | Fujii 연구실(나고야대)이 이 계열의 중심 |
| 상용: SkillCorner *Off-ball runs*, Gradient(PFF) *Measuring Off-Ball Movement* | 속도·가속 임계값으로 런을 검출하고 유형(침투, 오버랩, 지원 등)을 분류합니다 | 런 정의가 회사마다 다르고 학술적 검증은 부족합니다 |

### 1-3. 포지셔닝 평가: 강화학습·모방학습

| 연구 | 핵심 아이디어 |
|---|---|
| Dick & Brefeld 2019, *Learning to Rate Player Positioning in Soccer* (*Big Data*) | 심층 강화학습으로 상황 가치함수를 학습해 포지셔닝을 평가합니다 |
| Le et al. 2017, ***Data-Driven Ghosting*** (Sloan) / *Coordinated Multi-Agent Imitation Learning* (ICML) | 리그 평균 수비수의 움직임을 모방학습으로 생성("ghost")하고, 실제와 비교합니다 | 
| Yeh et al. 2019, **GVRNN** (CVPR) | 그래프 + VRNN으로 다양한 다중 에이전트 궤적을 생성 |
| Liu et al. 2020 (GIM), Luo et al. 2020 (역강화학습), Rahimian et al. 2022/2023 | 액션 가치함수를 학습해 선수를 평가하고 의사결정을 최적화합니다 |
| Nakahara, Fujii 등 2023, multi-agent deep RL 기반 on/off-ball 행동 가치 | 공을 가진 선수와 갖지 않은 선수를 함께 평가 |

### 1-4. 수비 오프더볼 평가 (최근 가장 뜨거운 영역)

| 연구 | 단위 | 핵심 |
|---|---|---|
| Bransen & Van Haaren 2020, *Player Chemistry* — JDI (Sloan) | 경기 | 수비수가 있을 때 상대 공격 성과 vs 기대치 |
| Merhej et al. 2021, *What happened next?* (KDD) | 액션 | 태클·인터셉트가 제거한 잠재 xT |
| Stöckl et al. 2021, *Making offensive play predictable* (Sloan) | 상황 | GCN으로 수비수가 막은 패스 옵션을 분석합니다(정성적) |
| Toda, Teranishi, Kushiro & Fujii 2022 (PLOS ONE) | 팀 | 볼 탈취·피공격 확률 모델로 팀 수비를 평가 |
| Forcher et al. 2022 (스코핑 리뷰), 2024 (XAI로 수비 성공 예측) | 팀 | 트래킹 기반 수비 연구 총정리 |
| Bauer & Anzer 2021, 카운터프레싱 탐지 (*DMKD*) | 상황 | 분데스리가 트래킹으로 게겐프레싱을 자동 탐지 |
| **Lee, Jo, Hong, Bauer & Ko 2025, exPress** (Sloan) | 개인 | **압박 상황에서 개인 선수의 기여를 문맥에 따라 평가**합니다(UOS 고상기 교수 그룹) |
| Everett et al. 2025 (IEEE DSAA) | 개인 | GAT 어텐션을 제거해 수비 영향을 측정합니다. 패스만 다루고 슈팅은 제외 |
| **Kim et al. 2025, DEFCON** | 개인 | 공격 옵션별 성공확률·기대가치·수비 책임도를 GAT로 추정해 EPV 변화를 분배합니다. **실제 수비 액션 기반 점수는 시장가치와 상관이 없지만, "위협 허용 페널티"는 강한 상관**을 보였습니다 |
| Groom et al. 2026 | 개인 | 공분산 의존 HMM으로 대인/지역 배정 → 역할 조건부 ghost (코너킥) |
| **Bischofberger et al. 2026, *Blame is easier than praise*** | 개인 | 수비 압박 영역(DPA)으로 책임을 배분합니다. "칭찬"(잘 막음)보다 **"비난"(위치 실수로 허용)** 을 측정하는 쪽이 훨씬 타당했습니다. 기존 인기 수비 지표 상당수가 타당성이 낮다는 결론 |

**흐름 요약**: 액션(태클 수) → 팀 단위 → 개인 반사실 책임 배분으로 발전했습니다. 공통 결론은 **"수비 액션 수는 수비 능력을 거의 설명하지 못한다"** 입니다.

### 1-5. 생성형 궤적 모델 (ghost의 최신판)

| 연구 | 내용 |
|---|---|
| Wang et al. 2024, **TacticAI** (*Nature Communications*, DeepMind × 리버풀) | 코너킥 상황 GNN: 수신자·슈팅 예측과 선수 배치 추천 |
| Kim et al. 2023, 공 궤적 추론 (KDD) | Set Transformer + 계층적 Bi-LSTM으로 선수 궤적만 보고 공 궤적을 추론 |
| 다중 에이전트 궤적 보간 (ECML PKDD), SoccerCPD (KDD 2022) | 결측 궤적 복원, 포메이션·역할 변화점 탐지 (김현성·고상기 등) |
| Sports-Traj 2024 (arXiv 2405.17680) | 스포츠 통합 궤적 생성 |
| **GenTac** (arXiv 2604.11786), **TacticGen** (arXiv 2604.18210, 1,432경기), 2026.04 | 확산 모델 기반 장기 다중 궤적 + 전술 이벤트 생성 |
| *Velocity completion for event-based positional data* (arXiv 2505.16199) | 이벤트 데이터의 위치 스냅샷에서 속도를 복원해 OBSO 같은 트래킹 모델을 적용 |

### 1-6. 집단 움직임·리더-팔로워

| 연구 | 내용 |
|---|---|
| Nagy et al. 2010 (*Nature*) | 비둘기 무리의 **방향 상관 지연시간(DCDT)** 으로 리더 위계를 측정 (원조) |
| *Quantitative analysis of leader-follower interactions between football players* | DCDT를 축구에 적용. 동료를 이끄는 선수는 상대 움직임도 이끄는 경향 |
| *Collective movement analysis reveals coordination tactics of team players* (Chaos, Solitons & Fractals, 2020) | 집단 움직임으로 팀 조직 전술을 분석. 동료와 움직임 상관이 높은 선수일수록 시장가치가 높다는 보고 |
| *Collective states and their transitions in football* (PLOS ONE 2021) | 팀이 정렬(polar) 상태와 무질서(swarm) 상태 사이를 빠르게 전환 |
| *Information-theoretical analysis of team dynamics* (2025, PMC11941434) | transfer entropy 등 정보이론으로 선수 간 영향을 측정 |

→ 리더-팔로워 분석은 **고전 통계(지연 상관, 정보이론) 수준에 머물러 있습니다.** 딥러닝 반사실 모델로 영향력을 측정하고 외부 라벨(주장 등)로 검증한 연구는 찾지 못했습니다.

### 1-7. 지각·인지: 스캐닝과 몸 방향

| 연구 | 내용 |
|---|---|
| Jordet et al. 2013 / 2020 (*Frontiers in Psychology*) | 수작업 영상 코딩. EPL 27명, 21경기, 9,574회 점유. **스캔 빈도가 높을수록 패스 성공확률이 높고(효과는 작음)**, CB·CM이 가장 많이 스캔하고, 강한 압박에서는 줄어듭니다 |
| 헤드밴드 IMU 연구 | 고개 회전을 센서로 측정. 스캔이 많을수록 패스 반응이 빠름 |
| Arbués-Sangüesa et al. 2020, *Using Player's Body-Orientation to Model Pass Feasibility* | 중계 영상에서 상체 방향을 추정(오차 중앙값 약 26°에서 딥러닝으로 약 12°)하고, 이를 패스 가능성 모델에 반영 |

→ **중계 영상에서 스캐닝(고개 돌림)을 자동 검출한 연구는 찾지 못했습니다.** 지금은 모두 수작업 코딩이나 센서에 의존합니다.

---

## 2. "수비수의 발밑"과 "빌드업은 정말 중요한가"

### 2-1. 수비수 볼 플레잉 능력을 수치화한 사례

| 구분 | 사례 | 측정 방식 | 평가 |
|---|---|---|---|
| 기본 지표 | 프로그레시브 패스/운반(FBref식: 자기 진영에서 10야드 이상 전진), 라인 브레이킹 패스 | 거리 임계값 | 압박·상대 블록 문맥을 무시합니다. 내려앉은 상대에게 패스를 많이 하면 숫자만 부풀려집니다 |
| 추세 | OptaPro: PL 센터백 90분당 패스 약 30개(2011/12) → 약 40개 | 집계 | 증가분 대부분은 높은 위치에서 나온 패스 |
| FIFA 기술 리포트 | U-20 월드컵 센터백의 전진 패스·수직 라인 브레이킹 패스 | 영상 코딩 | 상대가 내려앉아 압박 없이 볼을 주는 상황이 많다는 점을 스스로 지적 |
| 상용 | SkillCorner **Progressive Actions Under Intense Pressure** | 높은 압박 속에서 받은 볼을 8m 이상 전진시킨 비율. 압박 정도는 접근 시간 등 4요소로 산출 | 압박 문맥을 반영한 거의 유일한 지표지만, **독립적으로 검증되지 않았습니다** |
| 상용 | SkillCorner *Inside passes*(빌드업/창출 단계 × 압박 수준) | | 같은 한계 |
| 학술(패스 가치) | Power 2017 (risk/reward), Anzer & Bauer 2022 **xPass**, Robberechts 2023 **un-xPass**(창의성), QPass, VAEP/xT/OBV | 패스 성공확률 × 가치 변화 | 포지션 구분 없이 범용입니다. **센터백 빌드업에 특화하거나 압박 조건부로 검증한 논문은 찾지 못했습니다** |
| 학술(압박 쪽) | exPress(2025), Bauer & Anzer 2021, Bekkers 2025 | 압박하는 쪽의 가치 | **반대편, 즉 "압박을 벗겨내는 능력(press resistance)"의 학술 지표는 공백** |
| 심리·인지 | Jordet 스캐닝 | CB가 CM 다음으로 스캔을 많이 함 | "발밑"의 인지적 측면 |

### 2-2. 빌드업의 효과를 다룬 연구

| 연구 | 데이터 | 결과 | 한계 |
|---|---|---|---|
| Fernández-Navarro et al. 2016 (*J Sports Sci*), 2019 (*IJSSC*, *Evaluating the effectiveness of styles of play*) | 라리가·EPL | 점유 단위로 빌드업/카운터/직선형 등 스타일을 측정하고, 스타일과 결과의 관계를 분석 | 스타일 효과는 상대와 문맥에 크게 의존 |
| 세리에 A 점유형 vs 직선형 비교 (PubMed 41498677) | 이탈리아 1부 | **빌드업형 팀은 유럽대항전 진출 오즈가 13.5배** | 순수 상관. 강팀이 빌드업을 할 여유가 있는 것일 수 있음(역인과) |
| 전술 상황·스타일 KPI 연구 (MDPI *JFMK* 2024) | | 빌드업 단계의 점유형이 직선형보다 승리확률과 관련 (분류 정확도 81.9%) | 상관 |
| EPL 압박 효율 연구 (Baltic J. Sport Sci.) | EPL | 높은 압박 팀이 빌드업을 허용한 팀보다 성적이 좋음 | |
| **2019 골킥 규정 변경 (IFAB)**: 페널티 박스 안에서 골킥을 받을 수 있게 됨 | Opta·StatsBomb·J리그 | 짧은 골킥 비율: PL 28% → 40%(2019/20 초반), J1 19.4%(2017) → 46.5%(2020). 브라이턴은 6% → 75% 이상 | 서술 통계 위주. **인과 분석은 소규모(브라질 단일팀 38 vs 38경기)뿐** |
| PL 공식 분석 (2019/20, 288경기) | | 짧은 골킥에서 득점 5 vs 긴 골킥 0. 짧은 골킥 턴오버로 9실점 | 표본이 작고, 위험과 보상을 한 단위로 비교하지 않음 |
| American Soccer Analysis 2016 (골킥 가치) | MLS | 짧은 패스는 즉시 가치가 약간 더 높지만, **다음 점유까지 보면 효과가 역전**(긴 공은 수비가 깊게 자리잡게 함) | 2016년, 규정 변경 전 |
| 일본 블로그 인용 Kakuni 2024 | 분데스리가 | 높은 압박을 받은 뒤 볼 유지율 상위 5팀 = 순위 상위 5팀 | 원문 미확인 |
| 2025/26 PL 전술 트렌드 (premierleague.com) | PL | **긴 골킥이 다시 늘어남** (전방 맨투맨 압박이 확산된 영향) | "빌드업 만능론"에 대한 반례 |

**정리**: "빌드업을 하는 팀이 강하다"는 상관은 반복해서 관찰됩니다. 하지만 ① 강팀이라서 빌드업을 하는 역인과, ② 빌드업의 **위험(자기 진영 턴오버 → 실점)과 보상을 같은 단위로 비교한 연구가 드물고**, ③ **압박 강도별로** 나눠 본 연구, ④ 규정 변경이나 감독 교체를 이용한 **준실험(quasi-experiment) 설계**는 거의 없습니다. 2025/26 시즌 롱볼 회귀 현상까지 생각하면 "빌드업은 정말 이득인가?"는 **지금 묻기 좋은 질문**입니다.

---

## 3. 직접 찾은 연구 공백 (Gap Map)

| # | 공백 | 근거 | 학부 프로젝트 적합도 |
|---|---|---|---|
| G1 | **압박 저항(press resistance)·수비수 발밑의 검증된 학술 지표가 없음** | 압박하는 쪽(exPress, Pressing Intensity, 카운터프레싱)은 연구가 많지만 반대편은 상용 지표뿐 | ★★★ |
| G2 | **빌드업의 위험-보상을 같은 단위(EPV/xG)로, 압박 강도별·인과적으로 평가한 연구가 드묾** | 2-2절 | ★★★ |
| G3 | **오프더볼 지표가 중계 기반 트래킹(화면 밖 결측)에서도 유지되는가?** | DEFCON·Blame 등은 광학(전 선수) 트래킹을 씁니다. 공개 데이터(SkillCorner, PFF)와 대다수 구단·하위리그는 중계 기반. ELASTIC·궤적 보간 연구는 있지만 "지표의 강건성" 평가는 없음 | ★★★ |
| G4 | **공격과 수비 오프더볼 평가의 통합, 역할 조건부 비교** | DEFCON이 향후 과제로 명시 | ★★ (난이도 높음) |
| G5 | **리더십·조직 영향력의 딥러닝 반사실 측정과 외부 검증** | 1-6절: 지연 상관 수준에서 멈춤 | ★★ (검증 라벨이 약함) |
| G6 | **중계 영상에서 스캐닝(고개 돌림) 자동 검출** | 1-7절: 수작업 코딩뿐 | ★ (비전 난이도가 높음) |
| G7 | **이벤트 데이터만 있는 대규모 리그로 오프더볼 평가를 확장** | 360 프레임 → 전체 궤적 생성(확산/보간) → 트래킹 지표 전이. velocity completion 연구가 첫발 | ★★ |
| G8 | **여자축구 트래킹 기반 분석** | 공개 트래킹 대부분이 남자. Blame 논문이 여자 분데스리가를 썼지만 비공개 | ★★ (데이터 제약) |
| G9 | **교체·피로의 인과 효과** | 교체 스코핑 리뷰(33편)도 상관 위주이고 방법론이 이질적이라고 지적 | ★★ |
| G10 | **센터백 조합의 궁합** (볼 플레잉형 + 스토퍼형이 실제로 상보적인가) | Bransen & Van Haaren 2020이 선수 궁합을 다뤘지만 포지션 쌍의 역할 상보성은 미개척 | ★★★ |

---

## 4. 업데이트된 주제 추천

> **2026-10-29 추가**: 고상기 교수 연구실 논문 21편을 조사해 추천을 다시 조정했습니다. exPress(압박 xP, 압박 저항 언급), La Pausa(패스 타이밍), CIKM'25 궤적 복원, ScoutGPT(이적 적합도) 때문에 아래 순위가 바뀌었습니다. 최종 추천은 [`uos-ko-lab-research.md`](./uos-ko-lab-research.md) 4장을 보세요.

### ⭐ 새 1순위: "빌드업은 정말 이득인가? — 압박 조건부 빌드업 가치 모델과 센터백 '발밑' 지표" (G1 + G2 + G10)

질문하신 "수비수의 발밑"과 "빌드업의 실제 중요성"을 한 프로젝트로 묶은 주제입니다.

**연구 질문**
1. **RQ1 (팀)**: 자기 진영 빌드업은 **위험(턴오버 → 실점 기대)** 을 감안해도 순이익인가? **상대 압박 강도별로** 얼마나 달라지는가?
2. **RQ2 (선수)**: 센터백·골키퍼의 "발밑"을 **압박 조건부 기대 대비 초과 가치(Value Over Expected under Pressure)** 로 정의하면 안정적이고, 기존 지표(패스 성공률, 프로그레시브 패스)와 독립적인 정보를 주는가?
3. **RQ3 (확장)**: 볼 플레잉 CB와 스토퍼 CB의 조합은 상보적인가? 팀 빌드업 성공률과 실점에 대한 상호작용 효과를 봅니다.

**데이터 (모두 공개)**
- StatsBomb Open Data: **2015/16 빅5 리그 전 시즌(약 1,800경기)**. 모든 이벤트에 `under_pressure` 플래그가 붙어 있어 RQ1·RQ3의 표본을 확보할 수 있습니다.
- StatsBomb **360**(유로 2020/2024, 월드컵 2022, 여자 유로 2022/2025 등): 압박 거리, 패스 라인 차단 같은 공간 문맥을 제공합니다.
- **PFF 월드컵 2022 트래킹(64경기)**, Sportec(7경기), SkillCorner(10경기 + 압박 정보가 있는 Dynamic Events): 연속 압박 강도(Pressing Intensity)를 정밀하게 계산합니다.
- (선택) Transfermarkt 시장가치·포지션: 외적 타당도 검증용.

**방법**
1. **빌드업 시퀀스 정의**: 골킥이나 자기 진영 1/3 지역 점유 시작 → 하프라인 통과 / 턴오버 / 롱볼로 종료.
2. **압박 강도 측정**: 트래킹에서는 Bekkers의 Pressing Intensity(`unravelsports`), 360에서는 프레임 내 최근접 수비수 수와 거리로 근사합니다.
3. **가치 모델 (딥러닝)**: 360·트래킹 프레임을 그래프로 만들어 GNN(GAT)으로 패스 성공확률(xPass)과 성공·실패 시 EPV를 추정합니다. DEFCON이나 Fernández EPV의 분해 구조를 그대로 차용합니다.
4. **선수 지표**: 같은 압박 상황에서 **모델이 기대한 결과 대비 실제 결과**를 누적합니다. "강한 압박 속에서 공을 잃지 않고 전진시키는" 능력을 "기대 대비 초과"로 표현하는 방식입니다.
5. **팀 수준 인과 추정**: 빌드업 vs 롱볼 선택을 처치로 보고, 상황(점수, 시간, 상대 압박 강도, 전력 차)을 통제한 성향점수 가중이나 이중 강건(doubly robust) 추정으로 **"같은 상황에서 롱볼을 찼다면?"** 의 기대가치 차이를 계산합니다.
6. **검증**: 안정성(전반기 vs 후반기 split-half), 독립성(패스 성공률·프로그레시브 패스와의 상관), 외적 타당도(시장가치, 상위팀 이적 여부), 사례 연구.

**참신성**: 압박하는 쪽(exPress, DEFCON)의 거울상인 **"압박을 이겨내는 쪽"의 지표**입니다. 빌드업 논쟁을 위험-보상 단일 척도와 인과 추론으로 다룹니다. 2025/26 롱볼 회귀라는 시의성도 있습니다.
**도전성**: GNN 가치 모델 + 인과 추론 + 지표 검증 프레임워크.
**현실성**: 이벤트 데이터만으로도 RQ1·RQ2의 MVP가 가능하고, 트래킹은 정밀화 단계에서 붙입니다. ★★★

**8주 계획**

| 주 | 할 일 |
|---|---|
| 1 | StatsBomb 2015/16·360 다운로드, 빌드업 시퀀스 추출, 기초 통계 (짧은 골킥 vs 긴 골킥 결과) |
| 2 | 압박 피처 설계 (360 근사 + 트래킹 Pressing Intensity), xPass 베이스라인(XGBoost) |
| 3 | GNN xPass/EPV 학습 (360 프레임) |
| 4 | **MVP**: 압박 조건부 CB·GK 초과가치 지표 + 순위 |
| 5 | 팀 수준 인과 분석 (빌드업 vs 롱볼, 압박 강도별) |
| 6 | 검증 (안정성·독립성·시장가치), PFF 트래킹으로 정밀 검증 |
| 7 | CB 조합 궁합 분석(RQ3), 사례 시각화 |
| 8 | 발표 준비 |

---

### 2순위: "그 오프더볼 지표, 중계 화면에서도 믿을 수 있나? — 트래킹 결측에 대한 지표 강건성과 생성 모델 보정" (G3 + G7)

- **질문**: DEFCON·OBSO·C-OBSO·Pressing Intensity 같은 오프더볼 지표를 **중계 기반 트래킹**(화면 밖 선수 결측)으로 계산해도 선수 순위가 유지될까? 생성형 궤적 보간으로 얼마나 회복할 수 있을까?
- **방법**
  1. Sportec(광학, 전원 추적) 데이터에 **중계 카메라 시야 마스크를 시뮬레이션**합니다. 공 중심 시야각 모델이나 SkillCorner의 실제 결측 패턴을 학습해 적용합니다.
  2. 원본 지표 vs 결측 지표의 순위 상관과 오차를 측정합니다.
  3. Transformer·확산 기반 궤적 보간 모델로 결측 선수를 복원한 뒤 지표를 다시 계산하고 개선 폭을 비교합니다.
  4. 실제 중계 기반 데이터(SkillCorner, PFF)에 적용합니다.
- **장점**: **정답(원본 광학 트래킹)이 있어서 평가가 깔끔합니다.** 이 분야의 고질적 문제인 "정답 라벨 없음"을 피할 수 있습니다. 현장 의미도 큽니다: 대부분의 구단과 하위 리그는 중계 기반 데이터만 쓸 수 있습니다. 김현성 등의 궤적 보간, ELASTIC 연구와도 자연스럽게 이어집니다.
- **난이도**: 딥러닝 비중이 가장 높습니다(생성 모델). 데이터 양은 작지만(7경기 = 약 100만 프레임) 학습에는 충분합니다.

---

### 3순위: "누가 팀을 움직이는가 — 반사실 궤적 모델로 측정한 조직 영향력" (G5, 1차 1순위의 리더십 부분만 살림)

- 1차 문서의 지표 B입니다. 수비 오프더볼 평가(지표 A)는 선행연구와 겹치므로 버리고, **"선수 i의 움직임을 평균 행동으로 바꾸면 동료들의 예측 궤적이 얼마나 바뀌는가"** 에 집중합니다.
- 고전 방법(DCDT, transfer entropy)과 비교하고, 주장 여부·A매치 출전 수·포지션으로 수렴 타당도를 검증합니다.
- **리스크**: 정답 라벨이 약합니다. "리더십"이 아니라 **"조직 영향력"** 으로 정의해야 안전합니다.

---

### 4순위: "강팀 상대 빌드업 vs 롱볼 — 2019 골킥 규정 변경을 이용한 준실험" (G2의 인과 버전, 데이터 분석 중심)

- 규정 변경 전후로 같은 팀의 골킥 선택과 결과를 비교합니다(이중차분, DiD). 처치 강도는 감독 성향(예: 브라이턴 포터 부임)이나 변경 이전 짧은 패스 성향으로 정의합니다.
- **데이터 리스크**: 규정 변경 전후 시즌이 모두 공개된 이벤트 데이터가 부족합니다. StatsBomb의 바르셀로나 시즌들, Wyscout 2017/18, StatsBomb 최근 대회 정도라서 범위가 제한됩니다. 크롤링(WhoScored 등)이 필요할 수 있어 **1순위의 부록 분석**으로 넣는 쪽을 권합니다.

---

### 5순위 (도전형): "중계 영상에서 스캐닝 자동 검출" (G6)

- SoccerNet 영상 → 선수 추적 → 머리 자세 추정(RTMPose, 6DRepNet 등) → **볼 수신 직전 고개 회전 횟수**를 측정합니다. Jordet의 수작업 결과(포지션별 스캔 빈도, 스캔과 패스 성공의 관계)를 **자동으로 재현**할 수 있는지 봅니다.
- 세계 최초급 자동화 시도라 참신성은 최고지만, 중계 화면 해상도에서 머리 방향을 추정하기 어렵습니다. 범위를 "근접 화면 위주 수백 장면"으로 좁히고, 수작업 라벨 200~300개로 검증하는 설계가 필요합니다.

---

### 추천 요약

| 순위 | 주제 | 참신성 | 도전성 | 현실성 | 비고 |
|---|---|---|---|---|---|
| 1 | 압박 조건부 빌드업 가치 & CB 발밑 지표 | ★★★ | ★★★ | ★★★ | 질문하신 관심사와 정확히 일치. 이벤트만으로 MVP 가능 |
| 2 | 중계 트래킹 결측에 대한 지표 강건성 + 생성 보정 | ★★★ | ★★★ | ★★ | 딥러닝 비중 최대, 평가가 깔끔 |
| 3 | 반사실 조직 영향력(리더십) | ★★★ | ★★★ | ★★ | 검증 설계가 관건 |
| 4 | 골킥 규정 준실험 | ★★ | ★★ | ★★ | 1순위의 부록으로 |
| 5 | 스캐닝 자동 검출 | ★★★ | ★★★ | ★ | 고위험 |

> 1·2순위는 결합할 수도 있습니다. 예를 들어 1순위의 압박 강도를 SkillCorner(중계)와 Sportec(광학)에서 각각 계산해 차이를 보고하면 강건성 분석이 자연스럽게 따라옵니다.

---

## 참고문헌 / 링크 (조사 중 확인한 것)

**수비·오프더볼 최신**
- Kim et al. 2025, DEFCON: https://arxiv.org/abs/2512.10355
- Bischofberger et al. 2026, Blame is easier than praise: https://arxiv.org/abs/2606.19931
- Groom et al. 2026, Off-ball defensive role (CDHMM): https://arxiv.org/abs/2601.00748
- Lee et al. 2025, exPress (MIT Sloan SAC)
- Everett et al. 2025, GAT defensive influence (IEEE DSAA)
- Teranishi et al., C-OBSO: https://arxiv.org/abs/2206.01899
- Wu & Swartz, Off-the-ball actions: https://www.sfu.ca/~tswartz/papers/off-the-ball.pdf
- Llana et al. 2022, Is it worth the effort?: https://arxiv.org/abs/2204.02313
- Bekkers 2025, Pressing Intensity: https://arxiv.org/abs/2501.04712
- Soccermatics, Valuing off-ball actions: https://soccermatics.readthedocs.io/en/latest/lesson7/ValuingOffBall.html
- Gradient Sports, Measuring off-ball movement: https://www.gradientsports.com/blog/measuring-off-ball-movement-using-broadcast-tracking-event-data
- Dick & Brefeld 2019: https://journals.sagepub.com/doi/full/10.1089/big.2018.0054
- Fernández, Bornn & Cervone 2021, EPV: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8570314/

**생성 모델·궤적**
- Kim et al. 2023, Ball trajectory inference: https://arxiv.org/abs/2306.08206
- Velocity completion (event-based positional data): https://arxiv.org/abs/2505.16199
- GenTac: https://arxiv.org/abs/2604.11786 · TacticGen: https://arxiv.org/abs/2604.18210 · Sports-Traj: https://arxiv.org/abs/2405.17680
- Space evaluation at transitions: https://arxiv.org/abs/2505.14711

**집단 움직임**
- Collective movement analysis (Chaos, Solitons & Fractals 2020): https://www.sciencedirect.com/science/article/abs/pii/S0960077920302319
- Collective states and their transitions in football (PLOS ONE): https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0251970
- Information-theoretical analysis of team dynamics: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11941434/

**인지·비전**
- Jordet et al. 2020, Scanning in EPL: https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2020.553813/full
- Arbués-Sangüesa et al. 2020, Body orientation & pass feasibility: https://arxiv.org/abs/2004.07209

**빌드업·센터백**
- 세리에 A 점유형 vs 직선형: https://pubmed.ncbi.nlm.nih.gov/41498677/
- Evaluating the effectiveness of styles of play: https://www.researchgate.net/publication/333695307
- Tactical situations & playing styles as KPIs (MDPI): https://www.mdpi.com/2411-5142/9/2/88
- PL 골킥 규정 변경 트렌드: https://www.premierleague.com/en/news/1657509 · 2025/26 전술 트렌드: https://www.premierleague.com/en/news/4407434
- J리그 JSTATS 짧은 골킥: https://www.jleague.co/news/jstats-short-goal-kicks-soar-goalkeepers-more-involved-in-buildup-as-jleague-tactics-evolve
- StatsBomb/Hudl, How football is changing: https://www.hudl.com/blog/how-football-is-changing
- ASA 골킥 분석 2016: https://www.americansocceranalysis.com/home/2016/12/7/attention-goalkeepers-stop-kicking-those-long-balls
- SkillCorner, Progressive actions under intense pressure: https://skillcorner.com/articles/metric-explainer-progressive-actions-under-intense-pressure
- un-xPass (Robberechts et al. 2023): https://static.hudl.com/craft/Pieter-Robberechts-et-al-un-xPass-Measuring-Soccer-Players-Creativity.pdf
- 교체 스코핑 리뷰: https://pure.solent.ac.uk/en/publications/substitutions-in-elite-soccer-a-scoping-review/
- 공개 트래킹 희소성 (Bassek et al. 2025, *Sci. Data*): https://www.nature.com/articles/s41597-025-04505-y
