#!/bin/sh
# Preserve custom hook ownership; install only into an unused/shared default hook.
set -eu
root=$(git rev-parse --show-toplevel)
common=$(git rev-parse --path-format=absolute --git-common-dir)
effective=$(git config --get core.hooksPath || true)
if test -n "$effective" && test "$effective" != "$root/.githooks"; then
    echo 'Custom hooks are configured; integrate the publication guard without replacing them.' >&2
    exit 1
fi
source="$root/.githooks/pre-push"
destination="$common/hooks/pre-push"
if test -L "$destination"; then
    echo 'Existing hook symlink preserved; refusing replacement.' >&2
    exit 1
fi
if test -e "$destination" && ! cmp -s "$source" "$destination"; then
    echo 'Existing shared hook preserved; refusing replacement.' >&2
    exit 1
fi
mkdir -p "$common/hooks"
install -m 755 "$source" "$destination"
