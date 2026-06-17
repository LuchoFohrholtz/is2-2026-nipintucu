"""
Vercel Serverless Function entry point.
Adds the `src/` directory to sys.path so that `database`, `models`,
and `app` modules can be resolved correctly.
"""

import sys
from pathlib import Path

# Add src/ to the module search path so imports inside app.py work
SRC_DIR = str(Path(__file__).resolve().parent.parent / "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# Now import the Flask app — this triggers all `from database import …`
# and `from models import …` inside app.py
from app import app
