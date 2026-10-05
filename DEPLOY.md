# Deployment — www.die-unternehmensimmobilie.de

Statische Single-File-Landingpage auf GitHub Pages.

- Repo: https://github.com/steffensaur/die-unternehmensimmobilie-landingpage
- Quelle: Branch `main`, Verzeichnis `/`
- Custom Domain: `www.die-unternehmensimmobilie.de` (Datei `CNAME`)
- Quelle der Seite: Export aus `~/Downloads/Die Unternehmensimmobilie Redesign/website/`
  (`index.html` + `marktplatz.html`, gebündelte Single-File-Exporte). Beim Übernehmen
  werden Titel/Meta-Tags, `lang="de"` und ein dunkler Ladehintergrund ergänzt sowie
  der `componentDidUpdate`-Fehler der Marktplatz-Seite korrigiert.

Die Plattform-App (Next.js auf Cloudflare Workers, Zugang über `/zugang`) bleibt
davon unberührt und läuft weiter unter `app.die-unternehmensimmobilie.de`.
Die Landingpage verlinkt bereits dorthin.

## Seite aktualisieren

```bash
cp /pfad/zur/neuen-version.html index.html
git add index.html && git commit -m "Landingpage aktualisiert" && git push
```

Der Pages-Build startet automatisch und dauert bei ~0,9 MB rund 20 Sekunden.

## DNS (Cloudflare — Zone die-unternehmensimmobilie.de)

Nameserver liegen bei Cloudflare (`elijah`/`rosalyn.ns.cloudflare.com`).
Alle Records für GitHub Pages **ohne Proxy** anlegen (graue Wolke / "DNS only"),
sonst schlägt die Zertifikatsausstellung von GitHub fehl.

| Typ | Name | Wert | Proxy |
|-----|------|------|-------|
| A | @ | 185.199.108.153 | DNS only |
| A | @ | 185.199.109.153 | DNS only |
| A | @ | 185.199.110.153 | DNS only |
| A | @ | 185.199.111.153 | DNS only |
| AAAA | @ | 2606:50c0:8000::153 | DNS only |
| AAAA | @ | 2606:50c0:8001::153 | DNS only |
| AAAA | @ | 2606:50c0:8002::153 | DNS only |
| AAAA | @ | 2606:50c0:8003::153 | DNS only |
| CNAME | www | steffensaur.github.io | DNS only |

Bestehende Records, die bleiben müssen:

- `app` → Cloudflare Workers (Plattform-App) — **unverändert lassen**
- MX `mx00.ionos.de` / `mx01.ionos.de` und SPF-TXT (`include:_spf-eu.ionos.com`) — **unverändert lassen**
- Der bisherige Workers-Route/Record auf `@` und `www` muss entfernt werden,
  damit die A/AAAA-Records greifen.

## HTTPS

Nach DNS-Propagierung stellt GitHub automatisch ein Let's-Encrypt-Zertifikat aus.
Danach HTTPS erzwingen:

```bash
gh api -X PUT repos/steffensaur/die-unternehmensimmobilie-landingpage/pages -F https_enforced=true
```

## Offene Punkte

- **Stand 05.10.2026: DNS ist nicht umgestellt.** `www` und `@` laufen noch über den
  Cloudflare-Proxy auf den Worker der Plattform (307 → `/zugang`). Die Seite aus diesem
  Repo wird erst sichtbar, wenn die DNS-Tabelle oben umgesetzt ist.
- Im Redesign zeigen „Impressum", „Datenschutz", „AGB", „Über uns", „Kontakt" auf `#`,
  und alle Termin-Buttons auf den Anker `#termin` (keine Buchungs-URL hinterlegt).

- Die Footer-Links `/impressum`, `/datenschutz`, `/agb` sind relativ und laufen
  auf GitHub Pages ins Leere (404). Entweder als eigene HTML-Dateien im Repo
  anlegen oder auf bestehende Seiten der Plattform umbiegen.
