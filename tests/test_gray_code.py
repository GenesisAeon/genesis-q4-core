"""Tests for GrayCode — including the Hamming=1 invariant."""

import pytest
from genesis_q4.gray_code import GrayCode
from genesis_q4.constants import GRAY_ORDER


def test_encode_decode_roundtrip_all():
    """Gray encoding is perfectly invertible for all 16 states."""
    for n in range(16):
        assert GrayCode.decode(GrayCode.encode(n)) == n


def test_hamming_invariant_all_consecutive_pairs():
    """Core invariant: hamming(gray(n), gray(n+1)) == 1 for all n in 0..14.

    This is the mathematical guarantee that adjacent Q4 states differ
    by exactly one CREP dimension.
    """
    for n in range(15):
        dist = GrayCode.hamming_distance(GrayCode.encode(n), GrayCode.encode(n + 1))
        assert dist == 1, (
            f"Hamming distance between gray({n}) and gray({n+1}) is {dist}, expected 1"
        )


def test_hamming_distance_same_value():
    assert GrayCode.hamming_distance(7, 7) == 0


def test_hamming_distance_all_bits_differ():
    # 0b0000 vs 0b1111 → 4 bits differ
    assert GrayCode.hamming_distance(0b0000, 0b1111) == 4


def test_gray_order_constant_matches_full_sequence():
    """GRAY_ORDER must match the canonical GrayCode.full_sequence()."""
    assert GRAY_ORDER == GrayCode.full_sequence()


def test_gray_order_has_16_entries():
    assert len(GRAY_ORDER) == 16


def test_gray_order_contains_all_states():
    assert sorted(GRAY_ORDER) == list(range(16))


def test_gray_order_all_adjacent_pairs_hamming_1():
    """Every adjacent pair in GRAY_ORDER has Hamming distance = 1."""
    for i in range(15):
        a, b = GRAY_ORDER[i], GRAY_ORDER[i + 1]
        dist = GrayCode.hamming_distance(a, b)
        assert dist == 1, f"GRAY_ORDER[{i}]={a} and [{i+1}]={b}: Hamming={dist}"


def test_validate_sequence_valid():
    assert GrayCode.validate_sequence(GRAY_ORDER) is True


def test_validate_sequence_invalid():
    # 0 → 15 is a jump (multiple bits differ)
    assert GrayCode.validate_sequence([0, 15]) is False


def test_validate_sequence_single():
    assert GrayCode.validate_sequence([7]) is True


def test_neighbors_all_have_4_neighbors():
    """Each state in the tesseract has exactly 4 neighbors (4D hypercube)."""
    for i in range(16):
        assert len(GrayCode.neighbors(i)) == 4, f"State {i} has != 4 neighbors"


def test_neighbors_are_symmetric():
    """If b is a neighbor of a, then a is a neighbor of b."""
    for a in range(16):
        for b in GrayCode.neighbors(a):
            assert a in GrayCode.neighbors(b)


def test_encode_out_of_range():
    with pytest.raises(ValueError):
        GrayCode.encode(16)
    with pytest.raises(ValueError):
        GrayCode.encode(-1)


def test_decode_out_of_range():
    with pytest.raises(ValueError):
        GrayCode.decode(16)
