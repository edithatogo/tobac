"""Exercise real bounded subprocesses; no unrelated process is signalled."""

import os
import signal
import subprocess
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
GUARD = ROOT / "scripts/run_bounded.py"
pytestmark = pytest.mark.skipif(os.name != "posix", reason="POSIX process-group guard")


def invoke(code: str, *budgets: str):
    return subprocess.run(  # noqa: S603 -- Fixed local interpreter/guard; synthetic code only.
        [sys.executable, str(GUARD), *budgets, "--poll", "0.05", "--", sys.executable, "-c", code],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=10,
        check=False,
    )


def assert_stopped(pid: int) -> None:
    for _ in range(30):
        result = subprocess.run(  # noqa: S603 -- Fixed ps executable; observed owned child PID.
            ["/bin/ps", "-o", "stat=", "-p", str(pid)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=2,
            check=False,
        )
        if not result.stdout.strip() or result.stdout.strip().startswith("Z"):
            return
        time.sleep(0.05)
    pytest.fail("Owned descendant remains alive after guard cleanup")


def test_guard_preserves_failure_and_streams_output() -> None:
    result = invoke("print('child output'); raise SystemExit(7)")
    assert result.returncode == 7
    assert result.stdout.strip() == "child output"
    assert "peak sampled group RSS=" in result.stderr


def test_guard_stops_excess_rss() -> None:
    result = invoke("import time; x=bytearray(80*1024*1024); time.sleep(30)", "--max-rss-mib", "48")
    assert result.returncode == 137
    assert "RSS budget exceeded" in result.stderr


@pytest.mark.parametrize("early_exit", [False, True])
def test_guard_cleans_descendants_on_timeout_and_parent_exit(tmp_path, early_exit) -> None:
    pid_file = tmp_path / "child.pid"
    code = (
        "import subprocess,sys,time; from pathlib import Path; "
        "p=subprocess.Popen([sys.executable,'-c','import time; time.sleep(30)']); "
        f"Path({str(pid_file)!r}).write_text(str(p.pid)); "
        + ("time.sleep(0.1)" if early_exit else "time.sleep(30)")
    )
    result = invoke(code, "--timeout", "0.7")
    assert result.returncode == (0 if early_exit else 124)
    assert_stopped(int(pid_file.read_text()))


def test_guard_cleans_group_when_it_receives_sigterm(tmp_path) -> None:
    pid_file = tmp_path / "leader.pid"
    code = (
        "import os,time; from pathlib import Path; "
        f"Path({str(pid_file)!r}).write_text(str(os.getpid())); time.sleep(30)"
    )
    with subprocess.Popen(  # noqa: S603 -- Fixed local guard and synthetic child.
        [sys.executable, str(GUARD), "--", sys.executable, "-c", code],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ) as guard:
        try:
            for _ in range(100):
                if pid_file.exists():
                    break
                time.sleep(0.02)
            assert pid_file.exists()
            guard.send_signal(signal.SIGTERM)
            assert guard.wait(timeout=5) == 143
        finally:
            if guard.poll() is None:
                guard.kill()
                guard.wait(timeout=5)
    assert_stopped(int(pid_file.read_text()))


@pytest.mark.parametrize("budget", ["0", "-1", "nan", "inf"])
def test_guard_rejects_invalid_budgets_before_execution(budget) -> None:
    result = invoke("raise SystemExit(99)", "--max-rss-mib", budget)
    assert result.returncode == 2
    assert "Budget must be finite and positive" in result.stderr


def test_guard_counts_descendant_rss_and_preserves_unrelated_process() -> None:
    code = (
        "import subprocess,sys,time; "
        "workers=[subprocess.Popen([sys.executable,'-c',"
        "'import time; x=bytearray(40*1024*1024); time.sleep(30)']) for _ in range(2)]; "
        "time.sleep(30)"
    )
    with subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"]) as unrelated:
        try:
            result = invoke(code, "--max-rss-mib", "96")
            assert result.returncode == 137
            assert "RSS budget exceeded" in result.stderr
            assert unrelated.poll() is None
        finally:
            unrelated.terminate()
            unrelated.wait(timeout=5)
