"""Fuegt direkt unter dem Hero den Abschnitt "Der Service" ein (Erklaerung + Portfolio-Visualisierung).
Aufruf: python3 tools/patch_service.py"""
import json

path = "public/index.html"
s = open(path, encoding="utf-8").read()
esc = lambda x: json.dumps(x, ensure_ascii=False)[1:-1].replace("</", "<\\u002F")

def rep(old, new):
    global s
    o = esc(old)
    assert s.count(o) == 1, (old[:60], s.count(o))
    s = s.replace(o, esc(new))

def pillar(n, title, text, icon, d):
    return ('        <div data-reveal="%d" style="display: grid; grid-template-columns: 44px minmax(0,1fr); gap: 1rem; padding: 1.25rem 0; border-top: 1px solid var(--ui-w-08);">\n'
            '          <div style="width: 44px; height: 44px; border-radius: 10px; border: 1px solid var(--ui-cyan-brd); background: rgba(0,229,200,.06); color: var(--ui-cyan); display: flex; align-items: center; justify-content: center;">%s</div>\n'
            '          <div><div style="display: flex; align-items: baseline; gap: 10px; margin-bottom: 4px;"><span style="font-family: var(--ui-font-mono); font-size: 11px; color: var(--ui-cyan);">%s</span>'
            '<span style="font-family: var(--ui-font-display); font-size: 26px; letter-spacing: .03em; line-height: 1;">%s</span></div>'
            '<div style="font-size: 14px; color: var(--ui-w-60); line-height: 1.65; text-wrap: pretty;">%s</div></div>\n'
            '        </div>\n') % (d, icon, n, title, text)

SVG = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">%s</svg>'
I_ORT = SVG % '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>'
I_REV = SVG % '<path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6l7-3z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>'
I_CAL = SVG % '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/><circle cx="12" cy="15.5" r="1.6" fill="currentColor"/>'

def obj(name, meta, val, trend):
    return ('            <div style="display: flex; align-items: center; gap: 12px; padding: 11px 12px; background: var(--ui-ink-3); border: 1px solid var(--ui-w-08); border-radius: 7px;">'
            '<span style="width: 8px; height: 8px; border-radius: 2px; background: var(--ui-cyan); flex: none;"></span>'
            '<span style="flex: 1; min-width: 0;"><span style="display: block; font-size: 13px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">%s</span>'
            '<span style="display: block; font-family: var(--ui-font-mono); font-size: 10px; color: var(--ui-w-40); margin-top: 2px;">%s</span></span>'
            '<span style="text-align: right;"><span style="display: block; font-family: var(--ui-font-mono); font-size: 13px;">%s</span>'
            '<span style="display: block; font-family: var(--ui-font-mono); font-size: 10px; color: var(--ui-cyan); margin-top: 2px;">%s</span></span></div>\n') % (name, meta, val, trend)

MONTHS = "JFMAMJJASOND"
def month(i, m):
    if i == 2:   # Maerz: Strategiegespraech
        return ('<div style="flex: 1; display: flex; flex-direction: column; align-items: center; gap: 6px;"><div data-a="svc-pulse" style="width: 100%%; height: 22px; border-radius: 4px; background: var(--ui-cyan); box-shadow: 0 0 18px rgba(0,229,200,.5);"></div>'
                '<span style="font-family: var(--ui-font-mono); font-size: 9px; color: var(--ui-cyan);">%s</span></div>') % m
    if i == 1:   # Februar: Experten-Review
        return ('<div style="flex: 1; display: flex; flex-direction: column; align-items: center; gap: 6px;"><div style="width: 100%%; height: 22px; border-radius: 4px; border: 1px solid var(--ui-cyan-brd); background: rgba(0,229,200,.12); color: var(--ui-cyan); font-size: 11px; display: flex; align-items: center; justify-content: center;">✓</div>'
                '<span style="font-family: var(--ui-font-mono); font-size: 9px; color: var(--ui-w-60);">%s</span></div>') % m
    return ('<div style="flex: 1; display: flex; flex-direction: column; align-items: center; gap: 6px;"><div style="width: 100%%; height: 22px; border-radius: 4px; background: var(--ui-ink-4);"></div>'
            '<span style="font-family: var(--ui-font-mono); font-size: 9px; color: var(--ui-w-40);">%s</span></div>') % m

