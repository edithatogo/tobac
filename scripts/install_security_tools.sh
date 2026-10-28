#!/bin/sh
# Fixed macOS release archives, verified before executable extraction.
set -eu
test "$(uname -s)" = Darwin
test "$(uname -m)" = arm64
root=$(git rev-parse --show-toplevel)
destination="$root/.security-tools"
mkdir -p "$destination"
temporary=$(mktemp -d)
trap 'rm -rf "$temporary"' EXIT HUP INT TERM
curl --fail --location --max-time 120 https://github.com/gitleaks/gitleaks/releases/download/v8.30.1/gitleaks_8.30.1_darwin_arm64.tar.gz -o "$temporary/gitleaks.tar.gz"
echo "b40ab0ae55c505963e365f271a8d3846efbc170aa17f2607f13df610a9aeb6a5  $temporary/gitleaks.tar.gz" | shasum -a 256 -c -
tar -xzf "$temporary/gitleaks.tar.gz" -C "$temporary" gitleaks
curl --fail --location --max-time 120 https://github.com/rhysd/actionlint/releases/download/v1.7.12/actionlint_1.7.12_darwin_arm64.tar.gz -o "$temporary/actionlint.tar.gz"
echo "aba9ced2dee8d27fecca3dc7feb1a7f9a52caefa1eb46f3271ea66b6e0e6953f  $temporary/actionlint.tar.gz" | shasum -a 256 -c -
tar -xzf "$temporary/actionlint.tar.gz" -C "$temporary" actionlint
install -m 755 "$temporary/gitleaks" "$destination/gitleaks"
install -m 755 "$temporary/actionlint" "$destination/actionlint"
