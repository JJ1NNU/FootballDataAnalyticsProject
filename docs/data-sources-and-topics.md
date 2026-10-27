# 축구 오픈 데이터 조사 & 프로젝트 주제 추천

> 작성일: 2026-10-27 · 최종 발표: 2026-12-21 (남은 기간 약 8주)
> 출발점: 수업 노트북 `1-load-statistic-data.ipynb`(ClubElo, PL/UEFA/분데스리가 숨은 API, Wikipedia, Understat, soccerdata), `2-load-event-and-tracking-data.ipynb`(Metrica 이벤트·트래킹)

---

## Part 1. 오픈 축구 데이터 총정리

데이터의 "해상도" 순서로 정리했습니다. 위로 갈수록 구하기 쉽고, 아래로 갈수록 딥러닝에 쓸 만한 정보량이 많습니다.

### 1-1. 결과·순위·레이팅 (경기 단위)

| 소스 | 내용 | 접근 방법 | 비고 |
|---|---|---|---|
| **ClubElo** | 클럽 Elo 시계열 (1940년대~) | HTML/임베디드 JSON (노트북 참고), soccerdata | API 서버 불안정 → 노트북 방식 사용 |
| **eloratings.net** | 국가대표 Elo | 크롤링 | 국가대항전 언더독 분석용 |
| **football-data.co.uk** | 유럽 20여 개 리그 결과 + **배당률**(1993~) + 슈팅·코너 | CSV 직접 다운로드, `sd.MatchHistory` | 경기 예측 베이스라인·업셋 정의의 표준 데이터 |
| **martj42/international_results** (GitHub/Kaggle) | 1872년~현재 A매치 결과, 득점자, 승부차기 | CSV | |
| **openfootball** (GitHub) | 각국 리그 일정·결과 (퍼블릭 도메인) | txt/JSON | |
| **football-data.org / API-Football** | 일정·결과·라인업 | 무료 티어 API 키 | 호출 수 제한 |
| **Wikipedia** | 시즌 문서: 순위, 감독, 주장, 경기장 | `pd.read_html` (노트북 참고) | **주장(captain) 라벨**로 쓸 수 있음 |
| **K리그 데이터포털** (data.kleague.com) | K리그 기록 | 크롤링 | 국내 주제 시 |

### 1-2. 시즌·경기 집계 스탯 (선수/팀 단위)

| 소스 | 내용 | 접근 방법 | 비고 |
|---|---|---|---|
| **Understat** | 빅5+RPL, 2014/15~ xG, xA, **슈팅 좌표**, PPDA | `sd.Understat` | 장기간 xG 시계열이 필요하면 1순위 |
| **FBref** | 100개+ 대회 기본 기록 | `sd.FBref` | ⚠️ **2026년 1월 Opta가 데이터 피드를 끊어 고급 지표(xG, 프로그레시브 패스 등)가 삭제됨.** 기본 기록만 남음 |
| **Premier League / UEFA / Bundesliga 숨은 API** | 순위, 선수 지표, 관중, **최고속도·스프린트·뛴 거리** | 노트북의 `pulselive`, `compstats.uefa.com`, Firebase | 비공식 → 구조 변경 위험, 스냅샷을 저장해 둘 것 |
| **FotMob / SofaScore** | 경기 **평점**, 슈팅맵, 모멘텀 그래프, 히트맵 | 내부 JSON API (브라우저 네트워크 탭) | 평점 비교 대상으로 유용. 이용약관 확인, 요청 간격 두기 |
| **WhoScored** | Opta 이벤트(매치센터 JSON), 평점 | `sd.WhoScored` (Selenium) | 봇 차단 강함, 약관상 회색지대 |
| **The Analyst (Opta)** | 공개 기사·지표 | 크롤링 | |
| **Transfermarkt** | 시장가치 이력, 이적, **포지션 이력**, 부상, **감독 이력**, 출전 | `dcaribou/transfermarkt-datasets` (GitHub, 주간 갱신 CSV), 크롤링 | 감독/포지션/이적 주제의 핵심 조인 키 |
| **Capology** | 연봉 | 크롤링 | |
| **SoFIFA / Kaggle "FIFA 15~EA FC" 데이터셋** | EA FC 게임 능력치(연도별) | Kaggle CSV | 게임 능력치 타당성 검증 주제에 FM보다 현실적 |
| **FM 능력치 (fminside 등)** | Football Manager 능력치 | 크롤링 | 약관상 제약, 대량 수집 비추천 |
| **Kaggle European Soccer Database** | 2008~2016 25,000경기 + FIFA 능력치 + 배당 | SQLite | 오래됐지만 조인이 이미 되어 있음 |

