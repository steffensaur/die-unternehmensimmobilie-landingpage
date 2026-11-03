"""Ergaenzt im Abschnitt "Der Service" die Ablauf-Visualisierung
Foto der Immobilie -> Wert im Dashboard -> Experten-Review. Aufruf: python3 tools/patch_ablauf.py"""
import json

path = "public/index.html"
s = open(path, encoding="utf-8").read()
esc = lambda x: json.dumps(x, ensure_ascii=False)[1:-1].replace("</", "<\\u002F")

def rep(old, new):
    global s
    o = esc(old)
    assert s.count(o) == 1, (old[:60], s.count(o))
    s = s.replace(o, esc(new))

IMG = "f9752949-e799-4751-9aa5-48fa302bd2fa"  # Halle mit Kranbahn (Bundle-Asset)
CARD = "position: relative; display: flex; flex-direction: column; background: var(--ui-ink); border: 1px solid var(--ui-w-08); border-radius: 12px; overflow: hidden;"
VIS = "position: relative; aspect-ratio: 16 / 10; overflow: hidden; background: var(--ui-ink-3); border-bottom: 1px solid var(--ui-w-08);"

def caption(n, title, text):
    return ('<div style="padding: 1.1rem 1.25rem 1.3rem;"><div style="display: flex; align-items: baseline; gap: 10px; margin-bottom: 6px;">'
            '<span style="font-family: var(--ui-font-mono); font-size: 11px; color: var(--ui-cyan);">%s</span>'
            '<span style="font-family: var(--ui-font-display); font-size: 26px; letter-spacing: .03em; line-height: 1;">%s</span></div>'
            '<div style="font-size: 13px; color: var(--ui-w-60); line-height: 1.6;">%s</div></div>') % (n, title, text)

CORNER = '<div style="position: absolute; %s width: 18px; height: 18px; %s"></div>'
corners = "".join(CORNER % (pos, brd) for pos, brd in [
    ("left: 12px; top: 12px;", "border-left: 2px solid #00E5C8; border-top: 2px solid #00E5C8;"),
    ("right: 12px; top: 12px;", "border-right: 2px solid #00E5C8; border-top: 2px solid #00E5C8;"),
    ("left: 12px; bottom: 12px;", "border-left: 2px solid #00E5C8; border-bottom: 2px solid #00E5C8;"),
    ("right: 12px; bottom: 12px;", "border-right: 2px solid #00E5C8; border-bottom: 2px solid #00E5C8;")])

STEP1 = ('      <div data-flow-card="0" data-reveal="0" style="%s">\n'
         '        <div style="%s">'
         '<img src="%s" alt="Industriehalle mit Kranbahn" draggable="false" style="position: absolute; inset: 0; width: 100%%; height: 100%%; object-fit: cover; filter: grayscale(.3) brightness(.7);">'
         '<div data-a="flow-scan" style="position: absolute; left: 0; right: 0; top: 0; height: 2px; background: #00E5C8; box-shadow: 0 0 18px 4px rgba(0,229,200,.5);"></div>'
         + corners +
         '<span style="position: absolute; left: 14px; bottom: 14px; margin: 10px; font-family: var(--ui-font-mono); font-size: 10px; padding: 4px 8px; border-radius: 3px; background: #00E5C8; color: #080C10;">Halle · 4.200 m² · Kranbahn</span>'
         '</div>\n        %s\n      </div>\n') % (CARD, VIS, IMG, caption("01", "IHRE IMMOBILIE.", "Foto, Exposé oder Grundriss hochladen. Die KI erfasst die Objektdaten automatisch."))

bars = "".join('<div style="flex: 1; height: %d%%; border-radius: 2px 2px 0 0; background: %s;"></div>' % (h, "var(--ui-cyan)" if i == 7 else "rgba(0,229,200,%.2f)" % (.18 + i * .07))
               for i, h in enumerate([40, 46, 52, 50, 61, 70, 82, 100]))
