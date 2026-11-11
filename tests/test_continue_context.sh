#!/usr/bin/env bash
# Tests for plugin/skills/dev-setup/scripts/continue-context.sh. Usage: bash tests/test_continue_context.sh
set -u
here=$(cd "$(dirname "$0")/.." && pwd)
script="$here/plugin/skills/dev-setup/scripts/continue-context.sh"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
fail=0
pass=0
ok() { pass=$((pass + 1)); echo "ok   $1"; }
bad() { fail=$((fail + 1)); echo "FAIL $1"; echo "     got: $2"; }
expect_contains() { case "$3" in *"$2"*) ok "$1" ;; *) bad "$1 (missing: $2)" "$3" ;; esac; }
expect_empty() { [ -z "$2" ] && ok "$1" || bad "$1" "$2"; }

export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@t
repo="$tmp/repo"
git init -q "$repo" && git -C "$repo" commit -q --allow-empty -m init
plain="$tmp/plain"; mkdir "$plain"

# not found (git repo, no handoff)
out=$(cd "$repo" && bash "$script" "continue")
expect_contains "not found: message" "no _next-context_.md was found in" "$out"
expect_contains "not found: asks user" "ask which project/branch" "$out"
expect_contains "not found: names repo top" "$repo" "$out"

# non-git dir
out=$(cd "$plain" && bash "$script" "continue")
expect_contains "non-git: message" "no _next-context_.md was found in" "$out"
expect_contains "non-git: names cwd" "$plain" "$out"
expect_empty "non-git: non-trigger silent" "$(cd "$plain" && bash "$script" "hello")"

# found in current worktree
d="$repo/docs/agent_files/feat-x-20260101-0000"
mkdir -p "$d"
printf 'RESUME-MARKER-123\n' > "$d/_next-context_.md"
for p in "continue" "Continue." "  CONTINUE  " "continue with X" "continue, please" "continue
more"; do
  out=$(cd "$repo" && bash "$script" "$p")
  expect_contains "trigger [$p]: path" "$d/_next-context_.md" "$out"
  expect_contains "trigger [$p]: instruction" "Read the handoff file" "$out"
  case "$out" in *RESUME-MARKER-123*) bad "trigger [$p]: contents not injected" "$out" ;; *) ok "trigger [$p]: contents not injected" ;; esac
done
out=$(cd "$repo" && printf 'continue' | bash "$script")
expect_contains "stdin trigger" "Read the handoff file" "$out"
expect_empty "stdin non-trigger" "$(cd "$repo" && printf 'hi' | bash "$script")"

# non-triggers
for p in "continued work" "continues" "please continue" "discontinue" "continue_x" "" "yes"; do
  expect_empty "non-trigger [$p]" "$(cd "$repo" && bash "$script" "$p")"
done

# symlink refused
secret="$tmp/secret.txt"; printf 'TOP-SECRET-XYZ\n' > "$secret"
rm "$d/_next-context_.md"; ln -s "$secret" "$d/_next-context_.md"
out=$(cd "$repo" && bash "$script" "continue")
expect_contains "symlink: warning" "symlink or not a regular file" "$out"
case "$out" in *TOP-SECRET-XYZ*) bad "symlink: not leaked" "$out" ;; *) ok "symlink: not leaked" ;; esac
rm -f "$d/_next-context_.md"

# tracked file refused
printf 'TRACKED-MARKER\n' > "$d/_next-context_.md"
git -C "$repo" add -f "$d/_next-context_.md"
out=$(cd "$repo" && bash "$script" "continue")
expect_contains "tracked: warning" "tracked by git" "$out"
case "$out" in *TRACKED-MARKER*) bad "tracked: not leaked" "$out" ;; *) ok "tracked: not leaked" ;; esac
git -C "$repo" rm -q --cached -f "$d/_next-context_.md"
rm -f "$d/_next-context_.md"

# found only in another worktree
rm -f "$d/_next-context_.md"
git -C "$repo" worktree add -q -b other "$tmp/wt" 
mkdir -p "$tmp/wt/docs/agent_files/other-20260101-0000"
printf 'OTHER-WT\n' > "$tmp/wt/docs/agent_files/other-20260101-0000/_next-context_.md"
out=$(cd "$repo" && bash "$script" "continue")
expect_contains "other worktree found: path" "$tmp/wt/docs/agent_files/other-20260101-0000/_next-context_.md" "$out"
expect_contains "other worktree found: instruction" "Read the handoff file" "$out"
case "$out" in *OTHER-WT*) bad "other worktree: contents not injected" "$out" ;; *) ok "other worktree: contents not injected" ;; esac

# always exits 0
(cd "$plain" && bash "$script" "continue" >/dev/null); [ $? -eq 0 ] && ok "exit 0" || bad "exit 0" "nonzero"

echo "passed=$pass failed=$fail"
[ "$fail" -eq 0 ]