### 1-3. 이벤트 데이터 (액션 단위, 좌표 포함)

| 소스 | 규모 | 비고 |
|---|---|---|
| **StatsBomb Open Data** (`statsbombpy`, GitHub) | 3,000+ 경기. 2015/16 빅5 리그 전 시즌, 메시 라리가 전 경기, 레버쿠젠 23/24, 월드컵 2018/2022, 유로 2020/2024, 코파 2024, AFCON 2023, 챔스 결승들, **여자**: WSL 3시즌, NWSL 2018, 여자 월드컵 2019/2023, 여자 유로 2022/2025 | **360 프레임**(이벤트 순간의 화면 내 선수 위치) 포함 대회: 유로 2020/2024, 월드컵 2022, 여자 유로 2022/2025, 여자 월드컵 2023 등. 압박·xG·패스 높이 등 속성이 매우 풍부 |
| **Wyscout Public Dataset** (Pappalardo et al., *Sci. Data* 2019) | 1,941경기, 약 325만 이벤트 (2017/18 빅5 + 월드컵 2018 + 유로 2016) | PlayeRank 논문의 데이터. 선수 프로필 포함 |
| **Metrica Sample Data** | 3경기 (이벤트+트래킹, 익명) | 수업 노트북 사용 |
| **PFF FC (현 Gradient Sports) 월드컵 2022** | **64경기 전 경기 이벤트 + 트래킹 + 로스터** | 아래 트래킹 항목 참고 |
| **Sportec Open Data (DFL, Bassek et al.)** | 7경기 (분데스리가 1·2부) | 아래 트래킹 항목 참고 |
| **SkillCorner Dynamic Events** | 10경기 | 오프볼 런, 압박 상황 등 "트래킹에서 파생된 이벤트" |

### 1-4. 트래킹 데이터 (프레임 단위, 22명 + 공 좌표)

| 소스 | 규모 | 수집 방식 | 딥러닝 적합도 |
|---|---|---|---|
| **PFF FC / Gradient Sports – FIFA World Cup 2022** | **64경기 전체** (약 90시간+) | 경기장 기반 트래킹, ~30fps, 이벤트와 연결 | ★★★ 오픈 트래킹 중 **가장 큰 규모**. kloppy로 로드 가능. 다운로드·라이선스는 블로그에서 확인 필요 |
| **Sportec Open Data (IDSSE/DFL, Bassek et al. 2025, *Sci. Data*)** | 7경기 | 광학 트래킹 25fps + 공식 이벤트 동기화, CC-BY 4.0 | ★★ 품질 최상 → 테스트/일반화 검증용 |
| **SkillCorner Open Data** | A-League 2024/25 10경기(트래킹+Dynamic Events+Phases of Play) + 175경기 피지컬 집계, 구버전 9경기 | 중계화면 기반(화면 밖 선수는 추정/결측) | ★★ |
| **Metrica Sports Sample** | 3경기 | 25fps, 익명 | ★ 튜토리얼용 |
| **StatsBomb 360** | 수백 경기 | 이벤트 순간의 스냅샷만 (연속 프레임 아님) | ★★ 프레임 단위 모델(GNN 등)에 유용 |
| **Alfheim / SoccerMon (Tromsø)** | 소수 경기 + 여자팀 2시즌 GPS·웰니스 | 웨어러블 | 부하·부상 주제용 |
| **Last Row 클립** | 리버풀 골 장면 19개 | 영상에서 수작업 추출 | 데모용 |

### 1-5. 영상 데이터 (비전)

| 소스 | 내용 |
|---|---|
| **SoccerNet** | 유럽 리그 중계 500경기+ 영상. 과제별 라벨: Action Spotting, **Ball Action Spotting**(패스·드리블 등 공 이벤트 프레임), Camera Calibration(호모그래피), Player Tracking, Re-ID, Jersey Number, **Game State Reconstruction(GSR, 영상→2D 미니맵 좌표+등번호+팀)**, Dense Captioning. NDA 서명 후 다운로드 |
| **SoccerTrack (v1/v2)** | 어안·드론 영상 + GT 트래킹 |
| **SportsMOT / TeamTrack** | 다중 객체 추적 벤치마크 |
| 도구 | YOLO11 / RT-DETR(검출), ByteTrack/BoT-SORT(추적), **RTMPose / ViTPose**(자세), `sn-gamestate` 베이스라인, Roboflow `sports` |