STEP2 = ('      <div data-flow-card="1" data-reveal="1" style="%s">\n'
         '        <div style="%s padding: 16px; display: flex; flex-direction: column; justify-content: space-between;">'
         '<div style="display: flex; justify-content: space-between; align-items: center;"><span style="font-size: 11px; color: var(--ui-w-60);">Ihr Depot · Halle Leipzig</span>'
         '<span style="font-family: var(--ui-font-mono); font-size: 10px; color: var(--ui-cyan);">● Live</span></div>'
         '<div><div style="font-size: 9px; color: var(--ui-w-40); letter-spacing: .1em; text-transform: uppercase; margin-bottom: 4px;">Marktwert heute</div>'
         '<div style="display: flex; align-items: baseline; gap: 10px;"><span style="font-family: var(--ui-font-display); font-size: clamp(30px,3.4vw,40px); color: var(--ui-cyan); letter-spacing: .03em; line-height: 1;">€ 8,4 MIO.</span>'
         '<span style="font-family: var(--ui-font-mono); font-size: 11px; color: var(--ui-cyan);">+5,1 %%</span></div></div>'
         '<div style="display: flex; align-items: flex-end; gap: 4px; height: 26%%;">%s</div>'
         '</div>\n        %s\n      </div>\n') % (CARD, VIS, bars, caption("02", "WERT IM DASHBOARD.", "Der Marktwert erscheint in Ihrem Depot, neben Buchwert und Wertentwicklung."))

def check(label, d):
    return ('<div data-flow-check="%d" style="display: flex; align-items: center; gap: 8px; padding: 6px 10px; background: var(--ui-ink-4); border: 1px solid var(--ui-w-08); border-radius: 6px; font-size: 11px;">'
            '<span style="width: 14px; height: 14px; border-radius: 50%%; background: var(--ui-cyan); color: var(--ui-ink); font-size: 9px; display: flex; align-items: center; justify-content: center;">✓</span>%s</div>') % (d, label)
STEP3 = ('      <div data-flow-card="2" data-reveal="2" style="%s">\n'
         '        <div style="%s padding: 16px; display: flex; flex-direction: column; gap: 6px; justify-content: center;">'
         'CHECKS'
         '<div data-a="flow-stamp" style="position: absolute; right: 14px; bottom: 12px; transform: rotate(-8deg); padding: 6px 10px; border: 2px solid #00E5C8; border-radius: 6px; color: #00E5C8; font-family: var(--ui-font-mono); font-size: 11px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; background: rgba(8,12,16,.85);">Reviewed</div>'
         '</div>\n        %s\n      </div>\n') % (CARD, VIS, caption("03", "EXPERTEN-REVIEW.", "Unsere Immobilienexperten prüfen den Wert. Sie erhalten eine belastbare Grundlage."))
STEP3 = STEP3.replace("CHECKS", check("Lage &amp; Markt plausibilisiert", 0) + check("Zustand &amp; Ausstattung geprüft", 1) + check("Vergleichstransaktionen abgeglichen", 2))

def node(i, left):
    return ('<div data-flow-node="%d" style="position: absolute; left: %s; top: 50%%; width: 30px; height: 30px; margin: -15px 0 0 -15px; border-radius: 50%%; background: var(--ui-ink-2); border: 1px solid var(--ui-cyan-brd); color: var(--ui-cyan); '
            'font-family: var(--ui-font-mono); font-size: 11px; display: flex; align-items: center; justify-content: center;">0%d</div>') % (i, left, i + 1)

FLOW = (
'  <div style="position: relative; max-width: 1280px; margin: clamp(3.5rem,7vw,5.5rem) auto 0; padding: 0 clamp(1rem,4vw,2.5rem);">\n'
'    <div data-reveal="0" style="display: flex; flex-wrap: wrap; align-items: flex-end; justify-content: space-between; gap: 1rem 3rem; margin-bottom: 1.75rem;">\n'
'      <div><x-import component-from-global-scope="DieUnternehmensimmobilieDesignSystem_a5d1a5.Eyebrow" hint-size="200px,14px">So läuft es ab</x-import>'
'<h3 style="font-family: var(--ui-font-display); font-weight: 400; font-size: clamp(32px,4vw,52px); line-height: .92; letter-spacing: .03em; margin: .75rem 0 0;">VOM FOTO ZUM <span style="color: var(--ui-cyan);">GEPRÜFTEN WERT.</span></h3></div>\n'
'    </div>\n'
'    <div data-reveal="0" style="position: relative; height: 30px; margin: 0 0 18px;">'
'<div style="position: absolute; left: 16.66%; right: 16.66%; top: 50%; height: 1px; background: var(--ui-w-15);"></div>'
'<div style="position: absolute; left: 16.66%; right: 16.66%; top: 50%; height: 1px; overflow: visible;"><div data-a="flow-dot" style="position: absolute; left: 0; top: -4px; width: 9px; height: 9px; margin-left: -4px; border-radius: 50%; background: #00E5C8; box-shadow: 0 0 14px #00E5C8;"></div></div>'
+ node(0, "16.66%") + node(1, "50%") + node(2, "83.33%") +
'</div>\n'
'    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 260px), 1fr)); gap: 14px;">\n'
+ STEP1 + STEP2 + STEP3 +
'    </div>\n'
'  </div>\n')

