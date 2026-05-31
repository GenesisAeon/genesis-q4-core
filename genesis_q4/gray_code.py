"""Gray-Code encoding/decoding for Q4 state transitions.

Core invariant:
  hamming_distance(gray(n), gray(n+1)) == 1  for all n in 0..14

This guarantees single-bit transitions between adjacent Q4 states.
"""

from __future__ import annotations


class GrayCode:
    """Gray-Code utilities for 4-bit Q4 state transitions.

    The invariant hamming_distance(encode(n), encode(n+1)) == 1 is the
    mathematical foundation of the Q4 PolicyGate: state transitions may
    only change one CREP dimension at a time.
    """

    @staticmethod
    def encode(n: int) -> int:
        """Binary to Gray: g(n) = n XOR (n >> 1)."""
        if not 0 <= n <= 15:
            raise ValueError(f"n must be 0..15, got {n}")
        return n ^ (n >> 1)

    @staticmethod
    def decode(g: int) -> int:
        """Gray to binary (inverse Gray-Code)."""
        if not 0 <= g <= 15:
            raise ValueError(f"g must be 0..15, got {g}")
        mask = g >> 1
        n = g
        while mask:
            n ^= mask
            mask >>= 1
        return n

    @staticmethod
    def hamming_distance(a: int, b: int) -> int:
        """Number of differing bits between two integers."""
        return bin(a ^ b).count("1")

    @staticmethod
    def validate_sequence(state_ids: list[int]) -> bool:
        """Return True if every consecutive pair of states has Hamming distance 1.

        Checks plain Hamming distance on state IDs. Valid adjacent states
        are those whose binary representation differs in exactly one bit.
        """
        if len(state_ids) < 2:
            return True
        return all(
            GrayCode.hamming_distance(state_ids[i], state_ids[i + 1]) == 1
            for i in range(len(state_ids) - 1)
        )

    @staticmethod
    def neighbors(state_id: int) -> list[int]:
        """Return all state IDs reachable in exactly one bit-flip from state_id.

        These are the neighbors in the 4D hypercube: states whose binary
        representation differs from state_id in exactly 1 bit (Hamming = 1).
        Each state has exactly 4 neighbors.
        """
        if not 0 <= state_id <= 15:
            raise ValueError(f"state_id must be 0..15, got {state_id}")
        return sorted(state_id ^ (1 << bit) for bit in range(4))

    @staticmethod
    def full_sequence() -> list[int]:
        """Canonical Gray-Code traversal of all 16 states.

        Returns [0,1,3,2,6,7,5,4,12,13,15,14,10,11,9,8].
        Adjacent entries differ by exactly 1 bit (standard reflected Gray code).
        Computed as encode(g) for g in range(16).
        """
        return [g ^ (g >> 1) for g in range(16)]
