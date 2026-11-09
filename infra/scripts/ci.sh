#!/usr/bin/env bash
set -euo pipefail
ROOT="${CI_PROJECT_DIR:-$(git rev-parse --show-toplevel)}"
cd "$ROOT"
"$ROOT/infra/scripts/ci/validate-repo.sh" --root "$ROOT"
"$ROOT/infra/scripts/ci/check-size.sh" --root "$ROOT"
python3 scripts/validate.py --root .
python3 scripts/build.py --root . --out /tmp/package-ui-dist
jq -e . /tmp/package-ui-dist/manifest.json >/dev/null
echo "contract checks ok"
