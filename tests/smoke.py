import json, urllib.request, urllib.error, uuid
BASE = "http://127.0.0.1:8080"
def call(path, data=None, key=None):
    headers = {"Content-Type": "application/json"}
    if key: headers["Idempotency-Key"] = key
    req = urllib.request.Request(BASE+path, data=json.dumps(data).encode() if data is not None else None, headers=headers)
    with urllib.request.urlopen(req, timeout=5) as response:
        return json.load(response)
assert call("/health")["status"] == "ok"
assert call("/stock/DEMO-001")["stock"] == 42
assert call("/products/DEMO-001")["sku"] == "DEMO-001"
key = str(uuid.uuid4())
payload = {"sku":"DEMO-001","quantity":2}
assert call("/orders",payload,key) == call("/orders",payload,key)
try:
    call("/orders",{"sku":"DEMO-001","quantity":3},key)
except urllib.error.HTTPError as e:
    assert e.code == 409
else:
    raise AssertionError("Expected conflict")
print("Backend smoke tests passed")

def expect_error(code, path, data=None, key=None):
    try:
        call(path, data, key)
    except urllib.error.HTTPError as e:
        assert e.code == code, (e.code, code)
    else:
        raise AssertionError(f"Expected HTTP {code}")

expect_error(404, "/stock/UNKNOWN")
expect_error(404, "/products/UNKNOWN")
expect_error(400, "/orders", payload)
expect_error(400, "/orders", {"sku":"DEMO-001","quantity":0}, str(uuid.uuid4()))
expect_error(400, "/orders", {"sku":"DEMO-001","quantity":43}, str(uuid.uuid4()))
expect_error(400, "/orders", {"sku":"UNKNOWN","quantity":1}, str(uuid.uuid4()))
print("Negative backend tests passed")
