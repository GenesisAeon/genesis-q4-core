"""genesis-q4: 16-state space, Gray-Code encoding, and Tesseract topology.

Mathematical foundations:
  16 states = 4 bit   (H = log2(16) = 4 bit — NOT 16 bit)
  Gray-Code: g(n) = n XOR (n >> 1)
  Hamming distance between consecutive Gray-codes: always 1
  Tesseract: 16 vertices, 32 edges, 24 faces, 8 cells

No dependencies on other GenesisAeon repositories.
"""

from genesis_q4.constants import (
    CREP_DIMS,
    GRAY_ORDER,
    PHI_APPROX,
    Q4_BITS,
    Q4_ENTROPY_BITS,
    Q4_STATE_COUNT,
    TESSERACT_CELLS,
    TESSERACT_EDGES,
    TESSERACT_FACES,
    TESSERACT_VERTICES,
)
from genesis_q4.gray_code import GrayCode
from genesis_q4.navigator import Q4Navigator
from genesis_q4.serializer import (
    state_from_dict,
    state_from_json,
    state_space_to_json,
    state_to_dict,
    state_to_json,
)
from genesis_q4.state import Q4State
from genesis_q4.tesseract import Tesseract
from genesis_q4.transitions import InvalidTransitionError, Q4TransitionValidator

__all__ = [
    "Q4State",
    "GrayCode",
    "Tesseract",
    "Q4TransitionValidator",
    "InvalidTransitionError",
    "Q4Navigator",
    "state_to_dict",
    "state_from_dict",
    "state_to_json",
    "state_from_json",
    "state_space_to_json",
    "Q4_STATE_COUNT",
    "Q4_BITS",
    "Q4_ENTROPY_BITS",
    "TESSERACT_VERTICES",
    "TESSERACT_EDGES",
    "TESSERACT_FACES",
    "TESSERACT_CELLS",
    "GRAY_ORDER",
    "PHI_APPROX",
    "CREP_DIMS",
]

__version__ = "0.1.0"
