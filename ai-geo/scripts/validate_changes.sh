#!/bin/sh
set -eu
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$script_dir/../.." && pwd)
python3 "$repo_root/ai-geo/cli.py" doctor
python3 "$repo_root/tools/test_ai_geo_system.py" -v
