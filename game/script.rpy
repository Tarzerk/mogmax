# MOGMAX — Shared core
# Characters, sprite transforms, game/persistent state, the background
# helper, and the splashscreen — everything recycled across every chapter.
# Per-chapter content lives in chapter1.rpy, chapter2.rpy, etc.

# ─── Characters (used across the whole game) ─────────────────
image komic_ctc = Animation(
    "gui/komic/ctc/ctc_1.png", 1.50,
    "gui/komic/ctc/ctc_2.png", 0.02,
    "gui/komic/ctc/ctc_3.png", 0.02,
    "gui/komic/ctc/ctc_4.png", 0.02,
    "gui/komic/ctc/ctc_5.png", 0.20,
    "gui/komic/ctc/ctc_4.png", 0.02,
    "gui/komic/ctc/ctc_3.png", 0.02,
    "gui/komic/ctc/ctc_2.png", 0.02,
    xpos=0.5, ypos=650, xanchor=0.5, yanchor=0.5,
)

init python:
    renpy.music.register_channel("typewriter", mixer="sfx", loop=True)
    renpy.music.register_channel("dialogue_click", mixer="sfx", loop=False)

    def komic_dialogue_sfx(event, **kwargs):
        if event == "show":
            renpy.music.play(
                "audio/typewriter-soft-click.mp3",
                channel="typewriter",
                loop=True,
                relative_volume=0.20,
            )
        elif event == "slow_done":
            renpy.music.stop(channel="typewriter")
        elif event == "end":
            renpy.music.stop(channel="typewriter")
            renpy.music.play(
                "audio/typewriter-soft-click.mp3",
                channel="dialogue_click",
                loop=False,
                relative_volume=0.55,
            )

define narrator = Character(None, what_italic=True, what_color="#e2dde0", callback=komic_dialogue_sfx, ctc="komic_ctc", ctc_position="fixed")
define p = Character("[povname]", color="#88ff88", callback=komic_dialogue_sfx, ctc="komic_ctc", ctc_position="fixed")
define c = Character("Clav", color="#9aa8ff", callback=komic_dialogue_sfx, ctc="komic_ctc", ctc_position="fixed")
define stranger = Character("???", color="#9aa8ff", callback=komic_dialogue_sfx, ctc="komic_ctc", ctc_position="fixed")
define b = Character("Brayden", color="#7ab8ff", callback=komic_dialogue_sfx, ctc="komic_ctc", ctc_position="fixed")
define h = Character("Mr. Harker", color="#c0c0c0", callback=komic_dialogue_sfx, ctc="komic_ctc", ctc_position="fixed")
define eu = Character("Eugene", color="#b5d4a0", callback=komic_dialogue_sfx, ctc="komic_ctc", ctc_position="fixed")
define sol = Character("Soldier", color="#9c8e6a", callback=komic_dialogue_sfx, ctc="komic_ctc", ctc_position="fixed")
define cap = Character("Captain", color="#c9a14a", callback=komic_dialogue_sfx, ctc="komic_ctc", ctc_position="fixed")
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

transform eugene_left:
    zoom 0.39
    xalign 0.23
    yalign 1.0

transform clav_right:
    zoom 0.74
    xalign 0.82
    yalign 1.0


transform gigachad_file:
    zoom 0.50
    xalign 0.5
    yalign 1.0


# Critical decisions distort the story layer while the choice UI stays sharp.
transform critical_choice_world:
    subpixel True
    xalign 0.5
    yalign 0.5
    zoom 1.025
    blur 3.0
    parallel:
        linear 0.07 xoffset -5 yoffset 2
        linear 0.07 xoffset 4 yoffset -3
        linear 0.07 xoffset -3 yoffset -1
        linear 0.07 xoffset 5 yoffset 3
        linear 0.07 xoffset 0 yoffset 0
        repeat
    parallel:
        ease 0.55 blur 5.0
        ease 0.55 blur 2.5
        repeat

transform critical_choice_release:
    subpixel True
    xalign 0.5
    yalign 0.5
    xoffset 0
    yoffset 0
    zoom 1.0
    blur 0.0


transform eugene_mog_impact:
    subpixel True
    xalign 0.5
    yalign 0.5
    zoom 1.015
    xoffset 0
    yoffset 0
    linear 0.04 xoffset -16 yoffset 3
    linear 0.04 xoffset 14 yoffset -5
    linear 0.04 xoffset -11 yoffset -2
    linear 0.05 xoffset 8 yoffset 4
    easeout 0.12 xoffset 0 yoffset 0 zoom 1.0

# Mogbender gate guards — art is a wide sprite on a large mostly
# transparent canvas, so each needs its own zoom/anchor rather than clav_body's.
# The character sits at the canvas centre, so xoffset (not xalign) is what
# actually separates the two figures on screen. Soldier holds the left; the
# captain slides in from the right on "steps forward".
transform soldier_left:
    zoom 0.46
    yalign 1.0
    xalign 0.5
    xoffset -300

transform captain_enter:
    zoom 0.46
    yalign 1.0
    xalign 0.5
    xoffset 780
    ease 0.6 xoffset 300