rep('Beispielportfolio. Werte illustrativ.</div>\n    </div>\n  </div>\n</section>',
    'Beispielportfolio. Werte illustrativ.</div>\n    </div>\n  </div>\n' + FLOW + '</section>')

ANIM = """    const FL = 7200;
    const fd = this.q('[data-a=flow-dot]');
    fd && fd.animate([{ left: '0%', opacity: 0 }, { left: '0%', opacity: 1, offset: .06 }, { left: '50%', offset: .36 }, { left: '50%', offset: .5 }, { left: '100%', offset: .8 }, { left: '100%', opacity: 1, offset: .94 }, { left: '100%', opacity: 0 }], { duration: FL, iterations: Infinity, easing: 'ease-in-out' });
    [0, .36, .8].forEach((at, i) => {
      const on = { borderColor: 'rgba(0,229,200,.55)', boxShadow: '0 0 0 1px rgba(0,229,200,.25), 0 18px 50px rgba(0,229,200,.12)' }, off = { borderColor: 'rgba(255,255,255,.08)', boxShadow: '0 0 0 0 rgba(0,0,0,0)' };
      const end = Math.min(1, at + .3);
      const kf = [Object.assign({ offset: 0 }, at === 0 ? on : off), Object.assign({ offset: at }, on), Object.assign({ offset: end }, on), Object.assign({ offset: Math.min(1, end + .06) }, off)];
      if (kf[3].offset < 1) kf.push(Object.assign({ offset: 1 }, off));
      const card = this.q('[data-flow-card="' + i + '"]');
      card && card.animate(kf.filter((k, j) => j === 0 || k.offset > kf[j - 1].offset), { duration: FL, iterations: Infinity });
      const nd = this.q('[data-flow-node="' + i + '"]');
      nd && nd.animate([{ background: '#0E141C', color: '#00E5C8', offset: 0 }, { background: '#00E5C8', color: '#080C10', offset: Math.max(.001, at) }, { background: '#00E5C8', color: '#080C10', offset: end }, { background: '#0E141C', color: '#00E5C8', offset: Math.min(1, end + .06) }].filter((k, j, a) => j === 0 || k.offset > a[j - 1].offset), { duration: FL, iterations: Infinity });
    });
    const fs = this.q('[data-a=flow-scan]');
    fs && fs.animate([{ top: '0%', opacity: 0 }, { top: '0%', opacity: 1, offset: .05 }, { top: '100%', opacity: 1, offset: .3 }, { top: '100%', opacity: 0, offset: .34 }, { top: '100%', opacity: 0 }], { duration: FL, iterations: Infinity, easing: 'ease-in-out' });
    this.qa('[data-flow-check]').forEach(c => { const o = .8 + parseInt(c.dataset.flowCheck, 10) * .04; c.animate([{ opacity: .35, offset: 0 }, { opacity: .35, offset: o - .001 }, { opacity: 1, offset: o }, { opacity: 1, offset: 1 }], { duration: FL, iterations: Infinity }); });
    const st = this.q('[data-a=flow-stamp]');
    st && st.animate([{ opacity: 0, transform: 'rotate(-8deg) scale(1.6)', offset: 0 }, { opacity: 0, transform: 'rotate(-8deg) scale(1.6)', offset: .92 }, { opacity: 1, transform: 'rotate(-8deg) scale(1)', offset: .96 }, { opacity: 1, transform: 'rotate(-8deg) scale(1)', offset: 1 }], { duration: FL, iterations: Infinity });
"""
rep("    const D = 900, S = 3400, ease = 'cubic-bezier(.45,0,.25,1)';\n",
    "    const D = 900, S = 3400, ease = 'cubic-bezier(.45,0,.25,1)';\n" + ANIM)
open(path, "w", encoding="utf-8").write(s)
print("ok")
