# MOGMAX — Shared core
# Characters, sprite transforms, game/persistent state, the background
# helper, and the splashscreen — everything recycled across every chapter.
# Per-chapter content lives in chapter1.rpy, chapter2.rpy, etc.

# ─── Characters (used across the whole game) ─────────────────
define narrator = Character(None, what_italic=True, what_color="#a0a0a0")
define p = Character("[povname]", color="#88ff88")
define c = Character("Clav", color="#9aa8ff")
define stranger = Character("???", color="#9aa8ff")
define b = Character("Brayden", color="#7ab8ff")
define h = Character("Mr. Harker", color="#c0c0c0")
define eu = Character("Eugene", color="#b5d4a0")
define sol = Character("Soldier", color="#9c8e6a")
define cap = Character("Captain", color="#c9a14a")
# Gigachad never speaks under his own name — his lines come from offscreen
# as the existing "???" stranger Character above.

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
# Set during the story; read by later chapters for branching.
default brayden_threatened = False
default helped_eugene = False

# ─── Persistent state (across all saves / sessions) ──────────
default persistent.chapter1_complete = False
default persistent.chapter2_complete = False
default persistent.chapter3_complete = False

# ─── Audio mix levels (single source of truth) ───────────────
# Every audio file is loudness-normalized to ~-16 LUFS, so these are pure
# mix decisions, not per-file compensation. Stored in persistent so the
# Audio Check panel (main menu, dev) can tune them live and the values stick.
# To change the shipped defaults, edit the numbers below.
init python:
    # Re-applied every launch so these baked baselines are the source of truth
    # (the dev Audio Check panel still tunes live within a session).
    for _vname, _vdefault in (("vol_bed", 0.85), ("vol_music", 1.0),
                              ("vol_sfx", 0.85)):
        setattr(persistent, _vname, _vdefault)


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

    # ─── Placeholder helpers ─────────────────────────────────
    # Art and audio for newer chapters don't all exist yet. These return
    # the real asset when the file is present, otherwise a clearly-labeled
    # stand-in (or a silent no-op for audio) — so missing assets never crash
    # and lint stays clean. When the real file lands in images/ or audio/,
    # the asset auto-upgrades with no script change.

    def sprite_or_placeholder(path, label, w=420, h=620, tint="#1a1a2a"):
        if renpy.loader.loadable(path):
            return path
        return Composite(
            (w, h),
            (0, 0), Solid(tint, xysize=(w, h)),
            (0, 0), Text("[PLACEHOLDER]\n" + label, size=26, color="#cfcfe0",
                         text_align=0.5, xalign=0.5, yalign=0.5, xsize=w,
                         substitute=False),
        )

    def bg_or_placeholder(path, label=None):
        if renpy.loader.loadable(path):
            return bg_image(path)
        text = label or path
        return Composite(
            (config.screen_width, config.screen_height),
            (0, 0), Solid("#101018"),
            (0, 0), Text("[BG PLACEHOLDER]\n" + text, size=40, color="#5b5b78",
                         text_align=0.5, xalign=0.5, yalign=0.5,
                         substitute=False),
        )

    def play_sfx(path, channel="sound"):
        if renpy.loader.loadable(path):
            renpy.play(path, channel=channel)

    def play_music_safe(path, fadein=0.0, fadeout=0.0, **kw):
        if renpy.loader.loadable(path):
            renpy.music.play(path, fadein=fadein, fadeout=fadeout, **kw)

# ─── Base background (chapter-specific bgs live in their files) ───
image bg black = "#000000"

# ─── Placeholder sprites for characters whose art isn't in yet ───
# (Clav and Harker have real PNGs and auto-load from images/.)
image brayden neutral = sprite_or_placeholder("images/brayden neutral.png", "Brayden\nneutral")
image brayden smirk   = sprite_or_placeholder("images/brayden smirk.png",   "Brayden\nsmirk")
image eugene neutral  = sprite_or_placeholder("images/eugene neutral.png",  "Eugene\nneutral")
# Gigachad silhouettes — always back-facing / never turns around.
image gigachad desk = sprite_or_placeholder("images/gigachad desk.png", "GIGACHAD\n(back-facing, desk)", w=520, h=680, tint="#0d0d14")
image gigachad wall = sprite_or_placeholder("images/gigachad wall.png", "GIGACHAD\n(standing, wall)", w=460, h=680, tint="#0d0d14")


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
