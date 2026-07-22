#!/usr/bin/env python3
"""Plot TVC command/response/error/PWM from a CSV log."""

import argparse
from pathlib import Path

from tvc_analysis import get_command, get_measured, get_time_s, load_csv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--axis", choices=("pitch", "yaw"), default="pitch")
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    rows = load_csv(args.csv_path)
    t = get_time_s(rows)
    cmd = get_command(rows, args.axis)
    meas = get_measured(rows, args.axis)
    err = [c - y for c, y in zip(cmd, meas)]
    pwm_key = f"{args.axis}_pwm_us"
    pwm = [float(r[pwm_key]) for r in rows]

    out = args.out or Path("plots/examples") / f"{args.csv_path.stem}_{args.axis}_step_response.svg"
    out.parent.mkdir(parents=True, exist_ok=True)

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        _write_basic_svg(out, t, cmd, meas, err, pwm, args.axis)
        print(f"Saved plot: {out}")
        return

    fig, axes = plt.subplots(3, 1, figsize=(9, 7), sharex=True)
    fig.suptitle(f"Rev A Synthetic {args.axis.title()} Step Response")

    axes[0].plot(t, cmd, label="command", color="#2563eb", linewidth=2)
    axes[0].plot(t, meas, label="measured", color="#dc2626", linewidth=2)
    axes[0].set_ylabel("angle (deg)")
    axes[0].legend(loc="best")
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(t, err, color="#7c3aed", linewidth=2)
    axes[1].axhline(0, color="#111827", linewidth=0.8)
    axes[1].set_ylabel("error (deg)")
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(t, pwm, color="#059669", linewidth=2)
    axes[2].set_ylabel("PWM (us)")
    axes[2].set_xlabel("time (s)")
    axes[2].grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(out)
    print(f"Saved plot: {out}")


def _write_basic_svg(out, t, cmd, meas, err, pwm, axis):
    width, height = 900, 700
    margin_l, margin_r = 76, 24
    panel_h = 155
    tops = [85, 285, 485]

    def scale_series(values, top):
        lo = min(values)
        hi = max(values)
        if abs(hi - lo) < 1e-9:
            lo -= 1.0
            hi += 1.0
        pts = []
        for x, y in zip(t, values):
            sx = margin_l + (x - t[0]) / (t[-1] - t[0]) * (width - margin_l - margin_r)
            sy = top + panel_h - (y - lo) / (hi - lo) * panel_h
            pts.append((sx, sy))
        return pts, lo, hi

    def path(points):
        return " ".join(("M" if i == 0 else "L") + f"{x:.1f},{y:.1f}" for i, (x, y) in enumerate(points))

    cmd_pts, angle_lo, angle_hi = scale_series(cmd + meas, tops[0])
    # Re-scale command and measured against the same axis.
    def scale_with_bounds(values, top, lo, hi):
        return [
            (
                margin_l + (x - t[0]) / (t[-1] - t[0]) * (width - margin_l - margin_r),
                top + panel_h - (y - lo) / (hi - lo) * panel_h,
            )
            for x, y in zip(t, values)
        ]

    cmd_pts = scale_with_bounds(cmd, tops[0], angle_lo, angle_hi)
    meas_pts = scale_with_bounds(meas, tops[0], angle_lo, angle_hi)
    err_pts, err_lo, err_hi = scale_series(err, tops[1])
    pwm_pts, pwm_lo, pwm_hi = scale_series(pwm, tops[2])

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#f8fafc"/>',
        f'<text x="{margin_l}" y="42" font-family="Arial" font-size="24" font-weight="700" fill="#0f172a">Rev A Synthetic {axis.title()} Step Response</text>',
    ]

    panels = [
        ("angle (deg)", tops[0], angle_lo, angle_hi),
        ("error (deg)", tops[1], err_lo, err_hi),
        ("PWM (us)", tops[2], pwm_lo, pwm_hi),
    ]
    for label, top, lo, hi in panels:
        svg.append(f'<rect x="{margin_l}" y="{top}" width="{width-margin_l-margin_r}" height="{panel_h}" fill="#ffffff" stroke="#cbd5e1"/>')
        svg.append(f'<text x="18" y="{top + 82}" font-family="Arial" font-size="14" fill="#334155" transform="rotate(-90 18,{top + 82})">{label}</text>')
        svg.append(f'<text x="{margin_l - 54}" y="{top + 15}" font-family="Arial" font-size="12" fill="#64748b">{hi:.2f}</text>')
        svg.append(f'<text x="{margin_l - 54}" y="{top + panel_h}" font-family="Arial" font-size="12" fill="#64748b">{lo:.2f}</text>')

    svg.append(f'<path d="{path(cmd_pts)}" fill="none" stroke="#2563eb" stroke-width="2.5"/>')
    svg.append(f'<path d="{path(meas_pts)}" fill="none" stroke="#dc2626" stroke-width="2.5"/>')
    svg.append(f'<path d="{path(err_pts)}" fill="none" stroke="#7c3aed" stroke-width="2.5"/>')
    svg.append(f'<path d="{path(pwm_pts)}" fill="none" stroke="#059669" stroke-width="2.5"/>')
    svg.append(f'<text x="{margin_l}" y="68" font-family="Arial" font-size="13" fill="#2563eb">command</text>')
    svg.append(f'<text x="{margin_l + 88}" y="68" font-family="Arial" font-size="13" fill="#dc2626">measured</text>')
    svg.append(f'<text x="{width/2 - 30}" y="{height - 20}" font-family="Arial" font-size="14" fill="#334155">time (s)</text>')
    svg.append("</svg>")
    out.write_text("\n".join(svg) + "\n")


if __name__ == "__main__":
    main()
