# MOGMAX — Chapter 1: Chopped
# Characters (narrator, p, c, stranger, m, b, h) and shared sprite
# transforms / game state are defined in script.rpy.

# ─── Chapter backgrounds ─────────────────────────────────────
image bg cafeteria = bg_image("images/bg_cafeteria.jpg")
image bg cafeteria_clav = bg_image("images/bg_cafeteria.jpg")


# ═════════════════════════════════════════════════════════════
# CHAPTER 1 — CHOPPED
# ═════════════════════════════════════════════════════════════

label start:
    # Stop the menu theme as Chapter 1 begins — silence through the title
    # card and name prompt, until the cafeteria ambient fades in below.
    stop music fadeout 1.0

    scene bg black with fade
    pause 0.4
    show text "{size=54}Chapter 1 — Chopped{/size}" at truecenter with dissolve
    pause 1.8
    hide text with dissolve

    # Name input — player types their own name. Blank input falls back to "You".
    python:
        _typed_name = renpy.input("What's your name?", default="", length=20).strip()
        povname = _typed_name if _typed_name else "You"

    scene bg cafeteria with fade
    # Cross-fade menu theme into cafeteria ambient, ducked as a background
    # bed (~5 dB under the feature themes) so dialogue reads clearly.
    play music "audio/cafeteria_ambient.mp3" fadeout 1.0 fadein 1.5 volume 0.55
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
    narrator "You don't know what the joke is. You never do."
    narrator "But somehow, you're pretty sure it's you."
    pause 0.8

    play sound "audio/tray_slam.mp3"
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
    play sound "audio/pill_pickup.mp3"
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
    play sound "audio/swallow_sfx.mp3"
    narrator "You reach out and take the red pill."
    narrator "Clav nods slowly, like he already knew."
    show clav smile at clav_body
    c "Good."
    c "The work starts now."
    pause 1.2
    scene bg black with fade
    pause 0.4
    jump chapter2_start


label ltn_pill_ending:
    $ persistent.chapter1_complete = True
    # Crossfade from cafeteria ambient into the sad-piano mirror theme,
    # which then rides through the LTN monologue and into the credits.
    play music "audio/mirror_theme.mp3" fadeout 1.5 fadein 2.5
    play sound "audio/swallow_sfx.mp3"
    narrator "You reach for the blue pill."
    narrator "You swallow it before you can think about it."
    pause 0.5
    show clav stern at clav_body
    c "...blue."
    c "Of course."
    pause 0.4
    c "Low Tier Normie. That's what LTN stands for — just so we're clear."
    pause 0.3
    c "You just signed up for a lifetime of wet sandwiches and back-row cafeteria seating."
    c "That's fine. Someone has to."
    pause 0.6
    hide clav
    narrator "Clav sighs, stands up, and walks away without another word."
    pause 0.4
    narrator "The cafeteria carries on around you."
    narrator "Nothing changes."
    pause 1.5
    scene bg black with fade
    pause 0.6
    $ credits_from_chapter = 1
    jump roll_credits
