#!/usr/bin/env bash
set -e

echo "========================================================"
echo " [양자컴퓨팅 이론&실습 4주 부트캠프] 실습 환경 시작기 (macOS/Linux)"
echo "========================================================"
echo ""

# 1. uv 설치 확인 및 자동 설치
if ! command -v uv &> /dev/null; then
    echo "[*] uv 패키지 매니저가 설치되어 있지 않습니다."
    echo "[*] 초고속 uv 설치를 시작합니다 (약 5초 소요)..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
fi

# 2. 환경 동기화 (Python 3.12 + NumPy/Qiskit 설치)
echo "[*] Python 3.12 및 실습 패키지(NumPy, Qiskit) 환경 동기화 중..."
uv sync

# 3. Jupyter Lab 실행
echo ""
echo "[*] Jupyter Lab 실습 환경을 실행합니다..."
echo "[*] 잠시 후 기본 웹 브라우저에서 실습 창이 자동으로 열립니다!"
echo ""
uv run jupyter lab --notebook-dir=hands_on
