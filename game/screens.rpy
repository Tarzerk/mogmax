################################################################################
## Initialization
################################################################################

init offset = -1


################################################################################
## Styles
################################################################################

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")
    background Frame("gui/komic/button/choice_idle_background.png", Borders(28, 10, 28, 10))
    hover_background Frame("gui/komic/button/choice_hover_background.png", Borders(28, 10, 28, 10))
    selected_background Frame("gui/komic/button/choice_hover_background.png", Borders(28, 10, 28, 10))
    hover_sound "audio/ui_hover.ogg"
    activate_sound "audio/ui_click.ogg"
    mouse "button"

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/komic/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/komic/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/komic/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/komic/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/komic/frame.png", gui.frame_borders, tile=gui.frame_tile)



################################################################################
## In-game screens
################################################################################


## Say screen ##################################################################
##
## The say screen is used to display dialogue to the player. It takes two
## parameters, who and what, which are the name of the speaking character and
## the text to be displayed, respectively. (The who parameter can be None if no
## name is given.)
##
## This screen must create a text displayable with id "what", as Ren'Py uses
## this to manage text display. It can also create displayables with id "who"
## and id "window" to apply style properties.
##
## https://www.renpy.org/doc/html/screen_special.html#say

screen say(who, what):

    window:
        id "window"
        background ("gui/komic/textbox_transparent.png" if cinematic_dialogue else "gui/komic/textbox.png")

        if who is not None:

            window:
                style "namebox"
                text who id "who"

        text what id "what"


    ## If there's a side image, display it above the text. Do not display on the
    ## phone variant - there's no room.
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0


default cinematic_dialogue = False


transform cinematic_top_bar_slide:
    on show:
        yoffset -120
        easeout_cubic 0.5 yoffset 0
    on hide:
        easein_cubic 0.45 yoffset -120


transform cinematic_bottom_bar_slide:
    on show:
        yoffset 253
        easeout_cubic 0.5 yoffset 0
    on hide:
        easein_cubic 0.45 yoffset 253


screen cinematic_bars():
    zorder -5

    if cinematic_dialogue:
        add Solid("#000000"):
            xysize (1280, 120)
            ypos 0
            at cinematic_top_bar_slide

        add Solid("#000000"):
            xysize (1280, 253)
            ypos 467
            at cinematic_bottom_bar_slide


screen cinematic_caption(what, who=None):
    zorder 100

    window:
        style "window"
        background None

        if who is not None:
            window:
                style "namebox"
                text who:
                    style "say_label"

        text what:
            style "say_dialogue"


style story_card_text is default:
    font gui.interface_text_font
    size 36
    color "#dce5e0"
    bold True
    text_align 0.5

style story_card_subtitle is story_card_text:
    size 24
    color "#aeb8b2"
    bold False

style story_card_logo is story_card_text:
    size 110
    color "#ffffff"


init python:
    config.overlay_screens.append("cinematic_bars")

    def set_cinematic_dialogue(enabled):
        renpy.store.cinematic_dialogue = bool(enabled)
        renpy.restart_interaction()


style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background None

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background None
    padding (0, 0, 0, 0)

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos

    adjust_spacing False


## Input screen ################################################################
##
## This screen is used to display renpy.input. The prompt parameter is used to
## pass a text prompt in.
##
## This screen must create an input displayable with id "input" to accept the
## various input parameters.
##
## http://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xanchor gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


## Choice screen ###############################################################
##
## This screen is used to display the in-game choices presented by the menu
## statement. The one parameter, items, is a list of objects, each with caption
## and action fields.
##
## http://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):
    style_prefix "choice"

    if critical_choice_active:
        add Solid("#09070c70")

        hbox:
            xalign 0.5
            yalign 0.62
            spacing 28

            for i in items:
                textbutton i.caption:
                    action i.action
                    style "critical_choice_button"
    else:
        vbox:
            for i in items:
                textbutton i.caption action i.action


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 270
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")
    background Frame("gui/komic/button/choice_idle_background.png", gui.choice_button_borders)
    hover_background Frame("gui/komic/button/choice_hover_background.png", gui.choice_button_borders)
    selected_background Frame("gui/komic/button/choice_hover_background.png", gui.choice_button_borders)
    hover_sound "audio/ui_hover.ogg"
    activate_sound "audio/ui_click.ogg"
    mouse "button"

style choice_button_text is default:
    properties gui.text_properties("choice_button")

style critical_choice_button is choice_button:
    xysize (330, 72)
    padding (20, 12)

style critical_choice_button_text is choice_button_text:
    size 23
    bold True
    xalign 0.5
    yalign 0.5
    text_align 0.5


## Quick Menu screen ###########################################################
##
## The quick menu is displayed in-game to provide easy access to the out-of-game
## menus.

screen quick_menu():

    ## Ensure this appears on top of other screens.
    zorder 100

    if quick_menu:

        hbox:
            xalign 1.0
            yalign 0.0
            spacing -4

            imagebutton:
                auto "gui/komic/quick/skip_%s.png"
                action Skip()
                alternate Skip(fast=True, confirm=True)
                tooltip _("Skip")
                hover_sound "audio/ui_hover.ogg"
                activate_sound "audio/ui_click.ogg"
                mouse "button"

            imagebutton:
                auto "gui/komic/quick/save_%s.png"
                action ShowMenu("save")
                tooltip _("Save")
                hover_sound "audio/ui_hover.ogg"
                activate_sound "audio/ui_click.ogg"
                mouse "button"

            imagebutton:
                auto "gui/komic/quick/load_%s.png"
                action ShowMenu("load")
                tooltip _("Load")
                hover_sound "audio/ui_hover.ogg"
                activate_sound "audio/ui_click.ogg"
                mouse "button"

            imagebutton:
                auto "gui/komic/quick/history_%s.png"
                action ShowMenu("history")
                tooltip _("History")
                hover_sound "audio/ui_hover.ogg"
                activate_sound "audio/ui_click.ogg"
                mouse "button"

            imagebutton:
                auto "gui/komic/quick/options_%s.png"
                action ShowMenu("preferences")
                tooltip _("Preferences")
                hover_sound "audio/ui_hover.ogg"
                activate_sound "audio/ui_click.ogg"
                mouse "button"

        $ quick_tooltip = GetTooltip()
        if quick_tooltip:
            text quick_tooltip:
                xpos 1065
                ypos 70
                xsize 200
                text_align 0.5
                size 13
                color "#ffffff"
                outlines [(2, "#26302b", 0, 0)]


## This code ensures that the quick_menu screen is displayed in-game, whenever
## the player has not explicitly hidden the interface.
init python:
    config.overlay_screens.append("quick_menu")

default quick_menu = True

style quick_button is default
style quick_button_text is button_text

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.text_properties("quick_button")


