import sys, os, json
sys.path.insert(0, "/home/claude/SCAGS")
os.environ["JWT_SECRET"] = "test-secret"

from backend.app import app

client = app.test_client()
app.config["TESTING"] = True

PASS = "✅"
FAIL = "❌"

def p(label, ok, detail=""):
    mark = PASS if ok else FAIL
    print(f"  {mark} {label}" + (f" → {detail}" if detail else ""))

print("\n" + "="*55)
print("  SCAGS API — Full Test Suite")
print("="*55)

# ── Health ──────────────────────────────────────────────────
print("\n[1] GET /")
r = client.get("/")
d = json.loads(r.data)
p("Status 200", r.status_code == 200, f"got {r.status_code}")
p("Message present", "SCAGS" in d.get("message",""), d.get("message"))

# ── Register ─────────────────────────────────────────────────
print("\n[2] POST /auth/register")
r = client.post("/auth/register", json={
    "username": "pushpender",
    "email": "push@brcm.edu",
    "password": "secure123"
})
d = json.loads(r.data)
p("Status 201", r.status_code == 201, f"got {r.status_code}")
p("Success message", "registered" in d.get("message","").lower(), d)

# Duplicate registration
r2 = client.post("/auth/register", json={
    "username": "pushpender",
    "email": "push@brcm.edu",
    "password": "secure123"
})
p("Duplicate → 409", r2.status_code == 409, f"got {r2.status_code}")

# Missing fields
r3 = client.post("/auth/register", json={"username": "x"})
p("Missing fields → 400", r3.status_code == 400, f"got {r3.status_code}")

# ── Login ─────────────────────────────────────────────────────
print("\n[3] POST /auth/login")
r = client.post("/auth/login", json={
    "username": "pushpender",
    "password": "secure123"
})
d = json.loads(r.data)
p("Status 200", r.status_code == 200, f"got {r.status_code}")
p("Token returned", "token" in d, list(d.keys()))
TOKEN = d.get("token")

# Wrong password
r2 = client.post("/auth/login", json={
    "username": "pushpender",
    "password": "wrongpass"
})
p("Wrong password → 401", r2.status_code == 401, f"got {r2.status_code}")

# ── Branches ──────────────────────────────────────────────────
print("\n[4] GET /branches")
r = client.get("/branches")
branches = json.loads(r.data)
p("Status 200", r.status_code == 200)
p(f"Has branches", len(branches) > 0, branches)

# ── Recommend (no token) ──────────────────────────────────────
print("\n[5] POST /recommend (no auth)")
r = client.post("/recommend", json={"percentile": 97.5, "branch": "CSE"})
p("401 without token", r.status_code == 401, f"got {r.status_code}")

# ── Recommend (with token) ────────────────────────────────────
print("\n[6] POST /recommend (authenticated)")
headers = {"Authorization": f"Bearer {TOKEN}"}

r = client.post("/recommend", json={"percentile": 97.5, "branch": "CSE"}, headers=headers)
d = json.loads(r.data)
p("Status 200", r.status_code == 200, f"got {r.status_code}")
p(f"Results returned", d.get("count",0) > 0, f"{d.get('count')} colleges")
if d.get("results"):
    top = d["results"][0]
    p("Top result has score", "score" in top, top.get("name"))
    p("Cutoff ≤ percentile", top["cutoff"] <= 97.5, f"cutoff={top['cutoff']}")
    p("Score is numeric", isinstance(top["score"], float), top["score"])
    print(f"\n  Top 3 colleges for CSE @ 97.5%ile:")
    for i, c in enumerate(d["results"][:3], 1):
        print(f"    {i}. {c['name']} ({c['branch']}) — score={c['score']} cutoff={c['cutoff']} placement={c['placement']}%")

# ── Recommend with filters ────────────────────────────────────
print("\n[7] POST /recommend with filters")
r = client.post("/recommend", json={
    "percentile": 99.0,
    "branch": "CSE",
    "max_fees": 130000
}, headers=headers)
d = json.loads(r.data)
p("Status 200", r.status_code == 200)
p("Fees filter applied", all(c["fees"] <= 130000 for c in d.get("results",[])),
  f"{d.get('count')} results")

# ── Invalid input ─────────────────────────────────────────────
print("\n[8] Edge cases")
r = client.post("/recommend", json={"percentile": 150, "branch": "CSE"}, headers=headers)
p("Percentile > 100 → 400", r.status_code == 400, f"got {r.status_code}")

r = client.post("/recommend", json={"branch": "CSE"}, headers=headers)
p("Missing percentile → 400", r.status_code == 400, f"got {r.status_code}")

r = client.post("/recommend", json={"percentile": 50, "branch": "CSE"}, headers=headers)
d = json.loads(r.data)
p("Low percentile (50) → 0 results", d.get("count") == 0, f"got {d.get('count')}")

print("\n" + "="*55)
print("  All tests complete")
print("="*55 + "\n")