### 1-6. 파이썬 생태계 (파싱·전처리·모델)

- **로더/표준화**: `soccerdata`(크롤러 모음), `statsbombpy`, **`kloppy`**(StatsBomb·Wyscout·Metrica·Sportec·SkillCorner·PFF 등을 공통 포맷으로), `databallpy`(이벤트-트래킹 동기화), `floodlight`
- **가치 모델**: `socceraction`(SPADL 포맷, **VAEP**, **xT**), pitch control·EPV 구현(LaurieOnTracking / Friends of Tracking)
- **그래프 딥러닝**: **`unravelsports`**(트래킹 프레임 → PyTorch Geometric/Spektral 그래프 변환)
- **동기화 연구**: ETSY, **ELASTIC**(이벤트-트래킹 정렬, Sportec 기준 88% 정확 정렬)
- **시각화**: `mplsoccer`

> **실무 팁**: 숨은 API·크롤링 소스는 언제든 막힐 수 있습니다(ClubElo API 502, FBref 고급지표 삭제가 실제 사례). 프로젝트 초반에 필요한 데이터를 **한 번에 받아서 parquet로 저장**해 두세요.

---

## Part 2. 주제 추천

### 2-0. 판단 기준 요약

- **참신성**: 득점·xG 순위, 단순 승부 예측, "OOO 선수 분석"은 이미 흔합니다. **트래킹 데이터 + 반사실(counterfactual) 질문**은 아직 학부 수준에서 거의 다뤄지지 않은 영역이고, 공개 데이터(PFF 월드컵 64경기)가 최근에야 생겼습니다.
- **도전성**: 딥러닝을 할 수 있다면 **다중 에이전트 시계열 모델(Transformer/GNN)** 이 축구 트래킹에서 가장 의미 있는 난이도입니다.
- **현실성**: 8주 안에 끝내려면 ① 데이터가 이미 정제돼 있고 ② MVP(최소 결과물)가 3~4주차에 나오며 ③ 나머지는 확장으로 쌓을 수 있는 구조여야 합니다.
- **지표 개발 팁 (교수님 어필용)**: 새 지표를 만들면 Franks et al. (2016) *"Meta-analytics"* 의 세 기준을 꼭 보고하세요. **안정성**(같은 선수에서 경기·전후반 간 상관이 높은가), **변별력**(선수 간 분산이 충분한가), **독립성**(기존 지표, 예를 들어 득점·패스 수로 설명되지 않는 정보가 있는가). 이것만 해도 "그럴듯한 숫자"와 "믿을 수 있는 지표"가 구분됩니다. 질문하신 "믿을만한 평점"의 핵심 기준이기도 합니다.

### 2-1. ⭐ 1순위 추천: "그림자 팀(Ghost Team)으로 측정하는 오프더볼 영향력과 리더십"

**한 줄 요약**: 월드컵 2022 트래킹으로 "평균적인 선수라면 이 상황에서 어떻게 움직였을까"를 예측하는 다중 에이전트 딥러닝 모델을 만들고, 이를 기준선 삼아 ① 실제 움직임이 만든 **가치 차이**(오프더볼 기여)와 ② 한 선수의 움직임이 **동료의 움직임을 얼마나 바꾸는지**(조직·리더십 영향력)를 새 지표로 정의합니다.

**왜 좋은가**
- 질문하신 아이디어 중 **새 선수평가지표**, **리더십 같은 인격적 수치**, **믿을만한 평점**을 하나의 모델 위에서 다룰 수 있습니다.
- 공을 갖지 않은 시간(경기의 약 98%)은 이벤트 데이터로는 평가할 수 없어서, 업계에서도 아직 열린 문제입니다.
- "리더십"을 **집단 이동의 선행-후행 관계**로 정의하는 관점은 동물 집단행동 연구(Nagy et al., 2010 *Nature*, 비둘기 무리의 리더 위계)에서 가져온 것으로, 축구에 적용한 사례가 드뭅니다.

