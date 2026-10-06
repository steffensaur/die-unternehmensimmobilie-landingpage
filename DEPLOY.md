# Deployment — www.die-unternehmensimmobilie.de

Statische Landingpage als Cloudflare Worker (nur Static Assets, kein Skript).

- Worker: `die-unternehmensimmobilie-landingpage` (Cloudflare-Account „247spaces")
- Custom Domain: `www.die-unternehmensimmobilie.de` (siehe `wrangler.jsonc`)
- Inhalt: `public/` (`index.html`, `marktplatz.html`, `robots.txt`, `sitemap.xml`)
- Die Marktplatz-Seite ist unter `/marktplatz` erreichbar; `/marktplatz.html` leitet dorthin.

Die Plattform-App (Worker `sauer-gewerbeimmobilien-os`, Zugang über `/zugang`) läuft
weiter unter `app.`, `marktplatz.` und der Domain ohne www — dort nichts ändern.

## Seite aktualisieren

```bash
npx wrangler deploy
```

Falls Wrangler nicht angemeldet ist: vorher `npx wrangler login`.

## Quelle der Seiten

Export aus `~/Downloads/Die Unternehmensimmobilie Redesign/website/` (gebündelte
Single-File-Exporte). Beim Übernehmen werden Titel/Meta-Tags, `lang="de"` und ein dunkler
Ladehintergrund ergänzt sowie der `componentDidUpdate`-Fehler der Marktplatz-Seite
korrigiert. Ein frischer Export muss erneut so nachbearbeitet werden.

## Offene Punkte

- „Impressum", „Datenschutz", „AGB", „Über uns", „Kontakt" zeigen auf `#`.
- Alle Termin-Buttons zeigen auf den Anker `#termin` (keine Buchungs-URL hinterlegt).
- `die-unternehmensimmobilie.de` (ohne www) zeigt weiter auf die Plattform (`/zugang`).
