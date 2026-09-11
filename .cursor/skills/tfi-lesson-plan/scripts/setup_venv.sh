#!/usr/bin/env bash
# Create local venv and install PDF deps for this skill's scripts.
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
python3 -m venv .venv
.venv/bin/pip install -U pip
.venv/bin/pip install -r requirements.txt
echo "OK. Use: $DIR/.venv/bin/python list_chapters.py | extract_chapter.py"