**방법**
1. **데이터**: PFF 월드컵 2022 64경기(학습), Sportec 7경기(다른 리그·다른 트래킹 시스템에서의 일반화 검증), SkillCorner 10경기(선택). `kloppy` → 공통 좌표계, 공격 방향 통일, 10Hz 다운샘플.
2. **Ghost 모델**: 과거 T초(예: 2초)의 22명+공 궤적과 이벤트 문맥을 입력받아 다음 2~4초 각 선수 궤적을 예측합니다.
   - 아키텍처: 에이전트 축 attention + 시간 축 attention(Transformer, 예: AgentFormer/Baller2Vec 계열) 또는 GNN+GRU. 확률적 예측을 위해 다봉 분포(mixture) 출력이나 CVAE.
   - 베이스라인: 등속 운동, LSTM. 지표: ADE/FDE.
3. **지표 A — 오프더볼 가치(Off-Ball Value Added)**: 실제 위치와 ghost 위치에서 각각 **pitch control/EPV**(Spearman 2018, Fernández et al. 2021)를 계산해 차이를 누적합니다. 수비수라면 "평균 수비수가 섰을 위치 대비 상대 위협을 얼마나 줄였나"가 됩니다.
4. **지표 B — 영향력/리더십(Counterfactual Influence)**: 선수 i의 과거 궤적만 ghost(평균 행동)로 바꿨을 때 **동료들의 예측 궤적이 얼마나 변하는지**를 측정해 선수 간 방향성 영향 그래프를 만듭니다. 보조 지표로 고전적 lead-lag(지연 상관, transfer entropy)도 계산해 비교합니다.
5. **검증**
   - 안정성: 전반 vs 후반, 경기 간 split-half 상관.
   - 외적 타당성: 주장 여부(Wikipedia), A매치 출전 수, 나이, 포지션(CB·DM이 높을 것이라는 가설), 팀 성적과의 관계.
   - 사례 분석: 아르헨티나·모로코 등 팀의 "조직의 중심" 선수 시각화(애니메이션).

**MVP / 확장**
- MVP(4주차): 수비 라인만 대상으로 ghost 모델 + 지표 A.
- 확장: 지표 B, Sportec 일반화, 스카우팅 응용(같은 역할에서 지표가 높은 선수 추천).

**리스크와 대응**
- PFF 트래킹의 결측·노이즈 → 칼만/Savitzky–Golay 스무딩(노트북의 속도 계산 코드 재사용), 결측 구간 마스킹.
- "평균 선수" 모델이 너무 잘 맞으면 차이가 0에 수렴 → 확률적 모델을 쓰고 차이를 분포 기준(z-score/likelihood)으로 정의.
- 리더십의 정답 라벨이 없음 → "리더십"이라고 단정하지 말고 **"조직 영향력"** 으로 정의한 뒤 여러 간접 지표와의 수렴 타당도로 논증.

**핵심 참고문헌**: Le et al. 2017 *Data-Driven Ghosting* · Yeh et al. 2019 *Diverse Generation for Multi-Agent Sports Games (GVRNN)* · Fernández, Bornn & Cervone 2021 *EPV* · Spearman 2018 *Pitch Control* · Wang et al. 2024 *TacticAI* · Nagy et al. 2010 *Hierarchical group dynamics in pigeon flocks* · Franks et al. 2016 *Meta-analytics* · Bassek et al. 2025 *Sportec dataset*

---

### 2-2. 2순위: "여자축구는 정말 재미없나? — 서스펜스·서프라이즈로 '재미'를 정량화하기"

**한 줄 요약**: 경제학의 엔터테인먼트 이론(Ely, Frankel & Kamenica 2015, *Suspense and Surprise*)을 이용해, 딥러닝 **실시간 승리확률 모델**로 경기마다 서스펜스(앞으로 크게 바뀔 가능성)와 서프라이즈(실제로 크게 바뀐 정도)를 계산하고, 남녀 대회를 **전력 차·대회 단계를 통제한 뒤** 비교합니다.

