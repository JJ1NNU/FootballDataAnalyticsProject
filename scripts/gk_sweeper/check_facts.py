"""Re-check the plan 3-1 facts against the cached raw data (S01).

Per IDSSE match (cached in data/cache/gk_sweeper/facts_31/<match_id>.json so the
script can resume after an interruption):
  a. metadata pitch size and frame rate,
  b. raw ball frames in the XML, kloppy frames (only_alive=False), alive frames,
     frames with 22 players + ball coordinates,
  c. starting goalkeepers (metadata starting_position == Goalkeeper),
  d. event orientation and missing end coordinates of incomplete passes.
StatsBomb:
  e. shots.csv rows/columns, matches.csv 2015/16 EPL count, cached event files.

Writes data/derived/gk_sweeper/facts_31.json. Mismatches are recorded, not hidden.

Usage: python scripts/gk_sweeper/check_facts.py [--match J03WMX ...] [--skip-statsbomb]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

import pandas as pd
from kloppy import sportec
from kloppy.domain import BallState, PassResult, PositionType

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from gk_sweeper import config as C  # noqa: E402

CACHE_DIR = C.REPO_ROOT / "data" / "cache" / "gk_sweeper" / "facts_31"
OUT_FILE = C.DERIVED_DIR / "facts_31.json"

# plan 3-1: expected starting goalkeepers (home, away) by match
EXPECTED_GK = {
    "J03WMX": ("Schwäbe", "Sommer"),
    "J03WN1": ("Riemann", "Hrádecký"),
    "J03WPY": ("Kastenmeier", "Mathenia"),
    "J03WOH": ("Kastenmeier", "Stojanovic"),
    "J03WQQ": ("Kastenmeier", "Vasilj"),
    "J03WOY": ("Kastenmeier", "Kolke"),
    "J03WR9": ("Kastenmeier", "Luthe"),
}
# plan 3-1: one match reported with 14.6万 frames, 8.5万 alive (rounded to 0.1万)
PLAN_ONE_MATCH_TOTAL_MAN = 14.6
PLAN_ONE_MATCH_ALIVE_MAN = 8.5

_FRAMESET_RE = re.compile(rb'<FrameSet [^>]*TeamId="([^"]*)"')
_POSS_RE = re.compile(rb'BallPossession="([^"]*)"')
_STATUS_RE = re.compile(rb'BallStatus="([^"]*)"')


def fold(name: str) -> str:
    """Casefold and strip diacritics for surname comparison."""
    norm = unicodedata.normalize("NFKD", name)
    return "".join(ch for ch in norm if not unicodedata.combining(ch)).casefold().strip()


def raw_files(match_id: str) -> dict[str, Path]:
    d = C.RAW_IDSSE_DIR / match_id
    return {
        "meta": next(d.glob("DFL_02_01_matchinformation_*.xml")),
        "event": next(d.glob("DFL_03_02_events_raw_*.xml")),
        "tracking": next(d.glob("DFL_04_03_positions_raw_observed_*.xml")),
    }


def scan_raw_ball(tracking_xml: Path) -> dict:
    """Count raw ball frames and BallPossession / BallStatus values in the XML."""
    n, poss, status = 0, Counter(), Counter()
    in_ball = False
    with open(tracking_xml, "rb") as fh:
        for line in fh:
            if line.startswith(b"<FrameSet"):
                m = _FRAMESET_RE.search(line)
                in_ball = bool(m and m.group(1) == b"BALL")
            elif in_ball and line.startswith(b"<Frame "):
                n += 1
                mp, ms = _POSS_RE.search(line), _STATUS_RE.search(line)
                poss[mp.group(1).decode() if mp else "missing"] += 1
                status[ms.group(1).decode() if ms else "missing"] += 1
    return {"raw_ball_frames": n, "raw_ball_possession": dict(poss),
            "raw_ball_status": dict(status)}


def check_match(match_id: str) -> dict:
    files = raw_files(match_id)
    out: dict = {"match_id": match_id}
    meta_text = files["meta"].read_text(encoding="utf-8")
    px = re.search(r'PitchX="([^"]+)"', meta_text)
    py = re.search(r'PitchY="([^"]+)"', meta_text)
    out["meta_pitch_xml"] = [float(px.group(1)), float(py.group(1))]

    ds = sportec.load_tracking(meta_data=files["meta"], raw_data=files["tracking"],
                               only_alive=False)
    md = ds.metadata
    out["pitch_kloppy"] = [md.pitch_dimensions.pitch_length, md.pitch_dimensions.pitch_width]
    out["fps"] = md.frame_rate
    out["tracking_orientation"] = md.orientation.name
    home, away = md.teams[0], md.teams[1]
    out["teams"] = {"home": home.name, "away": away.name}

    # c. starting goalkeepers
    gks = {}
    for side, team in (("home", home), ("away", away)):
        gks[side] = [
            {"player_id": p.player_id, "full_name": p.full_name,
             "first_name": p.first_name, "last_name": p.last_name,
             "starting": p.starting}
            for p in team.players
            if p.starting_position == PositionType.Goalkeeper
        ]
    out["starting_gk"] = gks
    out["n_players_with_starting_position"] = sum(
        p.starting_position is not None for t in (home, away) for p in t.players)

    # b. frame counts
    team_of = {p: t.team_id for t in (home, away) for p in t.players}
    n_total = n_alive = n_complete = n_alive_complete = 0
    n_players_hist: Counter = Counter()
    gk_ids = {g["player_id"] for side in gks.values() for g in side}
    n_gk_missing = 0
    for fr in ds.frames:
        n_total += 1
        alive = fr.ball_state == BallState.ALIVE
        n_alive += alive
        coords = [pid for pid, pdata in fr.players_data.items()
                  if pdata.coordinates is not None]
        per_team = Counter(team_of[p] for p in coords)
        n_players_hist[len(coords)] += 1
        ball_ok = fr.ball_coordinates is not None
        complete = (ball_ok and per_team.get(home.team_id, 0) == C.PLAYERS_PER_TEAM
                    and per_team.get(away.team_id, 0) == C.PLAYERS_PER_TEAM)
        n_complete += complete
        n_alive_complete += alive and complete
        present_ids = {p.player_id for p in coords}
        n_gk_missing += not gk_ids.issubset(present_ids)
    out.update({
        "frames_total_kloppy": n_total, "frames_alive": n_alive,
        "frames_22_plus_ball": n_complete, "frames_alive_22_plus_ball": n_alive_complete,
        "frames_players_with_coords_hist": {str(k): v for k, v in sorted(n_players_hist.items())},
        "frames_missing_a_starting_gk": n_gk_missing,
    })
    out.update(scan_raw_ball(files["tracking"]))
    del ds

    # d. events
    ev = sportec.load_event(event_data=files["event"], meta_data=files["meta"])
    out["event_orientation"] = ev.metadata.orientation.name
    passes = [e for e in ev.events if e.event_type.name == "PASS"]
    incomplete = [e for e in passes if e.result is not None and e.result != PassResult.COMPLETE]
    complete = [e for e in passes if e.result == PassResult.COMPLETE]
    out["events_total"] = len(ev.events)
    out["passes_total"] = len(passes)
    out["passes_incomplete"] = len(incomplete)
    out["passes_incomplete_end_missing"] = sum(e.receiver_coordinates is None for e in incomplete)
    out["passes_complete_end_missing"] = sum(e.receiver_coordinates is None for e in complete)
    out["passes_result_none"] = sum(e.result is None for e in passes)
    return out


def evaluate_gk(results: dict) -> dict:
    rows, all_ids, one_each = [], set(), True
    for mid, r in results.items():
        for side, idx in (("home", 0), ("away", 1)):
            g = r["starting_gk"][side]
            one_each &= len(g) == 1
            exp = EXPECTED_GK[mid][idx]
            last = g[0]["last_name"] if len(g) == 1 else None
            all_ids.update(x["player_id"] for x in g)
            rows.append({
                "match_id": mid, "side": side, "team": r["teams"][side],
                "n_gk": len(g), "full_name": g[0]["full_name"] if g else None,
                "first_name": g[0]["first_name"] if g else None, "last_name": last,
                "expected_last_name": exp,
                "match": last is not None and fold(last) == fold(exp),
            })
    return {"rows": rows, "one_gk_per_team_match": one_each,
            "n_team_matches": len(rows), "n_distinct_gk": len(all_ids),
            "all_names_match": all(r["match"] for r in rows)}


def check_statsbomb() -> dict:
    shots = pd.read_csv(C.SB_SHOTS_CSV)
    matches = pd.read_csv(C.SB_MATCHES_CSV)
    epl = matches[(matches.competition_id == C.SB_PSHOT_COMPETITION_ID)
                  & (matches.season_id == C.SB_PSHOT_SEASON_ID)]
    files = sorted(C.RAW_SB_EVENTS_DIR.glob("*.json"))
    file_ids = {int(f.stem) for f in files}
    n_parse_ok, n_events = 0, 0
    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        n_parse_ok += isinstance(data, list) and len(data) > 0
        n_events += len(data)
    return {
        "shots_rows": len(shots),
        "shots_columns": list(shots.columns),
        "shots_required_columns_missing": [c for c in C.SB_SHOTS_COLUMNS if c not in shots.columns],
        "matches_epl_1516": len(epl),
        "matches_epl_1516_labels": sorted(set(zip(epl.competition, epl.season))),
        "event_files": len(files),
        "event_files_parse_ok": n_parse_ok,
        "event_rows_total": n_events,
        "event_bytes_total": sum(f.stat().st_size for f in files),
        "event_ids_equal_matches_csv": file_ids == set(epl.match_id.astype(int)),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--match", nargs="*", default=list(C.IDSSE_MATCH_IDS))
    parser.add_argument("--skip-statsbomb", action="store_true")
    args = parser.parse_args()
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    for mid in args.match:
        part = CACHE_DIR / f"{mid}.json"
        if part.exists():
            print(f"{mid}: cached")
            continue
        res = check_match(mid)
        part.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{mid}: done")

    if not all((CACHE_DIR / f"{m}.json").exists() for m in C.IDSSE_MATCH_IDS):
        print("not all matches checked yet; summary not written")
        return
    results = {m: json.loads((CACHE_DIR / f"{m}.json").read_text(encoding="utf-8"))
               for m in C.IDSSE_MATCH_IDS}
    summary = {
        "matches": results,
        "goalkeepers": evaluate_gk(results),
        "plan_one_match_frames": [
            m for m, r in results.items()
            if round(r["frames_total_kloppy"] / 1e4, 1) == PLAN_ONE_MATCH_TOTAL_MAN
            and round(r["frames_alive"] / 1e4, 1) == PLAN_ONE_MATCH_ALIVE_MAN
        ],
    }
    if not args.skip_statsbomb:
        summary["statsbomb"] = check_statsbomb()
    C.DERIVED_DIR.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(summary, ensure_ascii=False, indent=1, default=str),
                        encoding="utf-8")
    print(f"wrote {OUT_FILE}")


if __name__ == "__main__":
    main()
