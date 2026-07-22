#!/usr/bin/env python3
"""Log Pico USB serial CSV telemetry to data/.

Requires pyserial on the host:

    python3 -m pip install pyserial
"""

import argparse
from datetime import datetime
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", required=True, help="Serial port, e.g. /dev/tty.usbmodemXXXX")
    parser.add_argument("--baud", type=int, default=115200)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    try:
        import serial
    except ImportError as exc:
        raise SystemExit("pyserial is required: python3 -m pip install pyserial") from exc

    out = args.out or Path("data") / f"pico_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    out.parent.mkdir(parents=True, exist_ok=True)

    with serial.Serial(args.port, args.baud, timeout=1) as ser, open(out, "w", newline="") as f:
        print(f"Logging {args.port} -> {out}")
        while True:
            line = ser.readline().decode("utf-8", errors="replace")
            if line:
                print(line, end="")
                f.write(line)
                f.flush()


if __name__ == "__main__":
    main()
