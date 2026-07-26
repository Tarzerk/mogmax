# DEV TOOL — Audio level check panel.
# Open from the main menu: "Audio Check" (only shows when config.developer).
# Plays every cue at its real in-game mix level, with live -/+ per category.
# The numbers map to persistent.vol_* (set in script.rpy). Tune, then tell
# me the four values and I'll bake them as the shipped defaults.

init python:
    def _ac_play(path, channel, vol):
        renpy.music.play(path, channel=channel, relative_volume=vol, loop=(channel == "music"))

screen audio_check():
    modal True
    zorder 1500
    add Solid("#000000f5")

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 12

        text _("AUDIO CHECK — keep your system volume fixed") size 30 color "#ffcc66" xalign 0.5
        text _("Click a sound to hear it. −/+ changes that whole category. Stop music before judging SFX.") size 17 color "#999999" xalign 0.5
        null height 6

        # ── BEDS ──
        hbox:
            spacing 8
            text _("BED  [persistent.vol_bed:.2f]") size 22 color "#88ccff" xminimum 180 yalign 0.5
            textbutton _("−") text_size 26 action SetVariable("persistent.vol_bed", max(0.0, round(persistent.vol_bed - 0.05, 2)))
            textbutton _("+") text_size 26 action SetVariable("persistent.vol_bed", min(1.0, round(persistent.vol_bed + 0.05, 2)))
            null width 14
            textbutton _("cafeteria") text_size 18 action Function(_ac_play, "audio/cafeteria_ambient.mp3", "music", persistent.vol_bed)
            textbutton _("library") text_size 18 action Function(_ac_play, "audio/library_ambient.mp3", "music", persistent.vol_bed)
            textbutton _("desert") text_size 18 action Function(_ac_play, "audio/desert_ambient.mp3", "music", persistent.vol_bed)
            textbutton _("base") text_size 18 action Function(_ac_play, "audio/base_ambient.mp3", "music", persistent.vol_bed)

        # ── MUSIC ──
        hbox:
            spacing 8
            text _("MUSIC  [persistent.vol_music:.2f]") size 22 color "#ffaaff" xminimum 180 yalign 0.5
            textbutton _("−") text_size 26 action SetVariable("persistent.vol_music", max(0.0, round(persistent.vol_music - 0.05, 2)))
            textbutton _("+") text_size 26 action SetVariable("persistent.vol_music", min(1.0, round(persistent.vol_music + 0.05, 2)))
            null width 14
            textbutton _("menu") text_size 18 action Function(_ac_play, "audio/main_menu_theme.mp3", "music", persistent.vol_music)
            textbutton _("quiz") text_size 18 action Function(_ac_play, "audio/quiz_tension.mp3", "music", persistent.vol_music)
            textbutton _("mirror") text_size 18 action Function(_ac_play, "audio/mirror_theme.mp3", "music", persistent.vol_music)
            textbutton _("gigachad") text_size 18 action Function(_ac_play, "audio/gigachad_theme.mp3", "music", persistent.vol_music)
            textbutton _("montage") text_size 18 action Function(_ac_play, "audio/training_montage.mp3", "music", persistent.vol_music)

        # ── SFX ──
        hbox:
            spacing 8
            text _("SFX  [persistent.vol_sfx:.2f]") size 22 color "#aaffaa" xminimum 180 yalign 0.5
            textbutton _("−") text_size 26 action SetVariable("persistent.vol_sfx", max(0.0, round(persistent.vol_sfx - 0.05, 2)))
            textbutton _("+") text_size 26 action SetVariable("persistent.vol_sfx", min(1.0, round(persistent.vol_sfx + 0.05, 2)))
            null width 14
            textbutton _("tray") text_size 18 action Function(_ac_play, "audio/tray_slam.mp3", "sound", persistent.vol_sfx)
            textbutton _("pill") text_size 18 action Function(_ac_play, "audio/pill_pickup.mp3", "sound", persistent.vol_sfx)
            textbutton _("swallow") text_size 18 action Function(_ac_play, "audio/swallow_sfx.mp3", "sound", persistent.vol_sfx)
            textbutton _("bell") text_size 18 action Function(_ac_play, "audio/bell_school.mp3", "sound", persistent.vol_sfx)
            textbutton _("honk") text_size 18 action Function(_ac_play, "audio/honk.mp3", "sound", persistent.vol_sfx)
            textbutton _("scan") text_size 18 action Function(_ac_play, "audio/scan.mp3", "sound", persistent.vol_sfx * 0.85)
            textbutton _("buzz") text_size 18 action Function(_ac_play, "audio/text_buzz.mp3", "sound", persistent.vol_sfx)
            textbutton _("buzzer") text_size 18 action Function(_ac_play, "audio/quiz_buzzer.mp3", "sound", persistent.vol_sfx)
            textbutton _("mogging") text_size 18 action Function(_ac_play, "audio/mogging_sfx.mp3", "sound", persistent.vol_sfx)

        hbox:
            spacing 8
            text _("BATTLE CUES") size 18 color "#69e4ad" xminimum 180 yalign 0.5
            textbutton _("block scan") text_size 18 action Function(_ac_play, "audio/battle_block_scan.mp3", "sound", persistent.vol_sfx * 0.8)
            textbutton _("cringe") text_size 18 action Function(_ac_play, "audio/battle_cringe.mp3", "sound", persistent.vol_sfx * 0.9)
            textbutton _("aura beam") text_size 18 action Function(_ac_play, "audio/battle_aura_beam.mp3", "sound", persistent.vol_sfx * 0.85)
            textbutton _("super effective") text_size 18 action Function(_ac_play, "audio/battle_super_effective.mp3", "sound", persistent.vol_sfx * 0.9)
            textbutton _("recharge") text_size 18 action Function(_ac_play, "audio/battle_health_recharge.mp3", "sound", persistent.vol_sfx * 0.85)
            textbutton _("low health") text_size 18 action Function(_ac_play, "audio/battle_low_health.mp3", "sound", persistent.vol_sfx * 0.75)

        hbox:
            spacing 8
            text _("CHOICE CUE") size 18 color "#d9b4ff" xminimum 180 yalign 0.5
            textbutton _("critical loop") text_size 18 action Function(_ac_play, "audio/critical_choice_loop.mp3", "sound", persistent.vol_sfx * 0.65)

        null height 10
        hbox:
            spacing 24
            xalign 0.5
            textbutton _("■ Stop music") text_size 20 action Function(renpy.music.stop, channel="music")
            textbutton _("✕ Close") text_size 20 action Hide("audio_check")
