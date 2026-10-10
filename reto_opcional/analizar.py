#!/usr/bin/env python3
"""Resume pares crudos de tiempos sin seleccionar solo los mejores."""
import csv
import statistics as stats
import sys
from collections import defaultdict

def read(path):
    groups = defaultdict(list)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["modo"] != "reto":
                raise ValueError(f"modo inesperado: {row['modo']}")
            n, p = int(row["N"]), int(row["p"])
            ts, tp = float(row["t_seq"]), float(row["t_par"])
            if min(ts, tp) <= 0:
                raise ValueError("tiempo no positivo")
            groups[n, p].append(ts / tp)
    return groups

def runs(path):
    groups = defaultdict(list)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key = (int(row["N"]), int(row["p"]), int(row["corrida"]))
            groups[key].append(float(row["t_seq"]) / float(row["t_par"]))
    return groups

if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(path)
        if "confirmacion" in path:
            print("N,p,corrida,pares,mediana_S,min_S,max_S,pares_superlineales")
            for (n, p, run), speeds in sorted(runs(path).items()):
                print(f"{n},{p},{run},{len(speeds)},{stats.median(speeds):.6f},"
                      f"{min(speeds):.6f},{max(speeds):.6f},"
                      f"{sum(x > p for x in speeds)}")
            continue
        print("N,p,pares,mediana_S,min_S,max_S,pares_superlineales")
        for (n, p), speeds in sorted(read(path).items()):
            print(f"{n},{p},{len(speeds)},{stats.median(speeds):.6f},"
                  f"{min(speeds):.6f},{max(speeds):.6f},"
                  f"{sum(x > p for x in speeds)}")
