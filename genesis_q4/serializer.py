"""JSON/YAML serialization for Q4State and related structures."""

from __future__ import annotations

import json
from typing import Any

from genesis_q4.gray_code import GrayCode
from genesis_q4.state import Q4State


def state_to_dict(state: Q4State) -> dict[str, Any]:
    """Serialize a Q4State to a plain dict."""
    return {
        "C": state.C,
        "R": state.R,
        "E": state.E,
        "P": state.P,
        "id": state.id,
        "binary": state.binary,
        "gray_id": state.gray_id,
        "entropy_bits": state.entropy_bits,
    }


def state_from_dict(data: dict[str, Any]) -> Q4State:
    """Deserialize a Q4State from a plain dict."""
    return Q4State(C=int(data["C"]), R=int(data["R"]), E=int(data["E"]), P=int(data["P"]))


def state_to_json(state: Q4State) -> str:
    """Serialize a Q4State to a JSON string."""
    return json.dumps(state_to_dict(state), indent=2)


def state_from_json(text: str) -> Q4State:
    """Deserialize a Q4State from a JSON string."""
    return state_from_dict(json.loads(text))


def state_space_to_json() -> str:
    """Export the complete 16-state space as a JSON string."""
    states = [state_to_dict(Q4State.from_id(i)) for i in range(16)]
    return json.dumps(
        {
            "q4_state_space": {
                "count": 16,
                "bits": 4,
                "entropy_bits": 4.0,
                "description": "16 states = 4 bit. H = log2(16) = 4 bit.",
            },
            "states": states,
            "gray_sequence": GrayCode.full_sequence(),
        },
        indent=2,
    )


def try_import_yaml() -> Any:
    try:
        import yaml  # type: ignore[import-untyped]

        return yaml
    except ImportError:
        return None


def state_to_yaml(state: Q4State) -> str:
    """Serialize a Q4State to YAML. Requires pyyaml."""
    yaml = try_import_yaml()
    if yaml is None:
        raise ImportError("pyyaml is required for YAML serialization: pip install pyyaml")
    return yaml.dump(state_to_dict(state), default_flow_style=False)


def state_from_yaml(text: str) -> Q4State:
    """Deserialize a Q4State from YAML. Requires pyyaml."""
    yaml = try_import_yaml()
    if yaml is None:
        raise ImportError("pyyaml is required for YAML serialization: pip install pyyaml")
    return state_from_dict(yaml.safe_load(text))
