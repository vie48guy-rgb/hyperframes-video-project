# Finales Talking-Head-Video

Die fertige MP4 liegt unter `../exports/talking-head-recut.mp4` auf dem Branch `video-export`.

Die editierbare Komposition in `index.html` enthält deutsche Karaoke-Untertitel in lokal eingebundener Playfair Display. Das aktive Wort bekommt exakt von Wortstart bis Wortende das dezente blaue Feld `#365D7D`; der übrige Text ist weiß mit feinem dunklem Schatten. Die komplette Untertitelgruppe liegt zur besseren Lesbarkeit auf einem dunklen, leicht transparenten Hintergrund. Die Zooms fahren mit `sine.inOut` über jeweils 1,3 Sekunden zwischen 100 % und 112 % und halten dazwischen ihre Position.

`color-correction.json` enthält die exakte natürliche Aufhellung: eine glatte Kurve für Schatten/Mitteltöne mit geschütztem Weißpunkt und 2,5 % zusätzlicher Sättigung. `prepare_media.py` berechnet die Korrektur vorab in das Material, damit HyperFrames auch ohne Hardware-GPU zügig rendert. Diese globale Tonwertkorrektur hebt auch Schatten im Gesicht an; sie glättet oder maskiert keine Haut.

## Reproduzieren

Benötigt werden die ursprüngliche Aufnahme, Python 3, Node.js >=22, FFmpeg und ein Chromium-Browser. Die Originalaufnahme und generierte Medien sind nicht im Git-Repository enthalten. Die ursprüngliche Datei stammt aus dem vom Nutzer bereitgestellten Google-Drive-Link mit Datei-ID `1uePbOD0Lg-LR1yj4at7l0BCAHwOXWsQU`.

```bash
cd hyperframes
python prepare_media.py /pfad/zur/original.mp4
npm run check
npm run render
```

In der vorbereiteten Codex-Cloud-Umgebung kann alternativ die installierte HyperFrames-CLI verwendet werden:

```bash
export PATH=/workspace/.tools/hyperframes/node_modules/.bin:$PATH
export npm_config_cache=/workspace/.cache/npm
export DO_NOT_TRACK=1
export HYPERFRAMES_BROWSER_PATH=/usr/bin/chromium
export XDG_STATE_HOME=/workspace/.cache/state
hyperframes check . --samples 15
hyperframes render . --quality standard --fps 30 --workers 3
```

`edit-plan.json` bewahrt die Schnitt- und Zoomzeiten, `transcript.json` die Wortzeiten der gekürzten Fassung, `karaoke-words.json` die tatsächlich animierten Wörter. Alle Schriften und GSAP sind lokal eingebunden. Die Korrekturdatei lässt sich ändern und anschließend mit `prepare_media.py` neu berechnen. Die Untertitel und ihre Wort-Hintergründe werden direkt über die registrierte GSAP-Timeline animiert; CSS-Transitions mit einer unabhängigen Echtzeituhr werden nicht verwendet.

## Weiche Textfelder und Bildkarten

Die oberen Textfelder verwenden dasselbe Blau `#365D7D` wie das Karaoke-Wort. Sie blenden über bis zu 550 ms mit `sine.inOut` ein und aus; der Übergang kombiniert Deckkraft und eine Unschärfe von 8 auf 0 beziehungsweise 0 auf 8 Pixel. Während der Bildkarten entfallen überlappende obere Textfelder, damit die Grafiken sauber lesbar bleiben.

Die unveränderten Originalbilder sind unter `assets/` eingebunden. Die Challenge erscheint von 110 bis 116 Sekunden, der B1-Kurzcheck von 125 bis 131 Sekunden. Beide haben 700-ms-Ein- und Ausblendungen und stehen vollständig oberhalb der Untertitel. `image-cards.json` enthält die Zeitpunkte.

Zum Neubauen der HTML-Komposition nach Änderungen an der Konfiguration:

```bash
python build_composition.py
npm run check
npm run render
```

`--without-cards` erzeugt nur eine Textdesign-Vorschau; die reguläre Generierung verlangt beide Bilddateien.
