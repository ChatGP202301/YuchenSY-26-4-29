#!/bin/sh
set -eu
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$script_dir/../.." && pwd)
run_date=${AI_GEO_RUN_DATE:-$(date -u +%G-W%V)}
exec python3 "$repo_root/ai-geo/cli.py" run --site-root "$repo_root" --output "$repo_root/ai-geo/reports/runtime/weekly-$run_date"
