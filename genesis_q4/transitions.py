"""Q4 transition validation — enforces the Gray-Code policy gate."""

from __future__ import annotations


class InvalidTransitionError(Exception):
    """Raised when a Q4 state transition violates the Gray-Code invariant."""

    def __init__(self, from_id: int, to_id: int, hamming: int) -> None:
        self.from_id = from_id
        self.to_id = to_id
        self.hamming = hamming
        super().__init__(
            f"Invalid Q4 transition {from_id:04b}→{to_id:04b}: "
            f"Hamming distance = {hamming}, expected 1. "
            f"Only single-bit Gray-Code transitions are allowed."
        )


class Q4TransitionValidator:
    """Enforces the Gray-Code policy gate for Q4 state transitions.

    Core invariant:
      A valid transition changes exactly one CREP dimension (Hamming distance = 1
      between Gray-encoded state IDs). Multi-bit jumps are rejected.

    This enforces that the system state can only change in one CREP dimension
    at a time — the fundamental runtime invariant of the Q4 layer.
    """

    def is_valid(self, from_id: int, to_id: int) -> bool:
        """True if the transition changes exactly one CREP bit (Hamming distance = 1)."""
        from genesis_q4.gray_code import GrayCode

        return GrayCode.hamming_distance(from_id, to_id) == 1

    def validate(self, from_id: int, to_id: int) -> None:
        """Raise InvalidTransitionError if the transition changes more than one CREP bit."""
        from genesis_q4.gray_code import GrayCode

        dist = GrayCode.hamming_distance(from_id, to_id)
        if dist != 1:
            raise InvalidTransitionError(from_id, to_id, dist)

    def suggest_path(self, from_id: int, to_id: int) -> list[int]:
        """Return an optimal multi-step path from from_id to to_id.

        Uses the tesseract BFS shortest path — all intermediate transitions
        have Hamming distance = 1.
        """
        from genesis_q4.tesseract import Tesseract

        return Tesseract().shortest_gray_path(from_id, to_id)
