define config.name = _("MOGMAX")
define config.version = "0.5"
define gui.show_name = True
define gui.about = _("MOGMAX — a satirical visual novel about the Mogging Epidemic of 2026.\n\nDeveloped by Tarzerk and Cebolla.")
define build.name = "MOGMAX"

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
