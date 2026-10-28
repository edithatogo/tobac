"""Bound a POSIX command's process group by sampled RSS and elapsed time.

This is a polling guard, not a kernel allocation limit or a leak detector. Children
must stay in the owned process group; deliberately daemonized workers are unsupported.
Output is inherited rather than accumulated in memory. Nothing outside the newly
created process group is signalled.
"""

import argparse
import logging
import math
import os
import shutil
import signal
import subprocess
import sys
import time

LOGGER = logging.getLogger(__name__)
MAX_GIT_OVERRIDES = 128


def child_environment() -> dict[str, str]:
    """Preserve bindings while preventing Git's optional detached file watchers."""
    environment = dict(os.environ)
    try:
        count = int(environment.get("GIT_CONFIG_COUNT", "0"))
    except ValueError:
        msg = "Invalid inherited Git configuration count"
        raise RuntimeError(msg) from None
    if not 0 <= count <= MAX_GIT_OVERRIDES:
        msg = "Invalid inherited Git configuration count"
        raise RuntimeError(msg)
    for offset, key in enumerate(("core.fsmonitor", "core.untrackedCache")):
        environment[f"GIT_CONFIG_KEY_{count + offset}"] = key
        environment[f"GIT_CONFIG_VALUE_{count + offset}"] = "false"
    environment["GIT_CONFIG_COUNT"] = str(count + 2)
    return environment


def group_rss_mib(group: int, ps: str) -> float:
    """Sum resident memory for the owned process group using a bounded native probe."""
    result = subprocess.run(  # noqa: S603 -- Resolved ps executable and fixed argv; no shell.
        [ps, "-axo", "pgid=,rss="],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=5,
        check=True,
    )
    return (
        sum(
            int(rss)
            for pgid, rss in (line.split() for line in result.stdout.splitlines())
            if int(pgid) == group
        )
        / 1024
    )


def signal_group(group: int, signum: int) -> None:
    """Signal only the owned group; distinguish vanished groups from real denial."""
    try:
        os.killpg(group, signum)
    except ProcessLookupError:
        return
    except PermissionError:
        # macOS can return EPERM for a group containing only an unreaped zombie.
        # Recheck its actual members; a live denied group remains a hard failure.
        ps = shutil.which("ps")
        if ps is None:
            raise
        result = subprocess.run(  # noqa: S603 -- Resolved ps and fixed argv.
            [ps, "-axo", "pgid=,stat="],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=5,
            check=True,
        )
        if any(
            int(pgid) == group and not state.startswith("Z")
            for pgid, state in (line.split() for line in result.stdout.splitlines())
        ):
            raise


def stop_group(process: subprocess.Popen[bytes]) -> None:
    """Terminate owned descendants, escalate after a grace period, and reap the leader."""
    try:
        signal_group(process.pid, signal.SIGTERM)
        time.sleep(0.2)
        process.poll()
        signal_group(process.pid, signal.SIGKILL)
    finally:
        process.wait(timeout=5)


def run(command: list[str], max_rss_mib: float, timeout: float, poll: float) -> int:
    """Run one isolated group; fail closed and clean descendants on every exit path."""
    ps = shutil.which("ps")
    if ps is None or os.name != "posix":
        msg = "The RSS guard requires POSIX process groups and ps"
        raise RuntimeError(msg)
    process = subprocess.Popen(command, start_new_session=True, env=child_environment())  # noqa: S603 -- Explicit user argv, no shell; only optional Git watchers disabled in child environment.
    start = time.monotonic()
    peak = 0.0
    code = 1
    try:
        while process.poll() is None:
            peak = max(peak, group_rss_mib(process.pid, ps))
            if peak > max_rss_mib:
                LOGGER.error("RSS budget exceeded: %.1f > %.1f MiB", peak, max_rss_mib)
                code = 137
                break
            if time.monotonic() - start >= timeout:
                LOGGER.error("Time budget exceeded: %.1f seconds", timeout)
                code = 124
                break
            time.sleep(poll)
        else:
            code = process.returncode
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else 1
        raise
    except KeyboardInterrupt:
        code = 130
        raise
    finally:
        stop_group(process)
        LOGGER.warning("Resource guard: peak sampled group RSS=%.1f MiB; status=%s", peak, code)
    return code if code >= 0 else 128 - code


def positive(value: str) -> float:
    """Require finite positive command-line budgets."""
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        msg = "Budget must be finite and positive"
        raise argparse.ArgumentTypeError(msg)
    return number


def exit_signal(signum: int, _frame: object) -> None:
    """Unwind on termination so the owned process group is cleaned up."""
    raise SystemExit(128 + signum)


def main() -> int:
    """Parse bounded execution settings and preserve child failures."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-rss-mib", type=positive, default=4096.0)
    parser.add_argument("--timeout", type=positive, default=3300.0)
    parser.add_argument("--poll", type=positive, default=0.5)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if sys.version_info[:3] != (3, 15, 1):
        parser.error("Resource guard requires the qualified Python 3.15.1 runtime")
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("Supply a command after --")
    signal.signal(signal.SIGTERM, exit_signal)
    try:
        return run(command, args.max_rss_mib, args.timeout, args.poll)
    except KeyboardInterrupt:
        return 130
    except OSError, RuntimeError, subprocess.SubprocessError:
        LOGGER.exception("Resource guard failed")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
