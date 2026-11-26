import json, math, statistics
from pathlib import Path
for prefix, count in [("", 100), ("cold-", 20)]:
    rows = [json.loads(line) for line in Path(f"results/{prefix}samples.jsonl").read_text().splitlines()]
    assert len(rows) == 2 * count
    report = json.loads(Path(f"results/{prefix}summary.json").read_text())
    for i in range(count):
        pair = rows[2*i:2*i+2]
        assert [r["protocol"] for r in pair] == (["MCP", "UTCP"] if i % 2 == 0 else ["UTCP", "MCP"])
        assert all(r["iteration"] == i for r in pair)
    for protocol in ("MCP", "UTCP"):
        samples = [r for r in rows if r["protocol"] == protocol]
        assert all(r["ok"] is True and r["error"] is None for r in samples)
        values = [r["elapsed_ms"] for r in samples]
        assert all(math.isfinite(v) and v >= 0 for v in values)
        expected = report[protocol]
        assert expected["attempts"] == count and expected["failures"] == 0
        assert math.isclose(expected["p50_ms"], statistics.median(values))
        assert math.isclose(expected["p95_ms"], sorted(values)[math.ceil(.95*count)-1])
    print(f"Audited {len(rows)} {prefix or 'warm'} raw samples successfully")
