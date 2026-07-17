# Legacy save compatibility for the Chapter 3 -> Chapter 2 rename.
#
# Ren'Py saves can retain scene-list image names. Keep every former `bg ch3_*`
# name registered so those saves restore the same artwork from its new path.
# These are intentionally direct asset mappings rather than old chapter labels.
image bg ch3_bedroom    = bg_image("images/backgrounds/bg_ch2_bedroom.jpg")
image bg ch3_road       = bg_image("images/backgrounds/bg_ch2_road.jpg")
image bg ch3_gate       = bg_image("images/backgrounds/bg_ch2_gate.jpg")
image bg ch3_sign       = bg_image("images/backgrounds/bg_ch2_sign.jpg")
image bg ch3_corridor   = bg_image("images/backgrounds/bg_ch2_corridor.jpg")
image bg ch3_vault      = bg_image("images/backgrounds/bg_ch2_vault.jpg")
image bg ch3_lab        = bg_image("images/backgrounds/bg_ch2_lab.jpg")
image bg ch3_whiteboard = bg_image("images/backgrounds/bg_ch2_whiteboard.jpg")
image bg ch3_filewall   = bg_image("images/backgrounds/bg_ch2_filewall.jpg")
image bg ch3_gym        = bg_image("images/backgrounds/bg_ch2_gym.jpg")
image bg ch3_janitor    = bg_image("images/backgrounds/bg_ch2_janitor.jpg")


# Saves paused in the former travel screen may also retain its screen name.
# Delegate to the current implementation so behavior stays in one place.
screen ch3_travel_bar():
    use ch2_travel_bar
