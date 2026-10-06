"""Baut die Herleitung (Baukosten, Alterswertminderung, Lage) in die Schnell-Bewertung
von public/index.html ein. Aufruf: python3 tools/patch_kurzbewertung.py lage.json"""
import json, sys

lage = json.load(open(sys.argv[1], encoding="utf-8"))
path = "public/index.html"
s = open(path, encoding="utf-8").read()
esc = lambda x: json.dumps(x, ensure_ascii=False)[1:-1].replace("</", "<\\u002F")

def rep(old, new):
    global s
    o = esc(old)
    assert s.count(o) == 1, (old[:60], s.count(o))
    s = s.replace(o, esc(new))

ROW = ('<div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: baseline; gap: 4px 16px; padding: 10px 14px; border-top: 1px solid var(--ui-w-08); font-size: 12px;">'
       '<span style="min-width: 150px; color: %s;">%s</span>'
       '<span style="flex: 1; min-width: 200px; font-family: var(--ui-font-mono); font-size: 11px; color: var(--ui-w-60);">{{ %s }}</span>'
       '<span style="font-family: var(--ui-font-mono); color: %s;">{{ %s }}</span></div>\n')
W, C = "var(--ui-white)", "var(--ui-cyan)"
BLOCK = ('        <div style="margin-top: 10px; background: var(--ui-ink-3); border: 1px solid var(--ui-w-08); border-radius: 8px; overflow: hidden;">\n'
         '          <div style="padding: 10px 14px; font-size: 9px; color: var(--ui-w-40); letter-spacing: .1em; text-transform: uppercase;">Herleitung</div>\n'
         + "          " + ROW % (W, "Baukosten Neubau", "dBau", W, "dBauVal")
         + "          " + ROW % (W, "Alterswertminderung", "dAge", W, "dAgeVal")
         + "          " + ROW % (W, "Lage", "dLoc", W, "dLocVal")
         + "          " + ROW % (C, "Erstindikation", "dSum", C, "resTotal")
         + '          <div style="padding: 10px 14px; border-top: 1px solid var(--ui-w-08); font-size: 11px; color: var(--ui-w-40); line-height: 1.5;">Lage nach Entfernung zum nächsten Logistik-Kernmarkt: Region A bis 30 km (+10 %), B bis 70 km (±0 %), C bis 120 km (−10 %), D darüber (−20 %).</div>\n'
         '        </div>\n')

rep('label="Standort" placeholder="PLZ oder Stadt" hint-size',
    'label="Standort" placeholder="PLZ oder Stadt" value="{{ loc }}" on-change="{{ onLoc }}" hint-size')
rep('Ausführliche Bewertung →</a></div>\n        </div>\n      </sc-if>',
    'Ausführliche Bewertung →</a></div>\n        </div>\n' + BLOCK + '      </sc-if>')
rep("state = { type: 'logistik', area: '8.500', year: '2008', result: null,",
    "state = { type: 'logistik', area: '8.500', year: '2008', loc: '', result: null,")
rep("      onYear: e => this.setState({ year: e.target.value, result: null }),\n",
    "      onYear: e => this.setState({ year: e.target.value, result: null }),\n"
    "      loc: this.state.loc, onLoc: e => this.setState({ loc: e.target.value, result: null }),\n")
rep("hasResult: !!r, resTotal: r ? r.total : '', resRange: r ? r.range : '',",
    "hasResult: !!r, resTotal: r ? r.total : '', resRange: r ? r.range : '',\n"
    "      dBau: r ? r.bau : '', dBauVal: r ? r.bauVal : '', dAge: r ? r.age : '', dAgeVal: r ? r.ageVal : '', dLoc: r ? r.loc : '', dLocVal: r ? r.locVal : '', dSum: r ? r.sum : '',")

