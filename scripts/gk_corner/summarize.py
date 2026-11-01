"""Summarise the extracted tables into the descriptive numbers used in the
experiment plan (docs/gk-corner-experiment-plan.md) and a gold-candidate list
of goalkeeper-up corners for manual video verification.

Outputs: data/derived/summary.json, data/derived/gk_up_candidates.csv
"""
import json, os
import numpy as np
import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
D = os.path.join(ROOT, "data", "derived")


def rate(s):
    return round(float(s.mean()) * 100, 2) if len(s) else None


def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(100 * (c - h), 2), round(100 * (c + h), 2))


def main():
    out = {}
    sb = pd.read_csv(os.path.join(D, "statsbomb", "corners.csv"))
    sbm = pd.read_csv(os.path.join(D, "statsbomb", "matches.csv"))
    shots = pd.read_csv(os.path.join(D, "statsbomb", "shots.csv"))
    wy = pd.read_csv(os.path.join(D, "wyscout", "corners.csv"))
    sb = sb.merge(sbm[["match_id", "competition", "season", "gender", "international", "stage"]], on="match_id", how="left")
    out["statsbomb"] = dict(matches=int(sbm.match_id.nunique()), matches_360=int(sbm.has360.sum()),
                            corners=int(len(sb)), corners_360=int(sb.has360.sum()), shots=int(len(shots)),
                            competitions=int(sbm[["competition", "season"]].drop_duplicates().shape[0]))
    out["wyscout"] = dict(matches=int(wy.match_id.nunique()), corners=int(len(wy)))
    for name, f in [("skillcorner", "skillcorner/corners.csv"), ("sportec", "sportec/corners.csv")]:
        p = os.path.join(D, f)
        if os.path.exists(p):
            t = pd.read_csv(p)
            # keeper coordinates stuck at the pitch centre are missing values in the raw feed
            ok = ~t.att_gk_dist_own_goal.between(51.5, 54.5) & t.att_gk_dist_own_goal.notna()
            out[name] = dict(matches=int(t.match_id.nunique()), corners=int(len(t)), corners_valid_keeper=int(ok.sum()),
                             gk_crossed_halfway=int(t[ok].gk_crossed_halfway_30s.sum()),
                             gk_dist_own_goal_median=round(float(t[ok].att_gk_dist_own_goal.median()), 1),
                             att_in_box_mean=round(float(t.att_in_box.mean()), 2),
                             ball_in_def_third_s_median=(round(float(t.ball_in_def_third_s.median()), 1) if t.ball_in_def_third_s.notna().any() else None))

    # goalkeeper-up flags
    sb["gk_up_360"] = (sb.gk_x.fillna(0) > 90).astype(int)
    sb["gk_up"] = ((sb.gk_up_360 == 1) | (sb.gk_involved == 1) | (sb.opp_gk_far_60s == 1)).astype(int)
    sb["channel"] = (sb.gk_up_360.map({1: "360;", 0: ""}) + sb.gk_involved.map({1: "event;", 0: ""})
                     + sb.opp_gk_far_60s.map({1: "counter_shot;", 0: ""}))
    wy["channel"] = "event;"
    late = lambda d: d[(d.period == 2) & (d.minute >= 85)]
    cand_sb = sb[(sb.gk_up == 1)].assign(source="statsbomb")
    cand_wy = wy[wy.gk_involved == 1].assign(source="wyscout")
    cols = ["source", "match_id", "competition", "team", "opponent", "period", "minute", "score_diff", "channel", "goal_30s", "opp_goal_60s"]
    cand = pd.concat([cand_sb.reindex(columns=cols + ["gk_x", "has360", "season"]), cand_wy.reindex(columns=cols)], ignore_index=True)
    cand["plausible"] = ((cand.minute >= 80) & (cand.score_diff <= 0)).astype(int)
    cand.sort_values(["plausible", "source", "minute"], ascending=[False, True, False]).to_csv(os.path.join(D, "gk_up_candidates.csv"), index=False)
    out["gk_up_candidates"] = dict(total=int(len(cand)), plausible_late=int(cand.plausible.sum()),
                                   statsbomb=int(len(cand_sb)), wyscout=int(len(cand_wy)))

    # base rates of corners by game state (StatsBomb, regulation time)
    b = {}
    for label, d in [("all", sb[sb.period <= 2]), ("late85", late(sb)), ("late85_trailing1", late(sb)[late(sb).score_diff == -1]),
                     ("late85_trailing", late(sb)[late(sb).score_diff < 0]), ("late85_level", late(sb)[late(sb).score_diff == 0])]:
        n = len(d); k = int(d.opp_goal_60s.sum())
        b[label] = dict(n=n, goal_in_possession_pct=rate(d.poss_goal), xg_in_possession=round(float(d.poss_xg.mean()), 4),
                        goal_60s_pct=rate(d.goal_60s), opp_shot_60s_pct=rate(d.opp_shots_60s > 0),
                        opp_goal_60s_pct=rate(d.opp_goal_60s), opp_goal_60s_ci=wilson(k, n),
                        counter_reached_final_third_pct=rate(d.counter_reached_final_third))
    out["statsbomb_rates"] = b
    w = {}
    lw = wy[(wy.period == 2) & (wy.minute >= 85)]
    for label, d in [("all", wy[wy.period <= 2]), ("late85", lw), ("late85_trailing", lw[lw.score_diff < 0])]:
        n = len(d); k = int(d.opp_goal_60s.sum())
        w[label] = dict(n=n, goal_30s_pct=rate(d.goal_30s), opp_goal_60s_pct=rate(d.opp_goal_60s), opp_goal_60s_ci=wilson(k, n))
    out["wyscout_rates"] = w

    # attackers in box (360) vs outcome
    s360 = sb[(sb.has360 == 1) & sb.att_in_box.notna() & (sb.short == 0)]
    out["att_in_box"] = {int(a): dict(n=int(len(g)), xg_poss=round(float(g.poss_xg.mean()), 4), goal_pct=rate(g.poss_goal))
                         for a, g in s360.groupby("att_in_box") if len(g) >= 30}

    # empty-net conversion: shots by distance of the defending goalkeeper from goal
    s = shots[(shots.shot_type != "Penalty") & shots.gk_dist_goal.notna()]
    bins = [0, 6, 12, 20, 30, 200]
    s = s.assign(gk_bin=pd.cut(s.gk_dist_goal, bins, right=False))
    out["shots_by_gk_distance"] = {str(k): dict(n=int(len(g)), goal_pct=rate(g.goal), mean_xg=round(float(g.xg.mean()), 3),
                                                goals_over_xg=round(float(g.goal.sum() / max(g.xg.sum(), 1e-9)), 2))
                                   for k, g in s.groupby("gk_bin", observed=True)}
    out["shots_no_gk_in_frame"] = int(shots[(shots.has_freeze == 1) & shots.gk_dist_goal.isna()].shape[0])

    with open(os.path.join(D, "summary.json"), "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
