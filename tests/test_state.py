"""Tests for Q4State."""

import pytest

from genesis_q4.state import Q4State


def test_all_16_states_exist():
    states = Q4State.all_states()
    assert len(states) == 16


def test_state_ids_are_0_to_15():
    ids = [Q4State.from_id(i).id for i in range(16)]
    assert ids == list(range(16))


def test_from_id_roundtrip():
    for i in range(16):
        s = Q4State.from_id(i)
        assert s.id == i


def test_binary_property():
    assert Q4State.from_id(0).binary == "0000"
    assert Q4State.from_id(11).binary == "1011"
    assert Q4State.from_id(15).binary == "1111"


def test_from_binary_roundtrip():
    for i in range(16):
        s = Q4State.from_id(i)
        assert Q4State.from_binary(s.binary) == s


def test_entropy_bits_is_always_4():
    for i in range(16):
        assert Q4State.from_id(i).entropy_bits == 4.0


def test_state_id_formula():
    # id = 8*C + 4*R + 2*E + P
    s = Q4State(C=1, R=0, E=1, P=1)
    assert s.id == 8 + 0 + 2 + 1  # = 11


def test_invalid_flag_raises():
    with pytest.raises(ValueError):
        Q4State(C=2, R=0, E=0, P=0)
    with pytest.raises(ValueError):
        Q4State(C=0, R=-1, E=0, P=0)


def test_state_is_frozen():
    s = Q4State(C=1, R=0, E=0, P=0)
    with pytest.raises((AttributeError, TypeError)):
        s.C = 0  # type: ignore[misc]


def test_state_is_hashable():
    s1 = Q4State(C=1, R=0, E=1, P=1)
    s2 = Q4State.from_id(11)
    assert s1 == s2
    assert hash(s1) == hash(s2)
    assert len({s1, s2}) == 1


def test_state_repr():
    s = Q4State.from_id(11)
    assert "1011" in repr(s) or "11" in repr(s)


def test_flags_property():
    s = Q4State(C=1, R=0, E=1, P=1)
    assert s.flags == {"C": 1, "R": 0, "E": 1, "P": 1}


def test_gray_id_property():
    for i in range(16):
        s = Q4State.from_id(i)
        assert s.gray_id == i ^ (i >> 1)
