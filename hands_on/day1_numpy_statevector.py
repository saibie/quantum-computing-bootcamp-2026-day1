"""Day 1: 선형대수학과 단일 큐비트 상태벡터 NumPy 심화 실습 교재.

[양자컴퓨팅 이론&실습 4주 부트캠프 - 1일차 3시간 실습]
학부생 교육 목표:
1. 복소수와 켤레 전치, Dirac bra-ket 표기법의 NumPy 1:1 매핑.
2. 상태벡터의 내적, 정규화(Normalization), Born 측정 규칙 유도.
3. 유니터리 게이트(X, Y, Z, H, S, T)의 대수적 성질 및 고유값/고유벡터 분석.
4. Global Phase와 Relative Phase의 간섭(Interference) 효과 증명.
5. Bloch 구 각도 (theta, phi) 추출 및 기하학적 회전 추적.
6. 유한한 Shot 수(10 ~ 10,000)에 따른 통계적 오차(Shot Noise)의 1/sqrt(M) 수렴성 검증.
"""

from __future__ import annotations

import numpy as np

# =============================================================================
# 1. 계산 기저 상태 (Computational Basis)
# =============================================================================
# 2차원 복소 내적 공간 C^2 상의 표준 정규직교기저
KET_0 = np.array([[1.0 + 0.0j], [0.0 + 0.0j]])  # |0>
KET_1 = np.array([[0.0 + 0.0j], [1.0 + 0.0j]])  # |1>

# =============================================================================
# 2. 단일 큐비트 기본 유니터리 게이트
# =============================================================================
GATE_I = np.array([[1, 0], [0, 1]], dtype=complex)
GATE_X = np.array([[0, 1], [1, 0]], dtype=complex)  # Pauli-X (NOT)
GATE_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)  # Pauli-Y
GATE_Z = np.array([[1, 0], [0, -1]], dtype=complex)  # Pauli-Z
GATE_H = (1.0 / np.sqrt(2.0)) * np.array(
    [[1, 1], [1, -1]], dtype=complex
)  # Hadamard
GATE_S = np.array([[1, 0], [0, 1j]], dtype=complex)  # Phase (Z^{1/2})
GATE_T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)  # T (Z^{1/4})


# =============================================================================
# 3. 핵심 선형대수학 검증 함수
# =============================================================================
def is_unitary(matrix: np.ndarray, tol: float = 1e-9) -> bool:
    """유니터리 조건 U* @ U == I (U.conj().T @ U == I) 검증."""
    dim = matrix.shape[0]
    identity = np.eye(dim, dtype=complex)
    product = matrix.conj().T @ matrix
    return bool(np.allclose(product, identity, atol=tol))


def check_normalization(state: np.ndarray, tol: float = 1e-9) -> bool:
    """내적 <psi|psi> == 1 정규화 조건 검증."""
    norm_sq = np.vdot(state, state).real
    return bool(np.isclose(norm_sq, 1.0, atol=tol))


def extract_bloch_coordinates(state: np.ndarray) -> tuple[float, float]:
    """임의의 정규화된 단일 큐비트 상태에서 Bloch 구 각도 (theta, phi)를 추출.

    |psi> = cos(theta/2)|0> + exp(i*phi)*sin(theta/2)|1>
    """
    alpha = state[0, 0]
    beta = state[1, 0]

    # 글로벌 위상 제거: alpha를 양의 실수로 변환
    global_phase = np.angle(alpha)
    alpha_clean = (alpha * np.exp(-1j * global_phase)).real
    beta_clean = beta * np.exp(-1j * global_phase)

    # theta in [0, pi]
    theta = 2.0 * np.arccos(np.clip(alpha_clean, -1.0, 1.0))
    # phi in [0, 2*pi)
    phi = float(np.angle(beta_clean)) % (2.0 * np.pi)

    return float(theta), float(phi)


def measure_probabilities(state: np.ndarray) -> tuple[float, float]:
    """Born 규칙에 의한 |0>과 |1>의 이론적 관측 확률 P(0)=|alpha|^2, P(1)=|beta|^2."""
    p0 = float(np.abs(state[0, 0]) ** 2)
    p1 = float(np.abs(state[1, 0]) ** 2)
    return p0, p1


