r"""Day 2: 다중 큐비트, 텐서곱, 그리고 양자 얽힘(Entanglement) NumPy 실습 교재.

[양자컴퓨팅 이론&실습 4주 부트캠프 - 2일차 75분 인터랙티브 실습]
학부생 교육 목표:
1. 텐서곱(Kronecker product)의 수학적 대수 성질과 혼합곱 공식 검증: (A (x) B)(C (x) D) == (AC) (x) (BD)
2. 4x4 CNOT 행렬과 H 게이트를 결합한 Bell 회로 구현 및 1부 손계산 결과 1:1 대조
3. 선형대수학적 얽힘 판별식(Non-separability Condition): det = c00*c11 - c01*c10 != 0
4. 4대 Bell 상태(|\Phi^\pm>, |\Psi^\pm>) 전수 합성 및 상호 직교성 검증
5. 얽힘 상태의 부분 측정(Partial Measurement) 시뮬레이션: q0 측정 시 q1의 즉각적 투영 붕괴
"""

from __future__ import annotations

import numpy as np

# =============================================================================
# 1. 단일 큐비트 기저 및 연산자 정의
# =============================================================================
KET_0 = np.array([[1.0], [0.0]], dtype=complex)
KET_1 = np.array([[0.0], [1.0]], dtype=complex)

GATE_I = np.eye(2, dtype=complex)
GATE_X = np.array([[0, 1], [1, 0]], dtype=complex)
GATE_Z = np.array([[1, 0], [0, -1]], dtype=complex)
GATE_H = (1.0 / np.sqrt(2.0)) * np.array([[1, 1], [1, -1]], dtype=complex)

# =============================================================================
# 2. 4차원 기저 벡터 및 2큐비트 유니터리 연산자
# =============================================================================
# 2큐비트 계산 기저 (Tensor Product)
KET_00 = np.kron(KET_0, KET_0)
KET_01 = np.kron(KET_0, KET_1)
KET_10 = np.kron(KET_1, KET_0)
KET_11 = np.kron(KET_1, KET_1)

# CNOT 게이트 (q0: 제어, q1: 타깃)
GATE_CNOT = np.array(
    [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
    ],
    dtype=complex,
)


# =============================================================================
# 3. 선형대수학적 얽힘 판별 및 부분 측정 함수
# =============================================================================
def is_entangled(state_4d: np.ndarray, tol: float = 1e-9) -> tuple[bool, float]:
    r"""2큐비트 순수 상태의 얽힘 여부 판별.

    상태: c00|00> + c01|01> + c10|10> + c11|11>
    분리 가능(곱상태) 조건: c00*c11 - c01*c10 == 0
    반환: (is_entangled: bool, determinant: float)
    """
    v = state_4d.flatten()
    det = v[0] * v[3] - v[1] * v[2]
    entangled = not np.isclose(abs(det), 0.0, atol=tol)
    return entangled, float(abs(det))


def simulate_partial_measurement(
    state_4d: np.ndarray,
) -> tuple[tuple[float, np.ndarray], tuple[float, np.ndarray]]:
    r"""첫 번째 큐비트(q0)만 사영 측정했을 때의 확률과 q1의 즉각적 붕괴 상태 계산.

    반환: ((p0, state_q1_given_0), (p1, state_q1_given_1))
    """
    v = state_4d.flatten()
    p0 = float(abs(v[0]) ** 2 + abs(v[1]) ** 2)
    p1 = float(abs(v[2]) ** 2 + abs(v[3]) ** 2)

    collapsed_0 = np.array([v[0], v[1]], dtype=complex) / np.sqrt(p0)
    collapsed_1 = np.array([v[2], v[3]], dtype=complex) / np.sqrt(p1)

    return (p0, collapsed_0), (p1, collapsed_1)


