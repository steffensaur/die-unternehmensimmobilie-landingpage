# Deployment — www.die-unternehmensimmobilie.de

Statische Landingpage als Cloudflare Worker (Static Assets aus `public/`; `src/index.js` leitet nur
die Domain ohne www per 301 auf `https://www.` um).

- Worker: `die-unternehmensimmobilie-landingpage` (Cloudflare-Account „247spaces")
- Custom Domains: `www.die-unternehmensimmobilie.de` und `die-unternehmensimmobilie.de` (siehe `wrangler.jsonc`)
- `/zugang` auf www leitet auf `https://app.die-unternehmensimmobilie.de/zugang` (`public/_redirects`)
- Inhalt: `public/` (`index.html`, `marktplatz.html`, `robots.txt`, `sitemap.xml`)
- Die Marktplatz-Seite ist unter `/marktplatz` erreichbar; `/marktplatz.html` leitet dorthin.

Die Plattform-App (Worker `sauer-gewerbeimmobilien-os`, Zugang über `/zugang`) läuft
weiter unter `app.` und `marktplatz.` — dort nichts ändern. Die Domain ohne www gehört seit
25.10.2026 zur Landingpage.

## Seite aktualisieren

```bash
npx wrangler deploy
```

Falls Wrangler nicht angemeldet ist: vorher `npx wrangler login`.

## Quelle der Seiten

Export aus `~/Downloads/Die Unternehmensimmobilie Redesign/website/` (gebündelte
Single-File-Exporte). Beim Übernehmen werden Titel/Meta-Tags, `lang="de"` und ein dunkler
Ladehintergrund ergänzt sowie der `componentDidUpdate`-Fehler der Marktplatz-Seite
korrigiert. Außerdem müssen Event-Attribute auf normalen HTML-Elementen ohne Bindestrich
stehen (`onpointerdown=`, `onclick=` statt `on-pointer-down=`, `on-click=`), sonst hängt
die Laufzeit sie nicht an (Regler „Zwei Werte", Schritt-Auswahl im Marktplatz). Ein
frischer Export muss erneut so nachbearbeitet werden.

## Ergänzungen gegenüber dem Export (nur in diesem Repo)

- **Schnell-Bewertung mit Herleitung:** Baukosten Neubau (Fläche × €/m² je Objekttyp),
  Alterswertminderung (1,2 % pro Jahr, max. 45 %), Lage-Zu-/Abschlag nach Region A–D.
  Region = Entfernung zum nächsten Logistik-Kernmarkt (A bis 30 km +10 %, B bis 70 km ±0 %,
  C bis 120 km −10 %, D darüber −20 %). Kernmärkte und Ringe stehen in
  `tools/lageregionen.py`; das Skript erzeugt `tools/lage.json`, `tools/patch_kurzbewertung.py`
  baut sie in die Seite ein. PLZ-Daten: GeoNames (https://www.geonames.org, CC BY 4.0).
- **Regler „Zwei Werte":** Werttreiber-Labels (`tools/patch_regler_labels.py`), feste Höhe
  statt `aspect-ratio` + `min-height` (machte die Seite auf dem Handy überbreit).
- **24/7 Spaces:** Header-Hinweis „Ein Service von 24/7 Spaces" und Gruppen-Footer mit den
  Services UI / WH / LAB auf beiden Seiten (`tools/patch_247spaces.py`, Logo in `tools/assets/`).
  24/7 Warehouse und 24/7 Lab sind noch nicht verlinkt (keine öffentliche Zielseite).

## Offene Punkte

- „Impressum", „Datenschutz", „AGB", „Über uns", „Kontakt" zeigen auf `#`.
- Alle Termin-Buttons zeigen auf den Anker `#termin` (keine Buchungs-URL hinterlegt).