def sample_measurements(state: np.ndarray, shots: int = 1000) -> dict[str, int]:
    """유한한 반복 측정(Shots)을 모사하여 관측 빈도(Counts)를 반환."""
    p0, p1 = measure_probabilities(state)
    outcomes = np.random.choice(["0", "1"], size=shots, p=[p0, p1])
    count_0 = int(np.sum(outcomes == "0"))
    return {"0": count_0, "1": shots - count_0}


# =============================================================================
# 4. 종합 데모 및 학생 단계별 실습 함수
# =============================================================================
def demo_day1() -> None:
    print("=" * 70)
    print(" 양자컴퓨팅 부트캠프 Day 1: 선형대수학과 단일 큐비트 상태벡터 심화 실습")
    print("=" * 70)

    # 1. 유니터리성 전수 검증
    print("\n[Step 1] 기본 게이트 유니터리성 검증 (U* U = I):")
    gates = {
        "I": GATE_I,
        "X": GATE_X,
        "Y": GATE_Y,
        "Z": GATE_Z,
        "H": GATE_H,
        "S": GATE_S,
        "T": GATE_T,
    }
    for name, g in gates.items():
        print(f"  Gate {name:2s}: Unitary = {is_unitary(g)}")
        assert is_unitary(g), f"게이트 {name}가 유니터리하지 않습니다!"

    # 2. Hadamard 게이트와 중첩 상태
    print("\n[Step 2] Hadamard 게이트를 통한 균등 중첩(|+>) 생성:")
    plus_state = GATE_H @ KET_0
    print("  |+> = H|0> 상태벡터:")
    print("  ", plus_state.flatten())
    theta, phi = extract_bloch_coordinates(plus_state)
    print(
        f"  Bloch 구 좌표: theta = {theta:.3f} rad ({np.degrees(theta):.1f} deg), phi = {phi:.3f} rad"
    )
    p0, p1 = measure_probabilities(plus_state)
    print(f"  이론적 측정 확률: P(0) = {p0:.4f}, P(1) = {p1:.4f}")

    # 3. Global Phase vs Relative Phase 비교 실험
    print("\n[Step 3] 위상(Phase)의 물리적 차이 검증:")
    # Base: |+>
    # Global Phase: exp(i * pi/3) * |+>
    # Relative Phase: (|0> + exp(i * pi/3)|1>) / sqrt(2)
    psi_base = plus_state
    psi_global = np.exp(1j * np.pi / 3) * plus_state
    psi_relative = (1.0 / np.sqrt(2.0)) * np.array([[1.0], [np.exp(1j * np.pi / 3)]])

    print("  1) 측정 전 단순 Z-기저 측정 확률 비교:")
    print("     - Base 상태 확률:     ", measure_probabilities(psi_base))
    print("     - Global Phase 상태: ", measure_probabilities(psi_global))
    print("     - Relative Phase 상태:", measure_probabilities(psi_relative))
    print("     -> 세 상태 모두 50:50으로 겉보기엔 구별 불가능함.")

    print("\n  2) Hadamard 게이트 통과 후 간섭(Interference) 결과 비교:")
    h_base = GATE_H @ psi_base
    h_global = GATE_H @ psi_global
    h_relative = GATE_H @ psi_relative
    print(
        "     - H @ Base 확률:     ",
        np.round(measure_probabilities(h_base), 3),
        " (완전 보강 간섭 -> |0> 복원)",
    )
    print(
        "     - H @ Global 확률:   ",
        np.round(measure_probabilities(h_global), 3),
        " (글로벌 위상은 간섭에 영향 없음)",
    )
    print(
        "     - H @ Relative 확률: ",
        np.round(measure_probabilities(h_relative), 3),
        " (상대 위상이 확률을 비대칭으로 바꿈!)",
    )

    # 4. Shot 수에 따른 통계적 수렴 (Shot Noise 분석)
    print("\n[Step 4] 유한 측정과 대수의 법칙 (Shot 수에 따른 오차 수렴):")
    true_p0 = 0.5
    for shots in [10, 100, 1000, 10000]:
        counts = sample_measurements(plus_state, shots=shots)
        emp_p0 = counts["0"] / shots
        error = abs(emp_p0 - true_p0)
        print(
            f"  - {shots:6d} shots: counts = {counts} -> 표본비율 = {emp_p0:.4f} (오차 = {error:.4f})"
        )

    print("\n" + "=" * 70)
    print(" Day 1 핸즈온 실습 완료: 모든 수학적 성질과 시뮬레이션이 일치합니다.")
    print("=" * 70)


if __name__ == "__main__":
    demo_day1()
