# Shared helpers for the template verification hooks. Source this file, don't execute it.
#
# Used by test-template.sh (PostToolUse) and scaffold-check.sh (Stop).

# Cache layout, keyed by checkout path so clones and git worktrees don't share
# markers, baselines, or scaffold output.
#
# Sets: cache_root, marker, state
hook_cache_init() {
    local key
    key=$(printf '%s' "$1" | sha256sum | cut -c1-12)
    cache_root="${XDG_CACHE_HOME:-$HOME/.cache}/uv-copier-hooks/$key"
    marker="$cache_root/template-dirty"
    state="$cache_root/last-checked"
}

# Fingerprint of everything that affects generated output: the template tree
# (minus interpreter byte-code noise) and the copier questions.
generation_hash() {
    {
        find "$1/template" -type f ! -path '*/__pycache__/*' -print0 | LC_ALL=C sort -z | xargs -0 sha256sum
        sha256sum "$1/copier.yml"
    } | sha256sum | cut -d' ' -f1
}

# Payload readers. Print the field value, or the sentinel ERR when the payload
# cannot be parsed (or python3 is missing), so callers can fail safe instead of
# silently failing open.
payload_file_path() {
    python3 -c '
import json, sys
try:
    d = json.load(sys.stdin)
    ti = d.get("tool_input") or {}
    tr = d.get("tool_response") or {}
    print(ti.get("file_path") or tr.get("filePath") or "")
except Exception:
    print("ERR")
' 2>/dev/null || printf 'ERR'
}

payload_stop_active() {
    python3 -c '
import json, sys
try:
    d = json.load(sys.stdin)
    print("1" if d.get("stop_hook_active") else "0")
except Exception:
    print("ERR")
' 2>/dev/null || printf 'ERR'
}

# Trim a failing step's output to the part worth feeding back: strip ANSI
# escapes, keep the pytest failure report when present, else the tail.
summarize_failure() {
    local plain summary
    plain=$(sed -E "s/$(printf '\033')\[[0-9;]*[a-zA-Z]//g")
    summary=$(printf '%s\n' "$plain" | sed -nE '/= (FAILURES|ERRORS) =/,$p')
    [ -n "$summary" ] || summary=$(printf '%s\n' "$plain" | tail -40)
    printf '%s\n' "$summary"
}
