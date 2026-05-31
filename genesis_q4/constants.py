"""Constants for the genesis-q4 16-state space."""

from __future__ import annotations

from typing import Final

# 16 states = 4 bit. H = log2(16) = 4 bit. NOT 16 bit.
Q4_STATE_COUNT: Final[int] = 16
Q4_BITS: Final[int] = 4
Q4_ENTROPY_BITS: Final[float] = 4.0  # log2(16) at uniform distribution

# Tesseract topology (4D hypercube, mathematical graph — not metaphysical)
TESSERACT_VERTICES: Final[int] = 16
TESSERACT_EDGES: Final[int] = 32
TESSERACT_FACES: Final[int] = 24
TESSERACT_CELLS: Final[int] = 8

# Gray-Code traversal order for 4x4 grid layout.
# Adjacent entries differ by exactly 1 bit (Hamming distance = 1).
GRAY_ORDER: Final[list[int]] = [0, 1, 3, 2, 6, 7, 5, 4, 12, 13, 15, 14, 10, 11, 9, 8]

# Engineering approximation of the golden ratio.
# NOT exact: Phi = 1.6180339... Error < 0.2%.
PHI_APPROX: Final[float] = 1.6

# CREP dimension names in canonical order (C=bit3, R=bit2, E=bit1, P=bit0)
CREP_DIMS: Final[tuple[str, ...]] = ("C", "R", "E", "P")
