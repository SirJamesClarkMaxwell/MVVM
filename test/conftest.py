import sys
from pathlib import Path

# Adds 'src' folder to sys.path so `from src.` works
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
