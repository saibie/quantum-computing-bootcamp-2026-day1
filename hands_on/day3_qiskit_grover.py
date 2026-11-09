"""Day 3: 양자 간섭과 2-qubit Grover 알고리즘 심화 실습 교재.

[양자컴퓨팅 이론&실습 4주 부트캠프 - 3일차 3시간 실습]
학부생 교육 목표:
1. 양자 간섭의 수학적 메커니즘(보강 간섭과 상쇄 간섭)의 행렬/벡터 추적.
2. 4가지 타겟 기저(|00>, |01>, |10>, |11>)에 대한 Phase Oracle 설계.
3. 평균에 대한 대칭 반전(Inversion about the mean)을 수행하는 확산 연산자(Diffusion Operator) 구현.
4. 단 1회 연산만으로 타겟 상태 진폭이 100%로 수렴하는 과정의 수학적/코드적 증명.
5. 유한 측정에 따른 Shot Noise(통계적 요동) 및 실제 양자 하드웨어(NISQ)에서의 오류 특성 분석.
"""

from __future__ import annotations

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


# =============================================================================
# 1. NumPy 기반 Grover 연산자 엄밀 구현
# =============================================================================
def numpy_grover_step(
    target: str = "11",
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """NumPy만을 이용해 Grover 알고리즘의 3단계 상태벡터 변화를 계산.

    반환: (init_superposition, after_oracle, after_diffusion)
    """
    # 1. 초기 균등 중첩 |s> = 1/2 [1, 1, 1, 1]^T
    s_state = 0.5 * np.ones((4, 1), dtype=complex)

    # 2. Phase Oracle 행렬: I - 2|omega><omega|
    target_idx = {"00": 0, "01": 1, "10": 2, "11": 3}[target]
    oracle_matrix = np.eye(4, dtype=complex)
    oracle_matrix[target_idx, target_idx] = -1.0

    after_oracle = oracle_matrix @ s_state

    # 3. Diffusion 행렬: 2|s><s| - I
    diffusion_matrix = 2.0 * (s_state @ s_state.conj().T) - np.eye(
        4, dtype=complex
    )
    after_diffusion = diffusion_matrix @ after_oracle

    return s_state, after_oracle, after_diffusion


# =============================================================================
# 2. Qiskit 기반 Grover 회로 조립 함수
# =============================================================================
def build_grover_circuit(target: str = "11") -> QuantumCircuit:
    """타겟 문자열('00', '01', '10', '11')에 대한 2-qubit Grover 회로 생성."""
    qc = QuantumCircuit(2, name=f"Grover_{target}")

    # Step 1: 초기 균등 중첩 상태
    qc.h([0, 1])

    # Step 2: Phase Oracle (타겟 상태의 위상만 -1로 반전)
    # Qiskit Little-Endian 주의: target = 'q1 q0'
    if target == "00":
        qc.x([0, 1])
        qc.cz(0, 1)
        qc.x([0, 1])
    elif target == "01":  # q1=0, q0=1
        qc.x(1)
        qc.cz(0, 1)
        qc.x(1)
    elif target == "10":  # q1=1, q0=0
        qc.x(0)
        qc.cz(0, 1)
        qc.x(0)
    elif target == "11":  # q1=1, q0=1
        qc.cz(0, 1)
    else:
        raise ValueError(f"유효하지 않은 타겟: {target}")

    # Step 3: Diffusion Operator (H -> X -> CZ -> X -> H)
    qc.h([0, 1])
    qc.x([0, 1])
    qc.cz(0, 1)
    qc.x([0, 1])
    qc.h([0, 1])

    return qc


# =============================================================================
# 3. 종합 데모 실행 함수
# =============================================================================
def demo_day3() -> None:
    print("=" * 70)
    print(" 양자컴퓨팅 부트캠프 Day 3: 양자 간섭과 2-qubit Grover 탐색 알고리즘 심화 실습")
    print("=" * 70)

    # 1. NumPy 수학적 단계별 추적
    print("\n[Step 1] NumPy를 이용한 진폭 증폭 수치 검증 (|11> 타겟):")
    s0, s1, s2 = numpy_grover_step(target="11")
    print("  1) 초기 균등 중첩 |s>:    ", np.round(s0.flatten(), 3))
    print("  2) Oracle 적용 후 (위상반전):", np.round(s1.flatten(), 3))
    print("  3) Diffusion 후 (평균반전):  ", np.round(s2.flatten(), 3))
    print("  -> 비타겟(00, 01, 10)은 진폭 0으로 상쇄되고, 타겟(11)만 진폭 1.0으로 보강됨!")

    # 2. 4가지 모든 타겟에 대한 Qiskit 회로 검증
    print("\n[Step 2] 4가지 모든 타겟(|00>, |01>, |10>, |11>)에 대한 100% 탐색 검증:")
    for tgt in ["00", "01", "10", "11"]:
        qc = build_grover_circuit(target=tgt)
        sv = Statevector.from_instruction(qc)
        prob = sv.probabilities_dict().get(tgt, 0.0)
        print(f"  타겟 |{tgt}> 회로 실행: 적중 확률 = {prob * 100.0:.1f}%")
        assert np.isclose(prob, 1.0)

    # 3. Shot Noise와 표본 크기 수렴 분석
    print("\n[Step 3] 유한한 Shot 수에 따른 통계적 변동 (Shot Noise 분석):")
    qc_11 = build_grover_circuit(target="11")
    sv_11 = Statevector.from_instruction(qc_11)

    print("  타겟 |11> 회로의 Shot 수별 측정 결과:")
    for shots in [10, 50, 200, 1024, 8192]:
        counts = sv_11.sample_counts(shots=shots)
        hit_ratio = counts.get("11", 0) / shots
        print(
            f"  - Shots {shots:5d}: counts = {counts} -> 적중률 = {hit_ratio * 100.0:.2f}%"
        )

    print("\n[Step 4] 이상적 시뮬레이터 vs 실제 양자 하드웨어(NISQ)의 차이:")
    print("  - 이상적 상태벡터 시뮬레이터: 오류가 없으므로 100.0% 검출.")
    print(
        "  - 실제 초전도 양자 하드웨어: 2큐비트 CZ 게이트 오류 및 T1, T2 결어맞춤(Decoherence)으로 인해"
    )
    print("    실제 적중률은 약 85% ~ 95% 수준으로 측정되며 다른 상태의 오차가 함께 발생합니다.")

    print("\n" + "=" * 70)
    print(" Day 3 핸즈온 실습 완료: Grover 알고리즘의 진폭 증폭 원리가 입증되었습니다.")
    print("=" * 70)


if __name__ == "__main__":
    demo_day3()
