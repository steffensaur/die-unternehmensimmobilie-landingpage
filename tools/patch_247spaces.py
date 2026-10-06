"""Ergaenzt Header-Hinweis "Ein Service von 24/7 Spaces" und den Gruppen-Footer
(24/7 Spaces + Services) auf beiden Seiten. Aufruf: python3 tools/patch_247spaces.py"""
import json, base64

esc = lambda x: json.dumps(x, ensure_ascii=False)[1:-1].replace("</", "<\\u002F")
LOGO = "data:image/svg+xml;base64," + base64.b64encode(open("tools/assets/247spaces-logo-dark.svg", "rb").read()).decode()
URL = "https://www.247spaces.de"

HEADER = ('  <a href="%s" target="_blank" rel="noopener" style="display: flex; align-items: center; gap: 10px; padding-left: 1.25rem; border-left: 1px solid var(--ui-w-15); '
          'font-size: 9px; font-weight: 500; letter-spacing: .14em; text-transform: uppercase; color: var(--ui-w-60); white-space: nowrap;" style-hover="color: #fff;">'
          'Ein Service von<img src="%s" alt="24/7 Spaces" style="display: block; height: 32px; width: auto;"></a>\n') % (URL, LOGO)

def tile(code, bg, fg, name, sub, href=None):
    inner = ('<span style="flex: none; width: 44px; height: 44px; border-radius: 10px; background: %s; color: %s; display: flex; align-items: center; justify-content: center; '
             'font-family: var(--ui-font-mono); font-size: 12px; font-weight: 700; box-shadow: 0 6px 30px -6px %s;">%s</span>'
             '<span style="display: flex; flex-direction: column; gap: 2px;"><span style="font-size: 13px; font-weight: 500; color: #F5F3EE;">%s</span>'
             '<span style="font-size: 11px; color: rgba(245,243,238,.5);">%s</span></span>') % (bg, fg, bg, code, name, sub)
    box = "display: flex; align-items: center; gap: 12px; padding: 12px 14px; border-radius: 10px; background: #0C1218; border: 1px solid rgba(245,243,238,.08);"
    if href:
        return '      <a href="%s" style="%s" style-hover="border-color: rgba(245,243,238,.22);">%s</a>\n' % (href, box, inner)
    return '      <div style="%s">%s</div>\n' % (box, inner)

def footer(maxw, home):
    return ('<div data-screen-label="24/7 Spaces" style="background: #080C10;">\n'
            '  <div style="height: 2px; background: linear-gradient(90deg, #00D2A0, #EA6C1A, #7C3AED); opacity: .7;"></div>\n'
            '  <div style="max-width: %dpx; margin: 0 auto; padding: 2.5rem clamp(1rem,4vw,2.5rem); display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%%, 300px), 1fr)); gap: 2rem 4rem; align-items: center;">\n'
            '    <div style="display: flex; flex-direction: column; align-items: flex-start; gap: 1rem;">\n'
            '      <a href="%s" target="_blank" rel="noopener" style="display: flex;"><img src="%s" alt="24/7 Spaces" style="display: block; height: 52px; width: auto;"></a>\n'
            '      <p style="font-size: 13px; color: rgba(245,243,238,.62); line-height: 1.7; margin: 0; max-width: 380px;">Die Unternehmensimmobilie ist ein Service von 24/7 Spaces. Connecting Companies with Spaces.</p>\n'
            '    </div>\n'
            '    <div style="display: flex; flex-direction: column; gap: 8px;">\n'
            '      <div style="font-size: 9px; font-weight: 500; letter-spacing: .14em; text-transform: uppercase; color: rgba(245,243,238,.38); margin-bottom: 2px;">Services von 24/7 Spaces</div>\n'
            % (maxw, URL, LOGO)
            + tile("UI", "#00D2A0", "#080C10", "Die Unternehmensimmobilie", "Bewertung &amp; Verkauf", home)
            + tile("WH", "#EA6C1A", "#F5F3EE", "24/7 Warehouse", "Flächen &amp; Marktplatz")
            + tile("LAB", "#7C3AED", "#F5F3EE", "24/7 Lab", "Marketing")
            + '    </div>\n  </div>\n</div>\n')

PAGES = {
    "public/index.html": ('hint-size="220px,34px"></x-import>\n  <div style="display: flex; gap: 1.75rem; margin-left: auto;', 1200, "/"),
    "public/marktplatz.html": ('hint-size="220px,34px"></x-import></a>\n  <div style="display: flex; gap: 1.75rem; margin-left: auto;', 1280, "index.html"),
}
for path, (anchor, maxw, home) in PAGES.items():
    s = open(path, encoding="utf-8").read()
    for old, new in [(anchor, anchor.replace("\n  <div", "\n" + HEADER + "  <div", 1)),
                     ("</footer>\n\n</div>\n</x-dc>", "</footer>\n" + footer(maxw, home) + "\n</div>\n</x-dc>")]:
        assert s.count(esc(old)) == 1, (path, old[:50], s.count(esc(old)))
        s = s.replace(esc(old), esc(new))
    open(path, "w", encoding="utf-8").write(s)
    print("ok", path)
