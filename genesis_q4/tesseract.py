"""Tesseract: 4D hypercube as graph topology for the Q4 state space.

Topology (verified):
  Vertices: 16   (= the 16 Q4 states)
  Edges:    32   (= valid 1-bit transitions)
  Faces:    24   (= 2-bit similarity groups)
  Cells:     8   (= 3-bit subspaces)

This is a mathematical graph structure. Not a metaphysical claim.
"""

from __future__ import annotations

from collections import deque

from genesis_q4.constants import (
    TESSERACT_CELLS,
    TESSERACT_EDGES,
    TESSERACT_FACES,
    TESSERACT_VERTICES,
)
from genesis_q4.gray_code import GrayCode
from genesis_q4.state import Q4State


class Tesseract:
    """4D hypercube as the topological basis of the Q4 state space.

    Vertices are Q4 states (16 total). Edges connect states that differ
    by exactly 1 bit in their Gray-encoded representation (32 edges total).

    This class provides graph traversal, shortest-path, and export
    utilities. All operations are deterministic.
    """

    # Topology constants (read-only)
    VERTICES: int = TESSERACT_VERTICES
    EDGES: int = TESSERACT_EDGES
    FACES: int = TESSERACT_FACES
    CELLS: int = TESSERACT_CELLS

    def __init__(self) -> None:
        # Build adjacency list once at construction time.
        self._adj: dict[int, list[int]] = {
            i: GrayCode.neighbors(i) for i in range(16)
        }
        # Verify edge count: each edge counted from both ends.
        total = sum(len(v) for v in self._adj.values())
        assert total // 2 == TESSERACT_EDGES, (
            f"Expected {TESSERACT_EDGES} edges, got {total // 2}"
        )

    def neighbors(self, state_id: int) -> list[int]:
        """Return IDs of states adjacent to state_id (Hamming distance = 1 in Gray)."""
        if not 0 <= state_id <= 15:
            raise ValueError(f"state_id must be 0..15, got {state_id}")
        return list(self._adj[state_id])

    def neighbors_as_states(self, state: Q4State) -> list[Q4State]:
        """Return Q4State objects adjacent to `state`."""
        return [Q4State.from_id(i) for i in self.neighbors(state.id)]

    def are_adjacent(self, a: int, b: int) -> bool:
        """True if a and b are connected by a single edge in the tesseract."""
        return b in self._adj[a]

    def shortest_gray_path(self, from_id: int, to_id: int) -> list[int]:
        """BFS shortest path in the tesseract graph.

        Returns the list of state IDs from from_id to to_id (inclusive),
        following only valid 1-bit Gray-Code transitions. The path is
        optimal (minimum number of transitions).
        """
        if not (0 <= from_id <= 15 and 0 <= to_id <= 15):
            raise ValueError("State IDs must be 0..15")
        if from_id == to_id:
            return [from_id]

        visited = {from_id: None}  # state → predecessor
        queue: deque[int] = deque([from_id])
        while queue:
            current = queue.popleft()
            for neighbor in self._adj[current]:
                if neighbor not in visited:
                    visited[neighbor] = current
                    if neighbor == to_id:
                        return self._reconstruct(visited, from_id, to_id)
                    queue.append(neighbor)
        raise RuntimeError(f"No path from {from_id} to {to_id}")  # unreachable

    def _reconstruct(
        self, visited: dict[int, int | None], start: int, end: int
    ) -> list[int]:
        path = []
        current: int | None = end
        while current is not None:
            path.append(current)
            current = visited[current]
        path.reverse()
        return path

    def hamming_distance(self, a: int, b: int) -> int:
        """Shortest path length between two states (= number of bit flips needed)."""
        return len(self.shortest_gray_path(a, b)) - 1

    def all_edges(self) -> list[tuple[int, int]]:
        """Return all 32 edges as sorted (a, b) tuples with a < b."""
        edges = set()
        for a, neighbors in self._adj.items():
            for b in neighbors:
                edges.add((min(a, b), max(a, b)))
        return sorted(edges)

    def subspace(self, fixed_dims: dict[str, int]) -> list[int]:
        """Return all state IDs in a subspace with given fixed CREP dimensions.

        Example: subspace({"C": 1}) returns all 8 states with C=1.
        Example: subspace({"C": 1, "R": 0}) returns all 4 states with C=1, R=0.
        """
        dim_map = {"C": 3, "R": 2, "E": 1, "P": 0}
        result = []
        for state_id in range(16):
            state = Q4State.from_id(state_id)
            flags = state.flags
            if all(flags[d] == v for d, v in fixed_dims.items()):
                result.append(state_id)
        return sorted(result)

    def export_json(self) -> dict:
        """Export the tesseract as a JSON-serialisable graph dict."""
        return {
            "topology": {
                "vertices": self.VERTICES,
                "edges": self.EDGES,
                "faces": self.FACES,
                "cells": self.CELLS,
            },
            "nodes": [
                {
                    "id": i,
                    "binary": f"{i:04b}",
                    "gray_id": GrayCode.encode(i),
                    "neighbors": self._adj[i],
                }
                for i in range(16)
            ],
            "edges": [{"from": a, "to": b} for a, b in self.all_edges()],
        }

    def export_mermaid(self) -> str:
        """Export as a Mermaid graph diagram (subset: first 16 edges for readability)."""
        lines = ["graph LR"]
        for a, b in self.all_edges()[:16]:
            lines.append(f'    {a}["{a:04b}"] --- {b}["{b:04b}"]')
        lines.append("    %% Showing 16 of 32 tesseract edges")
        return "\n".join(lines)
