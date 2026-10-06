"""Erzeugt die Lage-Tabelle (PLZ/Ort -> Region A-D) fuer die Schnell-Bewertung.

Quelle: GeoNames Postal Codes DE (https://download.geonames.org/export/zip/DE.zip, CC BY 4.0).
Aufruf: python3 tools/lageregionen.py /pfad/zu/DE.txt > lage.json
"""
import sys, json, math, re, statistics
from collections import defaultdict

# Logistik-Kernmaerkte (Name, Bezugspunkte)
MARKETS = [
    ("Hamburg", [(53.55, 10.00)]),
    ("Berlin", [(52.52, 13.40)]),
    ("Leipzig/Halle", [(51.34, 12.37), (51.48, 11.97)]),
    ("München", [(48.14, 11.58)]),
    ("Frankfurt/Rhein-Main", [(50.11, 8.68)]),
    ("Düsseldorf", [(51.23, 6.78)]),
    ("Köln", [(50.94, 6.96)]),
    ("Ruhrgebiet", [(51.43, 6.76), (51.48, 7.22), (51.51, 7.47)]),
    ("Stuttgart", [(48.78, 9.18)]),
    ("Hannover", [(52.37, 9.73)]),
    ("Nürnberg", [(49.45, 11.08)]),
    ("Bremen", [(53.08, 8.80)]),
]
RINGS = [(30, "A"), (70, "B"), (120, "C")]  # km; darueber D
IDX = "0123456789ab"

def km(a, b):
    p = math.pi / 180
    h = math.sin((b[0]-a[0])*p/2)**2 + math.cos(a[0]*p)*math.cos(b[0]*p)*math.sin((b[1]-a[1])*p/2)**2
    return 12742 * math.asin(math.sqrt(h))

def code(pt):
    d, i = min((min(km(pt, q) for q in pts), i) for i, (_, pts) in enumerate(MARKETS))
    return next((r for lim, r in RINGS if d <= lim), "D") + IDX[i]

plz, names = defaultdict(list), defaultdict(lambda: defaultdict(list))
for line in open(sys.argv[1], encoding="utf-8"):
    f = line.rstrip("\n").split("\t")
    try: pt = (float(f[9]), float(f[10]))
    except ValueError: continue
    plz[f[1]].append(pt)
    names[f[2]][f[1]].append(pt)

med = lambda pts: (statistics.median(p[0] for p in pts), statistics.median(p[1] for p in pts))
plz_pt = {z: med(p) for z, p in plz.items()}

# PLZ als Laeufe gleicher Region
runs, last = [], None
for z in sorted(plz_pt):
    c = code(plz_pt[z])
    if c != last: runs.append(z + c); last = c

# Orte: nur Namen mit mehreren PLZ (groessere Orte), keine Firmen-PLZ
def norm(s): return re.sub(r"\s+", " ", s.lower().strip())
cities, size = {}, {}
for n, zs in names.items():
    if len(zs) < 2 or re.search(r"GmbH|\bAG\b|\bKG\b|e\.V\.|Bank|Versicherung|Postfach|\d", n): continue
    pts = [plz_pt[z] for z in zs]
    if max(km(pts[0], q) for q in pts) > 60: continue  # gleichnamige Orte in verschiedenen Regionen
    cities[norm(n)], size[norm(n)] = code(med(pts)), len(zs)
# Kurzformen: "frankfurt am main" -> "frankfurt", "halle (saale)" -> "halle"; bei Mehrdeutigkeit der groessere Ort
short = {}
for n, c in cities.items():
    s = re.split(r" \(| am | an der | im | in der | in | bei | vor der | ob der | a\. | a\.d\. | i\. ", n)[0]
    if s != n and s not in cities and size[n] > short.get(s, (0,))[0]: short[s] = (size[n], c)
for s, (_, c) in short.items(): cities[s] = c
# Logistikstandorte, die ueber den Ortsnamen sonst nicht eindeutig waeren
for n, pt in {"halle": (51.48, 11.97), "halle (saale)": (51.48, 11.97), "schkeuditz": (51.40, 12.22),
              "bad hersfeld": (50.87, 9.71), "großbeeren": (52.36, 13.31), "ludwigsfelde": (52.30, 13.26)}.items():
    cities[n] = code(pt)
by = defaultdict(list)
for n, c in sorted(cities.items()): by[c].append(n)
json.dump({"markets": [m for m, _ in MARKETS], "plz": ",".join(runs), "orte": {c: "|".join(v) for c, v in sorted(by.items())}}, sys.stdout, ensure_ascii=False)
