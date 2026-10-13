# Talking-head recut — Deutsche Untertitel

## Style Prompt
Ein ruhiger, moderner Talking-Head-Schnitt im originalen Hochformat. Die Person und ihre natürliche Gestik stehen im Mittelpunkt. Kurze, gut lesbare deutsche Untertitel auf Höhe des unteren Brustbereichs. Inhaltliche Schlüsselbegriffe erscheinen sparsam als weiße Schrift auf einem dezenten, leicht transparenten dunklen Feld im freien Raum oberhalb des Kopfes. Sanfte digitale Kamerafahrten alternieren zwischen 100 % und 112 %, mit 1,3 Sekunden Dauer und sine.inOut. Keine Musik oder zusätzlichen Szenen.

## Colors
- #FFFFFF: Untertitel mit feinem dunklem Textschatten
- #FAFAF7: Highlight-Text
- #365D7D: dezenter blauer Hintergrund ausschließlich des aktuell gesprochenen Wortes
- #151A20 mit 78 % Deckkraft: Highlight-Feld
- #0A1118: dezenter Textschatten der Untertitel
- #D5DADE: dezenter Rahmen

## Typography
Lokal eingebundene Playfair Display für alle Untertitel, 48 px, Gewicht 600, 1.4 Zeilenhöhe. Die separaten Themen-Highlights bleiben in DejaVu Sans, 50 px fett. Maximal zwei Untertitelzeilen; Highlights auf maximal zwei Zeilen. Das native Bildmaß nach Rotation ist 886 × 1920 px.

## Motion
Untertitel wechseln synchron ohne dekorative Verzögerung. Einzelne Wörter erhalten exakt von Wortstart bis Wortende das dezente blaue Hintergrundfeld. Der übrige Text ist weiß mit feinem Schatten. Highlights erscheinen mit einem kurzen, zurückhaltenden 140-ms-Fade. Zooms fahren mit sine.inOut über 1,3 Sekunden zwischen 100 % und 112 %. Dazwischen hält die Kamera ihre Ansicht für mehrere Sekunden.

## What NOT to Do
- Keine Grafiken oder Texte über dem Gesicht.
- Keine Übersetzung ins Englische.
- Keine künstliche Beschleunigung der Sprache.
- Keine auffälligen Farben, Bounce-Effekte oder Musik.
- Keine Wörter durch aggressive Pausenschnitte abschneiden.

## Farbkorrektur
Natürlich hellere Schatten und Mitteltöne, mit geschütztem Weißpunkt. Gleiche glatte Tonwertkurve für Rot, Grün und Blau: (0, 0.012), (0.10, 0.135), (0.30, 0.345), (0.60, 0.64), (0.82, 0.835), (1, 1). Sättigung 1.025. Keine Hautglättung oder Gesichtsmaske. Die Korrektur wird aus Performancegründen vorab mit FFmpeg in das Material gerechnet. Exakte Filter und Medienpfade stehen in color-correction.json; bake_color.py berechnet das korrigierte Material. Untertitel und Zooms bleiben in HyperFrames editierbar.
