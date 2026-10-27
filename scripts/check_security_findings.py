"""Validate recorded security dispositions; an empty registry does not replace a scanner."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from datetime import date

ROOT = Path(__file__).resolve().parents[1]


def validate(  # noqa: C901  # Keep accountable dispositions and proof checks visible.
    findings: list[dict[str, Any]], today: date, root: Path = ROOT
) -> None:
    """Require accountable disposition, unexpired exceptions and fix evidence."""
    seen: set[str] = set()
    for item in findings:
        for key in ("id", "owner", "component", "severity", "rationale", "status"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                msg = "Security finding requires identity, owner and rationale"
                raise ValueError(msg)
        if item["id"] in seen:
            msg = "Duplicate security finding identity"
            raise ValueError(msg)
        seen.add(item["id"])
        if item["severity"] not in {
            "critical",
            "high",
            "medium",
            "low",
            "informational",
        }:
            msg = "Unknown security severity"
            raise ValueError(msg)
        if item["status"] == "exception":
            expiry = datetime.fromisoformat(item["expires"]).date()
            if expiry < today:
                msg = "Expired security exception"
                raise ValueError(msg)
        elif item["status"] == "fixed":
            if not item.get("verification") or not item.get("artifacts"):
                msg = "Fixed finding requires verification and artifact identities"
                raise ValueError(msg)
            for artifact in item["artifacts"]:
                path = root / artifact["path"]
                if (
                    path.is_symlink()
                    or not path.resolve().is_relative_to(root.resolve())
                    or not path.is_file()
                    or hashlib.sha256(path.read_bytes()).hexdigest() != artifact["sha256"]
                ):
                    msg = "Security fix verification artifact missing or changed"
                    raise ValueError(msg)
        else:
            msg = "Unresolved security finding"
            raise ValueError(msg)


def main() -> None:
    """Check the maintained registry without changing security settings."""
    record = json.loads((ROOT / "engineering/security-findings.json").read_text(encoding="utf-8"))
    if record["schema"] != "tobac.security-findings.v1":
        msg = "Unsupported security findings schema"
        raise ValueError(msg)
    validate(record["findings"], datetime.now(UTC).date())


if __name__ == "__main__":
    main()
