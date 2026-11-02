#!/bin/sh
# Fixed release archives for qualified hosts, verified before executable extraction.
set -eu
security_archive_suffix=tar.gz
security_binary_suffix=
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
    MINGW*/x86_64)
        gitleaks_asset=windows_x64
        gitleaks_sha=d29144deff3a68aa93ced33dddf84b7fdc26070add4aa0f4513094c8332afc4e
        actionlint_asset=windows_amd64
        actionlint_sha=6e7241b51e6817ea6a047693d8e6fed13b31819c9a0dd6c5a726e1592d22f6e9
        security_archive_suffix=zip
        security_binary_suffix=.exe
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
verify_archive() {
    if command -v sha256sum >/dev/null 2>&1; then
        echo "$1  $2" | sha256sum -c -
    else
        echo "$1  $2" | shasum -a 256 -c -
    fi
}
extract_binary() {
    if [ "$security_archive_suffix" = zip ]; then
        unzip -p "$temporary/$1.zip" "$1.exe" > "$temporary/$1.exe"
    else
        tar -xzf "$temporary/$1.tar.gz" -C "$temporary" "$1"
    fi
}
curl --fail --location --max-time 120 "https://github.com/gitleaks/gitleaks/releases/download/v8.30.1/gitleaks_8.30.1_${gitleaks_asset}.${security_archive_suffix}" -o "$temporary/gitleaks.$security_archive_suffix"
verify_archive "$gitleaks_sha" "$temporary/gitleaks.$security_archive_suffix"
extract_binary gitleaks
curl --fail --location --max-time 120 "https://github.com/rhysd/actionlint/releases/download/v1.7.12/actionlint_1.7.12_${actionlint_asset}.${security_archive_suffix}" -o "$temporary/actionlint.$security_archive_suffix"
verify_archive "$actionlint_sha" "$temporary/actionlint.$security_archive_suffix"
extract_binary actionlint
install -m 755 "$temporary/gitleaks$security_binary_suffix" "$destination/gitleaks$security_binary_suffix"
install -m 755 "$temporary/actionlint$security_binary_suffix" "$destination/actionlint$security_binary_suffix"
