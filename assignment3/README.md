# 과제 3: VAEP로 레전드 평가하기 (요한 크루이프)

| 파일 | 내용 |
|---|---|
| `assignment3_vaep_cruyff.ipynb` | 제출할 분석 노트북 (문제 1~4의 코드와 실행 출력 전체) |
| `assignment3_report_cruyff.docx` | 제출할 보고서 (Word, 수정 가능). 제출 전에 PDF로 저장 |
| `outputs/` | 노트북이 저장한 표(csv)와 그림(png). 보고서의 모든 숫자와 그림은 여기서 가져옴 |
| `build_notebook.py` | 노트북 초안 생성 스크립트 (이후 노트북은 직접 수정했으므로 최신본은 `.ipynb`) |
| `csv_to_json.py`, `build_report.js` | `outputs/` → 보고서 생성 스크립트 |

다시 만드는 순서: `python build_notebook.py` → Colab 등에서 노트북 실행 → `outputs/` 복사 → `python csv_to_json.py` → `node build_report.js`.