################################################################################
## Main and Game Menu Screens
################################################################################

## Navigation screen ###########################################################
##
## This screen is included in the main and game menus, and provides navigation
## to other menus, and to start the game.

screen navigation(main_menu_layout=None):

    if main_menu_layout is None:
        $ main_menu_layout = main_menu

    if main_menu_layout:
        $ _newest_slot = renpy.newest_slot(r'auto|quick|\d')

        vbox:
            style_prefix "main_nav"
            xpos 935
            ypos 215
            spacing 7

            if _newest_slot:
                textbutton _("CONTINUE") action FileLoad(_newest_slot, slot=True, confirm=False)
                textbutton _("NEW GAME") action Confirm(_("Start a new game? Your existing saves stay available under Load."), yes=Start())
            else:
                textbutton _("NEW GAME") action Start()

            textbutton _("LOAD GAME") action ShowMenu("load")

            if persistent.chapter1_complete:
                textbutton _("CHAPTER SELECT") action ShowMenu("chapter_select")

            textbutton _("MINIGAMES") action ShowMenu("minigame_select")

            null height 14

            textbutton _("PREFERENCES") action ShowMenu("preferences")
            textbutton _("CREDITS") action Function(renpy.call_in_new_context, "roll_credits")

            if renpy.variant("pc"):
                textbutton _("QUIT") action Quit(confirm=False)

    else:
        vbox:
            style_prefix "navigation"
            xpos gui.navigation_xpos
            yalign 0.5
            spacing gui.navigation_spacing

            textbutton _("History") action ShowMenu("history")
            textbutton _("Save") action ShowMenu("save")
            textbutton _("Load") action ShowMenu("load")
            textbutton _("Preferences") action ShowMenu("preferences")

            if _in_replay:
                textbutton _("End Replay") action EndReplay(confirm=True)
            else:
                textbutton _("Main Menu") action MainMenu()

            textbutton _("About") action ShowMenu("about")

            if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):
                textbutton _("Help") action ShowMenu("help")

            if renpy.variant("pc"):
                textbutton _("Quit") action Quit(confirm=True)


style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")
    xsize 250
    ysize 50
    background Frame("gui/komic/button/choice_idle_background.png", Borders(32, 12, 32, 12))
    hover_background Frame("gui/komic/button/choice_hover_background.png", Borders(32, 12, 32, 12))
    selected_background Frame("gui/komic/button/choice_hover_background.png", Borders(32, 12, 32, 12))
    hover_sound "audio/ui_hover.ogg"
    activate_sound "audio/ui_click.ogg"
    mouse "button"

style navigation_button_text:
    properties gui.text_properties("navigation_button")
    color "#f1f4f2"
    hover_color "#ffffff"
    selected_color "#f2b84b"
    insensitive_color "#7f8983"
    xalign 0.5
    text_align 0.5
    size 20


style main_nav_button is default
style main_nav_button_text is gui_text

style main_nav_button:
    xsize 305
    ysize 44
    padding (18, 0, 18, 0)
    background Solid("#ffffff08")
    hover_background Solid("#79c98b22")
    selected_background Solid("#79c98b22")
    insensitive_background Solid("#ffffff04")
    hover_sound "audio/ui_hover.ogg"
    activate_sound "audio/ui_click.ogg"
    mouse "button"

style main_nav_button_text:
    font gui.interface_text_font
    size 19
    color "#dce5e0"
    hover_color "#79c98b"
    selected_color "#f2b84b"
    insensitive_color "#69716d"
    bold True
    xalign 0.0
    yalign 0.5
    text_align 0.0


## Main Menu screen ############################################################
##
## Used to display the main menu when Ren'Py starts.
##
## http://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu():

    ## This ensures that any other menu screen is replaced.
    tag menu

    style_prefix "main_menu"

    add Transform(gui.main_menu_background, size=(config.screen_width, config.screen_height))

    # A full-height command rail keeps the portrait unobstructed and gives the
    # title and controls one stable alignment edge.
    add Solid("#080c0ae8"):
        xpos 890
        xysize (390, 720)

    add Solid("#79c98b"):
        xpos 890
        xysize (3, 720)

    ## Actual menu contents are in the navigation screen.
    use navigation(main_menu_layout=True)

    if gui.show_name:

        text "[config.name!t]":
            style "main_menu_title"
            xpos 935
            ypos 58

        text _("BASED ON A TRUE STORY"):
            style "main_menu_version"
            xpos 938
            ypos 132

        add Solid("#79c98b"):
            xpos 938
            ypos 174
            xysize (64, 3)

    text "TARZERK + CEBOLLA":
        xpos 938
        ypos 658
        size 13
        color "#aeb8b2"

    text "v[config.version]":
        xalign 1.0
        xoffset -30
        ypos 658
        size 13
        color "#69716d"

    if config.developer:
        key "K_F8" action Show("audio_check")


style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text

style main_menu_vbox:
    xalign 1.0
    xoffset -20
    xsize 960
    yalign 1.0
    yoffset -20

style main_menu_text:
    properties gui.text_properties("main_menu", accent=True)

style main_menu_title:
    font gui.interface_text_font
    size 58
    color "#ffffff"
    bold True

style main_menu_version:
    font gui.interface_text_font
    size 14
    color "#aeb8b2"
    bold True


## Game Menu screen ############################################################
##
## This lays out the basic common structure of a game menu screen. It's called
## with the screen title, and displays the background, title, and navigation.
##
## The scroll parameter can be None, or one of "viewport" or "vpgrid". When
## this screen is intended to be used with one or more children, which are
## transcluded (placed) inside it.

screen game_menu(title, scroll=None, bg=None):

    style_prefix "game_menu"

    if main_menu:
        add Transform(gui.main_menu_background, size=(config.screen_width, config.screen_height))
    elif bg is not None:
        # Custom per-screen background (e.g. the Save/Load gigachad), scaled to
        # fill the screen and darkened so the slot grid stays legible.
        add Transform(bg, xysize=(config.screen_width, config.screen_height), fit="cover")
        add Solid("#000000aa")
    else:
        add gui.game_menu_background

    frame:
        style "game_menu_outer_frame"

        hbox:

            ## Reserve space for the navigation section.
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        vbox:
                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial 1.0

                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        transclude

                else:

                    transclude

    use navigation(main_menu_layout=False)

    textbutton _("Return"):
        style "return_button"

        action Return()

    label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 30
    top_padding 120

    background Solid("#101412cc")

style game_menu_navigation_frame:
    xsize 300
    yfill True

style game_menu_content_frame:
    left_margin 10
    right_margin 20
    top_margin 10
    padding (28, 24, 28, 24)
    background Frame("gui/komic/frame.png", Borders(22, 22, 22, 22))

style game_menu_viewport:
    xsize 865

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 10

