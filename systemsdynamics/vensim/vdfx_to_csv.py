"""
vdfx_to_csv.py
==============
Reads Vensim .mdl files (with their .vdfx data) using PySD and exports
simulation results to CSV — one CSV per model.

Usage:
    python vdfx_to_csv.py --folder /path/to/your/mdl/files

Requirements:
    pip install pysd pandas
"""

import argparse
import os
import sys
import pandas as pd

def run_model_to_csv(mdl_path: str, output_folder: str) -> None:
    """Run a single .mdl file through PySD and save output as CSV."""
    try:
        import pysd
    except ImportError:
        print("ERROR: PySD is not installed. Run: pip install pysd")
        sys.exit(1)

    base_name = os.path.splitext(os.path.basename(mdl_path))[0]
    csv_path = os.path.join(output_folder, f"{base_name}.csv")

    print(f"  Loading {mdl_path} ...")
    try:
        model = pysd.read_vensim(mdl_path)
        results = model.run()
        results.to_csv(csv_path)
        print(f"  Saved -> {csv_path}  ({len(results)} rows, {len(results.columns)} columns)")
    except Exception as e:
        print(f"  FAILED: {mdl_path}\n    Reason: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert Vensim .mdl files to CSV via PySD"
    )
    parser.add_argument(
        "--folder",
        required=True,
        help="Folder containing M-01.mdl ... M-19.mdl"
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output folder for CSVs (defaults to same folder as MDLs)"
    )
    parser.add_argument(
        "--prefix",
        default="M-",
        help="Filename prefix to filter (default: 'M-')"
    )
    args = parser.parse_args()

    if not os.path.isdir(args.folder):
        print(f"ERROR: Folder not found: {args.folder}")
        sys.exit(1)

    output_folder = args.output or args.folder
    os.makedirs(output_folder, exist_ok=True)

    mdl_files = sorted([
        f for f in os.listdir(args.folder)
        if f.endswith(".mdl") and f.startswith(args.prefix)
    ])

    if not mdl_files:
        print(f"No .mdl files starting with '{args.prefix}' found in {args.folder}")
        sys.exit(1)

    print(f"\nFound {len(mdl_files)} model(s) to process:\n")
    for fname in mdl_files:
        full_path = os.path.join(args.folder, fname)
        run_model_to_csv(full_path, output_folder)

    print(f"\nAll done. CSVs saved to: {output_folder}")


if __name__ == "__main__":
    main()