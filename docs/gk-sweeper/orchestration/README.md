# 연구 오케스트레이션 — 구조와 현황

기준 문서는 `docs/gk-sweeper-research-plan.md`(기획서)이고, 규칙은 루트 `CLAUDE.md`, 단계 실행 절차는 `run-research-step` 스킬에 있다.

## 1. 에이전트 구성

| 에이전트 | 정의 | 맡는 기획서 범위 |
|---|---|---|
| **총괄** (메인 세션) | — | 단계 배정, 판정, 사용자 질의(`grilling`), 기획서·결정 로그 갱신, 커밋 |
| spec-auditor | `.claude/agents/spec-auditor.md` | 모든 단계의 브리프(빈칸 찾기)와 감사. 읽기 전용 |
| data-engineer | `data-engineer.md` | 3절, 5-1·5-2, 7절 적재, Kaggle 입력 패키징 |
| stat-modeler | `stat-modeler.md` | 4-3, c·s_w, b, 5-4 |
| obso-engineer | `obso-engineer.md` | 4-1·4-2·4-4 구현(CPU FP64, GPU FP32), 4-7, 5-3 |
| kaggle-runner | `kaggle-runner.md` | Kaggle T4×2 Dataset·kernel 실행, 쿼터 기록 |
| analyst | `analyst.md` | 4-6, 5-5, 5-6 집계, 7절 분석, 그림 |
| report-writer | `report-writer.md` | 실험 파일 `E01~E16`, `00-summary.md` |
| Explore (내장) | — | 파일·사실 조회 |

## 2. 한 단계의 흐름

```
총괄 ─▶ spec-auditor(브리프) ─빈칸?─예─▶ 총괄이 사용자에게 질의 ─▶ 기획서·decisions.md 갱신 ─┐
            │아니오                                                                       │
            ▼                                                                             │
      담당 에이전트(실행) ─멈춤 질문?─예──────────────────────────────────────────────────┤
            │아니오                                                                       │
            ▼                                                                             ▼
   /code-review ─▶ spec-auditor(감사) ─▶ report-writer(Exx) ─▶ 총괄 판정·커밋 ─▶ 사용자 보고·승인
```

## 3. 페이즈와 체크포인트

| 페이즈 | 파일 | 단계 | 체크포인트 |
|---|---|---|---|
| P0 기반 | `P0-foundation.md` | S00–S01 | — |
| P1 데이터·학습 부품 | `P1-data-models.md` | S02–S05 | — |
| P2 OBSO 구현·설정 확정 | `P2-obso-config.md` | S06–S08 | 준비 완료 **12-03** |
| P3 GPU·본 계산 | `P3-gpu-main.md` | S09–S12 | 본 계산 완료 **12-06** |
| P4 분석·검증 | `P4-analysis.md` | S13–S18 | 분석·검증 완료 **12-10** |
| P5 레포트 | `P5-report.md` | S19–S21 | 레포트 완성 **12-12** |

체크포인트를 넘기면 기획서 9절의 생략 순서(Metrica → 5-6 비싼 항목 중 오프사이드 고정 외 → 5-5)를 적용할지 사용자에게 질의한다.

## 4. 단계 현황

| 단계 | 내용 | 담당 | 레포트 | 상태 |
|---|---|---|---|---|
| S00 | 기획서 전체 명세 감사와 빈칸 질의 | spec-auditor | — | 진행 중 |
| S01 | 환경·코드 골격·원자료 확보 | data-engineer | — | 대기 |
| S02 | 분석 프레임 적재 (3절) | data-engineer | E01 | 대기 |
| S03 | StatsBomb 학습 부품 (4-3) | stat-modeler | E02 | 대기 |
| S04 | c·s_w 추정 (4-4) | stat-modeler | E03 | 대기 |
| S05 | 좌표·동기화 검증 (5-1·5-2) | data-engineer | E04 | 대기 |
| S06 | OBSO CPU 기준 구현 (4-1·4-2·4-4) | obso-engineer | E05 | 대기 |
| S07 | C 검증·주 설정 확정 (5-3) | obso-engineer | E06 | 대기 |
| S08 | b 선택 (4-4) | stat-modeler | E07 | 대기 |
| S09 | GPU FP32 구현 | obso-engineer | (E08에 포함) | 대기 |
| S10 | Kaggle 연동 | 총괄·kaggle-runner | — | 대기 |
| S11 | 예비 실험 (4-7) | obso-engineer·kaggle-runner | E08 | 대기 |
| S12 | 본 계산 (4-1·4-5) | kaggle-runner | E09 | 대기 |
| S13 | RQ1·RQ3 (4-6) | analyst | E10·E12 | 대기 |
| S14 | RQ2 (4-6) | analyst | E11 | 대기 |
| S15 | S 검증 (5-4) | stat-modeler | E13 | 대기 |
| S16 | O 외적 타당성 (5-5) | analyst | E14 | 대기 |
| S17 | 민감도 (5-6) | kaggle-runner·analyst | E15 | 대기 |
| S18 | Metrica 재현 (7절, 선택) | data-engineer·analyst | E16 | 대기 |
| S19 | 그림 정비 (8절) | analyst | — | 대기 |
| S20 | 요약 종합·전체 교정 | report-writer | 00-summary | 대기 |
| S21 | 최종 감사·재현성 점검 | spec-auditor·총괄 | — | 대기 |

상태 값: 대기 / 진행 중 / 질의 중 / 완료(날짜).
