"""Tests for Q4State serialization."""

import json
import pytest
from genesis_q4.serializer import (
    state_to_dict,
    state_from_dict,
    state_to_json,
    state_from_json,
    state_space_to_json,
)
from genesis_q4.state import Q4State


def test_state_to_dict_structure():
    s = Q4State.from_id(11)
    d = state_to_dict(s)
    assert d["C"] == 1
    assert d["R"] == 0
    assert d["E"] == 1
    assert d["P"] == 1
    assert d["id"] == 11
    assert d["binary"] == "1011"
    assert d["entropy_bits"] == 4.0


def test_state_roundtrip_dict():
    for i in range(16):
        s = Q4State.from_id(i)
        assert state_from_dict(state_to_dict(s)) == s


def test_state_roundtrip_json():
    for i in range(16):
        s = Q4State.from_id(i)
        assert state_from_json(state_to_json(s)) == s


def test_json_is_valid():
    s = Q4State.from_id(7)
    text = state_to_json(s)
    data = json.loads(text)
    assert data["id"] == 7


def test_state_space_json_has_16_states():
    data = json.loads(state_space_to_json())
    assert len(data["states"]) == 16


def test_state_space_json_entropy_annotation():
    data = json.loads(state_space_to_json())
    assert data["q4_state_space"]["bits"] == 4
    assert data["q4_state_space"]["entropy_bits"] == 4.0
    # Must document the "4 bit, NOT 16 bit" invariant
    assert "4 bit" in data["q4_state_space"]["description"]


def test_state_space_json_gray_sequence():
    data = json.loads(state_space_to_json())
    seq = data["gray_sequence"]
    assert len(seq) == 16
    assert sorted(seq) == list(range(16))
