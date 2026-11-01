"""Corner-kick snapshots and follow-up dynamics from the Sportec / DFL open
dataset (Bassek et al. 2025, figshare 28196177, CC BY 4.0; optical tracking
at 25 Hz for 7 Bundesliga / 2. Bundesliga matches).

Match information and event XML must be in data/raw/sportec/. The 350-420 MB
position files are streamed from figshare and never written to disk.

Output: data/derived/sportec/corners.csv (same columns as skillcorner/corners.csv
plus score difference and the corner placing annotated by DFL).
"""
import csv, glob, json, os, re, urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RAW = os.path.join(ROOT, "data", "raw", "sportec")
OUT = os.path.join(ROOT, "data", "derived", "sportec")
FPS, WINDOW = 25, 30


def ts(s):
    return datetime.fromisoformat(s)


def position_urls():
    with urllib.request.urlopen("https://api.figshare.com/v2/articles/28196177", timeout=60) as r:
        files = json.load(r)["files"]
    return {re.search(r"DFL-MAT-\w+", f["name"]).group(0): f["download_url"] for f in files if "positions" in f["name"]}


def load_match(mid):
    info = ET.parse(glob.glob(os.path.join(RAW, f"*matchinformation*{mid}.xml"))[0]).getroot()
    gi = info.find(".//General")
    home = gi.get("HomeTeamId"); away = gi.get("GuestTeamId")
    env = info.find(".//Environment")
    length = float(env.get("PitchX")) if env is not None and env.get("PitchX") else 105.0
    gks, team_of = set(), {}
    for team in info.iter("Team"):
        for p in team.iter("Player"):
            team_of[p.get("PersonId")] = team.get("TeamId")
            if p.get("PlayingPosition") == "TW":
                gks.add(p.get("PersonId"))
    corners, score = [], {home: 0, away: 0}
    for ev in ET.parse(glob.glob(os.path.join(RAW, f"*events_raw*{mid}.xml"))[0]).getroot().iter("Event"):
        t = ts(ev.get("EventTime"))
        for child in ev.iter():
            if child.tag == "CornerKick":
                team = child.get("Team"); opp = away if team == home else home
                corners.append(dict(t=t, team=team, diff=score[team] - score[opp], placing=child.get("Placing")))
            if child.tag == "SuccessfulShot":
                shooter_team = next((c.get("Team") for c in ev.iter("ShotAtGoal")), None)
                if shooter_team in score:
                    score[shooter_team] += 1
    corners.sort(key=lambda c: c["t"])
    dedup = []
    for c in corners:
        if not dedup or (c["t"] - dedup[-1]["t"]).total_seconds() > 5:
            dedup.append(c)
    return home, away, length, gks, team_of, dedup


def scan_positions(url, corners):
    """Return {corner_index: {offset_s: {"players": {pid: (x, y)}, "ball": (x, y, possession)}}}."""
    sections = {}; targets = {}; snaps = {}
    cur = None
    with urllib.request.urlopen(url, timeout=1800) as r:
        for event, el in ET.iterparse(r, events=("start", "end")):
            if event == "start" and el.tag == "FrameSet":
                cur = dict(el.attrib)
            elif event == "end" and el.tag == "Frame":
                sec = cur["GameSection"]
                if sec not in sections:
                    sections[sec] = (int(el.get("N")), ts(el.get("T")))
                    n0, t0 = sections[sec]
                    for i, c in enumerate(corners):
                        dt = (c["t"] - t0).total_seconds()
                        if 0 <= dt < 75 * 60:
                            base = n0 + round(dt * FPS)
                            for k in range(WINDOW + 1):
                                targets[(sec, base + k * FPS)] = (i, k)
                key = (sec, int(el.get("N")))
                if key in targets:
                    i, k = targets[key]
                    s = snaps.setdefault(i, {}).setdefault(k, {"players": {}, "ball": None})
                    x, y = float(el.get("X")), float(el.get("Y"))
                    if cur.get("TeamId") == "BALL":
                        s["ball"] = (x, y, el.get("BallPossession"))
                    else:
                        s["players"][cur["PersonId"]] = (x, y)
                el.clear()
            elif event == "end" and el.tag == "FrameSet":
                el.clear()
    return snaps, sections