style game_menu_label:
    xpos 50
    ysize 120

style game_menu_label_text:
    size gui.title_text_size
    color "#ffffff"
    yalign 0.5
    outlines [(2, "#26302b", 0, 0)]

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -30


## About screen ################################################################
##
## This screen gives credit and copyright information about the game and Ren'Py.
##
## There's nothing special about this screen, and hence it also serves as an
## example of how to make a custom screen.

screen about():

    tag menu

    ## This use statement includes the game_menu screen inside this one. The
    ## vbox child is then included inside the viewport inside the game_menu
    ## screen.
    use game_menu(_("About"), scroll="viewport"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("[config.version!t]\n")

            hbox:
                spacing 15
                text _("Development & Writing") style "about_small"
                text _("Tarzerk & Cebolla")

            null height 15

            hbox:
                spacing 15
                text _("Engine") style "about_small"
                text _("Ren'Py by Tom \"PyTom\" Rothamel")

            hbox:
                spacing 15
                text _("GUI Scaffolding") style "about_small"
                text _("KOMIC by One Level Studio")

            null height 15

            hbox:
                spacing 15
                text _("Bonus Credits") style "about_small"
                text _("the Bee Movie (Dreamworks, 2007)")


            text _("\nMade with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only]")
            null height 15
            text _("[renpy.license!t]") size 20


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size

style about_small:
    size 20
    minwidth 260
    textalign 1.0
    yalign 0.9


## Load and Save screens #######################################################
##
## These screens are responsible for letting the player save the game and load
## it again. Since they share nearly everything in common, both are implemented
## in terms of a third screen, file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save https://
## www.renpy.org/doc/html/screen_special.html#load

screen save():

    tag menu

    use file_slots(_("Save"))


screen load():

    tag menu

    use file_slots(_("Load"))


screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))

    use game_menu(title, bg="gui/gigachad.jpg"):

        fixed:

            ## This ensures the input will get the enter event before any of the
            ## buttons do.
            order_reverse True

            ## The page name, which can be edited by clicking on a button.
            button:
                style "page_label"

                key_events True
                xalign 0.5
                action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value

            ## The grid of file slots.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action FileAction(slot)

                        has vbox

                        add FileScreenshot(slot) xalign 0.5

                        text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)

            ## Buttons to access other pages.
            hbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                spacing gui.page_spacing

                textbutton _("<") action FilePagePrevious()
                key "save_page_prev" action FilePagePrevious()

                if config.has_autosave:
                    textbutton _("{#auto_page}A") action FilePage("auto")

                if config.has_quicksave:
                    textbutton _("{#quick_page}Q") action FilePage("quick")

                ## range(1, 10) gives the numbers from 1 to 9.
                for page in range(1, 10):
                    textbutton "[page]" action FilePage(page)

                textbutton _(">") action FilePageNext()
                key "save_page_next" action FilePageNext()


style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    xpadding 50
    ypadding 3

style page_label_text:
    textalign 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.text_properties("page_button")

style slot_button:
    properties gui.button_properties("slot_button")
    background "gui/komic/button/slot_idle_background.png"
    hover_background "gui/komic/button/slot_hover_background.png"
    selected_background "gui/komic/button/slot_hover_background.png"
    hover_sound "audio/ui_hover.ogg"
    activate_sound "audio/ui_click.ogg"
    mouse "button"

style slot_button_text:
    properties gui.text_properties("slot_button")
    color "#ffffff"
    hover_color "#79c98b"


## Preferences screen ##########################################################
##
## The preferences screen allows the player to configure the game to better suit
## themselves.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

screen preferences():

    tag menu

    if renpy.mobile:
        $ cols = 2
    else:
        $ cols = 4

    use game_menu(_("Preferences"), scroll="viewport"):

        vbox:

            hbox:
                box_wrap True

                if renpy.variant("pc") or renpy.variant("web"):

                    vbox:
                        style_prefix "radio"
                        label _("Display")
                        textbutton _("Window") action Preference("display", "window")
                        textbutton _("Fullscreen") action Preference("display", "fullscreen")

                vbox:
                    style_prefix "check"
                    label _("Skip")
                    textbutton _("Unseen Text") action Preference("skip", "toggle")
                    textbutton _("After Choices") action Preference("after choices", "toggle")
                    textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle"))

                ## Additional vboxes of type "radio_pref" or "check_pref" can be
                ## added here, to add additional creator-defined preferences.

#begin language_picker

                vbox:
                    style_prefix "radio"
                    label _("Language")

                    textbutton "English" text_font "DejaVuSans.ttf" action Language(None)
                    textbutton "Česky" text_font "DejaVuSans.ttf" action Language("czech")
                    textbutton "Dansk" text_font "DejaVuSans.ttf" action Language("danish")
                    textbutton "Français" text_font "DejaVuSans.ttf" action Language("french")
                    textbutton "Italiano" text_font "DejaVuSans.ttf" action Language("italian")
                    textbutton "Bahasa Melayu" text_font "DejaVuSans.ttf" action Language("malay")
                    textbutton "Русский" text_font "DejaVuSans.ttf" action Language("russian")

                vbox:
                    style_prefix "radio"
                    label _(" ")

                    textbutton "Español" text_font "DejaVuSans.ttf" action Language("spanish")
                    textbutton "Українська" text_font "DejaVuSans.ttf" action Language("ukrainian")
                    # CJK language buttons removed — SourceHanSansLite.ttf isn't bundled.

#end language_picker

            null height (4 * gui.pref_spacing)

            hbox:
                style_prefix "slider"
                box_wrap True

                vbox:

                    label _("Text Speed")

                    bar value Preference("text speed")

                    label _("Auto-Forward Time")

                    bar value Preference("auto-forward time")

                vbox:

                    if config.has_music:
                        label _("Music Volume")

                        hbox:
                            bar value Preference("music volume")

                    if config.has_sound:

                        label _("Sound Volume")

                        hbox:
                            bar value Preference("sound volume")

                            if config.sample_sound:
                                textbutton _("Test") action Play("sound", config.sample_sound)


                    if config.has_voice:
                        label _("Voice Volume")

                        hbox:
                            bar value Preference("voice volume")

                            if config.sample_voice:
                                textbutton _("Test") action Play("voice", config.sample_voice)

                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing

                        textbutton _("Mute All"):
                            action Preference("all mute", "toggle")
                            style "mute_all_button"


style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 2

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize 225

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/komic/button/radio_[prefix_]foreground.png"

style radio_button_text:
    properties gui.text_properties("radio_button")

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/komic/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.text_properties("check_button")

style slider_slider:
    xsize 350

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 10

style slider_button_text:
    properties gui.text_properties("slider_button")

style slider_vbox:
    xsize 450


