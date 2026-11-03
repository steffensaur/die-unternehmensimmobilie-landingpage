"""Ersetzt die Ablauf-Grafik (patch_ablauf.py) durch einen animierten Workflow:
Dokumente -> Automatischer Review -> Bewertung durch Experten -> Regelmaessige Strategie-Calls.
Animation rein per CSS (im <helmet>), Zyklus T Sekunden. Aufruf: python3 tools/patch_workflow.py"""
import json, re

path = "public/index.html"
s = open(path, encoding="utf-8").read()
esc = lambda x: json.dumps(x, ensure_ascii=False)[1:-1].replace("</", "<\\u002F")
t = json.loads(re.search(r'<script type="__bundler/template">\n(.*?)\n\s*</script>', s, re.S).group(1))

def rep(old, new):
    global s
    o = esc(old)
    assert s.count(o) == 1, (old[:70], s.count(o))
    s = s.replace(o, esc(new))

# --- alte Ablauf-Grafik und ihre JS-Animation entfernen ---
a = t.index('  <div style="position: relative; max-width: 1280px; margin: clamp(3.5rem,7vw,5.5rem) auto 0;')
b = t.index('</section>', a)
OLD_FLOW = t[a:b]
a2 = t.index("    const FL = 7200;\n")
b2 = t.index("{ duration: FL, iterations: Infinity });\n", t.index("data-a=flow-stamp", a2)) + len("{ duration: FL, iterations: Infinity });\n")
rep(t[a2:b2], "")

T = 14  # Sekunden pro Zyklus
ON = "border-color:rgba(0,229,200,.6);box-shadow:0 0 0 1px rgba(0,229,200,.22),0 22px 60px rgba(0,229,200,.14)"
OFF = "border-color:rgba(255,255,255,.08);box-shadow:0 0 0 0 rgba(0,229,200,0)"
css = []
def kf(name, body): css.append("@keyframes %s{%s}" % (name, body))
def appear(name, p, end=97):
    kf(name, "0%%,%g%%{opacity:0;transform:translateY(6px)}%g%%,%g%%{opacity:1;transform:none}100%%{opacity:0;transform:translateY(6px)}" % (p, p + 3, end))
for k in range(4):
    a_, b_ = 25 * k, 25 * (k + 1)
    kf("wf-g%d" % k, "0%%,%g%%{%s}%g%%,%g%%{%s}%g%%,100%%{%s}" % (a_, OFF, a_ + 1, b_ - 1, ON, b_, OFF) if k else
       "0%%{%s}1%%,%g%%{%s}%g%%,100%%{%s}" % (OFF, b_ - 1, ON, b_, OFF))
    # Status: wartet / laeuft / erledigt
    kf("wf-w%d" % k, "0%%,%g%%{opacity:1}%g%%,100%%{opacity:0}" % (max(a_ - .01, 0), a_) if k else "0%,100%{opacity:0}")
    kf("wf-r%d" % k, "0%%,%g%%{opacity:0}%g%%,%g%%{opacity:1}%g%%,100%%{opacity:0}" % (a_, a_ + .01, b_ - .01, b_) if k else "0%%,%g%%{opacity:1}%g%%,100%%{opacity:0}" % (b_ - .01, b_))
    kf("wf-d%d" % k, "0%%,%g%%{opacity:0}%g%%,100%%{opacity:1}" % (b_ - .01, b_) if k < 3 else "0%,100%{opacity:0}")
for k in range(3):  # Datenpakete auf den Verbindungen
    p = 25 * (k + 1)
    for d, prop in (("h", "left"), ("v", "top")):
        kf("wf-p%s%d" % (d, k), "0%%,%g%%{%s:0;opacity:0}%g%%{%s:0;opacity:1}%g%%{%s:100%%;opacity:1}%g%%,100%%{%s:100%%;opacity:0}" % (p - 5, prop, p - 4.5, prop, p, prop, p + .5, prop))
kf("wf-loop", "0%,86%{right:0;opacity:0}87%{right:0;opacity:1}99%{right:100%;opacity:1}100%{right:100%;opacity:0}")
kf("wf-bar", "0%,26%{width:0}46%,97%{width:100%}100%{width:0}")
kf("wf-dash-h", "to{background-position:24px 0}")
kf("wf-dash-v", "to{background-position:0 24px}")
kf("wf-pulse", "0%,100%{opacity:1}50%{opacity:.35}")
kf("wf-stamp", "0%,68%{opacity:0;transform:rotate(-8deg) scale(1.6)}71%,97%{opacity:1;transform:rotate(-8deg) scale(1)}100%{opacity:0;transform:rotate(-8deg) scale(1)}")
for j, p in enumerate([3, 9, 15]): appear("wf-c%d" % j, p)
for j, p in enumerate([31, 36, 41]): appear("wf-x%d" % j, p)
appear("wf-hint", 45)
appear("wf-val", 58)
appear("wf-cal", 78)
for j, p in enumerate([82, 86, 90]): appear("wf-a%d" % j, p)

