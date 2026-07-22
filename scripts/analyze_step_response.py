#!/usr/bin/env python3
"""Analyze TVC step-response CSV logs."""

import argparse
from pathlib import Path

from tvc_analysis import analyze_step_response, load_csv, save_metrics


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--axis", choices=("pitch", "yaw"), default="pitch")
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    rows = load_csv(args.csv_path)
    metrics = analyze_step_response(rows, axis=args.axis)

    out = args.out or args.csv_path.with_suffix(f".{args.axis}.metrics.json")
    save_metrics(metrics, out)

    print(f"Saved metrics: {out}")
    for key, value in metrics.__dict__.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
