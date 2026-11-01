"""Extract corners, goalkeeper-forward events and key events from the public
Wyscout dataset (Pappalardo et al. 2019, figshare collection 4415000).

Expects the files downloaded and unzipped into data/raw/wyscout/
(events/events_*.json, matches/matches_*.json, players.json, teams.json).

Wyscout positions are percentages of the pitch in the acting team's attacking
direction (x = 0 own goal line, x = 100 opponent goal line).

Outputs (data/derived/wyscout/): corners.csv, gk_forward.csv, key_events.csv, matches.csv
"""
import csv, glob, json, os
from collections import defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RAW = os.path.join(ROOT, "data", "raw", "wyscout")
OUT = os.path.join(ROOT, "data", "derived", "wyscout")
PERIOD = {"1H": 1, "2H": 2, "E1": 3, "E2": 4}
OFFSET = {1: 0, 2: 45 * 60, 3: 90 * 60, 4: 105 * 60}
GOAL, OWN_GOAL, ACCURATE = 101, 102, 1801
# goalkeeper events whose coordinates are recorded in the opponent frame (Wyscout quirk)
GK_MIRRORED = {"Save attempt", "Goalkeeper leaving line"}


def gk_field_event(e, is_gk):
    return e.get("playerId") in is_gk and e["eventName"] not in GK_MIRRORED and e.get("subEventName") != "Goal kick" and bool(e.get("positions"))


def tags(e):
    return {t["id"] for t in e.get("tags", [])}


def clock(e):
    return OFFSET[PERIOD[e["matchPeriod"]]] + e["eventSec"]


def write(name, rows):
    cols = list(dict.fromkeys(k for r in rows for k in r))
    with open(os.path.join(OUT, name), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)


def main():
    os.makedirs(OUT, exist_ok=True)
    players = json.load(open(os.path.join(RAW, "players.json")))
    is_gk = {p["wyId"] for p in players if p["role"]["code2"] == "GK"}
    teams = {t["wyId"]: t["name"] for t in json.load(open(os.path.join(RAW, "teams.json")))}
    matches = {}
    for f in glob.glob(os.path.join(RAW, "matches", "*.json")):
        comp = os.path.basename(f)[8:-5]
        for m in json.load(open(f)):
            matches[m["wyId"]] = (comp, m)
    corners, gkf, keys, mrows = [], [], [], []
    for f in sorted(glob.glob(os.path.join(RAW, "events", "*.json"))):
        comp = os.path.basename(f)[7:-5]
        by_match = defaultdict(list)
        for e in json.load(open(f)):
            if e["matchPeriod"] in PERIOD:
                by_match[e["matchId"]].append(e)
        for mid, ev in by_match.items():
            ev.sort(key=lambda e: (PERIOD[e["matchPeriod"]], e["eventSec"]))
            mcomp, m = matches.get(mid, (comp, {}))
            tids = list({e["teamId"] for e in ev})
            home = next((int(k) for k, v in m.get("teamsData", {}).items() if v.get("side") == "home"), None)
            score = defaultdict(int); reds = defaultdict(int)
            mrows.append(dict(match_id=mid, competition=comp, gameweek=m.get("gameweek"), round_id=m.get("roundId"),
                              home=teams.get(home), label=m.get("label"), date=m.get("dateutc")))
            for i, e in enumerate(ev):
                t = e["teamId"]; opp = next((x for x in tids if x != t), None); tg = tags(e)
                per = PERIOD[e["matchPeriod"]]; minute = int(clock(e) // 60)
                x = e["positions"][0]["x"] if e.get("positions") else None
                diff = score[t] - score[opp]
                if gk_field_event(e, is_gk) and x > 50:
                    gkf.append(dict(match_id=mid, competition=comp, team=teams.get(t), period=per, minute=minute,
                                    event=e["eventName"], sub_event=e.get("subEventName"), x=x,
                                    y=e["positions"][0]["y"], score_diff=diff, red_diff=reds[opp] - reds[t]))
                if e.get("subEventName") == "Corner":
                    t0 = clock(e)
                    row = dict(match_id=mid, competition=comp, team=teams.get(t), opponent=teams.get(opp),
                               is_home=int(t == home), period=per, minute=minute, second=round(clock(e) % 60),
                               score_diff=diff, goals_for=score[t], goals_against=score[opp],
                               red_diff=reds[opp] - reds[t], accurate=int(ACCURATE in tg),
                               end_x=e["positions"][1]["x"] if len(e["positions"]) > 1 else None,
                               end_y=e["positions"][1]["y"] if len(e["positions"]) > 1 else None, gk_involved=0)
                    for h in (10, 30, 60):
                        row.update({f"shots_{h}s": 0, f"goal_{h}s": 0, f"opp_shots_{h}s": 0, f"opp_goal_{h}s": 0})
                    for g in ev[i + 1:]:
                        dt = clock(g) - t0
                        if PERIOD[g["matchPeriod"]] != per or dt > 60:
                            break
                        gt = tags(g)
                        if g["teamId"] == t and gk_field_event(g, is_gk) and g["positions"][0]["x"] > 80 and dt <= 30:
                            row["gk_involved"] = 1
                        is_shot = g["eventName"] == "Shot" or g.get("subEventName") in ("Free kick shot", "Penalty")
                        for h in (10, 30, 60):
                            if dt <= h:
                                if is_shot:
                                    pre = "" if g["teamId"] == t else "opp_"
                                    row[f"{pre}shots_{h}s"] += 1
                                    if GOAL in gt:
                                        row[f"{pre}goal_{h}s"] = 1
                                if OWN_GOAL in gt:
                                    row[("opp_" if g["teamId"] == t else "") + f"goal_{h}s"] = 1
                    corners.append(row)
                # score and red cards
                if GOAL in tg and (e["eventName"] == "Shot" or e.get("subEventName") in ("Free kick shot", "Penalty")):
                    score[t] += 1
                    keys.append(dict(match_id=mid, competition=comp, team=teams.get(t), period=per, minute=minute, kind="goal"))
                if OWN_GOAL in tg:
                    score[opp] += 1
                    keys.append(dict(match_id=mid, competition=comp, team=teams.get(opp), period=per, minute=minute, kind="own_goal_for"))
                if tg & {1701, 1703}:  # red card, second yellow
                    reds[t] += 1
                    keys.append(dict(match_id=mid, competition=comp, team=teams.get(t), period=per, minute=minute, kind="red_card"))
        print(comp, len(by_match), "matches", len(corners), "corners so far", flush=True)
    write("corners.csv", corners); write("gk_forward.csv", gkf); write("key_events.csv", keys); write("matches.csv", mrows)


if __name__ == "__main__":
    main()
