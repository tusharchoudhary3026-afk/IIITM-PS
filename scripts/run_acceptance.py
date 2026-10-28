import sys, pathlib, datetime, pytest
ROOT = pathlib.Path(__file__).resolve().parent.parent


class Collect:
    def __init__(self): self.rows = []
    def pytest_runtest_logreport(self, report):
        if report.when == "call" or (report.when == "setup" and report.skipped):
            self.rows.append((report.nodeid.split("::")[-1], report.outcome.upper()))


c = Collect()
pytest.main([str(ROOT / "tests"), "-q", "-p", "no:cacheprovider"], plugins=[c])
lines = [f"# Acceptance test run {datetime.datetime.now():%Y-%m-%d %H:%M}", "",
         "| Test | Outcome |", "|---|---|"] + [f"| {n} | {o} |" for n, o in c.rows]
(ROOT / "tests" / "results.md").write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