# ─── Game state (per save) ───────────────────────────────────
default povname = "You"
default aura = 50
default mogged_count = 0
default took_chad_pill = False
# Set during the story; read by later chapters for branching.
default brayden_threatened = False
default helped_eugene = False
# The Eugene choice is now mog-vs-lift (Mogbender). Both outcomes are recorded
# so the finale can read them (2×2 with the final choice).
default mogged_eugene = False
default critical_choice_active = False
default critical_choice_previous_quick_menu = True

# ─── Persistent state (across all saves / sessions) ──────────
default persistent.chapter1_complete = False
default persistent.chapter2_complete = False
# Legacy fields are retained only to migrate progress from the three-chapter
# development build.
default persistent.chapter3_complete = False
default persistent.chapter_numbering_v2 = False

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

    # Secondary looping channel for room-tone / ambience so it can run
    # alongside the music channel independently.
    renpy.music.register_channel("ambient", mixer="music", loop=True)
    renpy.music.register_channel("critical_choice", mixer="sfx", loop=True)

    def start_critical_choice():
        store.critical_choice_active = True
        store.critical_choice_previous_quick_menu = store.quick_menu
        store.quick_menu = False
        renpy.music.play(
            "audio/critical_choice_loop.mp3",
            channel="critical_choice",
            loop=True,
            fadein=0.25,
            relative_volume=persistent.vol_sfx * 0.65,
        )

    def stop_critical_choice():
        store.critical_choice_active = False
        store.quick_menu = store.critical_choice_previous_quick_menu
        renpy.music.stop(channel="critical_choice", fadeout=0.25)


# Migrate progress from the original three-chapter numbering. Old Chapter 2
# (Brainmaxxing) now completes Chapter 1; old Chapter 3 now completes Chapter 2.
init python:
    if not persistent.chapter_numbering_v2:
        _old_ch2_complete = bool(
            persistent.chapter2_complete or
            getattr(persistent, "completed_ch2", False)
        )
        _old_ch3_complete = bool(persistent.chapter3_complete)
        if getattr(persistent, "completed_ch1", False) or _old_ch2_complete:
            persistent.chapter1_complete = True
        persistent.chapter2_complete = _old_ch3_complete
        persistent.chapter_numbering_v2 = True

# ─── Background helper ────────────────────────────────────────
# Scales any image to fill the screen (1280×720) and crops aspect
# overflow so nothing is stretched. Source images can be any size.
init python:
    def bg_image(path):
        return Transform(path, xysize=(config.screen_width, config.screen_height), fit="cover")

# ─── Base background (chapter-specific bgs live in their files) ───
image bg black = "#000000"

# ─── Character sprites ───────────────────────────────────────
# Art lives under images/characters/<name>/. All shipped story sprites are
# referenced directly so a missing release asset is caught during testing.
image brayden neutral = "images/characters/brayden/brayden neutral.png"
image brayden mad     = "images/characters/brayden/brayden mad.png"
image brayden shocked = "images/characters/brayden/brayden shocked.png"
image brayden smirk   = "images/characters/brayden/brayden smirk.png"
image eugene neutral  = "images/characters/eugene/eugene_neutral.png"
image eugene sad      = "images/characters/eugene/eugene_sad.png"
image eugene happy    = "images/characters/eugene/eugene_happy.png"
# Gigachad silhouettes — always back-facing / never turns around.
image gigachad desk = "images/characters/gigachad/gigachad desk.png"
image gigachad wall = "images/characters/gigachad/gigachad wall.png"

# Mogbender gate guards — shown one at a time in the base-entrance scene.
image soldier = "images/characters/soldier/soldier.png"
image captain = "images/characters/captain/captain.png"


# ═════════════════════════════════════════════════════════════
# SPLASHSCREEN — Studio title + game logo before the main menu.
# Runs once per launch, then control returns to the main menu.
# ═════════════════════════════════════════════════════════════

label splashscreen:
    scene black
    pause 0.3
    show expression Text("a Tarzerk & Cebolla production", style="story_card_subtitle") as text at truecenter with dissolve
    pause 1.8
    hide text with dissolve
    pause 0.5
    show expression Text("MOGMAX", style="story_card_logo") as text at truecenter with dissolve
    pause 1.6
    hide text with dissolve
    pause 0.5
    return


# ═════════════════════════════════════════════════════════════
# BETWEEN-CHAPTER SAVE PROMPT
# Called at each chapter boundary so players can drop a clean checkpoint on
# top of the normal autosave. One-click: force_autosave writes to the auto
# page, which the main-menu Continue picks up — so "quit now, resume here"
# always works. Invoked via `call chapter_break("Chapter N complete")`.
# ═════════════════════════════════════════════════════════════

label chapter_break(done="Chapter complete"):
    menu:
        "[done]. Save your game?"

        "Save game":
            $ renpy.force_autosave(take_screenshot=True)
            "Progress saved — you can quit safely, and Continue will resume here."

        "Keep playing":
            pass

    return
