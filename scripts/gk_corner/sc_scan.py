"""Corner-kick snapshots and follow-up dynamics from SkillCorner open data
(A-League 2024/25, broadcast tracking at 10 fps, extrapolated positions).

For every `corner_for` interruption in the dynamic-events file we read the
tracking frames from the corner until 30 s later and record:
  * attacking goalkeeper position at the corner (distance from own goal line)
  * attackers / defenders inside the penalty box, attackers in own half
  * whether the attacking goalkeeper crossed halfway in the next 30 s
  * after possession is lost: seconds until the ball reaches the attacking
    team's defensive third, and how many attacking outfield players are
    goal-side of the ball at that moment (counter-attack exposure)

Output: data/derived/skillcorner/corners.csv
"""
import csv, json, os, urllib.request

RAW = "https://raw.githubusercontent.com/SkillCorner/opendata/master/data"
LFS = "https://media.githubusercontent.com/media/SkillCorner/opendata/master/data"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "data", "derived", "skillcorner")
WINDOW = 300  # frames = 30 s


def get_json(url):
    with urllib.request.urlopen(url, timeout=120) as r:
        return json.load(r)


def get_csv(url):
    with urllib.request.urlopen(url, timeout=120) as r:
        return list(csv.DictReader(r.read().decode("utf-8").splitlines()))


def frames(mid, wanted):
    """Stream the LFS tracking file and keep only the requested frame numbers."""
    out = {}
    with urllib.request.urlopen(f"{LFS}/matches/{mid}/{mid}_tracking_extrapolated.jsonl", timeout=600) as r:
        for line in r:
            fr = json.loads(line)
            if fr["frame"] in wanted:
                out[fr["frame"]] = fr
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    rows = []
    for m in get_json(f"{RAW}/matches.json"):
        mid = m["id"]
        meta = get_json(f"{RAW}/matches/{mid}/{mid}_match.json")
        half = meta["pitch_length"] / 2
        team_of = {p["id"]: p["team_id"] for p in meta["players"]}
        gk_ids = {p["id"] for p in meta["players"] if p["player_role"]["acronym"] == "GK"}
        ev = get_csv(f"{RAW}/matches/{mid}/{mid}_dynamic_events.csv")
        corners = []
        for e in ev:
            if e["game_interruption_before"] == "corner_for" and e["frame_start"]:
                f0 = int(e["frame_start"])
                if not corners or f0 - corners[-1]["f0"] > 50:
                    corners.append(dict(f0=f0, team=int(e["team_id"]), period=e["period"], minute=int(e["minute_start"]),
                                        game_state=e["game_state"]))
        wanted = {c["f0"] + k for c in corners for k in range(0, WINDOW + 1, 5)}
        fr = frames(mid, wanted)
        for c in corners:
            snap = fr.get(c["f0"])
            if not snap or not snap["player_data"]:
                continue
            att = c["team"]
            pos = {p["player_id"]: (p["x"], p["y"]) for p in snap["player_data"] if p["x"] is not None}
            opp_gk = [v for k, v in pos.items() if k in gk_ids and team_of.get(k) != att]
            att_gk = [v for k, v in pos.items() if k in gk_ids and team_of.get(k) == att]
            if not opp_gk:
                continue
            sgn = 1 if opp_gk[0][0] > 0 else -1  # +1: attacking towards +x
            fx = lambda v: sgn * v[0]  # x in attacking direction (opponent goal at +half)
            in_box = lambda v: fx(v) >= half - 16.5 and abs(v[1]) <= 20.16
            row = dict(match_id=mid, team_id=att, period=c["period"], minute=c["minute"], game_state=c["game_state"],
                       att_gk_x=round(fx(att_gk[0]), 1) if att_gk else None,
                       att_gk_dist_own_goal=round(fx(att_gk[0]) + half, 1) if att_gk else None,
                       att_in_box=sum(1 for k, v in pos.items() if team_of.get(k) == att and in_box(v)),
                       def_in_box=sum(1 for k, v in pos.items() if team_of.get(k) != att and team_of.get(k) and in_box(v)),
                       att_own_half=sum(1 for k, v in pos.items() if team_of.get(k) == att and k not in gk_ids and fx(v) < 0),
                       gk_crossed_halfway_30s=0, lost_possession_s=None, ball_in_def_third_s=None, att_goalside_at_def_third=None)
            lost = None
            for k in range(5, WINDOW + 1, 5):
                f = fr.get(c["f0"] + k)
                if not f or not f["player_data"]:
                    continue
                p2 = {p["player_id"]: (p["x"], p["y"]) for p in f["player_data"] if p["x"] is not None}
                if att_gk and any(fx(v) > 0 for kk, v in p2.items() if kk in gk_ids and team_of.get(kk) == att):
                    row["gk_crossed_halfway_30s"] = 1
                grp = (f.get("possession") or {}).get("group")
                att_group = "home team" if att == meta["home_team"]["id"] else "away team"
                if lost is None and grp and grp != att_group:
                    lost = k; row["lost_possession_s"] = k / 10
                b = f.get("ball_data") or {}
                if lost is not None and b.get("x") is not None and fx((b["x"], b["y"])) < -half / 3 and row["ball_in_def_third_s"] is None:
                    row["ball_in_def_third_s"] = k / 10
                    row["att_goalside_at_def_third"] = sum(1 for kk, v in p2.items() if team_of.get(kk) == att and kk not in gk_ids and fx(v) < fx((b["x"], b["y"])))
            rows.append(row)
        print(mid, len(corners), "corners", flush=True)
    cols = list(rows[0].keys())
    with open(os.path.join(OUT, "corners.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
    print("rows", len(rows))


if __name__ == "__main__":
    main()