A = "animation:%s " + str(T) + "s infinite"
rules = [
 ".wf-canvas{position:relative;border:1px solid rgba(0,229,200,.22);border-radius:16px;background:#080C10 radial-gradient(rgba(255,255,255,.07) 1px,transparent 1px) 0 0/22px 22px;padding:clamp(16px,2.6vw,28px);overflow:hidden}",
 ".wf-row{display:flex;align-items:stretch}",
 ".wf-node{flex:1 1 0;min-width:0;display:flex;flex-direction:column;gap:10px;background:#0E141C;border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:14px}",
 ".wf-link{flex:0 0 40px;align-self:center;position:relative;height:2px;background:repeating-linear-gradient(90deg,rgba(0,229,200,.55) 0 7px,transparent 7px 12px);background-size:24px 2px;animation:wf-dash-h 1s linear infinite}",
 ".wf-link i{position:absolute;top:-4px;left:0;width:10px;height:10px;margin-left:-5px;border-radius:50%;background:#00E5C8;box-shadow:0 0 14px #00E5C8;opacity:0}",
 ".wf-st{position:relative;height:18px;min-width:76px}",
 ".wf-st span{position:absolute;right:0;top:0;white-space:nowrap;font-family:var(--ui-font-mono);font-size:10px;padding:2px 7px;border-radius:9px}",
 ".wf-st .w{color:rgba(255,255,255,.45);border:1px solid rgba(255,255,255,.12);opacity:0}",
 ".wf-st .r{color:#080C10;background:#00E5C8;opacity:0}",
 ".wf-st .d{color:#00E5C8;border:1px solid rgba(0,229,200,.35)}",
 ".wf-loop{position:relative;margin:16px 12.5% 0;height:26px;border:1.5px dashed rgba(0,229,200,.35);border-top:none;border-radius:0 0 14px 14px}",
 ".wf-loop i{position:absolute;bottom:-5px;right:0;width:9px;height:9px;margin-right:-4px;border-radius:50%;background:#00E5C8;box-shadow:0 0 12px #00E5C8;opacity:0;" + (A % "wf-loop") + " linear}",
 ".wf-loop span{position:absolute;left:50%;bottom:-9px;transform:translateX(-50%);padding:0 10px;background:#080C10;white-space:nowrap;font-family:var(--ui-font-mono);font-size:10px;color:rgba(0,229,200,.85)}",
 ".wf-live{animation:wf-pulse 1.6s infinite}",
 ".wf-bar{width:100%;" + (A % "wf-bar") + " ease-in-out}",
 ".wf-stamp{" + (A % "wf-stamp") + "}",
 "@media (max-width:900px){.wf-row{flex-direction:column}.wf-link{flex:0 0 30px;width:2px;height:auto;background:repeating-linear-gradient(180deg,rgba(0,229,200,.55) 0 7px,transparent 7px 12px);background-size:2px 24px;animation-name:wf-dash-v}.wf-link i{top:0;left:-4px;margin:-5px 0 0}.wf-loop{display:none}}",
 "@media (prefers-reduced-motion:reduce){.wf-canvas *{animation:none!important}}",
]
for k in range(4):
    rules.append(".wf-n%d{%s}" % (k, A % ("wf-g%d" % k)))
    rules.append(".wf-n%d .wf-st .w{%s}.wf-n%d .wf-st .r{%s}.wf-n%d .wf-st .d{%s}" % (k, A % ("wf-w%d" % k), k, A % ("wf-r%d" % k), k, A % ("wf-d%d" % k)))
for k in range(3):
    rules.append(".wf-l%d i{%s ease-in}" % (k, A % ("wf-ph%d" % k)))
    rules.append("@media (max-width:900px){.wf-l%d i{animation-name:wf-pv%d}}" % (k, k))
for cls in ["c0", "c1", "c2", "x0", "x1", "x2", "hint", "val", "cal", "a0", "a1", "a2"]:
    rules.append(".wf-%s{%s}" % (cls, A % ("wf-" + cls)))
