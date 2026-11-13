"""Coolest-art-01 entry: write the bundled art to /output/entry.png.

The art is the cool.png file shipped beside this program. The program
just copies it, so the output is byte-for-byte identical on every run.

Standard library only. No network access, no randomness, no arguments.
Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "cool.png"
DEST_NAME = "entry.png"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    dest = output_dir / DEST_NAME
    shutil.copyfile(SOURCE, dest)
    # Guard against a truncated or partial copy: the output must be the
    # exact bytes of the bundled art.
    if _sha256(dest) != _sha256(SOURCE):
        dest.unlink(missing_ok=True)
        raise SystemExit("entry.png does not match the bundled art")
    print(f"wrote {dest} ({dest.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