- **참신성 높음**: 통념을 직접 검증하는 질문이고, "재미"를 측정 가능한 개념으로 바꾸는 과정 자체가 기여입니다. 결론이 어느 쪽이든 발표 가치가 있습니다.
- **데이터 현실성 최상**: StatsBomb에 남녀 대응 대회가 있습니다. 여자 월드컵 2019/2023 ↔ 남자 월드컵 2018/2022, 여자 유로 2022/2025 ↔ 남자 유로 2020/2024, WSL ↔ 2015/16 빅5. 360 데이터도 양쪽에 있습니다.
- **딥러닝**: 이벤트 시퀀스 Transformer로 실시간 승리확률(+기대 득점 흐름)을 학습합니다. 성별을 입력에 넣을지, 따로 학습할지 자체가 분석 포인트이고, 보정(calibration) 평가가 필수입니다.
- **추가 지표**: 경기 템포(분당 전진 거리, 데드볼 시간 비율), xT 흐름의 변동성, 전환 횟수, "의미 있는 위협" 빈도.
- **"재미" 라벨 검증**: YouTube Data API(하이라이트 조회수·좋아요, 노출 규모로 정규화), Reddit 매치 스레드 댓글 속도 등 관심 대리변수와 지표의 상관을 확인합니다.
- **주의**: 결론을 "증명"이 아니라 "검증"으로 설계하세요. 리그 간 수준 차이, 중계 품질 같은 교란요인을 명시하면 도전성과 신뢰도가 함께 올라갑니다.

---

### 2-3. 3순위: "멀티포지션의 조건 — 선수 스타일 임베딩으로 포지션 전환 적합도 예측"

**한 줄 요약**: 이벤트 시퀀스로 선수의 플레이 스타일 임베딩을 대조학습(contrastive learning)하고, Transfermarkt 포지션 이력에서 **실제 포지션 전환 사례**를 찾아 "전환 후 성과"를 예측하는 모델을 만든 뒤, 전환 후보 선수를 추천합니다.

- **데이터**: StatsBomb 2015/16 빅5 + Wyscout 2017/18 빅5(약 3,700경기), Transfermarkt 포지션·출전 이력. 성과는 VAEP/90을 새 포지션 동료 대비로 측정합니다.
- **딥러닝**: 액션 시퀀스 Transformer + 대조학습(같은 선수의 다른 경기 = positive). 임베딩 공간에서 포지션 간 "거리"와 전환 성공률의 관계를 분석합니다.
- **장점**: 결과물이 스카우터 관점의 추천이어서 발표 임팩트가 크고, "특정 팀에 특정 선수 추천" 아이디어와 바로 연결됩니다.
- **리스크**: 선수 이름 매칭(StatsBomb ↔ Wyscout ↔ Transfermarkt)에 시간이 듭니다. 전환 사례 수가 적을 수 있어서 시즌 범위가 겹치는지 1주차에 먼저 확인해야 합니다.

---

### 2-4. 도전형 옵션: "영상으로 퍼스트 터치(볼 트래핑) 품질 측정하기"

- **아이디어**: SoccerNet **Ball Action Spotting** 라벨로 패스 수신 순간을 찾습니다. 그다음 카메라 보정(호모그래피)으로 공·선수를 피치 좌표로 바꾸고, **수신 직후 공이 몸에서 얼마나 멀어지는지, 다음 액션까지 몇 프레임이 걸리는지, 압박 거리 대비 결과**를 측정해 "퍼스트 터치 지표"를 만듭니다. 자세 추정(RTMPose)으로 터치에 쓴 신체 부위도 분류할 수 있습니다.
- **참신성·도전성 최고**, **현실성은 낮음**: 중계 카메라 이동, 공 가림, 선수 신원 식별이 모두 어렵습니다. 8주 안에 하려면 범위를 **"수십 개 경기의 수신 장면 수백 개"** 로 좁히고, 수작업 라벨 일부로 검증하는 설계가 필요합니다.
- 단독 주제보다는 **팀원이 있으면 서브 모듈로** 붙이는 편이 안전합니다.

---

### 2-5. 생각하신 아이디어별 코멘트

