# MOGMAX — Shared core
# Characters, sprite transforms, game/persistent state, the background
# helper, and the splashscreen — everything recycled across every chapter.
# Per-chapter content lives in chapter1.rpy, chapter2.rpy, etc.

# ─── Characters (used across the whole game) ─────────────────
define narrator = Character(None, what_italic=True, what_color="#a0a0a0")
define p = Character("[povname]", color="#88ff88")
define c = Character("Clav", color="#9aa8ff")
define stranger = Character("???", color="#9aa8ff")
define m = Character("Maddie", color="#ffb3d1")
define b = Character("Brayden", color="#7ab8ff")
define h = Character("Mr. Harker", color="#c0c0c0")

# ─── Character sprite transforms ─────────────────────────────
transform harker_body:
    zoom 0.50
    xalign 0.7
    yalign 1.0


transform clav_chest:
    zoom 2.0
    xalign 0.5
    yalign 0.45

transform clav_body:
    zoom 0.78
    xalign 0.7
    yalign 1.0

# ─── Game state (per save) ───────────────────────────────────
default povname = "You"
default aura = 50
default mogged_count = 0
default took_chad_pill = False

# ─── Persistent state (across all saves / sessions) ──────────
default persistent.chapter1_complete = False
default persistent.chapter2_complete = False


# Migrate older persistent-flag names from earlier dev iterations,
# so progress isn't lost when the spec renamed them.
init python:
    if getattr(persistent, "completed_ch1", False) and not persistent.chapter1_complete:
        persistent.chapter1_complete = True
    if getattr(persistent, "completed_ch2", False) and not persistent.chapter2_complete:
        persistent.chapter2_complete = True

# ─── Background helper ────────────────────────────────────────
# Scales any image to fill the screen (1280×720) and crops aspect
# overflow so nothing is stretched. Source images can be any size.
init python:
    def bg_image(path):
        return Transform(path, xysize=(config.screen_width, config.screen_height), fit="cover")

# ─── Base background (chapter-specific bgs live in their files) ───
image bg black = "#000000"


# ═════════════════════════════════════════════════════════════
# SPLASHSCREEN — Studio title + game logo before the main menu.
# Runs once per launch, then control returns to the main menu.
# ═════════════════════════════════════════════════════════════

label splashscreen:
    scene black
    pause 0.3
    show text "{size=24}{color=#888888}a Tarzerk & Cebolla production{/color}{/size}" at truecenter with dissolve
    pause 1.8
    hide text with dissolve
    pause 0.5
    show text "{size=110}{color=#ffffff}MOGMAX{/color}{/size}" at truecenter with dissolve
    pause 1.6
    hide text with dissolve
    pause 0.5
    return
