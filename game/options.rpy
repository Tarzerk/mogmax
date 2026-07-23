define config.name = _("MOGMAX")
define config.version = "2.0"

# Per-user save location. REQUIRED for saves + persistent (progress, chapter
# unlocks, Preferences/volume) to survive across launches in a packaged build —
# without it they fall back into the game tree, which isn't a stable writable
# location inside a distributed .app/.exe. That fallback is the cause of
# "starts fresh every launch / Continue grayed." Do NOT change this string
# after release, or existing players lose access to their saves.
define config.save_directory = "MOGMAX"
define gui.show_name = True
define gui.about = _("MOGMAX — a satirical visual novel about the Mogging Epidemic of 2026.\n\nDeveloped by Tarzerk and Cebolla.")
define build.name = "MOGMAX"

# Match KOMIC's runtime icon setup so macOS uses the MOGMAX artwork when the
# game is launched directly through Ren'Py as well as from a packaged build.
define config.window_icon = "gui/window_icon.png"

# Explicit screen size — default Ren'Py without gui.rpy is 800x600,
# which makes our custom UI lay out incorrectly (buttons off-screen).
define config.screen_width = 1280
define config.screen_height = 720

# Window-close button quits immediately without showing a yesno prompt
# (we don't have a custom yesno_prompt screen and the bare default fails).
define config.quit_action = Quit(confirm=False)

# Auto-play the menu theme while the main menu screen is visible.
define config.main_menu_music = "audio/main_menu_theme.mp3"

# No voice acting — hide the Voice volume slider in Preferences.
define config.has_voice = False

# Channel mixer defaults (the Preferences sliders start here). All audio is
# loudness-normalized to ~-16 LUFS, so the per-cue mix lives in the VOL_*
# values in script.rpy — these sliders default to full so nothing starts
# accidentally quiet.
define config.default_music_volume = 1.0
define config.default_sfx_volume = 1.0
define config.sample_sound = "audio/ui_click.ogg"

# KOMIC supplies separate neutral and pressed cursor artwork. Buttons request
# the "button" cursor through their shared style.
define config.mouse = {
    "default": [("gui/komic/cursor/default.png", 0, 0)],
    "pressed_default": [("gui/komic/cursor/pressed.png", 0, 0)],
    "button": [("gui/komic/cursor/pressed.png", 0, 0)],
    "pressed_button": [("gui/komic/cursor/pressed.png", 0, 0)],
}


# The dev-only Audio Check panel is gated behind config.developer (so it's
# invisible in any built/released game). Belt-and-suspenders: also keep the
# file out of distribution builds entirely.
init python:
    build.classify('game/audio_check.rpy', None)
    build.classify('game/audio_check.rpyc', None)
    build.classify('dist/**', None)

    # The mouse wheel no longer scrolls dialogue back/forward anywhere in the
    # game — advancing is click/keyboard only. (Keyboard rollback and viewport
    # scrolling in menus are unaffected.)
    for _keysym in ("mousedown_4", "mousedown_5"):
        if _keysym in config.keymap.get("rollback", []):
            config.keymap["rollback"].remove(_keysym)
        if _keysym in config.keymap.get("rollforward", []):
            config.keymap["rollforward"].remove(_keysym)
