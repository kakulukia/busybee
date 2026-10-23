#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
uv sync --locked
mkdir -p .git/hooks
if [ -e .git/hooks/pre-commit ]; then
    echo "A pre-commit hook already exists. Integrate 'uv run --locked ruff check' and 'uv run --locked ruff format --check' manually."
    exit 1
fi
cat > .git/hooks/pre-commit <<'HOOK'
#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
files=()
while IFS= read -r -d '' file; do
    files+=("$file")
done < <(git diff --cached --name-only --diff-filter=ACM -z -- '*.py')
if [ "${#files[@]}" -gt 0 ]; then
    uv run --locked ruff check "${files[@]}"
    exec uv run --locked ruff format --check "${files[@]}"
fi
HOOK
chmod +x .git/hooks/pre-commit
