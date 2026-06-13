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

# Channel mixer defaults. All audio files are loudness-normalized
# (music ~-18 LUFS, SFX peak -1.5 dBFS), so these set the overall mix:
# music sits a touch under the SFX so dialogue/effects read clearly.
# Users can adjust both via the Preferences screen sliders.
define config.default_music_volume = 0.8
define config.default_sfx_volume = 0.75
