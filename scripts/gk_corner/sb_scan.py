"""Scan every StatsBomb open-data match and extract the tables needed for the
goalkeeper-up-for-corners study.

Raw JSON is streamed and discarded; only per-match results are cached under
data/cache/statsbomb/<match_id>.json so the scan can be resumed.

Outputs (data/derived/statsbomb/):
  matches.csv      one row per match (competition, stage, teams, final score)
  corners.csv      one row per corner kick, with game state, delivery, outcome
                   for both teams in the following window, goalkeeper-up flags
                   and 360 box counts when available
  shots.csv        every shot with xG, outcome and the defending goalkeeper's
                   position from the shot freeze frame (empty-net analysis)
  gk_forward.csv   every event by a goalkeeper in the opponent half
  key_events.csv   goals, own goals and red cards (for the win-probability model)

Usage: python3 scripts/gk_corner/sb_scan.py [--workers 16]
"""
import argparse, csv, json, math, os, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CACHE = os.path.join(ROOT, "data", "cache", "statsbomb")
OUT = os.path.join(ROOT, "data", "derived", "statsbomb")
GOAL = (120.0, 40.0)
BOX_X, BOX_Y = 102.0, (18.0, 62.0)


def get(url, tries=4):
    for _ in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=90) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
        except Exception:
            pass
    return None


def secs(e):
    return e["minute"] * 60 + e["second"]


def in_box(loc):
    return loc[0] >= BOX_X and BOX_Y[0] <= loc[1] <= BOX_Y[1]


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def gk_from_freeze(ff):
    """Defending goalkeeper location in a shot freeze frame (shooter's frame)."""
    for p in ff or []:
        if not p.get("teammate") and p.get("position", {}).get("name") == "Goalkeeper":
            return p["location"]
    return None


def window_stats(ev, i0, team, opp, t0, period, horizon):
    """Shots, xG and goals for both teams within `horizon` seconds after ev[i0]."""
    s = dict(xg=0.0, shots=0, goal=0, opp_xg=0.0, opp_shots=0, opp_goal=0, opp_gk_far=0)
    for f in ev[i0 + 1:]:
        if f["period"] != period or secs(f) - t0 > horizon:
            break
        if f["type"]["name"] == "Shot":
            sh = f["shot"]; g = int(sh["outcome"]["name"] == "Goal")
            if f["team"]["name"] == team:
                s["xg"] += sh.get("statsbomb_xg", 0); s["shots"] += 1; s["goal"] |= g
            elif f["team"]["name"] == opp:
                s["opp_xg"] += sh.get("statsbomb_xg", 0); s["opp_shots"] += 1; s["opp_goal"] |= g
                loc = gk_from_freeze(sh.get("freeze_frame"))
                if loc is None or dist(loc, GOAL) > 20:
                    s["opp_gk_far"] = 1
        elif f["type"]["name"] == "Own Goal For":
            if f["team"]["name"] == team: s["goal"] = 1
            elif f["team"]["name"] == opp: s["opp_goal"] = 1
    return s


