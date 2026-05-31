"""Tests for Q4TransitionValidator."""

import pytest

from genesis_q4.transitions import InvalidTransitionError, Q4TransitionValidator


def test_valid_transition_adjacent():
    v = Q4TransitionValidator()
    assert v.is_valid(0, 1) is True


def test_invalid_transition_multi_bit():
    v = Q4TransitionValidator()
    # 0 (0000) → 3 (0011): 2 bits differ in Gray encoding
    assert v.is_valid(0, 3) is False


def test_invalid_transition_same_state():
    v = Q4TransitionValidator()
    # Self-transition: Hamming = 0, not 1
    assert v.is_valid(5, 5) is False


def test_validate_raises_on_invalid():
    v = Q4TransitionValidator()
    with pytest.raises(InvalidTransitionError):
        v.validate(0, 15)


def test_validate_does_not_raise_on_valid():
    v = Q4TransitionValidator()
    # Should not raise
    v.validate(0, 1)


def test_suggest_path_is_valid():
    v = Q4TransitionValidator()
    path = v.suggest_path(0, 15)
    # Path must start at 0 and end at 15
    assert path[0] == 0
    assert path[-1] == 15
    # All steps must be valid
    for i in range(len(path) - 1):
        assert v.is_valid(path[i], path[i + 1])


def test_all_adjacent_pairs_are_valid():
    """All 32 tesseract edges are valid transitions."""
    from genesis_q4.tesseract import Tesseract

    v = Q4TransitionValidator()
    t = Tesseract()
    for a, b in t.all_edges():
        assert v.is_valid(a, b), f"Edge {a}→{b} should be valid"


def test_invalid_transition_error_message():
    err = InvalidTransitionError(0, 15, 4)
    assert "0000" in str(err)
    assert "1111" in str(err)
    assert "4" in str(err)
