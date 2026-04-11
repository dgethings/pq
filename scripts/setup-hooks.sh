#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HOOK_PATH="$REPO_ROOT/.git/hooks/commit-msg"

ALLOWED_TYPES="feat fix perf chore docs test refactor style ci build"

cat > "$HOOK_PATH" << 'HOOK_EOF'
#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
COMMIT_MSG_FILE="$1"
ALLOWED_TYPES="feat fix perf chore docs test refactor style ci build"

cd "$REPO_ROOT"
uv run conventional-pre-commit $ALLOWED_TYPES "$COMMIT_MSG_FILE"
HOOK_EOF

chmod +x "$HOOK_PATH"
echo "commit-msg hook installed at $HOOK_PATH"
echo "Allowed types: $ALLOWED_TYPES"
