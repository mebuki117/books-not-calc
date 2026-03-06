import json
from pathlib import Path

table = {}

for i in range(8,11):
    table[str(i)] = {}
    for j in range(7,12):
        table[str(i)][str(j)] = {}
        for k in range(1,13):
            cost = i*j*k
            stacks = cost // 64
            remainder = cost % 64

            table[str(i)][str(j)][str(k)] = {
                "cost": cost,
                "stacks": stacks,
                "remainder": remainder
            }

BASE_DIR = Path(__file__).resolve().parent
JSON_PATH = BASE_DIR / "data" / "cost_table.json"

path = JSON_PATH
path.parent.mkdir(parents=True, exist_ok=True)

with open(path,"w",encoding="utf-8") as f:
    json.dump(table,f,indent=2)