import json, sys, urllib.request, csv, os
from concurrent.futures import ThreadPoolExecutor
BASE = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"
COMPS = [(9,281),(1267,107),(43,106),(11,90),(7,235),(7,108),(44,107),(55,282),(55,43),(53,315),(53,106),(72,107)]
def get(url):
    try:
        with urllib.request.urlopen(url, timeout=60) as r: return json.load(r)
    except Exception: return None
def process(m, comp):
    mid = m["match_id"]; ev = get(f"{BASE}/events/{mid}.json"); ff = get(f"{BASE}/three-sixty/{mid}.json") or []
    if not ev: return []
    frames = {f["event_uuid"]: f for f in ff}
    teams = list(dict.fromkeys(x["team"]["name"] for x in ev))[:2]
    score = {t: 0 for t in teams}; rows = []
    gk = {}  # team -> set of goalkeeper player ids seen
    for e in ev:
        if e.get("position", {}).get("name") == "Goalkeeper": gk.setdefault(e["team"]["name"], set()).add(e["player"]["id"])
    for i, e in enumerate(ev):
        t = e["team"]["name"]; typ = e["type"]["name"]
        if typ == "Pass" and e["pass"].get("type", {}).get("name") == "Corner" and e["period"] <= 2:
            opp = [x for x in teams if x != t][0]
            fr = frames.get(e["id"]); gk_x = None; gk_vis = False
            if fr:
                for p in fr["freeze_frame"]:
                    if p.get("teammate") and p.get("keeper"): gk_vis = True; gk_x = p["location"][0]
            # event-based GK involvement within same possession
            poss = e["possession"]; gk_inv = False; xg = 0.0; goal = False
            j = i + 1; opp_xg = 0.0; opp_goal = False; t0 = e["minute"]*60 + e["second"]
            while j < len(ev):
                f = ev[j]; ft = f["minute"]*60 + f["second"]
                if f["period"] != e["period"] or ft - t0 > 30: break
                if f["possession"] == poss and f["team"]["name"] == t:
                    if f.get("player", {}).get("id") in gk.get(t, set()) and f.get("location", [0])[0] > 90: gk_inv = True
                    if f["type"]["name"] == "Shot":
                        xg += f["shot"].get("statsbomb_xg", 0); goal |= f["shot"]["outcome"]["name"] == "Goal"
                if f["team"]["name"] == opp and f["type"]["name"] == "Shot":
                    opp_xg += f["shot"].get("statsbomb_xg", 0); opp_goal |= f["shot"]["outcome"]["name"] == "Goal"
                j += 1
            rows.append(dict(comp=comp, match=mid, team=t, minute=e["minute"], period=e["period"],
                             diff=score[t] - score[opp], has360=fr is not None, gk_visible=gk_vis,
                             gk_x=gk_x, gk_involved=gk_inv, xg30=round(xg,4), goal30=goal, opp_xg30=round(opp_xg,4), opp_goal30=opp_goal))
        if typ == "Shot" and e["shot"]["outcome"]["name"] == "Goal": score[t] += 1
        if typ == "Own Goal For": score[t] += 1
    return rows
out = []
for cid, sid in COMPS:
    ms = get(f"{BASE}/matches/{cid}/{sid}.json") or []
    with ThreadPoolExecutor(8) as ex:
        for r in ex.map(lambda m: process(m, f"{cid}/{sid}"), ms): out.extend(r)
    print(cid, sid, len(ms), "matches", len(out), "corners so far", flush=True)
with open(sys.argv[1], "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
