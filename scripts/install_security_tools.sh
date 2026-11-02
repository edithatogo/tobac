#!/bin/sh
# Fixed release archives for qualified hosts, verified before executable extraction.
set -eu
case "$(uname -s)/$(uname -m)" in
    Darwin/arm64)
        gitleaks_asset=darwin_arm64
        gitleaks_sha=b40ab0ae55c505963e365f271a8d3846efbc170aa17f2607f13df610a9aeb6a5
        actionlint_asset=darwin_arm64
        actionlint_sha=aba9ced2dee8d27fecca3dc7feb1a7f9a52caefa1eb46f3271ea66b6e0e6953f
        ;;
    Linux/x86_64)
        gitleaks_asset=linux_x64
        gitleaks_sha=551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb
        actionlint_asset=linux_amd64
        actionlint_sha=8aca8db96f1b94770f1b0d72b6dddcb1ebb8123cb3712530b08cc387b349a3d8
        ;;
    *)
        echo 'Unsupported security-scanner host' >&2
        exit 1
        ;;
esac
root=$(git rev-parse --show-toplevel)
destination="$root/.security-tools"
mkdir -p "$destination"
temporary=$(mktemp -d)
trap 'rm -rf "$temporary"' EXIT HUP INT TERM
curl --fail --location --max-time 120 "https://github.com/gitleaks/gitleaks/releases/download/v8.30.1/gitleaks_8.30.1_${gitleaks_asset}.tar.gz" -o "$temporary/gitleaks.tar.gz"
echo "$gitleaks_sha  $temporary/gitleaks.tar.gz" | shasum -a 256 -c -
tar -xzf "$temporary/gitleaks.tar.gz" -C "$temporary" gitleaks
curl --fail --location --max-time 120 "https://github.com/rhysd/actionlint/releases/download/v1.7.12/actionlint_1.7.12_${actionlint_asset}.tar.gz" -o "$temporary/actionlint.tar.gz"
echo "$actionlint_sha  $temporary/actionlint.tar.gz" | shasum -a 256 -c -
tar -xzf "$temporary/actionlint.tar.gz" -C "$temporary" actionlint
install -m 755 "$temporary/gitleaks" "$destination/gitleaks"
install -m 755 "$temporary/actionlint" "$destination/actionlint"
