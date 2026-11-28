"""Cache raw source files under data/raw/ (plan 3-1).

* IDSSE: the original XML files kloppy's sportec open-data loader reads
  (kloppy._providers.sportec.get_IDSSE_url) -> data/raw/idsse/<match_id>/.
* StatsBomb open data: 2015/16 Premier League (competition 2, season 27)
  match list and raw event JSON -> data/raw/statsbomb/events/<match_id>.json.

Files already present are skipped, so the script can be re-run after an
interruption. Downloads go to a temporary ".part" file and are renamed only
when complete.

Usage: python scripts/gk_sweeper/fetch_raw.py [--idsse] [--statsbomb]
"""

from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
from kloppy._providers.sportec import get_IDSSE_url

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from gk_sweeper import config as C  # noqa: E402

SB_RAW_BASE = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"
IDSSE_DATA_TYPES = ("meta", "event", "tracking")
TIMEOUT_S = 120
MAX_WORKERS = 4


def download(url: str, dest: Path, retries: int = 3) -> str:
    """Download url to dest unless it already exists. Returns a status string."""
    if dest.exists() and dest.stat().st_size > 0:
        return "skipped"
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    last_err: Exception | None = None
    for _ in range(retries):
        try:
            with requests.get(url, stream=True, timeout=TIMEOUT_S) as resp:
                resp.raise_for_status()
                with open(tmp, "wb") as fh:
                    for chunk in resp.iter_content(chunk_size=1 << 20):
                        fh.write(chunk)
            tmp.replace(dest)
            return "downloaded"
        except (requests.RequestException, OSError) as err:  # retry transient errors
            last_err = err
    if tmp.exists():
        tmp.unlink()
    raise RuntimeError(f"download failed: {url}: {last_err}")


def idsse_paths(match_id: str) -> dict[str, tuple[str, Path]]:
    """Map data type -> (kloppy source URL, local cache path keeping the original file name)."""
    out = {}
    for data_type in IDSSE_DATA_TYPES:
        url = get_IDSSE_url(match_id, data_type)
        out[data_type] = (url, C.RAW_IDSSE_DIR / match_id / url.rsplit("/", 1)[-1])
    return out


def fetch_idsse() -> dict[str, int]:
    counts = {"downloaded": 0, "skipped": 0}
    for match_id in C.IDSSE_MATCH_IDS:
        for data_type, (url, dest) in idsse_paths(match_id).items():
            status = download(url, dest)
            counts[status] += 1
            print(f"IDSSE {match_id} {data_type}: {status} ({dest.stat().st_size} B)")
    return counts


def fetch_statsbomb() -> dict[str, int]:
    matches_url = f"{SB_RAW_BASE}/matches/{C.SB_PSHOT_COMPETITION_ID}/{C.SB_PSHOT_SEASON_ID}.json"
    download(matches_url, C.RAW_SB_MATCHES_FILE)
    matches = json.loads(C.RAW_SB_MATCHES_FILE.read_text(encoding="utf-8"))
    match_ids = sorted(int(m["match_id"]) for m in matches)
    print(f"StatsBomb match list: {len(match_ids)} matches")
    counts = {"downloaded": 0, "skipped": 0}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {
            pool.submit(download, f"{SB_RAW_BASE}/events/{mid}.json",
                        C.RAW_SB_EVENTS_DIR / f"{mid}.json"): mid
            for mid in match_ids
        }
        for fut in as_completed(futures):
            counts[fut.result()] += 1
    print(f"StatsBomb events: {counts}")
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--idsse", action="store_true")
    parser.add_argument("--statsbomb", action="store_true")
    args = parser.parse_args()
    both = not (args.idsse or args.statsbomb)
    if args.idsse or both:
        print("IDSSE:", fetch_idsse())
    if args.statsbomb or both:
        fetch_statsbomb()


if __name__ == "__main__":
    main()
