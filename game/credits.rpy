# MOGMAX — Credits Roll
# Screen-based scrolling credits with a visible skip button.
# Reads game/bee_movie.txt for bonus filler material.

init python:
    def _load_bee_movie_text():
        try:
            f = renpy.file("bee_movie.txt")
            try:
                data = f.read()
            finally:
                f.close()
            if isinstance(data, bytes):
                data = data.decode("utf-8", errors="replace")
            # Escape Ren'Py text-tag special chars so the script renders plain.
            data = data.replace("{", "{{").replace("[", "[[")
            return data
        except Exception as ex:
            return "(bee_movie.txt missing: " + str(ex) + ")"

    _BEE_TEXT = _load_bee_movie_text()

    _CREDITS_BODY = (
        "\n\n\n\n\n\n"
        "{size=90}MOGMAX{/size}\n"
        "\n\n"
        "{size=36}Chapter 1 — Chopped{/size}\n"
        "{size=36}Chapter 2 — Brainmaxxing{/size}\n"
        "\n\n\n\n\n"
        "{size=44}Developed by{/size}\n"
        "\n"
        "{size=72}{color=#9aa8ff}Tarzerk{/color}{/size}\n"
        "{size=36}&{/size}\n"
        "{size=72}{color=#ffb3d1}Cebolla{/color}{/size}\n"
        "\n\n\n\n\n\n"

        # ── Cast ──
        "{size=44}Cast{/size}\n"
        "\n\n"
        "{size=30}{color=#9aa8ff}Clav{/color}{/size}\n"
        "{size=20}{color=#888888}the Giga Mentor{/color}{/size}\n"
        "\n"
        "{size=30}{color=#7ab8ff}Brayden{/color}{/size}\n"
        "{size=20}{color=#888888}the Annoying Guy{/color}{/size}\n"
        "\n"
        "{size=30}{color=#ffb3d1}Maddie{/color}{/size}\n"
        "{size=20}{color=#888888}the Crush{/color}{/size}\n"
        "\n"
        "{size=30}{color=#c0c0c0}Mr. Harker{/color}{/size}\n"
        "{size=20}{color=#888888}the Vocab Enforcer{/color}{/size}\n"
        "\n"
        "{size=30}{color=#88ff88}You{/color}{/size}\n"
        "{size=20}{color=#888888}Future Brainmogger{/color}{/size}\n"
        "\n\n\n\n\n\n"

        # ── Thank you (moved BEFORE the bee movie script) ──
        "{size=44}Thank you for playing.{/size}\n"
        "\n"
        "{size=30}{color=#9aa8ff}Stay sigma.{/color}{/size}\n"
        "\n\n\n\n\n\n"

        # ── Bonus material ──
        "{size=32}— bonus material —{/size}\n"
        "{size=22}the Bee Movie (Dreamworks, 2007){/size}\n"
        "\n\n\n"
        + _BEE_TEXT +
        "\n\n\n\n\n"
    )


# Transform that scrolls the credits text from below the screen
# up past the top over 240 seconds.
transform _credits_scroll:
    xanchor 0.5
    xpos 0.5
    yanchor 0.0
    ypos 720
    linear 240.0 ypos -38000


# ─── Credits Screen ──────────────────────────────────────────
# Click anywhere OR the SKIP CREDITS button OR Esc/Enter/Space
# dismisses and returns to the caller (main menu or game).

screen credits_screen():
    modal True

    # Background + invisible "click anywhere to skip" catcher.
    button:
        xfill True
        yfill True
        background Solid("#000000")
        action Return()

    # Scrolling text body
    text _CREDITS_BODY at _credits_scroll:
        size 24
        color "#ffffff"
        text_align 0.5
        xmaximum 1100
        line_leading 2

    # Always-visible SKIP CREDITS button (bottom-center, on top of everything)
    frame:
        xalign 0.5
        yalign 0.93
        background Solid("#1a1a2add")
        padding (32, 14)

        textbutton "[[ SKIP CREDITS ]]":
            action Return()
            text_size 26
            text_color "#dddddd"
            text_hover_color "#88ff88"
            text_idle_color "#dddddd"

    # Keyboard shortcuts
    key "K_ESCAPE" action Return()
    key "K_RETURN" action Return()
    key "K_SPACE" action Return()


# Label so in-game flows can `jump roll_credits` and end up at main menu
# when the screen returns.
label roll_credits:
    call screen credits_screen
    return
