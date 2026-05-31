"""Navigator: shortest Gray-path computation between Q4 states."""

from __future__ import annotations

from genesis_q4.state import Q4State
from genesis_q4.tesseract import Tesseract


class Q4Navigator:
    """Finds optimal Gray-Code paths between Q4 states.

    All returned paths satisfy the Gray-Code invariant: every consecutive
    pair has Hamming distance = 1 in their Gray-encoded IDs.
    """

    def __init__(self) -> None:
        self._tess = Tesseract()

    def shortest_path(self, from_state: Q4State, to_state: Q4State) -> list[Q4State]:
        """Return the shortest valid Gray-path from from_state to to_state."""
        ids = self._tess.shortest_gray_path(from_state.id, to_state.id)
        return [Q4State.from_id(i) for i in ids]

    def path_length(self, from_state: Q4State, to_state: Q4State) -> int:
        """Number of transitions on the shortest path (= number of bit flips)."""
        return len(self.shortest_path(from_state, to_state)) - 1

    def is_direct_neighbor(self, a: Q4State, b: Q4State) -> bool:
        """True if a single Gray-Code transition connects a and b."""
        return self._tess.are_adjacent(a.id, b.id)

    def all_paths_of_length(self, from_id: int, length: int) -> list[list[int]]:
        """Return all paths of exactly `length` steps from from_id (DFS)."""
        results: list[list[int]] = []
        self._dfs(from_id, length, [from_id], results)
        return results

    def _dfs(
        self,
        current: int,
        remaining: int,
        path: list[int],
        results: list[list[int]],
    ) -> None:
        if remaining == 0:
            results.append(list(path))
            return
        for neighbor in self._tess.neighbors(current):
            path.append(neighbor)
            self._dfs(neighbor, remaining - 1, path, results)
            path.pop()
