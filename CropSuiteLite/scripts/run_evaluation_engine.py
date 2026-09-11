"""Private subprocess entry point; each invocation has its own working directory."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


if __name__ == '__main__':
    from CropSuite import CropSuiteLite
    CropSuiteLite(sys.argv[1]).run()
