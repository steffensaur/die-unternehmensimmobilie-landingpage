"""Ergaenzt im Regler "Dieselbe Halle. Zwei Werte." Werttreiber-Labels: links (Buchwert-Seite)
unscharf und pulsierend, rechts vom Regler scharf. Aufruf: python3 tools/patch_regler_labels.py"""
import json

path = "public/index.html"
s = open(path, encoding="utf-8").read()
esc = lambda x: json.dumps(x, ensure_ascii=False)[1:-1].replace("</", "<\\u002F")

def rep(old, new):
    global s
    o = esc(old)
    assert s.count(o) == 1, (old[:60], s.count(o))
    s = s.replace(o, esc(new))

# (Text, left, top)
LABELS = [("Flächenknappheit", "9%", "33%"), ("Kranbahnen", "52%", "33%"),
          ("Sale and Lease Back 10 Jahre", "27%", "47%"), ("Mieter Bonität", "60%", "61%"),
          ("Drittverwendungsfähigkeit", "7%", "68%")]
BASE = "position: absolute; left: %s; top: %s; padding: 6px 10px; border-radius: 4px; font-family: var(--ui-font-mono); font-size: 11px; white-space: nowrap; pointer-events: none; "
sharp = "".join(
    '      <div style="' + BASE % (l, t) + 'display: flex; align-items: center; gap: 8px; background: rgba(8,12,16,.86); border: 1px solid var(--ui-cyan-brd); color: #fff;">'
    '<span style="width: 6px; height: 6px; border-radius: 50%; background: #00E5C8; box-shadow: 0 0 10px #00E5C8;"></span>' + txt + "</div>\n"
    for txt, l, t in LABELS)
faint = "".join(
    '        <div data-ghost="%d" style="' % i + BASE % (l, t) + 'border: 1px solid rgba(255,255,255,.25); color: rgba(255,255,255,.75); filter: blur(2.5px); opacity: .35;">'
    '<span style="display: inline-block; width: 6px; height: 6px; margin-right: 8px;"></span>' + txt + "</div>\n"
    for i, (txt, l, t) in enumerate(LABELS))

rep('mix-blend-mode: color; opacity: .4;"></div>\n      <div data-a="split-top"',
    'mix-blend-mode: color; opacity: .4;"></div>\n' + sharp + '      <div data-a="split-top"')
rep('transparent 1px 40px);"></div>\n      </div>\n      <div style="position: absolute; left: 20px; top: 20px;',
    'transparent 1px 40px);"></div>\n' + faint + '      </div>\n      <div style="position: absolute; left: 20px; top: 20px;')
rep("    const D = 900, S = 3400, ease = 'cubic-bezier(.45,0,.25,1)';\n",
    "    const D = 900, S = 3400, ease = 'cubic-bezier(.45,0,.25,1)';\n"
    "    this.qa('[data-ghost]').forEach(g => g.animate([{ opacity: .2 }, { opacity: .6 }, { opacity: .2 }], { duration: 3200, delay: parseInt(g.dataset.ghost, 10) * 520, iterations: Infinity, easing: 'ease-in-out' }));\n")
open(path, "w", encoding="utf-8").write(s)
print("ok")