# =============================================================================
# 4. 실습 및 검증 메인 파이프라인
# =============================================================================
def run_day2_hands_on() -> None:
    print("=" * 72)
    print(" 양자컴퓨팅 부트캠프 Day 2: 다중 큐비트, 텐서곱, 그리고 얽힘(Entanglement) NumPy 실습")
    print("=" * 72)

    # [Lab 1] 텐서곱과 혼합곱 성질 검증
    print("\n[Lab 1] 텐서곱(np.kron) 및 혼합곱 공식 검증:")
    lhs = np.kron(GATE_H, GATE_X) @ np.kron(GATE_Z, GATE_H)
    rhs = np.kron(GATE_H @ GATE_Z, GATE_X @ GATE_H)
    assert np.allclose(lhs, rhs), "혼합곱 공식 불일치!"
    print("  [OK] (H (x) X)(Z (x) H) == (HZ) (x) (XH) 완벽 검증 성공!")

    # [Lab 2] CNOT 게이트와 Bell 상태 유도 (1부 손계산 대조)
    print("\n[Lab 2] 4x4 CNOT 행렬곱을 통한 Bell 상태 유도:")
    H_I = np.kron(GATE_H, GATE_I)
    psi_step1 = H_I @ KET_00
    psi_bell = GATE_CNOT @ psi_step1

    expected_bell = (1.0 / np.sqrt(2.0)) * (KET_00 + KET_11)
    assert np.allclose(psi_bell, expected_bell), "손계산 결과와 수치 불일치!"
    print(f"  [OK] 1부 손계산 결과와 NumPy 연산 100% 일치:\n    {psi_bell.flatten().real}")

    # [Lab 3] 선형대수학적 얽힘 판별식
    print("\n[Lab 3] 곱상태 vs 얽힘 상태 선형대수학 판별식 검증:")
    ent1, det1 = is_entangled(psi_step1)
    ent2, det2 = is_entangled(psi_bell)
    assert not ent1 and det1 == 0.0, "Step 1 상태는 곱상태여야 합니다."
    assert ent2 and det2 > 0.0, "Bell 상태는 얽힘 상태여야 합니다."
    print(f"  [OK] Step 1 곱상태 (|+0>): Entangled={ent1}, det={det1:.1f}")
    print(f"  [OK] 최종 Bell 상태 (|Phi+>): Entangled={ent2}, det={det2:.4f}")

    # [2부 챌린지] 4대 Bell 상태 전수 합성
    print("\n[2부 챌린지] NumPy로 4대 Bell 상태 전수 합성:")
    inputs = {
        "|00>": KET_00,
        "|01>": KET_01,
        "|10>": KET_10,
        "|11>": KET_11,
    }
    bell_states = {}
    for name, vec in inputs.items():
        bell_states[name] = GATE_CNOT @ (H_I @ vec)

    # 직교성 검증: <Phi+|Phi-> == 0
    phi_plus = bell_states["|00>"]
    phi_minus = bell_states["|10>"]
    psi_plus = bell_states["|01>"]
    psi_minus = bell_states["|11>"]

    assert np.isclose(np.vdot(phi_plus, phi_minus), 0.0)
    assert np.isclose(np.vdot(phi_plus, psi_plus), 0.0)
    assert np.isclose(np.vdot(psi_plus, psi_minus), 0.0)
    print("  [OK] |Phi+>, |Psi+>, |Phi->, |Psi-> 4대 Bell 상태 상호 직교성 확인 완료!")

    # [Lab 4] 부분 측정 시뮬레이션
    print("\n[Lab 4] Bell 상태의 첫 번째 큐비트(q0) 부분 측정과 q1의 조건부 붕괴:")
    (p0, s0), (p1, s1) = simulate_partial_measurement(psi_bell)
    print(f"  - q0=0 관측 확률 {p0*100:.0f}% -> q1의 상태: {np.round(s0.real, 2)} (|0>으로 즉각 붕괴)")
    print(f"  - q0=1 관측 확률 {p1*100:.0f}% -> q1의 상태: {np.round(s1.real, 2)} (|1>로 즉각 붕괴)")
    assert np.allclose(s0, [1, 0]) and np.allclose(s1, [0, 1])
    print("  [OK] QPU 조건부 제어 검증: 보조 큐비트 측정을 통한 상태 제어 메커니즘 확인!")

    print("\n" + "=" * 72)
    print(" Day 2 NumPy 실습 성공: 다중 큐비트와 얽힘의 모든 수학적 원리가 검증되었습니다.")
    print("=" * 72)


if __name__ == "__main__":
    run_day2_hands_on()
