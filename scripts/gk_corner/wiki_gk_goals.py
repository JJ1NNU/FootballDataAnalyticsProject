"""Collect goalkeeper goals listed on English Wikipedia as an auxiliary,
hand-checkable catalogue of real goalkeeper-forward incidents.

Output: data/derived/web/wikipedia_goalscoring_goalkeepers.csv and
        data/derived/web/wikipedia_premier_league_gk_goals.csv
"""
import io, os, urllib.request
import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "data", "derived", "web")
UA = {"User-Agent": "FootballDataAnalyticsProject research script"}


def tables(title):
    req = urllib.request.Request(f"https://en.wikipedia.org/wiki/{title}", headers=UA)
    return pd.read_html(io.StringIO(urllib.request.urlopen(req, timeout=60).read().decode()))


os.makedirs(OUT, exist_ok=True)
t = tables("List_of_goalscoring_goalkeepers")[0]
t.to_csv(os.path.join(OUT, "wikipedia_goalscoring_goalkeepers.csv"), index=False)
pl = tables("List_of_goalkeepers_who_have_scored_in_the_Premier_League")[0]
pl.to_csv(os.path.join(OUT, "wikipedia_premier_league_gk_goals.csv"), index=False)
print(t.shape, pl.shape)
print(t.head(5).to_string())
print(pl.to_string())
