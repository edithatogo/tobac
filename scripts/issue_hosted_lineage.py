"""Issue digest-only hosted evidence after full local native byte verification."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path

from hosted_lineage import (
    ARCHIVE,
    CHECKPOINT,
    IDENTITY,
    NAMESPACE,
    PROFILES,
    ROOT,
    command,
    digest,
    inventory_identity,
)
from lineage_preflight import verify
from source_handoff import read


def issue(key: Path, out: Path) -> None:
    """Keep the signing key and original bytes local and create a new signed receipt."""
    if out.exists() or Path(str(out) + ".sig").exists():
        msg = "Refusing to overwrite a hosted evidence generation"
        raise ValueError(msg)
    native = verify(Path(os.environ["TOBAC_LINEAGE_ATTEMPTS"]), Path(os.environ["TOBAC_LINEAGE_WHEEL"]), [])
    checkpoint = read(ROOT / CHECKPOINT)
    fields = (
        "attempt_id",
        "manifest",
        "receipt",
        "transformation",
        "validation",
        "output_inventory",
        "executed_input_objects",
        "originals",
        "artifacts",
    )
    pins = [
        CHECKPOINT,
        PROFILES,
        ARCHIVE + "scientific-runner-inputs.json",
        ARCHIVE + "native-source-refs.json",
        ARCHIVE + "transformation-interface.json",
        ARCHIVE + "runner-material.json",
        "engineering/requirements.lock",
        "requirements.lock",
        "noxfile.py",
        "scripts/qualify_integrations.py",
    ]
    pins.extend(p.relative_to(ROOT).as_posix() for p in (ROOT / ".github/workflows").glob("*.yml"))
    document = {
        "schema": "tobac.signed-native-lineage/v1",
        "issuer": IDENTITY,
        "issued_at": datetime.now(UTC).isoformat(),
        "scope": (
            "Native bytes verified locally; hosted verification authenticates this receipt "
            "and rechecks current scientific inputs."
        ),
        "rights": (
            "Digest-only proof. Original objects, private keys and the native attempt estate "
            "remain in owner-held local preservation."
        ),
        "verifier_sha256": digest(ROOT / "scripts/hosted_lineage.py"),
        "inventory_sha256": inventory_identity(ROOT),
        "pins": {name: digest(ROOT / name) for name in sorted(pins)},
        "native_readback": native,
        "runners": {
            name: {field: run[field] for field in fields}
            for name, run in checkpoint["runner_results"].items()
        },
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(document, sort_keys=True, indent=2) + "\n")
    ssh = shutil.which("ssh-keygen")
    if ssh is None or command([ssh, "-Y", "sign", "-f", str(key), "-n", NAMESPACE, str(out)]).returncode:
        msg = "Hosted evidence signing failed"
        raise ValueError(msg)
    sys.stdout.write(
        json.dumps(
            {
                "payload_sha256": digest(out),
                "signature_sha256": digest(Path(str(out) + ".sig")),
                "native_runners_verified": len(native["runners"]),
            }
        )
    )


def main() -> None:
    """Select an existing private signing key and a fresh output generation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--key", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    issue(args.key, args.out)


if __name__ == "__main__":
    main()
