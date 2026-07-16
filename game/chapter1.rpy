# MOGMAX — Chapter 1: Chopped
# Characters (narrator, p, c, stranger, b, h) and shared sprite
# transforms / game state are defined in script.rpy.

# ─── Chapter backgrounds ─────────────────────────────────────
image bg cafeteria = bg_image("images/backgrounds/bg_cafeteria.jpg")
image bg cafeteria_clav = bg_image("images/backgrounds/bg_cafeteria.jpg")


# ─── Case-file screen (blue-pill ending coda) ────────────────
# Styled like a printed dossier sliding out of a printer. Click / Enter /
# Space dismisses. Follows the modal full-screen idiom used by fail_screen
# (chapter2.rpy) and credits_screen (credits.rpy).
screen case_file_screen():
    modal True

    add Solid("#000000")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 820
        background Solid("#e8e4d8")
        padding (54, 44)

        vbox:
            spacing 12

            text "GIGAMAXXING RESEARCH DIVISION":
                size 30
                color "#1a1a1a"
                bold True
                xalign 0.5
            text "— CASE FILE —":
                size 22
                color "#444444"
                xalign 0.5

            null height 10
            add Solid("#1a1a1a", xysize=(712, 2))
            null height 10

            text "SUBJECT: [povname]":
                size 24
                color "#1a1a1a"
            text "POTENTIAL ASSESSED: Present":
                size 24
                color "#1a1a1a"
            text "PILL SELECTED: Blue":
                size 24
                color "#1a1a1a"
            text "SANDWICH: Wet. Subject was aware. Proceeded anyway.":
                size 24
                color "#1a1a1a"
            text "RECOMMENDATION: Do not follow up.":
                size 24
                color "#1a1a1a"

            null height 14
            add Solid("#1a1a1a", xysize=(712, 2))
            null height 10

            text "CASE STATUS:  {color=#aa1111}{b}CLOSED{/b}{/color}":
                size 34
                color "#1a1a1a"
                xalign 0.5

    # Dismiss on a left-click anywhere ("mousedown_1" is a direct key binding,
    # so it doesn't depend on a focusable button's hit area) or Enter / Space.
    key "mousedown_1" action Return()
    key "K_RETURN" action Return()
    key "K_SPACE" action Return()


# ═════════════════════════════════════════════════════════════
# CHAPTER 1 — CHOPPED
# ═════════════════════════════════════════════════════════════

label start:
    # Stop the menu theme as Chapter 1 begins — silence through the title
    # card and name prompt, until the cafeteria ambient fades in below.
    stop music fadeout 1.0

    scene bg black with fade
    pause 0.4
    show expression Text("CHAPTER 1 — CHOPPED", style="story_card_text", size=46) as text at truecenter with dissolve
    pause 1.8
    hide text with dissolve

    # Name input — player types their own name. Blank input falls back to "You".
    python:
        _typed_name = renpy.input("What's your name?", default="", length=20).strip()
        povname = _typed_name if _typed_name else "You"

    scene bg cafeteria with fade
    # Cross-fade menu theme into cafeteria ambient, ducked as a background
    # bed (~5 dB under the feature themes) so dialogue reads clearly.
    play music "audio/cafeteria_ambient.mp3" fadeout 1.0 fadein 1.5 volume persistent.vol_bed
    narrator "Your name is [povname]."
    narrator "At least, that's what it says on the detention slip sitting on Mr. Harker's desk — again."
    pause 0.3
    narrator "It's a Tuesday. Or maybe Wednesday."
    narrator "Honestly, you stopped keeping track somewhere around the third time you failed PE."
    pause 0.3
    narrator "You're sitting in the back of the cafeteria, alone, picking at a wet sandwich you found in your own backpack from last week."
    narrator "The expiration date is not something you want to think about."

    # Telltale-style fake-out choice — both branches converge to the same next
    # line. The notify uses the customized screen notify in screens.rpy.
    menu:
        "You should probably actually eat it."
        "Take a bite of the crust.":
            narrator "It tastes like cardboard, but at least it crunches."
        "Take a bite of the soggy middle.":
            narrator "Cold moisture spreads across your tongue. You try very hard not to think about what it is."

    $ renpy.notify("The sandwich will remember that.")

    pause 0.5
    narrator "Across the room, the popular kids are laughing."
    pause 0.3

    show brayden mad at clav_body with dissolve
    b "Eat up, LTN."
    narrator "Brayden doesn't even slow down. A single fry drops onto your tray as he passes — a coin tossed to a beggar."
    hide brayden with dissolve
    narrator "LTN. Low Tier Normie. Bottom of the barrel. Zero aura. The kind of person a room forgets while you're still in it."
    narrator "That's you. That's been you."
    pause 0.3

    narrator "You don't know what the joke is. You never do. You don't have to."
    narrator "But somehow, you're pretty sure it's you."
    pause 0.8

    play sound "audio/tray_slam.mp3" volume persistent.vol_sfx
    narrator "A tray slams on the table across from you."
    narrator "You flinch hard enough to knock your juice box onto the floor."
    pause 0.4

    scene bg cafeteria_clav with fade
    show clav neutral at clav_chest
    stranger "Relax."
    narrator "The voice is calm. Too calm. You look up."
    narrator "A guy sits across from you like he owns the cafeteria."
    narrator "Sharp eyes, clean fit, the kind of posture that makes you suddenly aware of how bad yours is."
    narrator "He looks at you the way a surgeon looks at a problem — like he already knows the solution."
    pause 0.4
    stranger "You're [povname], right?"
    narrator "Not a question, really."
    p "...Yeah?"
    c "I'm Clav."
    show clav smirk at clav_body
    narrator "He leans forward."
    show clav lean at clav_body
    c "And I've been watching you for a while."
    p "That's... kind of creepy."
    narrator "He smirks."
    c "Maybe. But here's the thing, [povname] — I think you're wasting your life."
    pause 0.4
    narrator "He pulls out two pills. One red, one blue."
    narrator "Slides them across the table."
    show clav lean at clav_body
    c "So I'm giving you a choice."

    pause 0.4

    # Pill-bottle SFX fires the moment the choice is presented.
    play sound "audio/pill_pickup.mp3" volume persistent.vol_sfx
    show clav stern at clav_body

    menu:
        "Two pills sit on the table. Clav watches, arms crossed."
        "The red pill — Become a Chad.":
            jump chad_pill_ending
        "The blue pill — Remain an LTN.":
            jump ltn_pill_ending


