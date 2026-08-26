#!/usr/bin/env bash
# PostToolUse hook: run the copier template test suite after template files change.
#
# Reads the hook payload on stdin, skips edits that cannot affect the generated
# output, and runs `uv run -m pytest` in testing/. Exits 2 on failure so the
# output is fed back to Claude as a blocking error.
set -uo pipefail

root="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
. "$root/.claude/hooks/lib.sh"
hook_cache_init "$root"

file=$(payload_file_path)
if [ "$file" = "ERR" ]; then
    # Unreadable payload: skip, but say so instead of silently disabling the gate.
    echo "test-template hook: could not parse the tool payload; skipping." >&2
    exit 0
fi

# Tolerate payloads that report paths relative to the project root.
case "$file" in
    ""|/*) ;;
    *) file="$root/$file" ;;
esac

# Only template sources and the copier questions change what gets generated.
case "$file" in
    "$root"/template/*|"$root"/copier.yml) ;;
    *) exit 0 ;;
esac

# Flag the change for the Stop hook, which scaffolds projects and lints & tests them. Set
# before pytest on purpose: a change that breaks this suite still needs the scaffold check
# once fixed, even if the fix arrives through an edit outside template/.
mkdir -p "$cache_root" && touch "$marker"

output=$(cd "$root/testing" && uv run -m pytest -q --no-header --color=no --tb=short --show-capture=no 2>&1)
status=$?

if [ "$status" -ne 0 ]; then
    # Copier prints every generated path; keep the failure report, not the noise.
    summary=$(printf '%s\n' "$output" | summarize_failure)
    printf 'Template tests failed after editing %s\n\n%s\n' "${file#"$root"/}" "$summary" >&2
    exit 2
fi

printf '{"suppressOutput": true, "systemMessage": "Template tests passed"}\n'