def process(m, comp):
    mid = m["match_id"]
    path = os.path.join(CACHE, f"{mid}.json")
    if os.path.exists(path):
        with open(path) as fh:
            return json.load(fh)
    ev = get(f"{BASE}/events/{mid}.json")
    if not ev:
        return None
    ff360 = get(f"{BASE}/three-sixty/{mid}.json") if comp["match_available_360"] else None
    frames = {f["event_uuid"]: f for f in (ff360 or [])}
    home_id = m["home_team"]["home_team_id"]
    ids = {}
    for e in ev:
        ids.setdefault(e["team"]["id"], e["team"]["name"])
    names = list(ids.values())
    home = ids.get(home_id, names[0])
    gk = {}
    for e in ev:
        if e.get("position", {}).get("name") == "Goalkeeper" and "player" in e:
            gk.setdefault(e["team"]["name"], set()).add(e["player"]["id"])
    score = {n: 0 for n in names}
    reds = {n: 0 for n in names}
    base = dict(match_id=mid, competition_id=comp["competition_id"], season_id=comp["season_id"])
    corners, shots, gkf, keys = [], [], [], []

    for i, e in enumerate(ev):
        t = e["team"]["name"]; typ = e["type"]["name"]
        if e["period"] == 5:
            continue
        opp = next((n for n in names if n != t), None)
        diff = score[t] - score[opp] if opp else 0

        # goalkeeper in the opponent half (any phase)
        if "player" in e and e["player"]["id"] in gk.get(t, set()) and e.get("location") and e["location"][0] > 60:
            gkf.append(dict(base, team=t, period=e["period"], minute=e["minute"], second=e["second"],
                            type=typ, x=round(e["location"][0], 1), y=round(e["location"][1], 1),
                            play_pattern=e["play_pattern"]["name"], score_diff=diff,
                            red_diff=reds[opp] - reds[t] if opp else 0))

        if typ == "Pass" and e["pass"].get("type", {}).get("name") == "Corner":
            p = e["pass"]; t0 = secs(e)
            row = dict(base, team=t, opponent=opp, is_home=int(t == home), period=e["period"],
                       minute=e["minute"], second=e["second"], score_diff=diff,
                       goals_for=score[t], goals_against=score[opp], red_diff=reds[opp] - reds[t],
                       side="left" if e["location"][1] < 40 else "right",
                       end_x=round(p["end_location"][0], 1), end_y=round(p["end_location"][1], 1),
                       length=round(p.get("length", 0), 1), height=p.get("height", {}).get("name"),
                       technique=p.get("technique", {}).get("name"), body_part=p.get("body_part", {}).get("name"),
                       completed=int("outcome" not in p), short=int(p.get("length", 99) < 15))
            # outcomes of the corner possession and the response windows
            poss = e["possession"]; pxg = 0.0; pshots = 0; pgoal = 0; gk_inv = 0; poss_end = None
            for j in range(i + 1, len(ev)):
                f = ev[j]
                if f["period"] != e["period"]:
                    break
                if f["possession"] != poss:
                    poss_end = j; break
                if f["team"]["name"] == t:
                    if "player" in f and f["player"]["id"] in gk.get(t, set()) and f.get("location", [0])[0] > 80:
                        gk_inv = 1
                    if f["type"]["name"] == "Shot":
                        pxg += f["shot"].get("statsbomb_xg", 0); pshots += 1
                        pgoal |= int(f["shot"]["outcome"]["name"] == "Goal")
            row.update(poss_xg=round(pxg, 4), poss_shots=pshots, poss_goal=pgoal, gk_involved=gk_inv)
            for h in (10, 30, 60):
                w = window_stats(ev, i, t, opp, t0, e["period"], h)
                row.update({f"{k}_{h}s": (round(v, 4) if isinstance(v, float) else v) for k, v in w.items()})
            # first opponent possession after the corner possession (counter-attack risk)
            cpos = dict(counter_start_x=None, counter_pattern=None, counter_secs=None, counter_shot=0,
                        counter_xg=0.0, counter_goal=0, counter_reached_final_third=0)
            if poss_end is not None:
                q = None
                for f in ev[poss_end:]:
                    if f["period"] != e["period"]:
                        break
                    if q is None and f["team"]["name"] == opp and f.get("location"):
                        q = f["possession"]; qt0 = secs(f)
                        cpos.update(counter_start_x=round(f["location"][0], 1), counter_pattern=f["play_pattern"]["name"])
                    if q is not None:
                        if f["possession"] != q:
                            break
                        cpos["counter_secs"] = secs(f) - qt0
                        if f["team"]["name"] == opp and f.get("location") and f["location"][0] > 80:
                            cpos["counter_reached_final_third"] = 1
                        if f["type"]["name"] == "Shot" and f["team"]["name"] == opp:
                            cpos["counter_shot"] = 1; cpos["counter_xg"] += f["shot"].get("statsbomb_xg", 0)
                            cpos["counter_goal"] |= int(f["shot"]["outcome"]["name"] == "Goal")
            cpos["counter_xg"] = round(cpos["counter_xg"], 4)
            row.update(cpos)
            # 360 freeze frame
            fr = frames.get(e["id"])
            row.update(has360=int(fr is not None), gk_visible=0, gk_x=None, att_in_box=None,
                       def_in_box=None, att_own_half=None, def_total_visible=None)
            if fr:
                ffp = fr["freeze_frame"]
                own_gk = [q for q in ffp if q.get("teammate") and q.get("keeper")]
                if own_gk:
                    row.update(gk_visible=1, gk_x=round(own_gk[0]["location"][0], 1))
                row.update(att_in_box=sum(1 for q in ffp if q.get("teammate") and not q.get("actor") and in_box(q["location"])),
                           def_in_box=sum(1 for q in ffp if not q.get("teammate") and in_box(q["location"])),
                           att_own_half=sum(1 for q in ffp if q.get("teammate") and not q.get("keeper") and q["location"][0] < 60),
                           def_total_visible=sum(1 for q in ffp if not q.get("teammate")))
            corners.append(row)

        if typ == "Shot":
            sh = e["shot"]; loc = gk_from_freeze(sh.get("freeze_frame"))
            shots.append(dict(base, team=t, period=e["period"], minute=e["minute"], second=e["second"],
                              x=round(e["location"][0], 1), y=round(e["location"][1], 1),
                              xg=round(sh.get("statsbomb_xg", 0), 4), outcome=sh["outcome"]["name"],
                              goal=int(sh["outcome"]["name"] == "Goal"), shot_type=sh.get("type", {}).get("name"),
                              body_part=sh.get("body_part", {}).get("name"), play_pattern=e["play_pattern"]["name"],
                              gk_x=round(loc[0], 1) if loc else None, gk_y=round(loc[1], 1) if loc else None,
                              gk_dist_goal=round(dist(loc, GOAL), 1) if loc else None, has_freeze=int(bool(sh.get("freeze_frame"))),
                              score_diff=diff))
            if sh["outcome"]["name"] == "Goal":
                score[t] += 1
                keys.append(dict(base, team=t, period=e["period"], minute=e["minute"], second=e["second"], kind="goal"))
        elif typ == "Own Goal For":
            score[t] += 1
            keys.append(dict(base, team=t, period=e["period"], minute=e["minute"], second=e["second"], kind="own_goal_for"))
        card = (e.get("foul_committed", {}) or {}).get("card", {}).get("name") or (e.get("bad_behaviour", {}) or {}).get("card", {}).get("name")
        if card in ("Red Card", "Second Yellow"):
            reds[t] += 1
            keys.append(dict(base, team=t, period=e["period"], minute=e["minute"], second=e["second"], kind="red_card"))

    res = dict(match=dict(base, competition=comp["competition_name"], season=comp["season_name"],
                          gender=comp["competition_gender"], international=int(comp["competition_international"]),
                          stage=m.get("competition_stage", {}).get("name"), home=home,
                          away=next((n for n in names if n != home), None), home_score=m.get("home_score"),
                          away_score=m.get("away_score"), has360=int(bool(frames)), match_date=m.get("match_date")),
               corners=corners, shots=shots, gk_forward=gkf, key_events=keys)
    with open(path, "w") as fh:
        json.dump(res, fh)
    return res


