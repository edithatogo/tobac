"""Additional synthetic Nox session; preserve the signed main Nox entry point."""

import nox

from noxfile import environment


@nox.session(python="3.15.2")
def properties(session: nox.Session) -> None:
    """Bounded scalar accounting; does not qualify native producer lineage."""
    environment(session, require_lock=True)
    session.run(
        "python",
        "-m",
        "pytest",
        "tests/engineering/test_accounting_properties.py",
        "-q",
        "--hypothesis-show-statistics",
        "--junitxml=outputs/engineering/accounting-properties.xml",
        *session.posargs,
    )
