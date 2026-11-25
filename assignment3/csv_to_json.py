"""Collect notebook outputs (outputs/*.csv) into outputs/report_data.json for the report builder."""
import json, glob, os
import pandas as pd
d = {}
for f in sorted(glob.glob("outputs/*.csv")):
    df = pd.read_csv(f)
    df.columns = ["_idx" if c.startswith("Unnamed") else c for c in df.columns]
    d[os.path.basename(f)[:-4]] = json.loads(df.to_json(orient="records"))
json.dump(d, open("outputs/report_data.json", "w"), ensure_ascii=False, indent=1)
print(list(d))
