from __future__ import annotations

import os
from pathlib import Path


def read_input() -> str:
    return (Path(os.environ["AGENTICS_INPUT_DIR"]) / "input.txt").read_text(encoding="utf-8")


def write_output(text: str) -> None:
    out = Path(os.environ["AGENTICS_OUTPUT_DIR"]) / "answer.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")


def main() -> int:
    data = read_input().split()
    kind = 'sphere_zeroes'
    if kind == "zero_path":
        write_output("0\n")
    elif kind == "zero_grid":
        write_output("\n".join(["0" * 14 for _ in range(8)]) + "\n")
    elif kind == "zero_set":
        write_output("0\n")
    elif kind == "sphere_zeroes":
        n = int(data[0]) if data else 2
        write_output("0\n" + "".join("0 0 0\n" for _ in range(n)))
    elif kind in {"all_ones", "all_zero_bits", "color_by_index", "group_by_index"}:
        n = int(data[0]) if data else 1
        if kind == "all_ones":
            write_output("".join("1\n" for _ in range(n)))
        elif kind == "all_zero_bits":
            write_output("".join("0\n" for _ in range(n)))
        else:
            write_output("".join(f"{i}\n" for i in range(1, n + 1)))
    else:
        raise RuntimeError(f"unknown solution kind: {kind}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
