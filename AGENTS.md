# AGENTS.md

## Running MOGMAX

- This is a Ren'Py 8.5 project.
- Default local SDK path on this machine:
  `/Users/tarzerk/builds/renpy-8.5.3-sdk/renpy.sh`
- Run lint before handing changes back:
  `/Users/tarzerk/builds/renpy-8.5.3-sdk/renpy.sh /Users/tarzerk/Developer/mogmax lint`
- Launch the game for manual testing:
  `/Users/tarzerk/builds/renpy-8.5.3-sdk/renpy.sh /Users/tarzerk/Developer/mogmax`
- Developer shortcut: press `Shift+D` in-game to open the debug skip menu.

## Editing Rules

- Before editing story script, preview the intended story beat or scene plan with the user and get approval.
- Before editing gameplay, explain what will change and confirm with the user first.
- Keep story and gameplay edits scoped to the requested scene/system.
- Check sprite placement against the game's default window size before handing off.
- The game is hardcoded to `1280x720` in `game/options.rpy` and `game/gui.rpy`; use those dimensions when judging overlap and layout.
- Make sure character sprites, captions, choices, menus, and minigame UI do not overlap in the 1280x720 layout.
- Run Ren'Py lint after script or screen edits.