CSS = "<style>\n/* Workflow-Grafik (tools/patch_workflow.py) */\n" + "\n".join(css + rules) + "\n</style>\n"

SV = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">%s</svg>'
ICONS = [SV % '<path d="M12 15V4M7.5 8.5L12 4l4.5 4.5"/><path d="M4 15v3a2 2 0 002 2h12a2 2 0 002-2v-3"/>',
         SV % '<rect x="4" y="4" width="16" height="16" rx="3"/><path d="M9 9h6M9 12h6M9 15h3"/><circle cx="17" cy="17" r="3.2" fill="#0E141C"/><path d="M19.4 19.4L21 21"/>',
         SV % '<circle cx="12" cy="8" r="3.5"/><path d="M5 20c.8-3.6 3.6-5.5 7-5.5s6.2 1.9 7 5.5"/>',
         SV % '<rect x="3" y="5" width="18" height="15" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/><path d="M9 15l2 2 4-4"/>']

def head(k, title):
    return ('<div style="display: flex; align-items: center; gap: 10px;">'
            '<span style="flex: none; width: 30px; height: 30px; border-radius: 8px; border: 1px solid var(--ui-cyan-brd); background: rgba(0,229,200,.07); color: var(--ui-cyan); display: flex; align-items: center; justify-content: center;">%s</span>'
            '<span style="flex: 1; font-family: var(--ui-font-mono); font-size: 10px; color: var(--ui-cyan);">0%d</span>'
            '<span class="wf-st"><span class="w">wartet</span><span class="r">● läuft</span><span class="d">✓ erledigt</span></span></div>'
            '<div style="font-size: 14px; font-weight: 500; line-height: 1.3; min-height: 2.6em;">%s</div>') % (ICONS[k], k + 1, title)

ROW = 'display: flex; align-items: center; gap: 8px; padding: 7px 9px; background: var(--ui-ink-3); border: 1px solid var(--ui-w-08); border-radius: 6px; font-size: 11px;'
def file(cls, name, src):
    return ('<div class="%s" style="%s"><span style="font-family: var(--ui-font-mono); font-size: 9px; padding: 2px 4px; border-radius: 3px; background: rgba(0,229,200,.14); color: var(--ui-cyan);">PDF</span>'
            '<span style="flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">%s</span><span style="font-family: var(--ui-font-mono); font-size: 9px; color: var(--ui-w-40);">%s</span></div>') % (cls, ROW, name, src)
def field(cls, k, v):
    return ('<div class="%s" style="display: flex; justify-content: space-between; gap: 8px; font-size: 11px;"><span style="color: var(--ui-w-60);">%s</span>'
            '<span style="font-family: var(--ui-font-mono);">%s</span></div>') % (cls, k, v)
def agenda(cls, txt):
    return '<div class="%s" style="display: flex; align-items: center; gap: 8px; font-size: 11px; color: var(--ui-w-70);"><span style="width: 5px; height: 5px; border-radius: 50%%; background: var(--ui-cyan);"></span>%s</div>' % (cls, txt)

N1 = ('<div class="wf-node wf-n0">' + head(0, "Dokumente hochladen oder übersenden") +
      file("wf-c0", "Grundriss_Halle.pdf", "Upload") + file("wf-c1", "Mietvertrag_2021.pdf", "E-Mail") + file("wf-c2", "Exposé_Leipzig.pdf", "Upload") +
      '<div style="margin-top: auto; font-size: 11px; color: var(--ui-w-40);">Per Upload oder einfach per E-Mail an uns.</div></div>')
N2 = ('<div class="wf-node wf-n1">' + head(1, "Automatischer Review") +
      '<div style="height: 4px; border-radius: 2px; background: var(--ui-ink-4); overflow: hidden;"><div class="wf-bar" style="height: 100%; background: var(--ui-cyan);"></div></div>' +
      field("wf-x0", "Nutzfläche", "4.200 m²") + field("wf-x1", "Baujahr", "2014") + field("wf-x2", "Mietvertrag bis", "2031") +
      '<div class="wf-hint" style="margin-top: auto; padding: 6px 9px; border-radius: 6px; background: rgba(255,184,0,.08); border: 1px solid rgba(255,184,0,.3); font-size: 11px; color: var(--ui-w-70);">Hinweis: Energieausweis fehlt</div></div>')
