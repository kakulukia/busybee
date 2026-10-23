#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
exec uv run --locked --no-dev uwsgi --yaml settings/webseite.yml
