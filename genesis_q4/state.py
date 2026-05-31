"""Q4State: the 4-bit state in the GenesisAeon Q4 state space."""

from __future__ import annotations

from dataclasses import dataclass

from genesis_q4.constants import Q4_ENTROPY_BITS

# Module-level cache for all_states() — avoids ClassVar mutation issues on frozen dataclass.
_ALL_STATES: list["Q4State"] | None = None


@dataclass(frozen=True)
class Q4State:
    """4-bit state in the GenesisAeon Q4 state space.

    Each field is a binary flag (0 or 1) for one CREP dimension:
      C — Coherence
      R — Resonance
      E — Emergence
      P — Poetics

    State ID: 8*C + 4*R + 2*E + P   (0..15)
    16 states = 4 bit. NOT 16 bit.

    All instances are immutable (frozen=True) and hashable.
    """

    C: int
    R: int
    E: int
    P: int

    def __post_init__(self) -> None:
        for name, value in (("C", self.C), ("R", self.R), ("E", self.E), ("P", self.P)):
            if value not in (0, 1):
                raise ValueError(f"Q4State.{name} must be 0 or 1, got {value!r}")

    @property
    def id(self) -> int:
        """Integer ID in range 0..15."""
        return 8 * self.C + 4 * self.R + 2 * self.E + self.P

    @property
    def binary(self) -> str:
        """4-character binary string, e.g. '1011'."""
        return f"{self.id:04b}"

    @property
    def gray_id(self) -> int:
        """Gray-encoded ID: id XOR (id >> 1)."""
        n = self.id
        return n ^ (n >> 1)

    @property
    def entropy_bits(self) -> float:
        """Shannon entropy contribution at uniform distribution: log2(16) = 4.0 bit."""
        return Q4_ENTROPY_BITS

    @property
    def flags(self) -> dict[str, int]:
        """CREP flags as a plain dict."""
        return {"C": self.C, "R": self.R, "E": self.E, "P": self.P}

    @classmethod
    def from_id(cls, state_id: int) -> "Q4State":
        """Construct a Q4State from its integer ID (0..15)."""
        if not 0 <= state_id <= 15:
            raise ValueError(f"state_id must be 0..15, got {state_id}")
        return cls(
            C=(state_id >> 3) & 1,
            R=(state_id >> 2) & 1,
            E=(state_id >> 1) & 1,
            P=state_id & 1,
        )

    @classmethod
    def from_binary(cls, bits: str) -> "Q4State":
        """Construct from a 4-character binary string, e.g. '1011'."""
        if len(bits) != 4 or not all(b in "01" for b in bits):
            raise ValueError(f"bits must be a 4-character binary string, got {bits!r}")
        return cls.from_id(int(bits, 2))

    @classmethod
    def all_states(cls) -> list["Q4State"]:
        """Return all 16 Q4States ordered by ID (0..15)."""
        global _ALL_STATES
        if _ALL_STATES is None:
            _ALL_STATES = [cls.from_id(i) for i in range(16)]
        return list(_ALL_STATES)

    def __repr__(self) -> str:
        return f"Q4State(C={self.C}, R={self.R}, E={self.E}, P={self.P}, id={self.id})"

    def __str__(self) -> str:
        return f"Q4[{self.binary}]"