## History screen ##############################################################
##
## This is a screen that displays the dialogue history to the player. While
## there isn't anything special about this screen, it does have to access the
## dialogue history stored in _history_list.
##
## https://www.renpy.org/doc/html/history.html

screen history():

    tag menu

    ## Avoid predicting this screen, as it can be very large.
    predict False

    use game_menu(_("History"), scroll=("vpgrid" if gui.history_height else "viewport")):

        style_prefix "history"

        for h in _history_list:

            window:

                ## This lays things out properly if history_height is None.
                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"
                        substitute False

                        ## Take the color of the who text from the Character, if
                        ## set.
                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                text what:
                    substitute False

        if not _history_list:
            label _("The dialogue history is empty.")

define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art" }

style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    textalign gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    textalign gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5


## Help screen #################################################################
##
## A screen that gives information about key and mouse bindings. It uses other
## screens (keyboard_help, mouse_help, and gamepad_help) to display the actual
## help.

screen help():

    tag menu

    default device = "keyboard"

    use game_menu(_("Help"), scroll="viewport"):

        style_prefix "help"

        vbox:
            spacing 15

            hbox:

                textbutton _("Keyboard") action SetScreenVariable("device", "keyboard")
                textbutton _("Mouse") action SetScreenVariable("device", "mouse")

                if GamepadExists():
                    textbutton _("Gamepad") action SetScreenVariable("device", "gamepad")

            if device == "keyboard":
                use keyboard_help
            elif device == "mouse":
                use mouse_help
            elif device == "gamepad":
                use gamepad_help


screen keyboard_help():

    hbox:
        label _("Enter")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Space")
        text _("Advances dialogue without selecting choices.")

    hbox:
        label _("Arrow Keys")
        text _("Navigate the interface.")

    hbox:
        label _("Escape")
        text _("Accesses the game menu.")

    hbox:
        label _("Ctrl")
        text _("Skips dialogue while held down.")

    hbox:
        label _("Tab")
        text _("Toggles dialogue skipping.")

    hbox:
        label _("Page Up")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Page Down")
        text _("Rolls forward to later dialogue.")

    hbox:
        label "H"
        text _("Hides the user interface.")

    hbox:
        label "S"
        text _("Takes a screenshot.")

    hbox:
        label "V"
        text _("Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}.")

    hbox:
        label "Shift+A"
        text _("Opens the accessibility menu.")


screen mouse_help():

    hbox:
        label _("Left Click")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Middle Click")
        text _("Hides the user interface.")

    hbox:
        label _("Right Click")
        text _("Accesses the game menu.")

    hbox:
        label _("Mouse Wheel Up")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Mouse Wheel Down")
        text _("Rolls forward to later dialogue.")


screen gamepad_help():

    hbox:
        label _("Right Trigger\nA/Bottom Button")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Left Trigger\nLeft Shoulder")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Right Shoulder")
        text _("Rolls forward to later dialogue.")

    hbox:
        label _("D-Pad, Sticks")
        text _("Navigate the interface.")

    hbox:
        label _("Start, Guide")
        text _("Accesses the game menu.")

    hbox:
        label _("Y/Top Button")
        text _("Hides the user interface.")

    textbutton _("Calibrate") action GamepadCalibrate()


style help_button is gui_button
style help_button_text is gui_button_text
style help_label is gui_label
style help_label_text is gui_label_text
style help_text is gui_text

style help_button:
    properties gui.button_properties("help_button")
    xmargin 8

style help_button_text:
    properties gui.text_properties("help_button")

style help_label:
    xsize 250
    right_padding 20

style help_label_text:
    size gui.text_size
    xalign 1.0
    textalign 1.0



################################################################################
## Additional screens
################################################################################


## Confirm screen ##############################################################
##
## The confirm screen is called when Ren'Py wants to ask the player a yes or no
## question.
##
## http://www.renpy.org/doc/html/screen_special.html#confirm

