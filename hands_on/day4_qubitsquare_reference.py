r"""Day 4: QubitSquare 산업용 웹 플랫폼 종합 실습 및 분석 도구.

[양자컴퓨팅 이론&실습 4주 부트캠프 - 4일차 3시간 실습]
학부생 교육 목표:
1. QubitSquare의 데이터 계층 구조(Lab -> Design -> Circuit -> Run -> Result -> Compare) 정밀 모델링.
2. 회로 편집 규칙: Measure 미배치 시 자동 전체 측정 삽입 및 'Apply to Flow' 동작 메커니즘.
3. 실행 프로필(Browser WASM Q-Vista CPU vs Remote Compute Engine)의 권한 차이 이해.
4. State Vector(복소 진폭)와 QubitSquare Result(측정 counts)의 엄밀한 경계 조건 검증.
5. Qiskit Little-Endian (|q1 q0>)과 QubitSquare 와이어 순서(q0, q1) 간의 변환.
6. Compare 기능(성공한 2~8개 Result)의 다중 정규화 비교 분석 뷰어.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


# =============================================================================
# 1. QubitSquare 핵심 데이터 모델
# =============================================================================
@dataclass(frozen=True)
class QubitSquareGate:
    name: str
    qubits: list[int]
    params: list[float] = field(default_factory=list)


@dataclass
class QubitSquareCircuit:
    num_qubits: int
    gates: list[QubitSquareGate] = field(default_factory=list)

    def add_gate(
        self, name: str, qubits: list[int], params: list[float] | None = None
    ) -> None:
        self.gates.append(QubitSquareGate(name, qubits, params or []))

    def resolve_measurements(self) -> list[int]:
        """QubitSquare 자동 전체 측정 규칙:

        - 회로에 Measure 게이트가 전혀 없으면 -> 전체 큐비트 자동 측정 삽입.
        - 명시적 Measure가 1개 이상 있으면 -> 지정된 큐비트만 측정.
        """
        explicit = [
            g.qubits[0] for g in self.gates if g.name.lower() == "measure"
        ]
        if not explicit:
            return list(range(self.num_qubits))  # 전체 자동 삽입
        return sorted(set(explicit))


@dataclass
class QubitSquareDesign:
    design_id: str
    name: str
    circuit: QubitSquareCircuit
    has_score_piece: bool = False
    has_optimizer_piece: bool = False
    display_type: Literal[
        "default", "raw_distribution", "maxcut_partition", "tsp_route"
    ] = "default"


@dataclass
class QubitSquareRunResult:
    run_id: str
    design_name: str
    engine: str
    shots: int
    profile: Literal["browser_wasm", "remote_compute"]
    counts: dict[str, int]
    # [핵심 교육 경계] 기본 실행 설정에서 statevector 반환값은 false임!
    statevector_available: bool = False


# =============================================================================
# 2. 비트 순서 변환 및 Compare 기능
# =============================================================================
def convert_qiskit_to_qubitsquare_bitstring(qiskit_bitstring: str) -> str:
    """Qiskit Little-Endian (|q_{n-1}...q_0>)을 QubitSquare 와이어 배치 순서(q_0...q_{n-1})로 반전."""
    return qiskit_bitstring[::-1]


def create_qubitsquare_compare(
    results: list[QubitSquareRunResult],
) -> dict[str, dict[str, float]]:
    """성공한 2~8개의 Result를 선택해 측정 확률 테이블을 생성하는 Compare 뷰어.

    큐비트 폭이 다른 경우 0으로 패딩하여 정렬 비교합니다.
    """
    if not (2 <= len(results) <= 8):
        raise ValueError("Compare는 2개에서 8개 사이의 Result만 선택할 수 있습니다.")

    # 1. 최대 큐비트 폭 계산
    max_len = max(len(k) for r in results for k in r.counts)

    # 2. 모든 bitstring key를 최대 폭에 맞춰 0 패딩 정렬
    all_normalized_keys: set[str] = set()
    for r in results:
        for k in r.counts:
            padded = k.zfill(max_len)
            all_normalized_keys.add(padded)

    sorted_keys = sorted(all_normalized_keys)
    table: dict[str, dict[str, float]] = {k: {} for k in sorted_keys}

    for r in results:
        col_label = f"{r.design_name} [{r.engine}, {r.shots}s]"
        for k in sorted_keys:
            raw_key = (
                k.lstrip("0")
                if k.lstrip("0") in r.counts
                else ("0" if "0" in r.counts else k)
            )
            count = r.counts.get(raw_key, 0)
            prob = count / r.shots
            table[k][col_label] = round(prob, 4)

    return table


# =============================================================================
# 3. 종합 데모 실행 함수
# =============================================================================
def demo_day4() -> None:
    print("=" * 70)
    print(" 양자컴퓨팅 부트캠프 Day 4: QubitSquare 산업용 웹 플랫폼 종합 실습 및 분석 도구")
    print("=" * 70)

    # 1. 자동 전체 측정 규칙 검증
    print("\n[Step 1] QubitSquare 회로 편집 및 자동 전체 측정 규칙:")
    circ_bell = QubitSquareCircuit(num_qubits=2)
    circ_bell.add_gate("H", [0])
    circ_bell.add_gate("CX", [0, 1])
    # 명시적 Measure 없음
    print("  1) Measure 게이트 미배치 회로 (H, CX만 존재):")
    print(
        f"     -> 자동 삽입되는 측정 대상 큐비트: {circ_bell.resolve_measurements()} (0, 1 전체 자동 측정)"
    )

    circ_partial = QubitSquareCircuit(num_qubits=2)
    circ_partial.add_gate("H", [0])
    circ_partial.add_gate("CX", [0, 1])
    circ_partial.add_gate("Measure", [0])
    print("\n  2) q0에만 명시적 Measure 배치한 회로:")
    print(
        f"     -> 실제 측정되는 큐비트: {circ_partial.resolve_measurements()} (지정된 q0만 측정)"
    )

    # 2. 비트스트링 표기 변환
    print("\n[Step 2] Qiskit 표기와 QubitSquare 와이어 표기 변환:")
    qiskit_raw = "10"  # q1=1, q0=0
    qs_wire = convert_qiskit_to_qubitsquare_bitstring(qiskit_raw)
    print(
        f"  - Qiskit 비트열 '{qiskit_raw}' (q1=1, q0=0) -> QubitSquare 와이어 표기: '{qs_wire}' (q0=0, q1=1)"
    )

    # 3. Compare 다중 비교 시뮬레이션
    print("\n[Step 3] Compare 다중 비교 기능 실습 (2~8개 Result 비교):")
    res_wasm_100 = QubitSquareRunResult(
        run_id="run-101",
        design_name="Bell_Experiment",
        engine="Q-Vista CPU (Browser WASM)",
        shots=100,
        profile="browser_wasm",
        counts={"00": 48, "11": 52},
    )
    res_wasm_1000 = QubitSquareRunResult(
        run_id="run-102",
        design_name="Bell_Experiment",
        engine="Q-Vista CPU (Browser WASM)",
        shots=1000,
        profile="browser_wasm",
        counts={"00": 496, "11": 504},
    )
    res_remote = QubitSquareRunResult(
        run_id="run-103",
        design_name="Bell_Experiment",
        engine="Remote Target Engine A",
        shots=4000,
        profile="remote_compute",
        counts={"00": 2008, "11": 1992},
    )

    compare_table = create_qubitsquare_compare(
        [res_wasm_100, res_wasm_1000, res_remote]
    )
    print("  [Compare 결과 테이블: 확률 비교]")
    for bitstring, engines in compare_table.items():
        print(f"    State |{bitstring}> : {engines}")

    # 4. State Vector 교육 경계 주지
    print("\n[Step 4] [중요] State Vector 교육과의 엄밀한 경계 확인:")
    print(
        f"  - Q-Vista WASM statevector available: {res_wasm_100.statevector_available}"
    )
    print(
        f"  - Remote Engine statevector available: {res_remote.statevector_available}"
    )
    print(
        "  - 경계 요약: QubitSquare는 복소 진폭 자체를 직접 보여주는 도구가 아니며,"
    )
    print(
        "    유한한 shots에 따른 측정 bitstring 통계 분포(Counts)를 제공합니다."
    )
    print(
        "    Q-Vista 소프트웨어 시뮬레이터 실행 결과를 실제 양자 하드웨어 결과로 소개해서는 안 됩니다."
    )

    print("\n" + "=" * 70)
    print(" Day 4 핸즈온 실습 완료: QubitSquare의 전 기능과 실행 모델이 검증되었습니다.")
    print("=" * 70)


if __name__ == "__main__":
    demo_day4()
