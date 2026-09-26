"""
Snake Spiel - Einfache Version für Anfänger
=============================================

Dieses Spiel nutzt nur das "turtle"-Modul, das in Python bereits
eingebaut ist. Es muss also NICHTS zusätzlich installiert werden.

Steuerung:
    Pfeiltasten - Schlange bewegen
    Fenster schließen oder Strg+C im Terminal - Spiel beenden

Der Code ist bewusst einfach gehalten, damit man ihn gut verstehen
und danach selbst erweitern kann (z.B. Highscore speichern,
Level, Hindernisse, Geschwindigkeit ändern, ...).
"""

import turtle
import random
import time


# ---------------------------------------------------------
# 1. Grundeinstellungen
# ---------------------------------------------------------

BREITE = 600
HOEHE = 600
SCHRITT = 20          # Wie weit sich die Schlange pro Schritt bewegt
GESCHWINDIGKEIT = 0.1  # Kleinere Zahl = schnelleres Spiel (Wartezeit in Sekunden)

# ---------------------------------------------------------
# 2. Bildschirm (Fenster) einrichten
# ---------------------------------------------------------

fenster = turtle.Screen()
fenster.title("Snake - Anfänger Version")
fenster.bgcolor("black")
fenster.setup(width=BREITE, height=HOEHE)
fenster.tracer(0)  # Automatisches Zeichnen aus -> wir aktualisieren manuell (schneller)

# ---------------------------------------------------------
# 3. Punktestand-Anzeige
# ---------------------------------------------------------

punkte = 0
highscore = 0

anzeige = turtle.Turtle()
anzeige.speed(0)
anzeige.shape("square")
anzeige.color("white")
anzeige.penup()
anzeige.hideturtle()
anzeige.goto(0, HOEHE / 2 - 40)


def anzeige_aktualisieren():
    anzeige.clear()
    text = f"Punkte: {punkte}   Highscore: {highscore}"
    anzeige.write(text, align="center", font=("Courier", 18, "normal"))


anzeige_aktualisieren()

# ---------------------------------------------------------
# 4. Der Kopf der Schlange
# ---------------------------------------------------------

kopf = turtle.Turtle()
kopf.speed(0)
kopf.shape("square")
kopf.color("lime")
kopf.penup()
kopf.goto(0, 0)
kopf.direction = "stop"

# Liste für die Körper-Segmente der Schlange
segmente = []

# ---------------------------------------------------------
# 5. Das Futter (der Apfel)
# ---------------------------------------------------------

futter = turtle.Turtle()
futter.speed(0)
futter.shape("circle")
futter.color("red")
futter.penup()
futter.goto(0, 100)


def futter_neu_platzieren():
    """Setzt das Futter an eine zufällige Position im Spielfeld."""
    x = random.randint(-(BREITE // 2 - SCHRITT), BREITE // 2 - SCHRITT)
    y = random.randint(-(HOEHE // 2 - SCHRITT), HOEHE // 2 - SCHRITT)
    # Auf das Raster runden, damit alles sauber ausgerichtet bleibt
    x = round(x / SCHRITT) * SCHRITT
    y = round(y / SCHRITT) * SCHRITT
    futter.goto(x, y)


# ---------------------------------------------------------
# 6. Steuerung: Richtung ändern
# ---------------------------------------------------------

def gehe_hoch():
    if kopf.direction != "runter":
        kopf.direction = "hoch"


def gehe_runter():
    if kopf.direction != "hoch":
        kopf.direction = "runter"


def gehe_links():
    if kopf.direction != "rechts":
        kopf.direction = "links"


def gehe_rechts():
    if kopf.direction != "links":
        kopf.direction = "rechts"


fenster.listen()
fenster.onkeypress(gehe_hoch, "Up")
fenster.onkeypress(gehe_runter, "Down")
fenster.onkeypress(gehe_links, "Left")
fenster.onkeypress(gehe_rechts, "Right")


# ---------------------------------------------------------
# 7. Bewegung ausführen
# ---------------------------------------------------------

def bewegen():
    if kopf.direction == "hoch":
        kopf.sety(kopf.ycor() + SCHRITT)
    elif kopf.direction == "runter":
        kopf.sety(kopf.ycor() - SCHRITT)
    elif kopf.direction == "links":
        kopf.setx(kopf.xcor() - SCHRITT)
    elif kopf.direction == "rechts":
        kopf.setx(kopf.xcor() + SCHRITT)


# ---------------------------------------------------------
# 8. Hauptspiel-Schleife
# ---------------------------------------------------------

while True:
    fenster.update()  # Zeichnet das aktuelle Bild

    # --- Kollision mit dem Rand prüfen ---
    if (
        kopf.xcor() > BREITE / 2 - SCHRITT
        or kopf.xcor() < -BREITE / 2 + SCHRITT
        or kopf.ycor() > HOEHE / 2 - SCHRITT - 40
        or kopf.ycor() < -HOEHE / 2 + SCHRITT
    ):
        time.sleep(1)
        kopf.goto(0, 0)
        kopf.direction = "stop"

        # Alle Segmente entfernen
        for segment in segmente:
            segment.goto(1000, 1000)
        segmente.clear()

        punkte = 0
        anzeige_aktualisieren()

    # --- Kollision mit dem Futter prüfen ---
    if kopf.distance(futter) < 20:
        futter_neu_platzieren()

        # Neues Segment hinzufügen
        neues_segment = turtle.Turtle()
        neues_segment.speed(0)
        neues_segment.shape("square")
        neues_segment.color("darkgreen")
        neues_segment.penup()
        segmente.append(neues_segment)

        punkte += 10
        if punkte > highscore:
            highscore = punkte
        anzeige_aktualisieren()

    # --- Körper bewegen (von hinten nach vorne) ---
    for index in range(len(segmente) - 1, 0, -1):
        x = segmente[index - 1].xcor()
        y = segmente[index - 1].ycor()
        segmente[index].goto(x, y)

    if len(segmente) > 0:
        segmente[0].goto(kopf.xcor(), kopf.ycor())

    bewegen()

    # --- Kollision mit dem eigenen Körper prüfen ---
    for segment in segmente:
        if segment.distance(kopf) < 20:
            time.sleep(1)
            kopf.goto(0, 0)
            kopf.direction = "stop"

            for seg in segmente:
                seg.goto(1000, 1000)
            segmente.clear()

            punkte = 0
            anzeige_aktualisieren()
            break

    time.sleep(GESCHWINDIGKEIT)

fenster.mainloop()