from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT.parent / "tools" / "book-kit" / "export_epub.py"


if __name__ == "__main__":
    subprocess.run([sys.executable, str(TOOL), str(ROOT)], check=True)