| 아이디어 | 참신성 | 도전성 | 현실성 | 코멘트 |
|---|---|---|---|---|
| 여자축구가 재미없다는 통념 | ★★★ | ★★ | ★★★ | → **2순위**로 구체화 |
| 감독 vs 선수 영향 비교 | ★★ | ★★ | ★★ | 인과 식별이 핵심. 감독 이동을 이용한 two-way fixed effects(AKM 모형) + Understat xG 차이 + Transfermarkt 시장가치(선수단 질 통제). 선행연구: Muehlheusser et al. 2018. 딥러닝 비중이 낮음 |
| 발롱도르·골든보이 적합성 | ★ | ★ | ★★★ | 단독으로는 약함. **새 지표를 만든 뒤 "이 지표로 보면 누가 받았어야 했나"를 응용 사례로** 넣기에 좋음 |
| 포지션 변경 제안 / 멀티포지션 조건 | ★★★ | ★★★ | ★★ | → **3순위** |
| 믿을만한 평점 | ★★ | ★★ | ★★★ | "믿을만함"을 안정성·변별력·독립성(Franks 2016)으로 정의하고 FotMob/SofaScore 평점과 비교하면 좋음. 1순위 지표의 평가 틀로 흡수 가능 |
| 리더십 수치화 | ★★★ | ★★★ | ★★ | → **1순위의 지표 B** |
| 언더독 분석·예측 | ★ | ★★ | ★★★ | 흔한 주제. 차별화하려면 "스타일 상성"(예: 점유형 강팀 vs 저블록 약팀)을 Elo·배당 대비 잔차로 설명하는 각도가 필요 |
| 새 평가지표 / feature | ★★★ | ★★★ | ★★ | → 1순위 전체 |
| 선행연구 개선 | ★★ | ★★ | ★★★ | 예: VAEP/xT를 360 프레임 기반 GNN으로 확장(입력에 주변 선수 위치 추가). 안전한 플랜 B |
| 특정 팀에 선수 추천 | ★★ | ★★ | ★★★ | 3순위 또는 1순위의 응용 장으로 |
| FM 능력치 적합성 | ★★ | ★ | ★★ | FM 대신 **EA FC 능력치**(Kaggle에 연도별 공개)로 하면 데이터 문제가 해결됨. "게임 스카우터가 놓치는 선수" 분석은 재미있지만 깊이를 내기 어려움 |
| 비전 기반 반응속도·트래핑 | ★★★ | ★★★ | ★ | → 도전형 옵션 2-4 |

---

## Part 3. 1순위 주제 8주 일정 (10/27 → 12/21)

| 주차 | 기간 | 할 일 | 산출물 |
|---|---|---|---|
| 1 | 10/27–11/02 | PFF WC2022·Sportec 다운로드, `kloppy` 로드, EDA, 문헌 정리 | 데이터 parquet, 문헌 표 |
| 2 | 11/03–11/09 | 전처리(방향 통일, 스무딩, 10Hz, 결측 마스크), pitch control 구현 | 학습용 텐서 데이터셋 |
| 3 | 11/10–11/16 | 베이스라인(등속, LSTM) + Transformer/GNN ghost 모델 1차 학습 | ADE/FDE 표 |
| 4 | 11/17–11/23 | **MVP**: 수비 라인 지표 A 계산 | 중간 점검용 결과 |
| 5 | 11/24–11/30 | 지표 B(반사실 영향력), lead-lag 비교 | 영향 그래프 |
| 6 | 12/01–12/07 | 검증: 안정성, 주장·포지션 타당도, Sportec 일반화 | 검증 리포트 |
| 7 | 12/08–12/14 | 사례 분석, 애니메이션 시각화, ablation | 그림·영상 |
| 8 | 12/15–12/21 | 발표 자료, 리허설 | 최종 발표 |

**플랜 B**: 3주차까지 ghost 모델 학습이 불안정하면 StatsBomb 360 프레임 기반 GNN으로 "주변 선수 위치를 반영한 VAEP"(선행연구 개선형)로 전환합니다. 데이터·코드의 절반 이상을 재사용할 수 있습니다.

---

## 참고 링크

- StatsBomb Open Data: https://github.com/statsbomb/open-data · 여자 유로 2025 공개: https://www.hudl.com/blog/hudl-statsbomb-free-euro-2025-data
- PFF/Gradient WC2022: https://www.blog.fc.pff.com/blog/enhanced-2022-world-cup-dataset · https://www.gradientsports.com/blog/enhanced-2022-world-cup-dataset
- SkillCorner Open Data: https://github.com/SkillCorner/opendata · Analytics Cup: https://skillcorner.com/analytics-cup-2027
- Sportec / databallpy: https://pypi.org/project/databallpy/ · ELASTIC: https://arxiv.org/abs/2508.09238
- Metrica Sample Data: https://github.com/metrica-sports/sample-data
- SoccerNet 2025 Challenges: https://arxiv.org/abs/2508.19182
- FBref 고급지표 삭제: https://awfulannouncing.com/soccer/sports-reference-pulls-advanced-data-agreement-violation-dispute.html
- kloppy: https://github.com/PySport/kloppy · socceraction: https://github.com/ML-KULeuven/socceraction · unravelsports: https://github.com/UnravelSports/unravelsports · soccerdata: https://soccerdata.readthedocs.io
