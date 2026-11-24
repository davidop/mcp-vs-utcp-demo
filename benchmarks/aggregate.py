"""Aggregate measured JSONL samples; never synthesize timings."""
import json, statistics, math, sys
from collections import defaultdict
groups=defaultdict(list)
for path in sys.argv[1:]:
    with open(path) as f:
        for line in f:
            sample=json.loads(line)
            groups[sample["protocol"]].append(sample)
report={}
for protocol, samples in groups.items():
    times=sorted(s["elapsed_ms"] for s in samples if s.get("ok") is True)
    report[protocol]={"attempts":len(samples),"failures":len(samples)-len(times),"p50_ms":statistics.median(times) if times else None,"p95_ms":times[math.ceil(.95*len(times))-1] if times else None}
print(json.dumps(report,indent=2))
