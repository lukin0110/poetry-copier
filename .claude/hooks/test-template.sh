#!/usr/bin/env bash
# PostToolUse hook: run the copier template test suite after template files change.
#
# Reads the hook payload on stdin, skips edits that cannot affect the generated
# output, and runs `uv run -m pytest` in testing/. Exits 2 on failure so the
# output is fed back to Claude as a blocking error.
set -uo pipefail

root="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"

file=$(python3 -c '
import json, sys
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)
ti = d.get("tool_input") or {}
tr = d.get("tool_response") or {}
print(ti.get("file_path") or tr.get("filePath") or "")
')

# Only template sources and the copier questions change what gets generated.
case "$file" in
    "$root"/template/*|"$root"/copier.yml) ;;
    *) exit 0 ;;
esac

output=$(cd "$root/testing" && uv run -m pytest -q --no-header --color=no --tb=short --show-capture=no 2>&1)
status=$?

if [ "$status" -ne 0 ]; then
    # Copier prints every generated path; keep the failure report, not the noise.
    summary=$(printf '%s\n' "$output" | sed -nE '/= (FAILURES|ERRORS) =/,$p')
    [ -n "$summary" ] || summary=$(printf '%s\n' "$output" | tail -40)
    printf 'Template tests failed after editing %s\n\n%s\n' "${file#"$root"/}" "$summary" >&2
    exit 2
fi

printf '{"suppressOutput": true, "systemMessage": "Template tests passed"}\n'