N3 = ('<div class="wf-node wf-n2" style="position: relative;">' + head(2, "Bewertung durch einen Experten") +
      '<div class="wf-val" style="padding: 10px; border-radius: 8px; background: var(--ui-ink-4); border: 1px solid var(--ui-cyan-brd);">'
      '<div style="font-size: 9px; color: var(--ui-w-40); letter-spacing: .1em; text-transform: uppercase; margin-bottom: 4px;">Marktwert · geprüft</div>'
      '<div style="font-family: var(--ui-font-display); font-size: 30px; color: var(--ui-cyan); letter-spacing: .03em; line-height: 1;">€ 8,4 MIO.</div>'
      '<div style="font-family: var(--ui-font-mono); font-size: 10px; color: var(--ui-w-60); margin-top: 4px;">Bandbreite € 7,9 – 8,8 Mio.</div></div>'
      '<div style="margin-top: auto; font-size: 11px; color: var(--ui-w-40);">Lage, Zustand und Vergleichswerte von einem Experten plausibilisiert.</div>'
      '<div class="wf-stamp" style="position: absolute; right: 12px; bottom: 42px; padding: 4px 8px; border: 2px solid #00E5C8; border-radius: 5px; color: #00E5C8; font-family: var(--ui-font-mono); font-size: 10px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; background: rgba(8,12,16,.9); transform: rotate(-8deg);">Freigegeben</div></div>')
N4 = ('<div class="wf-node wf-n3">' + head(3, "Regelmäßige Strategie-Calls") +
      '<div class="wf-cal" style="display: flex; align-items: center; gap: 10px; padding: 8px 10px; border-radius: 8px; background: var(--ui-ink-4); border: 1px solid var(--ui-cyan-brd);">'
      '<div style="width: 38px; text-align: center; border-radius: 6px; overflow: hidden; border: 1px solid var(--ui-w-15);"><div style="font-family: var(--ui-font-mono); font-size: 8px; background: var(--ui-cyan); color: var(--ui-ink); padding: 1px 0;">MÄR</div>'
      '<div style="font-family: var(--ui-font-display); font-size: 18px; line-height: 1.2;">12</div></div>'
      '<div><div style="font-size: 12px; font-weight: 500;">Strategie-Call</div><div style="font-family: var(--ui-font-mono); font-size: 10px; color: var(--ui-w-60);">30 Min · Video</div></div></div>' +
      agenda("wf-a0", "Wertentwicklung &amp; Markt") + agenda("wf-a1", "Finanzierung &amp; Liquidität") + agenda("wf-a2", "Nachfolge, Verkauf, Standort") + '</div>')

def link(k): return '<div class="wf-link wf-l%d"><i></i></div>' % k

FLOW = (
'  <div style="position: relative; max-width: 1280px; margin: clamp(3.5rem,7vw,5.5rem) auto 0; padding: 0 clamp(1rem,4vw,2.5rem);">\n'
'    <div data-reveal="0" style="margin-bottom: 1.5rem;"><x-import component-from-global-scope="DieUnternehmensimmobilieDesignSystem_a5d1a5.Eyebrow" hint-size="200px,14px">So läuft es ab</x-import>'
'<h3 style="font-family: var(--ui-font-display); font-weight: 400; font-size: clamp(32px,4vw,52px); line-height: .92; letter-spacing: .03em; margin: .75rem 0 0;">VOM DOKUMENT ZUR <span style="color: var(--ui-cyan);">STRATEGIE.</span></h3></div>\n'
'    <div data-reveal="1" class="wf-canvas">\n'
'      <div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 8px 16px; margin-bottom: 16px; font-family: var(--ui-font-mono); font-size: 11px; color: var(--ui-w-60);">'
'<span>workflow · halle-leipzig</span><span style="display: flex; align-items: center; gap: 8px; color: var(--ui-cyan);"><span class="wf-live" style="width: 7px; height: 7px; border-radius: 50%; background: #00E5C8; box-shadow: 0 0 10px #00E5C8;"></span>Workflow aktiv</span></div>\n'
'      <div class="wf-row">' + N1 + link(0) + N2 + link(1) + N3 + link(2) + N4 + '</div>\n'
'      <div class="wf-loop"><i></i><span>↻ regelmäßig: neue Unterlagen, Neubewertung, nächster Call</span></div>\n'
'    </div>\n'
'  </div>\n')

rep(OLD_FLOW, FLOW)
rep("*{box-sizing:border-box}\n</style>\n\n</helmet>", "*{box-sizing:border-box}\n</style>\n" + CSS + "\n</helmet>")
open(path, "w", encoding="utf-8").write(s)
print("ok", len(CSS))