SECTION = (
'<section id="service" data-screen-label="Der Service" style="position: relative; overflow: hidden; padding: clamp(4rem,9vw,7rem) 0; background: var(--ui-ink-2); border-bottom: 1px solid var(--ui-w-08);">\n'
'  <div style="position: absolute; width: 640px; height: 640px; border-radius: 50%; background: radial-gradient(circle,#00E5C8,transparent 65%); top: -220px; right: -220px; opacity: .08; filter: blur(130px); pointer-events: none;"></div>\n'
'  <div style="position: relative; max-width: 1280px; margin: 0 auto; padding: 0 clamp(1rem,4vw,2.5rem); display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 380px), 1fr)); gap: 3rem 4rem; align-items: center;">\n'
'    <div style="display: flex; flex-direction: column;">\n'
'      <div data-reveal="0"><x-import component-from-global-scope="DieUnternehmensimmobilieDesignSystem_a5d1a5.Eyebrow" lead="dot" hint-size="200px,14px">Der Service</x-import></div>\n'
'      <h2 data-reveal="0" style="font-family: var(--ui-font-display); font-weight: 400; font-size: clamp(42px,5.6vw,76px); line-height: .9; letter-spacing: .03em; margin: 1rem 0 2rem; text-wrap: balance;">DER WERT IHRER UNTERNEHMENS&shy;- UND <span style="color: var(--ui-cyan);">BETRIEBS&shy;IMMOBILIEN.</span></h2>\n'
'      <div style="display: flex; flex-direction: column; border-bottom: 1px solid var(--ui-w-08);">\n'
+ pillar("01", "AN EINEM ORT.", "Alle Standorte in einem Depot: Marktwert, Buchwert und Wertentwicklung auf einen Blick.", I_ORT, 1)
+ pillar("02", "REVIEWED VON EXPERTEN.", "Jede Bewertung wird von unseren Immobilienexperten geprüft und plausibilisiert.", I_REV, 2)
+ pillar("03", "EINMAL IM JAHR STRATEGIEGESPRÄCH.", "Wir tauschen uns mit Ihnen aus: Wertentwicklung, Finanzierung, Nachfolge und nächste Schritte.", I_CAL, 3)
+ '      </div>\n'
'    </div>\n'
'    <div data-reveal="2" style="position: relative;">\n'
'      <div style="background: var(--ui-ink); border: 1px solid var(--ui-cyan-brd); border-radius: 14px; overflow: hidden; box-shadow: 0 30px 80px rgba(0,0,0,.5);">\n'
'        <div style="display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 14px 18px; background: var(--ui-ink-3); border-bottom: 1px solid var(--ui-w-08);">\n'
'          <span style="font-size: 13px; font-weight: 500;">Ihr Immobilien-Depot</span>\n'
'          <x-import component-from-global-scope="DieUnternehmensimmobilieDesignSystem_a5d1a5.Tag" tone="cyan" dot="{{ true }}" hint-size="70px,20px">Live</x-import>\n'
'        </div>\n'
'        <div style="padding: 18px;">\n'
'          <div style="display: flex; flex-wrap: wrap; align-items: flex-end; justify-content: space-between; gap: 8px 16px; padding: 16px; background: var(--ui-ink-4); border: 1px solid var(--ui-cyan-brd); border-radius: 9px; margin-bottom: 10px;">\n'
'            <div><div style="font-size: 9px; color: var(--ui-w-40); letter-spacing: .1em; text-transform: uppercase; margin-bottom: 6px;">Gesamtwert · 3 Standorte</div>'
'<div style="font-family: var(--ui-font-display); font-size: clamp(38px,5vw,52px); color: var(--ui-cyan); letter-spacing: .03em; line-height: 1;">€ 18,6 MIO.</div></div>\n'
'            <div style="text-align: right; font-family: var(--ui-font-mono); font-size: 11px; color: var(--ui-w-60); line-height: 1.7;">Buchwert € 6,1 Mio.<br><span style="color: var(--ui-cyan);">+4,2 % ggü. Vorjahr</span></div>\n'
'          </div>\n'
'          <div style="display: flex; flex-direction: column; gap: 6px;">\n'
+ obj("Logistikhalle · Leipzig", "12.400 m² · Region A", "€ 8,4 Mio.", "+5,1 %")
+ obj("Produktionshalle · Nürnberg", "7.850 m² · Region A", "€ 6,4 Mio.", "+3,1 %")
+ obj("Werkstatt &amp; Lager · Kassel", "4.100 m² · Region C", "€ 3,8 Mio.", "+3,9 %")
+ '          </div>\n'
'          <div style="display: flex; align-items: center; gap: 10px; margin-top: 10px; padding: 10px 12px; background: rgba(0,229,200,.06); border: 1px solid var(--ui-cyan-brd); border-radius: 7px; font-size: 12px;">'
'<span style="width: 22px; height: 22px; border-radius: 50%; background: var(--ui-cyan); color: var(--ui-ink); display: flex; align-items: center; justify-content: center; font-size: 12px; flex: none;">✓</span>'
'<span style="flex: 1;">Experten-Review abgeschlossen</span><span style="font-family: var(--ui-font-mono); font-size: 11px; color: var(--ui-w-60);">Feb.</span></div>\n'
'          <div style="margin-top: 14px; padding-top: 14px; border-top: 1px solid var(--ui-w-08);">\n'
'            <div style="display: flex; justify-content: space-between; gap: 12px; margin-bottom: 10px;"><span style="font-size: 9px; color: var(--ui-w-40); letter-spacing: .1em; text-transform: uppercase;">Ihr Jahresrhythmus</span>'
'<span style="font-family: var(--ui-font-mono); font-size: 11px; color: var(--ui-cyan);">Strategiegespräch · März</span></div>\n'
'            <div style="display: flex; gap: 4px;">' + "".join(month(i, m) for i, m in enumerate(MONTHS)) + '</div>\n'
'          </div>\n'
'        </div>\n'
'      </div>\n'
'      <div style="font-size: 11px; color: var(--ui-w-40); margin-top: 10px;">Beispielportfolio. Werte illustrativ.</div>\n'
'    </div>\n'
'  </div>\n'
'</section>\n\n')

rep('</section>\n\n<section data-screen-label="Buchwert vs Marktwert"', '</section>\n\n' + SECTION + '<section data-screen-label="Buchwert vs Marktwert"')
rep("    const D = 900, S = 3400, ease = 'cubic-bezier(.45,0,.25,1)';\n",
    "    const D = 900, S = 3400, ease = 'cubic-bezier(.45,0,.25,1)';\n"
    "    const svcPulse = this.q('[data-a=svc-pulse]');\n"
    "    svcPulse && svcPulse.animate([{ boxShadow: '0 0 0 rgba(0,229,200,0)', opacity: .75 }, { boxShadow: '0 0 22px rgba(0,229,200,.65)', opacity: 1 }, { boxShadow: '0 0 0 rgba(0,229,200,0)', opacity: .75 }], { duration: 2400, iterations: Infinity, easing: 'ease-in-out' });\n")
open(path, "w", encoding="utf-8").write(s)
print("ok")
