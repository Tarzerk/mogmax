# MOGMAX — GTA-style loading screens
# Shown before a chapter is "laid" — i.e. when starting a New Game or
# Continuing a save. Two display modes:
#
#   "parallax" — GTA-IV style. A character cutout and the background scroll
#                slowly in OPPOSITE directions (char drifts right, bg drifts
#                left) with a touch of zoom, giving a fake-3D depth push.
#                Built from in-game sprites + bgs, so you can author new ones
#                with just art that already exists.
#
#   "stills"   — single full-screen images from images/loadscreens/.
#
# Flip LS_MODE below to switch. Three screens × (FADE + HOLD) ≈ 15s total.
#
# Music is deliberately left UNTOUCHED here: whatever bed is already playing
# (the main-menu theme on a fresh start, or the save's restored music on a
# continue) keeps going underneath until the chapter itself swaps it.
#
# Everything is drawn on a dedicated "loadscreen" layer that sits on top of
# everything, so showing/clearing it never disturbs the scene the engine
# restored from a loaded save — when the layer clears, the player drops right
# back into wherever they were.

define LS_MODE = "parallax"          # "parallax" or "stills"

# Put a fresh top layer above the defaults (master/transient/screens/overlay).
init -10 python:
    if "loadscreen" not in config.layers:
        config.layers = config.layers + ["loadscreen"]

init python:
    # Per-screen on-screen time and the cross-fade length between them.
    LOAD_SCREEN_COUNT = 3
    LOAD_SCREEN_HOLD = 4.0
    LOAD_SCREEN_FADE = 1.0

    # ── "stills" mode pool ──────────────────────────────────────
    # Every GTA still in images/loadscreens/. Only loadable paths are used,
    # so a missing file never crashes the sequence.
    LOAD_SCREENS = [
        "images/loadscreens/JamaicanPosse-GTAIV-EntryScreen.png",
        "images/loadscreens/LCPD-GTAIV-EntryScreen.png",
        "images/loadscreens/NikoHelicopter-GTAIV-EntryScreen.png",
        "images/loadscreens/NikoHidden-GTAIV-EntryScreen.png",
        "images/loadscreens/Prostitute-GTAIV-EntryScreen.png",
        "images/loadscreens/NikoChased-GTAIV-EntryScreen.png",
    ]

    # ── "parallax" mode pool ────────────────────────────────────
    # Each entry = a background + a character cutout + which side the
    # character stands on ("right" or "left"; the bg drifts the other way).
    # To author a new one, just add a dict — any existing bg image path and
    # any defined character image name works.
    LS_PARALLAX = [
        {"bg": "images/bg_cafeteria.jpg", "char": "clav neutral",  "side": "right"},
        {"bg": "images/bg_cafeteria.jpg", "char": "clav smirk",    "side": "left"},
        {"bg": "images/bg_cafeteria.jpg", "char": "clav thinking", "side": "right"},
        {"bg": "images/bg_cafeteria.jpg", "char": "clav lean",     "side": "left"},
    ]


# ─── Parallax drift transforms ───────────────────────────────
# Duration runs a bit longer than (FADE + HOLD) so the motion never visibly
# halts before the cross-fade. `ease` gives a slow-in/slow-out GTA feel and
# subpixel keeps the slow pan smooth. Bg is zoomed past 1.0 so the pan never
# exposes an edge.

# Character on the RIGHT: bg eases left, character eases right.
transform ls_bg_left:
    subpixel True
    align (0.5, 0.5)
    zoom 1.16 xoffset 26
    ease 6.5 zoom 1.21 xoffset -26

transform ls_char_right:
    subpixel True
    xalign 0.72 yalign 1.0
    zoom 0.88 xoffset -20
    ease 6.5 zoom 0.90 xoffset 20

# Character on the LEFT (mirror): bg eases right, character eases left.
transform ls_bg_right:
    subpixel True
    align (0.5, 0.5)
    zoom 1.16 xoffset -26
    ease 6.5 zoom 1.21 xoffset 26

