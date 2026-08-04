from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
APP_DIR = ROOT_DIR / "app"

sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(APP_DIR))