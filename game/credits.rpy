# MOGMAX — Credits
# Timed, chapter-specific credit cards. No scrolling and no filler text.

init python:
    _CREDITS_TECH_CARDS = [
        (
            "list",
            _("Engine & Interface"),
            "",
            _("Ren'Py — Tom \"PyTom\" Rothamel\nKOMIC GUI Kit — One Level Studio"),
            4.5,
        ),
    ]

    _CREDITS_CHAPTER_1_ASSETS = [
        (
            "list",
            _("Background Photography"),
            "",
            _("Classroom — Diana ✨ (Pexels)\nBullying photo series — Mikhail Nilov (Pexels)\nHope — Aidan Roof (Pexels)\nHallway — Enrique Silva (Pexels)"),
            5.5,
        ),
        (
            "list",
            _("Background Images"),
            "",
            _("Cafeteria — Archweb\nCity view — 晓春 胡 (Pexels)\nAdditional school and environment images — Pexels contributors"),
            5.0,
        ),
    ]

    _CREDITS_CHAPTER_2_ASSETS = [
        (
            "list",
            _("Background Photography"),
            "",
            _("Bedroom — Edgard Motta (Pexels)\nCorridor — Peter Edlefsen Holmboe\nArea 51 gate — Pete Woodhead (Flickr)\nArea 51 warning sign — X51 (CC BY-SA 3.0)"),
            5.5,
        ),
        (
            "list",
            _("Background Images"),
            "",
            _("Whiteboard — Karolina Grabowska / Kaboompics\nFacility environments — Wikimedia Commons contributors\nDesert and facility images — Pexels contributors"),
            5.0,
        ),
    ]

    _CREDITS_CHAPTER_1_MUSIC = (
        "list",
        _("Featured Music"),
        "",
        _("“Soviet Connection — The Theme from Grand Theft Auto IV” — Michael Hunter\n“Wii Sports Title Theme” — Kazumi Totaka"),
        6.5,
    )

    _CREDITS_CHAPTER_2_MUSIC = (
        "list",
        _("Featured Music"),
        "",
        _("“Scarface (Push It to the Limit)” — Paul Engemann\n“POUND CAKE” — THOT SQUAD"),
        4.5,
    )

    _CREDITS_END_CARDS = [
        ("ending", "", _("Thank you for playing."), _("Stay sigma."), 4.5),
    ]

    def build_credits_cards(from_chapter=0):
        if from_chapter == 1:
            cards = [
                ("role", _("Developed by"), "Tarzerk", "", 3.5),
                ("role", _("Written by"), "Tarzerk", "", 3.5),
                ("role", _("Additional Writing"), "Cebolla", "", 3.5),
                ("role", _("Additional Development"), "Cebolla", "", 3.5),
                _CREDITS_CHAPTER_1_MUSIC,
            ]
            cards.extend(_CREDITS_CHAPTER_1_ASSETS)
        elif from_chapter == 2:
            cards = [
                ("role", _("Developed by"), "Tarzerk", "", 3.5),
                ("role", _("Written by"), "Tarzerk", "", 3.5),
                _CREDITS_CHAPTER_2_MUSIC,
            ]
            cards.extend(_CREDITS_CHAPTER_2_ASSETS)
        else:
            cards = [
                ("role", _("Developed by"), "Tarzerk", "", 3.5),
                ("role", _("Chapter 1 — Written by"), "Tarzerk", "", 3.5),
                ("role", _("Chapter 1 — Additional Writing"), "Cebolla", "", 3.5),
                ("role", _("Chapter 1 — Additional Development"), "Cebolla", "", 3.5),
                ("role", _("Chapter 2 — Written by"), "Tarzerk", "", 3.5),
                _CREDITS_CHAPTER_1_MUSIC,
                _CREDITS_CHAPTER_2_MUSIC,
            ]
            cards.extend(_CREDITS_CHAPTER_1_ASSETS)
            cards.extend(_CREDITS_CHAPTER_2_ASSETS)

        cards.extend(_CREDITS_TECH_CARDS)
        cards.extend(_CREDITS_END_CARDS)
        return cards


# Which chapter the credits were reached from (0 = combined menu credits).
default credits_from_chapter = 0
default credits_continue_to_chapter2 = False
default credits_skip_available = False


transform _credits_card_enter:
    alpha 0.0
    yoffset 10
    ease 0.35 alpha 1.0 yoffset 0


screen credits_skip_overlay():
    zorder 200

    timer 8.0 action SetVariable("credits_skip_available", True)

    if credits_skip_available:
        textbutton _("[[ SKIP CREDITS ]]"):
            action Return("skip")
            xalign 0.96
            yalign 0.94
            text_size 21
            text_color "#aaaaaa"
            text_hover_color "#88ff88"
            text_idle_color "#aaaaaa"


screen credits_card_screen(card):
    modal True

    add Solid("#000000")

    # Click anywhere to advance one card.
    button:
        xfill True
        yfill True
        background None
        action Return("next")

    timer card[4] action Return("next")

    fixed at _credits_card_enter:
        xfill True
        yfill True

        vbox:
            xalign 0.5
            yalign 0.48
            xmaximum 1120
            spacing 20

            if card[0] == "title":
                text card[2]:
                    size 94
                    bold True
                    color "#ffffff"
                    xalign 0.5
                    text_align 0.5

                if card[1]:
                    text card[1]:
                        size 34
                        color "#aeb8b2"
                        xalign 0.5
                        text_align 0.5

            elif card[0] == "role":
                text card[1]:
                    size 38
                    color "#b8b8b8"
                    xalign 0.5
                    text_align 0.5

                text card[2]:
                    size 68
                    bold True
                    color "#ffffff"
                    xalign 0.5
                    text_align 0.5

            elif card[0] == "ending":
                text card[2]:
                    size 52
                    bold True
                    color "#ffffff"
                    xalign 0.5
                    text_align 0.5

                text card[3]:
                    size 34
                    color "#9aa8ff"
                    xalign 0.5
                    text_align 0.5

            else:
                text card[1]:
                    size 40
                    bold True
                    color "#b8b8b8"
                    xalign 0.5
                    text_align 0.5

                text card[3]:
                    size 29
                    color "#ffffff"
                    xalign 0.5
                    text_align 0.5
                    line_spacing 8

    if credits_skip_available:
        key "K_ESCAPE" action Return("skip")
    key "K_RETURN" action Return("next")
    key "K_SPACE" action Return("next")


# Called from chapter endings, the main menu, and developer navigation.
label roll_credits:
    $ _credits_origin = credits_from_chapter
    $ _credits_continue = credits_continue_to_chapter2
    $ _credits_cards = build_credits_cards(credits_from_chapter)
    $ _credits_index = 0
    $ credits_skip_available = False
    show screen credits_skip_overlay

    while _credits_index < len(_credits_cards):
        call screen credits_card_screen(_credits_cards[_credits_index])
        if _return == "skip":
            $ _credits_index = len(_credits_cards)
        else:
            $ _credits_index += 1

    hide screen credits_skip_overlay

    if _credits_origin == 2:
        stop music fadeout 1.0

    # Reset shared state before either returning or continuing the story.
    $ credits_from_chapter = 0
    $ credits_continue_to_chapter2 = False
    $ credits_skip_available = False

    if _credits_continue:
        jump chapter2_start

    return
