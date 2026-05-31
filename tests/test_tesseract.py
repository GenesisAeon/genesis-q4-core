"""Tests for the Tesseract graph topology."""

from genesis_q4.tesseract import Tesseract
from genesis_q4.state import Q4State
from genesis_q4.constants import TESSERACT_EDGES, TESSERACT_VERTICES


def test_vertex_count():
    t = Tesseract()
    assert t.VERTICES == 16 == TESSERACT_VERTICES


def test_edge_count():
    t = Tesseract()
    edges = t.all_edges()
    assert len(edges) == 32 == TESSERACT_EDGES


def test_each_vertex_has_4_neighbors():
    t = Tesseract()
    for i in range(16):
        assert len(t.neighbors(i)) == 4, f"State {i} should have 4 neighbors"


def test_adjacency_is_symmetric():
    t = Tesseract()
    for a in range(16):
        for b in t.neighbors(a):
            assert a in t.neighbors(b)


def test_shortest_path_same_state():
    t = Tesseract()
    assert t.shortest_gray_path(0, 0) == [0]


def test_shortest_path_adjacent():
    t = Tesseract()
    path = t.shortest_gray_path(0, 1)
    assert len(path) == 2
    assert path[0] == 0
    assert path[-1] == 1


def test_shortest_path_length_optimality():
    """All shortest paths must be minimum length (BFS guarantee)."""
    t = Tesseract()
    # 0 (0000) to 15 (1111): 4 bits differ, minimum 4 steps
    path = t.shortest_gray_path(0, 15)
    assert len(path) == 5  # 4 transitions = 5 states


def test_shortest_path_all_valid_transitions():
    """Every step in a shortest path must change exactly one bit (Hamming = 1 on state IDs)."""
    from genesis_q4.gray_code import GrayCode

    t = Tesseract()
    for start in range(16):
        for end in range(16):
            path = t.shortest_gray_path(start, end)
            for i in range(len(path) - 1):
                a, b = path[i], path[i + 1]
                dist = GrayCode.hamming_distance(a, b)
                assert dist == 1, f"Invalid step {a}→{b} in path {start}→{end}"


def test_export_json_structure():
    t = Tesseract()
    data = t.export_json()
    assert data["topology"]["vertices"] == 16
    assert data["topology"]["edges"] == 32
    assert data["topology"]["faces"] == 24
    assert data["topology"]["cells"] == 8
    assert len(data["nodes"]) == 16
    assert len(data["edges"]) == 32


def test_export_mermaid_returns_string():
    t = Tesseract()
    mermaid = t.export_mermaid()
    assert isinstance(mermaid, str)
    assert "graph LR" in mermaid


def test_subspace_c1_has_8_states():
    t = Tesseract()
    states = t.subspace({"C": 1})
    assert len(states) == 8
    for sid in states:
        assert Q4State.from_id(sid).C == 1


def test_subspace_cr11_has_4_states():
    t = Tesseract()
    states = t.subspace({"C": 1, "R": 1})
    assert len(states) == 4
    for sid in states:
        s = Q4State.from_id(sid)
        assert s.C == 1 and s.R == 1


def test_are_adjacent():
    t = Tesseract()
    assert t.are_adjacent(0, 1) is True
    assert t.are_adjacent(0, 15) is False