def write(name, rows):
    if not rows:
        return
    cols = list(dict.fromkeys(k for r in rows for k in r))
    with open(os.path.join(OUT, name), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--workers", type=int, default=16); a = ap.parse_args()
    os.makedirs(CACHE, exist_ok=True); os.makedirs(OUT, exist_ok=True)
    comps = get(f"{BASE}/competitions.json")
    jobs = []
    for c in comps:
        for m in get(f"{BASE}/matches/{c['competition_id']}/{c['season_id']}.json") or []:
            jobs.append((m, c))
    print(f"{len(jobs)} matches in {len(comps)} competition-seasons", flush=True)
    results = []
    with ThreadPoolExecutor(a.workers) as ex:
        futs = [ex.submit(process, m, c) for m, c in jobs]
        for k, f in enumerate(as_completed(futs), 1):
            r = f.result()
            if r: results.append(r)
            if k % 200 == 0: print(f"{k}/{len(jobs)} done", flush=True)
    for key, fname in [("corners", "corners.csv"), ("shots", "shots.csv"), ("gk_forward", "gk_forward.csv"), ("key_events", "key_events.csv")]:
        write(fname, [row for r in results for row in r[key]])
    write("matches.csv", [r["match"] for r in results])
    print(f"done: {len(results)} matches", flush=True)


if __name__ == "__main__":
    main()
