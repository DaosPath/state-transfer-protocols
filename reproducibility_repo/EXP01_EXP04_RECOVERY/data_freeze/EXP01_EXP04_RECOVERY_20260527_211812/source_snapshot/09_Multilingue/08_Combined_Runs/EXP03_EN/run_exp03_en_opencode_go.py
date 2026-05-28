import sys
from pathlib import Path


PARENT = Path(__file__).resolve().parents[1]
if str(PARENT) not in sys.path:
    sys.path.insert(0, str(PARENT))

import exp03_language_common as common


if __name__ == "__main__":
    raise SystemExit(common.main("EN"))
