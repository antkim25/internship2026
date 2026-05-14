"""
generate_math_jsons.py
======================
Generates the abstractModel JSON files for Section 2.1 math function tests
(M-01 through M-19) ready to pass to the simulate_sd MCP tool.

Usage:
    python generate_math_jsons.py --output /path/to/output/folder

Each file is named M-01.json ... M-19.json
"""

import argparse
import json
import math
import os


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def ref(value: str) -> dict:
    """Shorthand for a ReferenceStructure node."""
    return {"syntaxType": "ReferenceStructure", "reference": str(value)}


def call(call_type: str, *arguments) -> dict:
    """Shorthand for a CallStructure node."""
    return {
        "syntaxType": "CallStructure",
        "callType": call_type,
        "arguments": list(arguments),
    }


def auxiliary(name: str, ast: dict, units: str = "dimensionless") -> dict:
    return {
        "name": name,
        "components": [{
            "type": "Auxiliary",
            "subtype": "Normal",
            "subscripts": [[], []],
            "ast": ast,
        }],
        "units": units,
        "limits": [None, None],
        "documentation": "",
    }


def constant(name: str, value) -> dict:
    """An auxiliary that holds a constant numeric value."""
    return auxiliary(name, ref(str(value)))


def wrap_model(elements: list, original_path: str) -> dict:
    """Wrap elements in the full abstractModel envelope."""
    return {
        "abstractModel": {
            "originalPath": original_path,
            "sections": [{
                "name": "__main__",
                "type": "main",
                "path": "/",
                "params": [],
                "returns": [],
                "subscripts": [],
                "constraints": [],
                "testInputs": [],
                "split": False,
                "viewsDict": {},
                "elements": elements,
            }]
        }
    }


def simulate_sd_call(model_json: dict,
                     final_time: int = 20,
                     initial_time: int = 0,
                     time_step: int = 1) -> dict:
    """Wrap a model JSON in the full simulate_sd call body."""
    return {
        "model_json": model_json,
        "time_step": time_step,
        "initial_time": initial_time,
        "final_time": final_time,
        "parameters": {},
    }


# ---------------------------------------------------------------------------
# Model definitions
# ---------------------------------------------------------------------------

MODELS = {}

# M-01  MIN(A, B) — A=5, B=3  → Result = 3
MODELS["M-01"] = wrap_model([
    auxiliary("Result", call("MIN", ref("A"), ref("B"))),
    constant("A", 5),
    constant("B", 3),
], "M-01_min.mdl")

# M-02  MAX(A, B) — A=5, B=3  → Result = 5
MODELS["M-02"] = wrap_model([
    auxiliary("Result", call("MAX", ref("A"), ref("B"))),
    constant("A", 5),
    constant("B", 3),
], "M-02_max.mdl")

# M-03  ABS(X) — X=−7  → Result = 7
MODELS["M-03"] = wrap_model([
    auxiliary("Result", call("ABS", ref("X"))),
    constant("X", -7),
], "M-03_abs.mdl")

# M-04  EXP(X) — X=2  → Result ≈ 7.389
MODELS["M-04"] = wrap_model([
    auxiliary("Result", call("EXP", ref("X"))),
    constant("X", 2),
], "M-04_exp.mdl")

# M-05  LN(X) — X=e  → Result ≈ 1.0
MODELS["M-05"] = wrap_model([
    auxiliary("Result", call("LN", ref("X"))),
    constant("X", round(math.e, 10)),   # 2.718281828…
], "M-05_ln.mdl")

# M-06  LOG(X, 10) — X=100  → Result ≈ 2.0
MODELS["M-06"] = wrap_model([
    auxiliary("Result", call("LOG", ref("X"), ref("10"))),
    constant("X", 100),
], "M-06_log.mdl")

# M-07  SQRT(X) — X=9  → Result = 3.0
MODELS["M-07"] = wrap_model([
    auxiliary("Result", call("SQRT", ref("X"))),
    constant("X", 9),
], "M-07_sqrt.mdl")

# M-08  SIN(X) — X=π/2  → Result ≈ 1.0
MODELS["M-08"] = wrap_model([
    auxiliary("Result", call("SIN", ref("X"))),
    constant("X", round(math.pi / 2, 10)),  # 1.5707963268
], "M-08_sin.mdl")