OLD_CALC = """  calc() {
    const rate = { logistik: 1150, produktion: 850, kuehl: 1450, gewerbe: 950 }[this.state.type] || 1000;
    const area = parseFloat(String(this.state.area).replace(/\\./g, '').replace(',', '.')) || 0;
    const y = parseInt(this.state.year, 10) || 2000;
    const f = Math.max(0.55, 1 - Math.max(0, 2026 - y) * 0.012);
    const v = area * rate * f;
"""
NEW_CALC = """  // Lage-Tabelle: erzeugt mit tools/lageregionen.py (PLZ-Daten: GeoNames, CC BY 4.0)
  MARKETS = %s;
  PLZ = '%s';
  ORTE = %s;
  region(input) {
    const q = String(input || '').toLowerCase().replace(/\\s+/g, ' ').trim();
    if (!q) return null;
    const m = q.match(/\\b\\d{5}\\b/);
    if (m) {
      let code = '';
      for (const run of this.PLZ.split(',')) { if (run.slice(0, 5) <= m[0]) code = run.slice(5); else break; }
      return code || '';
    }
    if (!this.orte) { this.orte = {}; for (const c in this.ORTE) this.ORTE[c].split('|').forEach(n => { this.orte[n] = c; }); }
    const name = q.replace(/[,;].*$/, '').trim();
    return this.orte[name] || this.orte[name.split(/ \\(| am | an der | im | in | bei /)[0]] || '';
  }
  calc() {
    const rate = { logistik: 1150, produktion: 850, kuehl: 1450, gewerbe: 950 }[this.state.type] || 1000;
    const area = parseFloat(String(this.state.area).replace(/\\./g, '').replace(',', '.')) || 0;
    const y = parseInt(this.state.year, 10) || 2000;
    const age = Math.max(0, new Date().getFullYear() - y);
    const awm = Math.min(0.45, age * 0.012);
    const bau = area * rate, abzug = bau * awm;
    const code = this.region(this.state.loc);
    const reg = code ? code[0] : '';
    const lf = { A: 0.1, B: 0, C: -0.1, D: -0.2 }[reg] || 0;
    const lage = (bau - abzug) * lf;
    const v = bau - abzug + lage;
    const num = (n, d) => n.toLocaleString('de-DE', { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 });
    const pct = (p, d) => (p > 0 ? '+' : p < 0 ? '−' : '±') + num(Math.abs(p) * 100, d) + ' %%';
    const market = code ? this.MARKETS[parseInt(code[1], 36)] : '';
    const where = { A: 'Kernmarkt ' + market, B: 'Umland ' + market, C: 'erweitertes Umland ' + market, D: 'abseits der Kernmärkte' }[reg];
    const locText = reg ? 'Region ' + reg + ' · ' + where + ' · ' + pct(lf)
      : (code === null ? 'Kein Standort angegeben' : 'Standort nicht erkannt, bitte PLZ eingeben') + ' · ohne Lageanpassung';
"""
rep(OLD_CALC, NEW_CALC % (json.dumps(lage["markets"], ensure_ascii=False), lage["plz"], json.dumps(lage["orte"], ensure_ascii=False)))
rep("    return { total: fmt(v), range: fmt(v * 0.88) + ' – ' + fmt(v * 1.12) };",
    "    return { total: fmt(v), range: fmt(v * 0.88) + ' – ' + fmt(v * 1.12),\n"
    "      bau: num(area) + ' m² × ' + num(rate) + ' €/m²', bauVal: fmt(bau),\n"
    "      age: age + (age === 1 ? ' Jahr' : ' Jahre') + ' × 1,2 %' + (age * 0.012 > 0.45 ? ', max. −45 %' : ' = ' + pct(-awm, 1)), ageVal: '− ' + fmt(abzug),\n"
    "      loc: locText, locVal: lage ? (lage > 0 ? '+ ' : '− ') + fmt(Math.abs(lage)) : '± € 0',\n"
    "      sum: 'Baukosten − Alterswertminderung ± Lage' };")
open(path, "w", encoding="utf-8").write(s)
print("ok", len(s))
