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

## Release And itch.io

- Release builds are produced by `.github/workflows/build.yml` when a `v*` tag is pushed.
- Before tagging, update `config.version` in `game/options.rpy`, run lint, and make sure the release commit is on or destined for `main`.
- Use a matching tag such as `v2.1` for `config.version = "2.1"`.
- Push the tag to GitHub. The workflow builds Windows/Linux, macOS, and web packages and publishes them on the matching GitHub Release.
- Wait for the `Build distributables` workflow to finish successfully before uploading to itch.io.
- Use the `MOGMAX-<version>-web.zip` release asset for itch.io. It must contain `index.html` at the ZIP root.
- Stage the browser build on the testing playground first:
  `https://tarzerk.itch.io/mogmax-testing`
- Test the staged build at 1280x720, including the main menu, save/load, Chapter 1, Chapter 2 transitions, debug scene navigation, battles, and ending flow.
- After the staged build passes, upload the same web ZIP to the real page:
  `https://tarzerk.itch.io/mogmax`
- On both itch pages, mark only the newest web ZIP as `This file will be played in the browser`; hide or remove superseded browser builds so itch does not launch an old file.
- Keep the embed at 1280x720, mobile friendly, with the fullscreen button enabled.
- Do not change the real page's black/red theme during a release unless the user asks. The old Gigachad banner was intentionally removed.
