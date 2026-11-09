# 양자컴퓨팅 이론 및 실습 (12시간 집중 부트캠프)

본 저장소는 **[양자컴퓨팅 이론 및 실습]** 4주(총 12시간) 집중 강좌의 공식 학생용 배포 저장소입니다.  
강의 교재(PDF), 주차별 Jupyter Notebook 실습 파일, 원클릭 실습 환경 구동 스크립트가 포함되어 있습니다.

- **강사**: 서상협 ((주)큐렌스 / Q-Rence)
- **대상**: 양자컴퓨팅에 입문하는 학부생 및 연구원
- **사전 요구사항**: 기본적인 파이썬 문법 이해 (파이썬이 컴퓨터에 설치되어 있지 않아도 아래 원클릭 실행기로 자동 세팅됩니다!)

---

## 🚀 3초 만에 실습 환경 시작하기 (가장 추천하는 방법)

파이썬 설치 버전 충돌이나 가상환경 설정 번거로움 없이, 최신 패키지 매니저 `uv`가 파이썬(Python 3.12)과 필수 라이브러리(NumPy, Qiskit, Jupyter Lab)를 격리된 환경에 즉시 세팅해 줍니다.

### 🪟 Windows 사용자
1. 본 저장소를 다운로드(Git Clone 또는 우측 상단 `Code` -> `Download ZIP` 후 압축 해제)합니다.
2. 폴더 내의 **`start_windows.bat`** 파일을 더블 클릭하여 실행합니다.
3. 잠시 후 패키지 동기화가 완료되면 기본 웹 브라우저에 **Jupyter Lab** 실습 화면이 자동으로 열립니다.

> **참고**: Windows 보안 경고(SmartScreen)가 뜨는 경우, `추가 정보` 클릭 후 `실행`을 눌러주시면 됩니다.

---

### 🍎 macOS 및 Linux 사용자
1. 터미널을 열고 본 저장소 폴더로 이동합니다.
2. 아래 명령어를 실행합니다:
   ```bash
   chmod +x start_mac.sh
   ./start_mac.sh
   ```
3. 자동으로 필요한 환경이 구성되고 브라우저에 **Jupyter Lab**이 실행됩니다.

---

## 🛠️ 수동 명령어 실행 (터미널/CLI 사용자)

이미 `uv`가 설치되어 있거나 터미널 사용이 익숙하시다면 아래 명령어로 직접 구동할 수 있습니다:

```bash
# 1. 저장소 클론
git clone https://github.com/saibie/quantum-computing-bootcamp-2026.git
cd quantum-computing-bootcamp-2026

# 2. 의존성 패키지 동기화 및 Jupyter Lab 실행
uv sync
uv run jupyter lab --notebook-dir=hands_on
```

---

## 📂 폴더 구조 안내

```text
├── docs/                               # 강의 교재 및 참고 문서 (PDF)
│   ├── syllabus_12hours.pdf            # 4주 강의 계획서 및 커리큘럼
│   ├── lecture_notes_12hours.pdf       # 수식/원리 통합 렉처노트
│   ├── day1_statevector.pdf            # Day 1 강의 슬라이드
│   ├── day2_entanglement.pdf           # Day 2 강의 슬라이드
│   ├── day3_algorithms.pdf             # Day 3 강의 슬라이드
│   └── day4_qubitsquare.pdf            # Day 4 강의 슬라이드
│
├── hands_on/                           # 주차별 핸즈온 실습 코드
│   ├── day1_numpy_statevector.ipynb    # [Day 1] 상태벡터, 브라켓 표기법, 단일 큐비트 게이트
│   ├── day2_numpy_entanglement.ipynb   # [Day 2] 텐서곱, CNOT 게이트, 벨 상태(Bell State)
│   ├── day3_qiskit_grover.ipynb        # [Day 3] Qiskit 1.x 기반 그로버 알고리즘 탐색
│   └── day4_qubitsquare_reference.ipynb# [Day 4] QubitSquare 클라우드 및 하드웨어 실습
│
├── start_windows.bat                   # Windows 원클릭 실습 실행기
├── start_mac.sh                        # Mac/Linux 원클릭 실습 실행기
├── pyproject.toml                      # 프로젝트 메타데이터 및 의존성 정의
└── uv.lock                             # 라이브러리 버전 고정 락파일
```

---

## 💡 주차별 학습 로드맵

| 주차 | 주제 | 핵심 내용 | 실습 환경 |
| :--- | :--- | :--- | :--- |
| **Day 1** | 단일 큐비트와 상태벡터 | 중첩($\alpha\|0\rangle + \beta\|1\rangle$), 파울리 게이트, 아다마르($H$), 블로흐 구면 | Pure NumPy |
| **Day 2** | 다중 큐비트와 양자 얽힘 | 크로네커 텐서곱($\otimes$), CNOT 게이트, 4대 벨 상태, 국소 측정 확률 | Pure NumPy |
| **Day 3** | 양자 알고리즘 기초 | 오라클(Oracle), 디퓨전(Diffusion), 그로버 탐색(Grover's Algorithm) | Qiskit 1.x |
| **Day 4** | 양자 하드웨어 및 클라우드 | QubitSquare 플랫폼, 양자 회로 합성, 실제 백엔드 잡(Job) 제출 | Qiskit & QubitSquare |

---

## 🌐 Google Colab 대안 (비상용)

로컬 PC 환경 설정에 어려움이 있을 경우, 웹 브라우저에서 바로 실행 가능한 Google Colab을 이용하실 수 있습니다:
1. [Google Colab](https://colab.research.google.com/) 접속
2. `GitHub` 탭 선택 후 `saibie/quantum-computing-bootcamp-2026` 입력
3. 원하는 주차의 `.ipynb` 파일을 열고 실행 (Colab 첫 셀에서 `!pip install qiskit qiskit-aer` 실행 필요)

---

## 📬 문의 및 지원
- 강의 내용 및 실습 환경 관련 문의: 강의 시간 중 질의응답 또는 GitHub Issue 등록
- 저작권: 본 자료의 저작권은 **(주)큐렌스** 및 강사 **서상협**에게 있습니다. 교육 목적 외 무단 배포 및 상업적 이용을 금합니다.
