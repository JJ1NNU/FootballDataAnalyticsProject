"""Figures for the proposal deck (docs/slides/).

Usage: python3 scripts/gk_corner/make_slide_figures.py <statsbomb_events_3857257.json> <three_sixty_3857257.json>
Outputs PNGs to docs/slides/figures/.
"""
import json, os, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
D = os.path.join(ROOT, "data", "derived")
OUT = os.path.join(ROOT, "docs", "slides", "figures")
RED, BLUE, GREY, INK = "#C0392B", "#1F5FA8", "#B8BEC6", "#22262B"

for name in ["Malgun Gothic", "NanumGothic", "Noto Sans CJK KR", "WenQuanYi Zen Hei"]:
    if any(name in f.name for f in font_manager.fontManager.ttflist):
        plt.rcParams["font.family"] = name
        break
plt.rcParams.update({"axes.spines.top": False, "axes.spines.right": False, "font.size": 13,
                     "axes.edgecolor": INK, "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK})


def dots():
    sb = pd.read_csv(os.path.join(D, "statsbomb", "corners.csv"), usecols=["match_id"])
    wy = pd.read_csv(os.path.join(D, "wyscout", "corners.csv"), usecols=["match_id"])
    cand = pd.read_csv(os.path.join(D, "gk_up_candidates.csv"))
    n, k = len(sb) + len(wy), int(cand.plausible.sum())
    cols = 300; rows = int(np.ceil(n / cols))
    idx = np.arange(n); x, y = idx % cols, idx // cols
    rng = np.random.default_rng(7); hot = rng.choice(n, k, replace=False)
    fig, ax = plt.subplots(figsize=(10, 6.6), dpi=200)
    ax.scatter(x, y, s=0.35, c=GREY, linewidths=0)
    ax.scatter(x[hot], y[hot], s=28, c=RED, linewidths=0)
    ax.set_xlim(-2, cols + 1); ax.set_ylim(rows + 1, -2); ax.axis("off")
    fig.savefig(os.path.join(OUT, "s4_corners_dots.png"), bbox_inches="tight", transparent=True)
    plt.close(fig)
    return n, k


def pitch_half(ax):
    kw = dict(color="#8A9199", lw=1.4)
    ax.plot([60, 120, 120, 60, 60], [0, 0, 80, 80, 0], **kw)
    ax.plot([102, 120, 120, 102, 102], [18, 18, 62, 62, 18], **kw)
    ax.plot([114, 120, 120, 114, 114], [30, 30, 50, 50, 30], **kw)
    ax.plot([120, 120], [36, 44], color=INK, lw=4)
    ax.add_patch(plt.Circle((108, 40), 0.5, color="#8A9199"))
    t = np.linspace(np.radians(127), np.radians(233), 50)
    ax.plot(108 + 10 * np.cos(t), 40 + 10 * np.sin(t), **kw)
    ax.set_xlim(58, 122); ax.set_ylim(82, -2); ax.set_aspect("equal"); ax.axis("off")


def frame(ev_path, ff_path, event_id="00c74d1d-5860-4013-ac8d-a40f29c3aef4"):
    ev = {e["id"]: e for e in json.load(open(ev_path))}
    ff = {f["event_uuid"]: f for f in json.load(open(ff_path))}[event_id]
    e = ev[event_id]
    fig, ax = plt.subplots(figsize=(8, 10), dpi=200)
    pitch_half(ax)
    poly = np.array(ff["visible_area"]).reshape(-1, 2)
    ax.fill(poly[:, 0], poly[:, 1], color="#EEF1F4", zorder=0)
    for p in ff["freeze_frame"]:
        x, y = p["location"]
        if p.get("keeper") and p.get("teammate"):
            ax.scatter(x, y, s=520, marker="*", c=BLUE, edgecolors="white", linewidths=1.2, zorder=4)
            ax.annotate("덴마크 골키퍼", (x, y), xytext=(x - 34, y - 14), fontsize=16, color=BLUE,
                        arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.5), zorder=5)
        elif p.get("teammate"):
            ax.scatter(x, y, s=170, c=BLUE, edgecolors="white", linewidths=1, zorder=3)
        else:
            ax.scatter(x, y, s=170, c=RED, edgecolors="white", linewidths=1, zorder=3)
    bx, by = e["location"]
    ax.scatter(bx, by, s=60, c="white", edgecolors=INK, zorder=5)
    ax.scatter([], [], s=120, c=BLUE, label="덴마크(공격)"); ax.scatter([], [], s=120, c=RED, label="호주(수비)")
    ax.legend(loc="lower left", frameon=False, fontsize=13)
    fig.savefig(os.path.join(OUT, "s6_360_frame.png"), bbox_inches="tight", transparent=True)
    plt.close(fig)


def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return 100 * p, 100 * (c - h), 100 * (c + h)


def charts():
    sb = pd.read_csv(os.path.join(D, "statsbomb", "corners.csv"))
    reg = sb[sb.period <= 2]
    late = reg[(reg.period == 2) & (reg.minute >= 85) & (reg.score_diff < 0)]
    vals = [wilson(int(g.opp_goal_60s.sum()), len(g)) for g in (reg, late)]
    fig, ax = plt.subplots(figsize=(6, 4.6), dpi=200)
    labels = ["전체 코너", "85분 이후\n지고 있을 때"]
    for i, (m, lo, hi) in enumerate(vals):
        ax.bar(i, m, color=[GREY, RED][i], width=0.55)
        ax.errorbar(i, m, yerr=[[m - lo], [hi - m]], color=INK, capsize=8, lw=1.6)
        ax.text(i, hi + 0.12, f"{m:.2f}%", ha="center", fontsize=16, fontweight="bold", color=INK)
    ax.set_xticks([0, 1], labels); ax.set_ylabel("코너 후 60초 안 실점률 (%)")
    ax.set_ylim(0, 3.2)
    fig.savefig(os.path.join(OUT, "s7_concede_rate.png"), bbox_inches="tight", transparent=True)
    plt.close(fig)

    s = sb[(sb.has360 == 1) & (sb.short == 0) & sb.att_in_box.between(4, 7)]
    g = s.groupby("att_in_box").poss_xg.agg(["mean", "std", "count"])
    se = g["std"] / np.sqrt(g["count"])
    fig, ax = plt.subplots(figsize=(6, 4.6), dpi=200)
    ax.errorbar(g.index, g["mean"], yerr=1.96 * se, fmt="o-", color=BLUE, ecolor=BLUE, capsize=8, lw=2, ms=9)
    for a, m, c in zip(g.index, g["mean"], g["count"]):
        ax.text(a + 0.08, m, f"n={c}", fontsize=11, color="#5A6169", va="center")
    ax.set_xticks(g.index, [f"{int(a)}명" for a in g.index]); ax.set_xlabel("박스 안 공격 인원")
    ax.set_ylabel("코너 한 번의 기대득점(xG)"); ax.set_ylim(0, 0.085)
    fig.savefig(os.path.join(OUT, "s7_attackers_xg.png"), bbox_inches="tight", transparent=True)
    plt.close(fig)
    return vals


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print("dots", dots())
    frame(sys.argv[1], sys.argv[2])
    print("concede", charts())