def main():
    os.makedirs(OUT, exist_ok=True)
    urls = position_urls(); rows = []
    for mid, url in sorted(urls.items()):
        home, away, length, gks, team_of, corners = load_match(mid)
        snaps, sections = scan_positions(url, corners)
        # attacked goal from the ball at the corner kick; keeper of each team = defender nearest
        # its own goal at the opponent's corners (robust to missing goalkeeper labels)
        geo = {}
        for i, c in enumerate(corners):
            s0 = snaps.get(i, {}).get(0)
            if not s0 or not s0["ball"] or not s0["players"]:
                continue
            xs = [v[0] for v in s0["players"].values()]
            mid_x = 0.0 if min(xs) < 0 else length / 2
            bx = s0["ball"][0] - mid_x
            if abs(bx) < 40:
                continue
            geo[i] = (mid_x, 1 if bx > 0 else -1)
        votes = {}
        for i, (mid_x, sgn) in geo.items():
            s0 = snaps[i][0]; att = corners[i]["team"]
            goal = (mid_x + sgn * length / 2, 34.0 if mid_x else 0.0)
            defenders = [(abs(v[0] - goal[0]) + abs(v[1] - goal[1]), k) for k, v in s0["players"].items()
                         if team_of.get(k) not in (att, None)]
            if defenders:
                k = min(defenders)[1]; votes.setdefault(team_of[k], {}).setdefault(k, 0); votes[team_of[k]][k] += 1
        keeper = {t: max(v, key=v.get) for t, v in votes.items()}
        for i, c in enumerate(corners):
            if i not in geo:
                continue
            fr = snaps[i]; s0 = fr[0]; mid_x, sgn = geo[i]; att = c["team"]; half = length / 2
            fx = lambda v: sgn * (v[0] - mid_x)
            in_box = lambda v: fx(v) >= half - 16.5 and abs(v[1] - (0 if mid_x == 0 else 34)) <= 20.16
            gk_id = keeper.get(att)
            gk = s0["players"].get(gk_id)
            att_flag = "1" if att == home else "2"
            row = dict(match_id=mid, team=att, minute=None, score_diff=c["diff"], placing=c["placing"],
                       keeper_id=gk_id, att_gk_x=round(fx(gk), 1) if gk else None,
                       att_gk_dist_own_goal=round(fx(gk) + half, 1) if gk else None,
                       att_in_box=sum(1 for k, v in s0["players"].items() if team_of.get(k) == att and in_box(v)),
                       def_in_box=sum(1 for k, v in s0["players"].items() if team_of.get(k) not in (att, None) and in_box(v)),
                       att_own_half=sum(1 for k, v in s0["players"].items() if team_of.get(k) == att and k != gk_id and fx(v) < 0),
                       gk_crossed_halfway_30s=0, lost_possession_s=None, ball_in_def_third_s=None, att_goalside_at_def_third=None)
            for sec, (n0, t0) in sections.items():
                dt = (c["t"] - t0).total_seconds()
                if 0 <= dt < 75 * 60:
                    row["minute"] = int(dt // 60) + {"firstHalf": 0, "secondHalf": 45, "firstHalfExtra": 90, "secondHalfExtra": 105}.get(sec, 0)
                    row["period"] = sec
            row["valid_snapshot"] = int(row["att_in_box"] + row["def_in_box"] >= 8)
            lost = None
            for k in range(1, WINDOW + 1):
                s = fr.get(k)
                if not s:
                    continue
                if gk_id in s["players"] and fx(s["players"][gk_id]) > 0:
                    row["gk_crossed_halfway_30s"] = 1
                if s["ball"]:
                    bx, by, poss = s["ball"]
                    if lost is None and poss and poss != att_flag:
                        lost = k; row["lost_possession_s"] = k
                    if lost is not None and row["ball_in_def_third_s"] is None and fx((bx, by)) < -half / 3:
                        row["ball_in_def_third_s"] = k
                        row["att_goalside_at_def_third"] = sum(1 for kk, v in s["players"].items()
                                                               if team_of.get(kk) == att and kk != gk_id and fx(v) < fx((bx, by)))
            rows.append(row)
        print(mid, len(corners), "corners", flush=True)
    with open(os.path.join(OUT, "corners.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print("rows", len(rows))


if __name__ == "__main__":
    main()
