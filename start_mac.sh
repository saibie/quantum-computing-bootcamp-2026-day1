#!/usr/bin/env bash
set -euo pipefail

# 스크립트가 위치한 디렉토리로 작업 경로 고정
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================================"
echo " Quantum Computing Bootcamp Day 1 - Environment Starter"
echo "========================================================"
echo ""

# 1. macOS 및 Linux 주요 실행 경로를 PATH에 등록
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"

# 2. uv 패키지 매니저 설치 확인 및 자동 설치
if ! command -v uv &> /dev/null; then
    echo "[*] uv package manager not found."
    echo "[*] Installing uv automatically (takes about 5 seconds)..."
    
    if command -v curl &> /dev/null; then
        curl -LsSf https://astral.sh/uv/install.sh | sh
    elif command -v wget &> /dev/null; then
        wget -qO- https://astral.sh/uv/install.sh | sh
    else
        echo "[ERROR] Neither curl nor wget is available. Please install uv manually: https://docs.astral.sh/uv/"
        exit 1
    fi
    
    export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
fi

# uv 설치 최종 검증
if ! command -v uv &> /dev/null; then
    echo "[ERROR] uv was installed but not detected in PATH."
    echo "[ERROR] Please restart your terminal and run ./start_mac.sh again."
    exit 1
fi

echo "[OK] uv detected: $(uv --version)"
echo ""

# 3. 가상환경 및 의존성 동기화 (Python 3.12, NumPy, Qiskit, Jupyter Lab)
echo "[*] Synchronizing Python environment and lab packages (uv sync)..."
if ! uv sync; then
    echo ""
    echo "[ERROR] uv sync failed. Please check your internet connection and try again."
    exit 1
fi

# 4. Jupyter Lab 실행
echo ""
echo "[*] Launching Jupyter Lab in your browser..."
echo "[*] Please keep this terminal window OPEN during your lab session."
echo ""
exec uv run jupyter lab --notebook-dir=hands_on
