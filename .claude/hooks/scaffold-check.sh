#!/usr/bin/env bash
# Stop hook: scaffold projects from the working tree and run their lint & test suites.
#
# This is the local equivalent of the `generate_package` / `generate_fastapi` jobs in
# .github/workflows/test.yml. CI drives those through a devcontainer; Docker is not available
# here, so the generated projects are built natively with uv instead.
#
# Trigger: runs when the generation fingerprint (template/ + copier.yml, see lib.sh) differs
# from the one recorded at the last successful check — this catches edits made through any
# tool, including shell commands that bypass the PostToolUse hook — or when that hook flagged
# an Edit/Write. Standalone use runs unconditionally for the given variants:
#
#   .claude/hooks/scaffold-check.sh package fastapi
#
# Exits 2 on failure so the output is fed back to Claude as a blocking error.
set -uo pipefail

root="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
. "$root/.claude/hooks/lib.sh"
hook_cache_init "$root"

default_variants=(package fastapi)
variants=("$@")
hook_mode=0

# Fingerprint before generating: edits landing mid-run leave a stale recorded hash, which
# re-arms the check on the next stop instead of losing them.
current_hash=$(generation_hash "$root")

if [ ${#variants[@]} -eq 0 ]; then
    hook_mode=1
    active=$(payload_stop_active)
    # Already stopped once for this turn: do not block again. An unreadable payload gets the
    # same treatment — failing open here could loop the Stop hook, skipping once cannot.
    [ "$active" = "0" ] || exit 0
    if [ -f "$state" ]; then
        if [ "$(cat "$state")" = "$current_hash" ]; then
            # Nothing generated-affecting changed since the last successful check. A leftover
            # marker means an edit was flagged and then reverted; drop it.
            rm -f "$marker"
            exit 0
        fi
    elif [ ! -f "$marker" ]; then
        # First stop in this checkout with nothing flagged: adopt the current content as the
        # baseline (it is what HEAD's own CI validated) rather than paying a cold check now.
        mkdir -p "$cache_root" && printf '%s\n' "$current_hash" > "$state"
        exit 0
    fi
    variants=("${default_variants[@]}")
fi

mkdir -p "$cache_root" || { printf 'Scaffold check: cannot create %s\n' "$cache_root" >&2; exit 2; }

# One check per checkout at a time; a concurrent run already covers the current content, and
# any edit it misses re-arms the fingerprint comparison on the next stop.
exec 9>"$cache_root/lock"
if ! flock -n 9; then
    echo "Scaffold check already running for this checkout; skipping." >&2
    exit 0
fi

# Check one variant. Runs as a subshell so variants can run concurrently; writes its failing
# step name and output to files for the parent to report.
check_variant() (
    variant="$1"
    dir="$cache_root/scaffold/$variant"
    log="$cache_root/$variant.log"
    stepf="$cache_root/$variant.step"
    rm -f "$log" "$stepf"

    fail_step() {
        printf '%s' "$1" > "$stepf"
        printf '%s\n' "$output" > "$log"
        exit 1
    }

    # Same answers as the generate_* jobs in .github/workflows/test.yml.
    case "$variant" in
        fastapi)
            name="McFly API"
            url="https://github.com/lukin0110/mcfly-api/"
            desc="A package used in tests to test a scaffolded FastAPI app"
            ;;
        *)
            name="McFly"
            url="https://github.com/lukin0110/mcfly/"
            desc="A package used in tests to test a scaffolded python package"
            ;;
    esac

    mkdir -p "$dir" || { output="mkdir failed: $dir"; fail_step "setup"; }
    # Drop the previously generated files so renames and deletions are picked up, but keep the
    # warm state (venv, git, lockfile, tool caches) that makes repeat runs fast.
    find "$dir" -mindepth 1 -maxdepth 1 \
        ! -name .venv ! -name .git ! -name uv.lock ! -name .ruff_cache ! -name .pytest_cache \
        -exec rm -rf {} +

    # --vcs-ref=HEAD makes copier clone the repo and layer the dirty working tree on top (it
    # commits the draft changes into the clone, never into this repo), so uncommitted template
    # edits are included and gitignored noise is excluded. copier itself runs from the pinned
    # testing/ environment rather than whatever is on PATH.
    output=$(uv run --project "$root/testing" copier copy --quiet --defaults --overwrite \
        --vcs-ref=HEAD "$root" "$dir" \
        --data ci="github" \
        --data repository_url="$url" \
        --data name="$name" \
        --data description="$desc" \
        --data package_type="$variant" \
        --data use_pydantic=yes \
        --data use_makefile=no \
        --data python_version="3.14" \
        --data package_slug="mcfly" 2>&1) || fail_step "copier copy"

    # `poe lint` refuses to run without git, and `pre-commit --all-files` only sees tracked files.
    [ -d "$dir/.git" ] || { output=$(git -C "$dir" init 2>&1) || fail_step "git init"; }
    output=$(git -C "$dir" add -A 2>&1) || fail_step "git add"

    # Strip this repo's virtualenv from the environment: VIRTUAL_ENV / UV_PROJECT_ENVIRONMENT
    # point at /opt/venv and uv would sync the generated project's dependencies into it. The
    # color knobs keep the captured output plain for the failure report.
    run() {
        (cd "$dir" && env -u VIRTUAL_ENV UV_PROJECT_ENVIRONMENT=.venv \
            NO_COLOR=1 PYTEST_ADDOPTS=--color=no PRE_COMMIT_COLOR=never "$@")
    }
    output=$(run uv sync 2>&1) || fail_step "uv sync"
    output=$(run uv run --no-sync poe lint 2>&1) || fail_step "poe lint"
    output=$(run uv run --no-sync poe test 2>&1) || fail_step "poe test"
)

pids=()
for variant in "${variants[@]}"; do
    check_variant "$variant" &
    pids+=($!)
done

failed=""
for i in "${!variants[@]}"; do
    wait "${pids[$i]}" || failed="${failed:-${variants[$i]}}"
done

if [ -n "$failed" ]; then
    step=$(cat "$cache_root/$failed.step" 2>/dev/null || echo "unknown step")
    summary=$(summarize_failure < "$cache_root/$failed.log")
    printf 'Scaffold check failed: %s / %s\n\n%s\n' "$failed" "$step" "$summary" >&2
    exit 2
fi

# Record success only when the run covered the full default set — a partial manual run must
# not silence the pending hook-mode check for the variants it skipped.
covers_default=1
for v in "${default_variants[@]}"; do
    case " ${variants[*]} " in
        *" $v "*) ;;
        *) covers_default=0 ;;
    esac
done
if [ "$covers_default" = 1 ]; then
    printf '%s\n' "$current_hash" > "$state"
    rm -f "$marker"
fi

printf '{"suppressOutput": true, "systemMessage": "Scaffold check passed (%s)"}\n' "$(IFS=,; echo "${variants[*]}")"
