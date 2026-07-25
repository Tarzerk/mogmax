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

- Use semantic versions in `MAJOR.MINOR.PATCH` form. Increment MAJOR for a major edition or save-incompatible change, MINOR for new chapters or features, and PATCH for fixes and polish.
- Start each release by creating `release/<version>` from the exact approved `main` commit, for example `release/2.1.0`. Create this branch before QA so later changes to `main` cannot alter the candidate being tested.
- Update `config.version` in `game/options.rpy` to match the release version. Run lint and build from the release branch.
- Deploy the release branch to the testing playground first:
  `https://tarzerk.itch.io/mogmax-testing`
- QA may be updated freely. Put release-blocking fixes on the same release branch and redeploy it until the candidate passes.
- Test at 1280x720, including the main menu, save/load, Chapter 1, Chapter 2 transitions, debug scene navigation, battles, and ending flow.
- Do not promote a QA candidate to the real page until the user explicitly says it is approved for release.
- After approval, build once from the exact approved release commit and promote the same artifacts to GitHub and the real itch.io page. Do not rebuild from a different commit between QA approval and production.
- Tag the approved release commit as `v<version>`, for example `v2.1.0`. Pushing a `v*` tag runs `.github/workflows/build.yml`, which builds Windows/Linux, macOS, and web packages and publishes the matching GitHub Release.
- Windows and Mac ZIPs are the primary itch.io releases. The HTML5 build is substantially slower and should remain hidden unless the user explicitly asks to restore browser play.
- Build platform-specific desktop ZIPs from the approved commit:
  `/Users/tarzerk/builds/renpy-8.5.3-sdk/renpy.sh /Users/tarzerk/builds/renpy-8.5.3-sdk/launcher distribute /path/to/mogmax --package win --package mac`
- Upload the exact desktop ZIPs to the testing page with Butler:
  `butler push /path/to/MOGMAX-<version>-win.zip tarzerk/mogmax-testing:windows --userversion <version>`
  `butler push /path/to/MOGMAX-<version>-mac.zip tarzerk/mogmax-testing:osx --userversion <version>`
- After QA approval, promote the same ZIPs to the real page:
  `butler push /path/to/MOGMAX-<version>-win.zip tarzerk/mogmax:windows --userversion <version>`
  `butler push /path/to/MOGMAX-<version>-mac.zip tarzerk/mogmax:osx --userversion <version>`
- Keep both itch projects set to `Downloadable`. Mark the Windows channel for Windows, mark the macOS channel for macOS, and hide the `html5` and other superseded web uploads.
- Prefer Butler for release uploads. Large builds are less reliable through the browser uploader.
- The real page is:
  `https://tarzerk.itch.io/mogmax`
- Do not edit either itch page's description during a build-only release update unless the user specifically requests copy changes.
- Keep the itch download instructions current. Include the Windows unzip/run steps and the macOS Gatekeeper path: click `Done`, open `System Settings > Privacy & Security`, click `Open Anyway`, then confirm `Open`. Link to Apple's official override guide and remind players to bypass the warning only for a copy downloaded from the official MOGMAX itch page.
- Do not change the real page's black/red theme during a release unless the user asks. The old Gigachad banner was intentionally removed.
- Keep the real itch.io page set to `Draft` and hidden from the public until the user explicitly approves publishing it. Uploading a build is not permission to switch the page to `Public`.
- After release, merge the release branch back into `main` if it contains version or release fixes that are not already there.
- For a production hotfix, branch from the released tag into the next PATCH release, such as `release/2.1.1`, and repeat the same QA and approval gates.
- The existing `v2.1` build is the one-time initial release. Do not move or replace its published tag; use the full three-part version format for future releases.