screen confirm(message, yes_action, no_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 30

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("Yes") action yes_action
                textbutton _("No") action no_action

    ## Right-click and escape answer "no".
    key "game_menu" action no_action


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame("gui/komic/frame.png", gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    textalign 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.text_properties("confirm_button")


## Skip indicator screen #######################################################
##
## The skip_indicator screen is displayed to indicate that skipping is in
## progress.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 6

            text _("Skipping")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## This transform is used to blink the arrows one after another.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/komic/frame.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    ## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE
    ## glyph in it.
    font "DejaVuSans.ttf"


## Notify screen ###############################################################
##
## The notify screen is used to show the player a message. (For example, when
## the game is quicksaved or a screenshot has been taken.)
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text "[message!tq]"

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/komic/frame.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")


## NVL screen ##################################################################
##
## This screen is used for NVL-mode dialogue and menus.
##
## http://www.renpy.org/doc/html/screen_special.html#nvl


screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            spacing gui.nvl_spacing

        ## Displays dialogue in either a vpgrid or the vbox.
        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            use nvl_dialogue(dialogue)

        ## Displays the menu, if given. The menu may be displayed incorrectly if
        ## config.narrator_menu is set to True.
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


## This controls the maximum number of NVL-mode entries that can be displayed at
## once.
define config.nvl_list_length = 6

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    textalign gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    textalign gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    textalign gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.text_properties("nvl_button")



################################################################################
## Mobile Variants
################################################################################

style pref_vbox:
    variant "medium"
    xsize 450

## Since a mouse may not be present, we replace the quick menu with a version
## that uses fewer and bigger buttons that are easier to touch.
screen quick_menu():
    variant "touch"

    zorder 100

    if quick_menu:
        hbox:
            xalign 1.0
            yalign 0.0
            spacing 10

            imagebutton:
                idle Transform("gui/komic/quick/skip_idle.png", xysize=(72, 90))
                hover Transform("gui/komic/quick/skip_hover.png", xysize=(72, 90))
                action Skip()
                alternate Skip(fast=True, confirm=True)
                activate_sound "audio/ui_click.ogg"

            imagebutton:
                idle Transform("gui/komic/quick/continue_idle.png", xysize=(72, 90))
                hover Transform("gui/komic/quick/continue_hover.png", xysize=(72, 90))
                action Preference("auto-forward", "toggle")
                activate_sound "audio/ui_click.ogg"

            imagebutton:
                idle Transform("gui/komic/quick/save_idle.png", xysize=(72, 90))
                hover Transform("gui/komic/quick/save_hover.png", xysize=(72, 90))
                action ShowMenu("save")
                activate_sound "audio/ui_click.ogg"

            imagebutton:
                idle Transform("gui/komic/quick/options_idle.png", xysize=(72, 90))
                hover Transform("gui/komic/quick/options_hover.png", xysize=(72, 90))
                action ShowMenu("preferences")
                activate_sound "audio/ui_click.ogg"


style window:
    variant "small"
    background "gui/komic/textbox.png"

style nvl_window:
    variant "small"
    background "gui/phone/nvl.png"

style main_menu_frame:
    variant "small"
    background "gui/phone/overlay/main_menu.png"

style game_menu_outer_frame:
    variant "small"
    background "gui/phone/overlay/game_menu.png"

style game_menu_navigation_frame:
    variant "small"
    xsize 340

style game_menu_content_frame:
    variant "small"
    top_margin 0

style game_menu_viewport:
    variant "small"
    xsize 870

style pref_vbox:
    variant "small"
    xsize 400

style slider_pref_vbox:
    variant "small"
    xsize None

style slider_pref_slider:
    variant "small"
    xsize 600

# Shrink the title.
style main_menu_vbox:
    variant "small"
    xsize 900


################################################################################
## MOGMAX — Custom screens
################################################################################

## Chapter Select screen — reached from the main menu after completing Ch1.
screen chapter_select():
    tag menu

    add Solid("#0a0a0a")

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 22

        text "CHAPTER SELECT":
            size 60
            color "#ffffff"
            xalign 0.5

        text "Warning: starting a chapter overwrites your current progress.":
            size 16
            color "#888888"
            xalign 0.5
            italic True

        null height 30

        # Chapter 1 — always unlocked
        textbutton "Chapter 1 — Chopped / Brainmaxxing":
            action Confirm(
                "Start Chapter 1?\nThis will overwrite your current game progress.",
                yes=Start("start")
            )
            xalign 0.5
            text_size 32
            text_color "#cccccc"
            text_hover_color "#ffffff"

        # Chapter 2 — locked until the complete Chopped/Brainmaxxing arc ends.
        if persistent.chapter1_complete:
            textbutton "Chapter 2 — Gigamaxxing":
                action Confirm(
                    "Start Chapter 2?\nThis will overwrite your current game progress.",
                    yes=Start("chapter2_start")
                )
                xalign 0.5
                text_size 32
                text_color "#cccccc"
                text_hover_color "#ffffff"
        else:
            vbox:
                xalign 0.5
                spacing 2
                text "🔒  Chapter 2 — Gigamaxxing":
                    size 32
                    color "#555555"
                    xalign 0.5
                text "(Complete Chapter 1 to unlock)":
                    size 16
                    color "#444444"
                    xalign 0.5
                    italic True

        null height 40

        textbutton "← BACK":
            action Return()
            xalign 0.5
            text_size 24
            text_color "#888888"
            text_hover_color "#ffffff"


## Free-play minigames. Story mode always launches the approachable profiles;
## the original playtest tuning remains available here as Hard mode.
screen minigame_select():
    tag menu

    add Transform(gui.main_menu_background, size=(config.screen_width, config.screen_height))
    add Solid("#050806e8")

    text "MINIGAMES":
        xpos 74
        ypos 54
        size 48
        color "#ffffff"
        bold True

    text "TRAINING ARCHIVE":
        xpos 77
        ypos 112
        size 15
        color "#79c98b"
        bold True

    vbox:
        xpos 74
        ypos 166
        spacing 14

        frame:
            xysize (1132, 126)
            background Solid("#101613f2")
            padding (26, 20)

            hbox:
                yalign 0.5
                spacing 24

                vbox:
                    xsize 610
                    spacing 7
                    text "MEWING GEOMETRY":
                        size 25
                        color "#f1f4f2"
                        bold True
                    text "Lock each position and hold the final frame.":
                        size 15
                        color "#9aa6a0"

                textbutton "PLAY":
                    xysize (210, 62)
                    yalign 0.5
                    background Solid("#1e6f43")
                    hover_background Solid("#2a9c5f")
                    text_size 19
                    text_color "#ffffff"
                    text_bold True
                    action Function(renpy.call_in_new_context, "freeplay_mewing")

        frame:
            xysize (1132, 126)
            background Solid("#101613f2")
            padding (26, 20)

            hbox:
                yalign 0.5
                spacing 16

                vbox:
                    xsize 610
                    spacing 7
                    text "AURA HARVESTER 6000":
                        size 25
                        color "#f1f4f2"
                        bold True
                    text "Catch green drops. Hard preserves the original precision rules.":
                        size 15
                        color "#9aa6a0"

                textbutton "NORMAL":
                    xysize (210, 62)
                    yalign 0.5
                    background Solid("#1e6f43")
                    hover_background Solid("#2a9c5f")
                    text_size 18
                    text_color "#ffffff"
                    text_bold True
                    action Function(renpy.call_in_new_context, "freeplay_aura_normal")

                textbutton "HARD":
                    xysize (210, 62)
                    yalign 0.5
                    background Solid("#702f2f")
                    hover_background Solid("#963d3d")
                    text_size 18
                    text_color "#ffffff"
                    text_bold True
                    action Function(renpy.call_in_new_context, "freeplay_aura_hard")

        frame:
            xysize (1132, 126)
            background Solid("#101613f2")
            padding (26, 20)

            hbox:
                yalign 0.5
                spacing 16

                vbox:
                    xsize 610
                    spacing 7
                    text "DERMAL PURGE":
                        size 25
                        color "#f1f4f2"
                        bold True
                    text "Clear three waves. Hard preserves the original recovery clock.":
                        size 15
                        color "#9aa6a0"

                textbutton "NORMAL":
                    xysize (210, 62)
                    yalign 0.5
                    background Solid("#1e6f43")
                    hover_background Solid("#2a9c5f")
                    text_size 18
                    text_color "#ffffff"
                    text_bold True
                    action Function(renpy.call_in_new_context, "freeplay_acne_normal")

                textbutton "HARD":
                    xysize (210, 62)
                    yalign 0.5
                    background Solid("#702f2f")
                    hover_background Solid("#963d3d")
                    text_size 18
                    text_color "#ffffff"
                    text_bold True
                    action Function(renpy.call_in_new_context, "freeplay_acne_hard")

    textbutton "BACK":
        xpos 74
        ypos 650
        xysize (180, 46)
        background Solid("#ffffff0c")
        hover_background Solid("#79c98b22")
        text_size 17
        text_color "#c7d0cb"
        text_hover_color "#ffffff"
        text_bold True
        action Return()


label freeplay_mewing:
    $ reset_mewing_minigame()
    $ renpy.call_screen("mewing_minigame")
    return


label freeplay_aura_normal:
    $ reset_aura_harvester("normal")
    $ renpy.call_screen("aura_harvester")
    return


label freeplay_aura_hard:
    $ reset_aura_harvester("hard")
    $ renpy.call_screen("aura_harvester")
    return


label freeplay_acne_normal:
    $ reset_acne_minigame("normal", allow_quit=True)
    $ renpy.call_screen("acne_pop_minigame")
    return


label freeplay_acne_hard:
    $ reset_acne_minigame("hard", allow_quit=True)
    $ renpy.call_screen("acne_pop_minigame")
    return


################################################################################
## DEV SKIP MENU — press Shift+D anywhere (in dev mode) to jump to a scene.
## Saves having to play through the full quiz every test pass.
################################################################################

init python:
    if config.developer:
        # Show the global key-handler overlay on every screen.
        config.overlay_screens.append("dev_overlay")


screen dev_overlay():
    zorder 999
    if config.developer:
        key "shift_K_d" action Show("dev_skip_menu")


init python:
    import math

    class SleepyEyeOverlay(renpy.Displayable):
        def __init__(self, opening=0.0, **kwargs):
            super(SleepyEyeOverlay, self).__init__(**kwargs)
            self.opening = max(0.0, min(2.0, float(opening)))

        def render(self, width, height, st, at):
            width = int(config.screen_width)
            height = int(config.screen_height)
            rv = renpy.Render(width, height)
            canvas = rv.canvas()

            if self.opening <= 0.01:
                canvas.rect("#000000", (0, 0, width, height))
                return rv

            if self.opening >= 1.95:
                return rv

            center_y = height / 2.0
            half_open = 295.0 * self.opening
            edge_open = max(0.0, self.opening - 1.0) * (height / 2.0)
            points = []

            for i in range(49):
                x = (width * i) / 48.0
                curve = math.sin(math.pi * (x / float(width)))
                points.append((x, curve))

            upper_lid = [(x, center_y - edge_open - (half_open * curve)) for x, curve in points]
            lower_lid = [(x, center_y + edge_open + (half_open * curve)) for x, curve in points]

            canvas.polygon("#000000", [(0, 0), (width, 0)] + list(reversed(upper_lid)))
            canvas.polygon("#000000", lower_lid + [(width, height), (0, height)])

            return rv


    class SleepyEyeAnimation(SleepyEyeOverlay):
        timeline = (
            (0.00, 0.00),
            (0.45, 0.00),
            (1.25, 0.15),
            (1.75, 0.15),
            (2.15, 0.00),
            (2.50, 0.00),
            (4.25, 0.82),
            (5.35, 2.00),
        )

        def __init__(self, **kwargs):
            super(SleepyEyeAnimation, self).__init__(0.0, **kwargs)

        def opening_at(self, st):
            previous_t, previous_opening = self.timeline[0]

            for next_t, next_opening in self.timeline[1:]:
                if st <= next_t:
                    span = max(next_t - previous_t, 0.001)
                    progress = (st - previous_t) / span
                    eased = progress * progress * (3.0 - (2.0 * progress))
                    return previous_opening + ((next_opening - previous_opening) * eased)

                previous_t, previous_opening = next_t, next_opening

            return self.timeline[-1][1]

        def render(self, width, height, st, at):
            self.opening = self.opening_at(st)
            renpy.redraw(self, 0.0)
            return super(SleepyEyeAnimation, self).render(width, height, st, at)


screen sleepy_eye_overlay(opening=0.0):
    zorder 1100
    add SleepyEyeOverlay(opening)


screen sleepy_eye_animation():
    zorder 1100
    add SleepyEyeAnimation()


screen dev_skip_jump_button(label_text, jump_label, setup_actions=[]):
    textbutton label_text:
        action setup_actions + [
            Hide("dev_chapter1_skip_menu"),
            Hide("dev_chapter2_skip_menu"),
            Hide("dev_minigame_skip_menu"),
            Hide("dev_battle_skip_menu"),
            Hide("dev_skip_menu"),
            Jump(jump_label),
        ]
        xalign 0.5
        text_size 18


screen dev_skip_call_button(label_text, call_label):
    textbutton label_text:
        action [
            Hide("dev_minigame_skip_menu"),
            Hide("dev_battle_skip_menu"),
            Hide("dev_skip_menu"),
            Function(renpy.call_in_new_context, call_label),
        ]
        xalign 0.5
        text_size 19


screen dev_skip_menu():
    modal True
    zorder 1000

    frame:
        xalign 0.5
        yalign 0.5
        xysize (760, 500)
        background Solid("#000000ee")
        padding (36, 26)

        vbox:
            xfill True
            spacing 14

            text "DEV MENU":
                size 30
                color "#ff8888"
                xalign 0.5

            text "SHIFT+D TO OPEN ANYWHERE":
                size 12
                color "#777777"
                xalign 0.5

            null height 4

            hbox:
                xalign 0.5
                spacing 44

                vbox:
                    xsize 300
                    spacing 9

                    text "STORY JUMPS":
                        size 18
                        color "#b8c0bc"
                        bold True
                        xalign 0.5

                    textbutton "Chapter 1 scenes":
                        action [Hide("dev_skip_menu"), Show("dev_chapter1_skip_menu")]
                        xalign 0.5
                        text_size 22

                    textbutton "Chapter 2 scenes":
                        action [Hide("dev_skip_menu"), Show("dev_chapter2_skip_menu")]
                        xalign 0.5
                        text_size 22

                    textbutton "Credits roll":
                        action [Hide("dev_skip_menu"), Jump("roll_credits")]
                        xalign 0.5
                        text_size 20

                vbox:
                    xsize 300
                    spacing 9

                    text "PLAYTESTS":
                        size 18
                        color "#69e4ad"
                        bold True
                        xalign 0.5

                    textbutton "Training minigames":
                        action [Hide("dev_skip_menu"), Show("dev_minigame_skip_menu")]
                        xalign 0.5
                        text_size 22

                    textbutton "Mog battles":
                        action [Hide("dev_skip_menu"), Show("dev_battle_skip_menu")]
                        xalign 0.5
                        text_size 22

            null height 18

            textbutton "Close (Esc)":
                action Hide("dev_skip_menu")
                xalign 0.5
                text_size 18
                text_color "#888888"

    key "K_ESCAPE" action Hide("dev_skip_menu")


screen dev_chapter1_skip_menu():
    modal True
    zorder 1001

    frame:
        xalign 0.5
        yalign 0.5
        xysize (840, 580)
        background Solid("#050505f4")
        padding (34, 24)

        vbox:
            xfill True
            spacing 10

            text "CHAPTER 1 SCENES":
                size 28
                color "#ff8888"
                xalign 0.5

            text "Chopped + Brainmaxxing":
                size 13
                color "#777777"
                xalign 0.5

            textbutton "Back to dev menu":
                action [Hide("dev_chapter1_skip_menu"), Show("dev_skip_menu")]
                xalign 0.5
                text_size 16
                text_color "#888888"

            null height 4

            hbox:
                xalign 0.5
                spacing 34

                vbox:
                    xsize 360
                    spacing 7

                    text "CHOPPED":
                        size 17
                        color "#b8c0bc"
                        bold True
                        xalign 0.5

                    use dev_skip_jump_button("Start / name prompt", "start")

                    use dev_skip_jump_button("Red pill handoff", "chad_pill_ending", [SetVariable("took_chad_pill", True)])

                    use dev_skip_jump_button("Blue pill ending", "ltn_pill_ending")

                    null height 8

                    text "BRAINMAXXING":
                        size 17
                        color "#b8c0bc"
                        bold True
                        xalign 0.5

                    use dev_skip_jump_button("Flashcards", "chapter1_brainmaxxing", [SetVariable("brainmaxxing_attempt", 1)])

                    use dev_skip_jump_button("Quiz", "class_quiz", [SetVariable("brainmaxxing_attempt", 1)])

                vbox:
                    xsize 360
                    spacing 7

                    text "QUIZ OUTCOMES":
                        size 17
                        color "#b8c0bc"
                        bold True
                        xalign 0.5

                    use dev_skip_jump_button("Pass scene", "pass_class_scene", [SetVariable("brain_score", 10), SetVariable("final_score", 100), SetVariable("brayden_threatened", True)])

                    use dev_skip_jump_button("Fail scene", "fail_class_scene", [SetVariable("brainmaxxing_attempt", 1), SetVariable("brain_score", 3), SetVariable("final_score", 30)])

                    use dev_skip_jump_button("Mirror finale", "mirror_scene", [SetVariable("final_score", 100), SetVariable("brayden_threatened", True)])

                    use dev_skip_jump_button("Chapter 2 handoff", "chapter2_start", [SetVariable("brayden_threatened", True)])

                    use dev_skip_jump_button("Credits roll", "roll_credits", [SetVariable("credits_from_chapter", 1)])

            null height 8

            textbutton "Back":
                action [Hide("dev_chapter1_skip_menu"), Show("dev_skip_menu")]
                xalign 0.5
                text_size 18
                text_color "#888888"

    key "K_ESCAPE" action [Hide("dev_chapter1_skip_menu"), Show("dev_skip_menu")]


screen dev_chapter2_skip_menu():
    modal True
    zorder 1001

    default ch2_setup = [SetVariable("took_chad_pill", True), SetVariable("brayden_threatened", True)]

    frame:
        xalign 0.5
        yalign 0.5
        xysize (1120, 650)
        background Solid("#050505f4")
        padding (34, 24)

        vbox:
            xfill True
            spacing 10

            text "CHAPTER 2 SCENES":
                size 28
                color "#ff8888"
                xalign 0.5

            text "Gigamaxxing":
                size 13
                color "#777777"
                xalign 0.5

            textbutton "Back to dev menu":
                action [Hide("dev_chapter2_skip_menu"), Show("dev_skip_menu")]
                xalign 0.5
                text_size 16
                text_color "#888888"

            null height 4

            hbox:
                xalign 0.5
                spacing 38

                vbox:
                    xsize 500
                    spacing 6

                    text "ARRIVAL":
                        size 17
                        color "#b8c0bc"
                        bold True
                        xalign 0.5

                    use dev_skip_jump_button("Title card", "chapter2_start", ch2_setup)

                    use dev_skip_jump_button("Pickup", "chapter2_pickup", ch2_setup)

                    use dev_skip_jump_button("Road trip", "chapter2_road", ch2_setup)

                    use dev_skip_jump_button("Restricted sign", "chapter2_restricted_sign", ch2_setup)

                    use dev_skip_jump_button("Gate + soldiers", "chapter2_gate", ch2_setup)

                    null height 8

                    text "FACILITY":
                        size 17
                        color "#b8c0bc"
                        bold True
                        xalign 0.5

                    use dev_skip_jump_button("Base security / vault", "chapter2_base", ch2_setup)

                    use dev_skip_jump_button("Lab reveal", "chapter2_lab_reveal", ch2_setup)

                    use dev_skip_jump_button("Gigachad hallway", "chapter2_gigachad_hall", ch2_setup)

                    use dev_skip_jump_button("Projection gallery", "chapter2_projection_gallery", ch2_setup)

                vbox:
                    xsize 500
                    spacing 6

                    text "TRAINING":
                        size 17
                        color "#b8c0bc"
                        bold True
                        xalign 0.5

                    use dev_skip_jump_button("Training intro", "chapter2_training", ch2_setup)

                    use dev_skip_jump_button("Montage aftermath", "dev_ch2_training_montage", ch2_setup)

                    use dev_skip_jump_button("Kai tutorial battle", "dev_ch2_kai_tutorial", ch2_setup)

                    use dev_skip_jump_button("Kai graduation spar", "dev_ch2_kai_graduation", ch2_setup)

                    null height 8

                    text "ENDING RUN":
                        size 17
                        color "#b8c0bc"
                        bold True
                        xalign 0.5

                    use dev_skip_jump_button("Eugene choice", "chapter2_eugene", ch2_setup)

                    use dev_skip_jump_button("Drive home", "chapter2_return", ch2_setup)

                    use dev_skip_jump_button("Text invite finale", "dev_ch2_invite", ch2_setup)

                    use dev_skip_jump_button("Credits roll", "roll_credits", ch2_setup + [SetVariable("credits_from_chapter", 2)])

            null height 6

            textbutton "Back":
                action [Hide("dev_chapter2_skip_menu"), Show("dev_skip_menu")]
                xalign 0.5
                text_size 18
                text_color "#888888"

    key "K_ESCAPE" action [Hide("dev_chapter2_skip_menu"), Show("dev_skip_menu")]


screen dev_minigame_skip_menu():
    modal True
    zorder 1001

    frame:
        xalign 0.5
        yalign 0.5
        xysize (560, 420)
        background Solid("#050505f4")
        padding (34, 24)

        vbox:
            xfill True
            spacing 12

            text "TRAINING MINIGAMES":
                size 26
                color "#69e4ad"
                xalign 0.5

            textbutton "Back to dev menu":
                action [Hide("dev_minigame_skip_menu"), Show("dev_skip_menu")]
                xalign 0.5
                text_size 16
                text_color "#888888"

            null height 4

            use dev_skip_call_button("Mewing Geometry", "dev_test_mewing")

            use dev_skip_call_button("Aura Harvester", "dev_test_aura")

            use dev_skip_call_button("Dermal Purge", "dev_test_acne")

            null height 10

            textbutton "Back":
                action [Hide("dev_minigame_skip_menu"), Show("dev_skip_menu")]
                xalign 0.5
                text_size 18
                text_color "#888888"

    key "K_ESCAPE" action [Hide("dev_minigame_skip_menu"), Show("dev_skip_menu")]


screen dev_battle_skip_menu():
    modal True
    zorder 1001

    frame:
        xalign 0.5
        yalign 0.5
        xysize (560, 470)
        background Solid("#050505f4")
        padding (34, 24)

        vbox:
            xfill True
            spacing 12

            text "MOG BATTLES":
                size 26
                color "#69e4ad"
                xalign 0.5

            textbutton "Back to dev menu":
                action [Hide("dev_battle_skip_menu"), Show("dev_skip_menu")]
                xalign 0.5
                text_size 16
                text_color "#888888"

            null height 4

            use dev_skip_call_button("Kai tutorial", "dev_test_kai_tutorial")

            use dev_skip_call_button("Kai graduation", "dev_test_kai_graduation")

            use dev_skip_call_button("Brayden battle", "dev_test_brayden")

            use dev_skip_call_button("Clav battle", "dev_test_clav")

            null height 10

            textbutton "Back":
                action [Hide("dev_battle_skip_menu"), Show("dev_skip_menu")]
                xalign 0.5
                text_size 18
                text_color "#888888"

    key "K_ESCAPE" action [Hide("dev_battle_skip_menu"), Show("dev_skip_menu")]


label dev_test_mewing:
    $ reset_mewing_minigame()
    $ renpy.call_screen("mewing_minigame")
    return


label dev_test_aura:
    $ reset_aura_harvester()
    $ renpy.call_screen("aura_harvester")
    return


label dev_test_acne:
    $ reset_acne_minigame(allow_quit=True)
    $ renpy.call_screen("acne_pop_minigame")
    return


label dev_test_kai_tutorial:
    $ start_mog_battle("kai_tutorial")
    $ renpy.call_screen("mog_battle_screen")
    return


label dev_test_kai_graduation:
    $ start_mog_battle("kai_graduation")
    $ renpy.call_screen("mog_battle_screen")
    return


label dev_test_brayden:
    $ start_mog_battle("brayden")
    $ renpy.call_screen("mog_battle_screen")
    return


label dev_test_clav:
    $ start_mog_battle("clav")
    $ renpy.call_screen("mog_battle_screen")
    return


# ─── Chapter 2 road time-skip card ───────────────────────────
screen ch2_travel_bar():
    modal True
    add Solid("#000000")

    text "MANY HOURS LATER":
        style "story_card_text"
        xalign 0.5
        yalign 0.5

    timer 1.8 action Return()


################################################################################
## STUDY FLASHCARDS — Chapter 1 Brainmaxxing vocab study
##
## Reads VOCAB from chapter1_brainmaxxing.rpy. Tracks flipped cards in
## `brainmaxxing_studied` (reset to empty each entry).
## Click TAKE THE QUIZ to return → study_done → class_quiz.
################################################################################

screen study_flashcards():
    add "bg library"
    add Solid("#0a0a0ad0")

    # Header
    vbox:
        xalign 0.5
        yalign 0.035
        spacing 3
        text "CLAV'S BOOTCAMP — THE LIST":
            size 30
            color "#ffffff"
            xalign 0.5
            outlines [(2, "#000000", 0, 0)]
        text "Click each card. Flip them all if you want a real shot.":
            size 13
            color "#aaaaaa"
            xalign 0.5
            italic True
        # Rotating Clav quip — picked when the screen is entered
        text "{color=#9aa8ff}Clav:{/color}  {i}\"[brainmaxxing_clav_quip]\"{/i}":
            size 14
            color "#bbbbbb"
            xalign 0.5

    # 5 × 2 grid of 10 cards
    vpgrid:
        cols 5
        xalign 0.5
        yalign 0.52
        spacing 10

        for idx in range(len(VOCAB)):
            button:
                xysize (215, 230)
                if idx in brainmaxxing_studied:
                    background Solid("#2a3a55")
                    hover_background Solid("#3a4a65")
                else:
                    background Solid("#1a1a2a")
                    hover_background Solid("#2a2a3a")
                action ToggleSetMembership(brainmaxxing_studied, idx)

                if idx in brainmaxxing_studied:
                    vbox:
                        xalign 0.5
                        yalign 0.5
                        xmaximum 200
                        spacing 6
                        text VOCAB[idx]["word"]:
                            size 18
                            color "#88ff88"
                            bold True
                            xalign 0.5
                            text_align 0.5
                        text VOCAB[idx]["correct"]:
                            size 12
                            color "#dddddd"
                            xalign 0.5
                            text_align 0.5
                        text VOCAB[idx]["example"]:
                            size 10
                            color "#aaaaaa"
                            italic True
                            xalign 0.5
                            text_align 0.5
                else:
                    text VOCAB[idx]["word"]:
                        size 20
                        color "#cccccc"
                        xalign 0.5
                        yalign 0.5
                        text_align 0.5

    textbutton "▶  TAKE THE QUIZ":
        xalign 0.5
        yalign 0.95
        text_size 26
        text_color "#88ff88"
        text_hover_color "#ffffff"
        action Return()


################################################################################
## QUIZ QUESTION — Chapter 1 Brainmaxxing quiz screen
##
## Called via:
##   renpy.call_screen("quiz_question", q_num=N, total=7, word="...", options=[...])
## Returns the option tag selected ("correct" / "wrong" / "joke").
################################################################################

screen quiz_question(q_num=1, total=7, word="", options=[]):
    modal True
    add Solid("#0a0a0a")

    # Re-check time + buzzer + timeout four times a second.
    timer 0.25 repeat True action Function(_quiz_tick)

    # Live countdown (re-evaluated on every screen redraw / timer tick).
    $ time_left = max(0, int(quiz_duration - (_qtime.time() - quiz_start_time)))

    frame:
        xalign 0.97
        yalign 0.04
        background Solid("#1a1a2acc")
        padding (16, 8)
        text "[time_left]s":
            size 36
            color ("#ff4444" if time_left <= 10 else "#cccccc")
            bold True

    # Header
    vbox:
        xalign 0.5
        yalign 0.07
        spacing 4
        text "Mr. Harker's Pop Quiz":
            size 22
            color "#aaaaaa"
            xalign 0.5
            italic True
        text "Question [q_num] of [total]":
            size 16
            color "#666666"
            xalign 0.5

    # Pinned question — large and visible throughout
    vbox:
        xalign 0.5
        yalign 0.32
        spacing 10
        text "Define:":
            size 26
            color "#888888"
            xalign 0.5
        text "[word]":
            size 64
            color "#ffffff"
            bold True
            xalign 0.5
            outlines [(2, "#3a3a55", 0, 0)]

    # Answer buttons
    vbox:
        xalign 0.5
        yalign 0.80
        spacing 12

        for option_text, option_value in options:
            textbutton option_text:
                action Return(option_value)
                xalign 0.5
                xsize 880
                text_size 22
                text_color "#dddddd"
                text_hover_color "#88ff88"
                text_align 0.5
                background Solid("#1a1a2a")
                hover_background Solid("#2a2a4a")
                padding (24, 14)
