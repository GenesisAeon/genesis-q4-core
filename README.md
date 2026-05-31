# genesis-q4-core

**16-State Q4 Space · Gray-Code Encoding · Tesseract Topology**

[![PyPI](https://img.shields.io/pypi/v/genesis-q4-core)](https://pypi.org/project/genesis-q4-core/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)

The mathematical foundation of the [GenesisAeon](https://github.com/GenesisAeon) cognitive runtime:
a fully tested, zero-dependency Python library for the 16-state Q4 state space.

---

## Mathematical Foundations

| Concept | Value |
|---|---|
| State count | 16 |
| Bits required | **4 bit** (`H = log₂(16) = 4 bit` — **not** 16 bit) |
| Gray-Code | `g(n) = n XOR (n >> 1)` |
| Hamming distance (consecutive Gray states) | always **1** |
| Tesseract vertices | 16 |
| Tesseract edges | 32 |
| Tesseract faces | 24 |
| Tesseract cells | 8 |

The **Tesseract** is a 4D hypercube with 16 vertices — a topological data structure,
not a metaphysical statement.

---

## Installation

```bash
pip install genesis-q4-core
# with YAML support:
pip install "genesis-q4-core[yaml]"
# with CLI:
pip install "genesis-q4-core[cli]"
```

## Quick Start

```python
from genesis_q4 import Q4State, GrayCode, Tesseract, Q4TransitionValidator

# Create a state
s = Q4State(C=1, R=0, E=1, P=1)
print(s.id)           # 11
print(s.binary)       # "1011"
print(s.gray_id)      # 10
print(s.entropy_bits) # 4.0  (log₂(16) = 4 bit)

# Gray-Code
print(GrayCode.encode(5))  # 7
print(GrayCode.decode(7))  # 5
# Core invariant: consecutive Gray codes differ by exactly 1 bit
for n in range(15):
    assert GrayCode.hamming_distance(GrayCode.encode(n), GrayCode.encode(n+1)) == 1

# Tesseract navigation
t = Tesseract()
print(t.neighbors(0))               # [1, 2, 4, 8]
print(t.shortest_gray_path(0, 15))  # [0, 1, 3, 7, 15]

# Transition validation (Gray-Code policy gate)
v = Q4TransitionValidator()
v.validate(0, 1)    # OK — Hamming distance = 1
v.validate(0, 15)   # raises InvalidTransitionError — Hamming = 4
path = v.suggest_path(0, 15)  # [0, 1, 3, 7, 15]
```

## CLI

```bash
genesis-q4 state --id 11          # Show state 1011
genesis-q4 path --from 0 --to 15  # Shortest Gray path
genesis-q4 validate --from 5 --to 7
genesis-q4 visualize --format mermaid
```

## State Space

The 16 Q4 states encode binary flags for four CREP dimensions:

| Dimension | Bit | Default Threshold |
|---|---|---|
| C — Coherence | 3 (MSB) | 0.5 |
| R — Resonance | 2 | 0.6 |
| E — Emergence | 1 | 0.7 |
| P — Poetics | 0 (LSB) | 0.8 |

State ID = `8*C + 4*R + 2*E + P`

## Gray-Code Order (4×4 grid)

```
 0  1  3  2
 6  7  5  4
12 13 15 14
10 11  9  8
```

Adjacent cells differ by exactly 1 bit — the canonical layout for the
unified-mandala GrayGrid component.

## Tesseract Topology

```
Vertices: 16  (= Q4 states)
Edges:    32  (= valid 1-bit transitions)
Faces:    24  (= 2-bit similarity groups)
Cells:     8  (= 3-bit subspaces)
```

Each vertex has exactly 4 neighbors. All paths from `shortest_gray_path()`
are BFS-optimal.

## TypeScript

```typescript
import { makeQ4State, q4StateFromId, GRAY_ORDER } from "./Q4State";
import { gray, hammingDistance, isValidTransition } from "./grayCode";
import { Tesseract } from "./hypercube";

const s = q4StateFromId(11);
// { C:1, R:0, E:1, P:1, id:11, binary:"1011", grayId:10, entropyBits:4.0 }

const t = new Tesseract();
console.log(t.shortestGrayPath(0, 15)); // [0, 1, 3, 7, 15]
```

## Benchmark Targets

| Metric | Target |
|---|---|
| `hamming_invariant` | All 15 consecutive pairs = 1 bit ✓ |
| `state_count` | Exactly 16 ✓ |
| `entropy_bits` | 4.0 (log₂(16)) ✓ |
| `tesseract_edges` | Exactly 32 ✓ |
| `encode_decode_roundtrip` | Gray invertible for all 16 states ✓ |
| `path_optimality` | BFS-shortest for all 256 pairs ✓ |

## Repository Structure

```
genesis-q4-core/
├── genesis_q4/
│   ├── __init__.py
│   ├── constants.py      # PHI_APPROX, GRAY_ORDER, topology constants
│   ├── state.py          # Q4State dataclass
│   ├── gray_code.py      # Gray-Code encode/decode/validate
│   ├── tesseract.py      # 4D hypercube graph topology
│   ├── transitions.py    # Q4TransitionValidator + InvalidTransitionError
│   ├── navigator.py      # Shortest Gray-path navigation
│   └── serializer.py     # JSON/YAML export
├── typescript/src/
│   ├── Q4State.ts
│   ├── grayCode.ts
│   └── hypercube.ts
├── tests/
│   ├── test_state.py
│   ├── test_gray_code.py     # Hamming=1 invariant (all 15 pairs)
│   ├── test_tesseract.py
│   ├── test_transitions.py
│   └── test_serializer.py
├── pyproject.toml
└── CITATION.cff
```

## Notes on Constants

- `PHI_APPROX = 1.6` — Engineering approximation of Φ = 1.6180339...
  Error < 0.2%. **Not** the exact golden ratio.
  Used for layout spacing in unified-mandala (1.6rem gap).

## Roadmap

This repo is **Phase 1** of the GenesisAeon Q4 integration roadmap.
Subsequent phases integrate Q4 into:

- `genesis-os` — Q4Mapper (CREP float → Q4State), NATS `ga.frame.*` subjects
- `sigillin` — SHA256-anchored state snapshots with Q4 encoding
- `unified-mandala` — GrayGrid + Tesseract visualisation
- `HexaAgent` — Agent roles with Q4-aware memory and replay

## Citation

```bibtex
@software{genesis_q4_core_2026,
  author  = {Römer, Johann and {MOR Research Collective}},
  title   = {genesis-q4-core: 16-State Q4 Space with Gray-Code and Tesseract Topology},
  year    = {2026},
  doi     = {10.5281/zenodo.XXXXXXX},
  url     = {https://github.com/GenesisAeon/genesis-q4-core},
}
```

## License

MIT © Johann Römer, MOR Research Collective