# M-09  COS(X) — X=0  → Result = 1.0
MODELS["M-09"] = wrap_model([
    auxiliary("Result", call("COS", ref("X"))),
    constant("X", 0),
], "M-09_cos.mdl")

# M-10  TAN(X) — X=π/4  → Result ≈ 1.0
MODELS["M-10"] = wrap_model([
    auxiliary("Result", call("TAN", ref("X"))),
    constant("X", round(math.pi / 4, 10)),  # 0.7853981634
], "M-10_tan.mdl")

# M-11  ATAN(X) — X=1  → Result ≈ 0.785 (π/4)
MODELS["M-11"] = wrap_model([
    auxiliary("Result", call("ATAN", ref("X"))),
    constant("X", 1),
], "M-11_atan.mdl")

# M-12  POW(X, N) — X=2, N=8  → Result = 256
MODELS["M-12"] = wrap_model([
    auxiliary("Result", call("POW", ref("X"), ref("N"))),
    constant("X", 2),
    constant("N", 8),
], "M-12_pow.mdl")

# M-13  ROUND(X) — X=2.7  → Result = 3
MODELS["M-13"] = wrap_model([
    auxiliary("Result", call("ROUND", ref("X"))),
    constant("X", 2.7),
], "M-13_round.mdl")

# M-14  FLOOR(X) — X=2.9  → Result = 2
MODELS["M-14"] = wrap_model([
    auxiliary("Result", call("FLOOR", ref("X"))),
    constant("X", 2.9),
], "M-14_floor.mdl")

# M-15  CEIL(X) — X=2.1  → Result = 3
MODELS["M-15"] = wrap_model([
    auxiliary("Result", call("CEIL", ref("X"))),
    constant("X", 2.1),
], "M-15_ceil.mdl")

# M-16  IF_THEN_ELSE(TIME < 10, 3, 7) → switches from 3 to 7 at t=10
#   We use TIME directly so the switch happens at a known step.
MODELS["M-16"] = wrap_model([
    auxiliary("Result", call(
        "IF_THEN_ELSE",
        {
            "syntaxType": "ArithmeticStructure",
            "operators": ["<"],
            "arguments": [
                {"syntaxType": "ReferenceStructure", "reference": "time"},
                {"syntaxType": "ReferenceStructure", "reference": "10"},
            ]
        },
        ref("Low_Value"),
        ref("High_Value"),
    )),
    constant("Low_Value", 3),
    constant("High_Value", 7),
], "M-16_if_then_else.mdl")

# M-17  MAX(ABS(X), Y) — X=−3, Y=2  → Result = 3
MODELS["M-17"] = wrap_model([
    auxiliary("Result", call(
        "MAX",
        call("ABS", ref("X")),
        ref("Y"),
    )),
    constant("X", -3),
    constant("Y", 2),
], "M-17_nested_max_abs.mdl")

# M-18  XIDZ(A, B, Z) — B=0  → Result = Z (no divide-by-zero error)
MODELS["M-18"] = wrap_model([
    auxiliary("Result", call("XIDZ", ref("A"), ref("B"), ref("Fallback"))),
    constant("A", 10),
    constant("B", 0),
    constant("Fallback", 99),
], "M-18_xidz.mdl")

# M-19  ZIDZ(A, B) — B=0  → Result = 0 (no divide-by-zero error)
MODELS["M-19"] = wrap_model([
    auxiliary("Result", call("ZIDZ", ref("A"), ref("B"))),
    constant("A", 10),
    constant("B", 0),
], "M-19_zidz.mdl")


# ---------------------------------------------------------------------------
# Write files
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate M-01..M-19 simulate_sd JSON files"
    )
    parser.add_argument(
        "--output",
        default=".",
        help="Folder to write JSON files into (default: current directory)"
    )
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    for test_id, model_json in MODELS.items():
        payload = simulate_sd_call(model_json, final_time=20)
        out_path = os.path.join(args.output, f"{test_id}.json")
        with open(out_path, "w") as f:
            json.dump(payload, f, indent=2)
        print(f"Written: {out_path}")

    print(f"\nAll {len(MODELS)} JSON files written to: {args.output}")


if __name__ == "__main__":
    main()