transform ls_char_left:
    subpixel True
    xalign 0.28 yalign 1.0
    zoom 0.88 xoffset 20
    ease 6.5 zoom 0.90 xoffset -20


# ─── Fake loading bar (test scaffolding) ─────────────────────
# Cosmetic only — it fills smoothly across the whole sequence and is NOT tied
# to any real asset loading. Here so the test reads like a real loading screen;
# a real implementation can drive it from actual load progress or keep it fake.
screen ls_loading_bar(total):
    zorder 300
    vbox:
        xalign 0.5
        yalign 0.90
        spacing 8
        text "LOADING":
            size 20
            color "#ffffff"
            outlines [(2, "#000000", 0, 0)]
        frame:
            xsize 720
            ysize 22
            background Solid("#000000bb")
            padding (4, 4)
            bar:
                value AnimatedValue(100.0, 100.0, delay=total, old_value=0.0)
                xsize 712
                ysize 14
                left_bar Solid("#ffaa22")
                right_bar Solid("#33333366")
                thumb None


# Shows LOAD_SCREEN_COUNT screens, cross-fading, then clears the layer and
# returns. Call this (don't jump) so control comes back to the caller.
label loading_screens:
    python:
        import random
        _fade = Dissolve(LOAD_SCREEN_FADE)

        # Fake progress bar across the full sequence (test scaffolding).
        _total = LOAD_SCREEN_COUNT * (LOAD_SCREEN_FADE + LOAD_SCREEN_HOLD)
        renpy.show_screen("ls_loading_bar", _total, _layer="loadscreen")

        if LS_MODE == "parallax":
            _pool = [c for c in LS_PARALLAX
                     if renpy.loader.loadable(c["bg"])
                     and renpy.loader.loadable("images/%s.png" % c["char"])]
            random.shuffle(_pool)
            _picks = _pool[:LOAD_SCREEN_COUNT] if _pool else []

            for _cfg in _picks:
                _right = _cfg.get("side", "right") == "right"
                _bg_t = ls_bg_left if _right else ls_bg_right
                _ch_t = ls_char_right if _right else ls_char_left
                # Same tags every loop, so with_statement cross-dissolves the
                # previous screen into the next. Each show restarts the drift.
                renpy.show("ls_back", what=Solid("#000000"), layer="loadscreen", zorder=0)
                renpy.show("ls_bg",   what=bg_image(_cfg["bg"]), at_list=[_bg_t], layer="loadscreen", zorder=1)
                renpy.show("ls_char", what=renpy.displayable(_cfg["char"]), at_list=[_ch_t], layer="loadscreen", zorder=2)
                renpy.with_statement(_fade)
                renpy.pause(LOAD_SCREEN_HOLD, hard=True)

        else:  # "stills"
            _avail = [p for p in LOAD_SCREENS if renpy.loader.loadable(p)]
            if len(_avail) >= LOAD_SCREEN_COUNT:
                _picks = random.sample(_avail, LOAD_SCREEN_COUNT)
            else:
                _picks = [(_avail * LOAD_SCREEN_COUNT)[i] for i in range(LOAD_SCREEN_COUNT)] if _avail else []

            for _p in _picks:
                renpy.show("ls_back", what=Solid("#000000"), layer="loadscreen", zorder=0)
                renpy.show("ls_bg",   what=bg_image(_p), layer="loadscreen", zorder=1)
                renpy.with_statement(_fade)
                renpy.pause(LOAD_SCREEN_HOLD, hard=True)

        # Fade the loadscreen layer back out, revealing whatever is underneath
        # (black on a new game; the restored save scene on a continue).
        renpy.hide_screen("ls_loading_bar", layer="loadscreen")
        renpy.scene(layer="loadscreen")
        renpy.with_statement(_fade)
    return


# ─── Continue hook ───────────────────────────────────────────
# Ren'Py runs `after_load` every time a save is loaded, so this covers the
# main-menu "Continue" button (and any in-game load). The New Game path is
# handled separately at the top of `label start` in chapter1.rpy.
label after_load:
    call loading_screens
    return