label chad_pill_ending:
    $ persistent.chapter1_complete = True
    $ took_chad_pill = True
    stop music fadeout 1.5
    play sound "audio/swallow_sfx.mp3" volume persistent.vol_sfx
    narrator "You reach out and take the red pill."
    narrator "Clav nods slowly, like he already knew."
    show clav smile at clav_body
    c "Good."
    c "The work starts now."
    c "And I mean that more literally than you think."
    pause 0.8
    show clav stern at clav_body
    c "Library. After last bell."
    p "...why the library?"
    c "Tomorrow Harker springs a quiz nobody sees coming. You're going to pass it."
    p "How would you even know that—"
    c "Bring nothing but your brain."
    hide clav with dissolve
    narrator "He never answers the question. He just lets it hang there — like he already knows you'll show up anyway."
    pause 1.0
    scene bg black with fade
    pause 0.4
    # Merged chapter: Chopped flows straight into Brainmaxxing — no mid-chapter
    # save prompt here (the real chapter break is after the mirror monologue).
    jump chapter2_start


label ltn_pill_ending:
    $ persistent.chapter1_complete = True
    # No music here — the blue ending plays cold and quiet, then hands off
    # to the silent case-file coda.
    play sound "audio/swallow_sfx.mp3" volume persistent.vol_sfx
    narrator "You reach for the blue pill."
    narrator "You swallow it before you can think about it."
    pause 0.5
    show clav stern at clav_body
    c "...blue."
    c "Of course."
    pause 0.4
    c "Enjoy the sandwich."
    pause 0.4
    hide clav with dissolve
    narrator "Clav stands and walks away. No speech. No goodbye. Just footsteps fading into the cafeteria noise."
    pause 1.0

    # ── CASE FILE CODA ──
    # Cut away from the cafeteria — kill its ambient bed so the research-office
    # coda (case file + Gigachad's desk) plays in clean silence.
    stop music fadeout 2.0
    scene bg black with fade
    pause 0.6
    $ play_sfx("audio/printer.mp3")
    pause 0.8
    call screen case_file_screen
    pause 0.3

    scene bg black
    stranger "So. How was he?"
    pause 0.4
    c "...Blue pill."
    pause 0.5
    stranger "Hm."
    pause 0.6

    scene bg city_view with fade
    show gigachad wall at clav_body with dissolve
    narrator "A figure sits at a massive desk by the window. He sets the report down on a stack of identical files. He does not turn around."
    pause 0.6
    stranger "How shameful."
    pause 1.5

    scene bg black with fade
    pause 0.6
    $ credits_from_chapter = 1
    jump roll_credits
