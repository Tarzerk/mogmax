#!/usr/bin/env bash
#
# Build → sign → notarize → staple the macOS release of MOGMAX.
#
# The end state this produces is a .dmg that a stranger can download and
# double-click with no Gatekeeper prompt at all. That requires four things to
# all be true, and skipping any one of them silently downgrades the result to
# "still shows the scary dialog":
#
#   1. Signed with a *Developer ID Application* cert (NOT "Apple Development",
#      which cannot be notarized).
#   2. Signed with the hardened runtime enabled (--options runtime).
#   3. Signed with a secure timestamp (--timestamp).
#   4. Notarized by Apple, and the resulting ticket *stapled* into the .dmg so
#      it validates offline.
#
# Usage:
#   tools/release_mac.sh                # build, sign, notarize, staple
#   tools/release_mac.sh --skip-build   # reuse the existing dist output
#   tools/release_mac.sh --no-notarize  # sign only (fast local smoke test)
#
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RENPY_SDK="${RENPY_SDK:-$HOME/builds/renpy-8.5.3-sdk}"
NOTARY_PROFILE="${NOTARY_PROFILE:-mogmax-notary}"
ENTITLEMENTS="$REPO_ROOT/tools/mac_entitlements.plist"

SKIP_BUILD=0
NOTARIZE=1
for arg in "$@"; do
  case "$arg" in
    --skip-build)  SKIP_BUILD=1 ;;
    --no-notarize) NOTARIZE=0 ;;
    *) echo "unknown flag: $arg" >&2; exit 2 ;;
  esac
done

step() { printf '\n\033[1;36m==> %s\033[0m\n' "$1"; }
die()  { printf '\n\033[1;31mERROR: %s\033[0m\n' "$1" >&2; exit 1; }

# ---------------------------------------------------------------------------
# Preflight. Fail loudly *before* a 5-minute build rather than after it.
# ---------------------------------------------------------------------------
step "Preflight"

# Grab the Developer ID Application identity. We match on that exact prefix so
# a stray "Apple Development" cert can never be picked up by accident — that
# substitution is the single most common way a "signed" build still gets
# blocked on other people's machines.
IDENTITY="$(security find-identity -v -p codesigning \
  | grep 'Developer ID Application' \
  | head -n1 \
  | sed -E 's/.*"(.*)"/\1/')" || true

if [ -z "${IDENTITY:-}" ]; then
  die "No 'Developer ID Application' certificate in the keychain.
     Found instead:
$(security find-identity -v -p codesigning | sed 's/^/       /')

     Create one at https://developer.apple.com/account/resources/certificates
     (type: Developer ID Application) and double-click the downloaded .cer."
fi
echo "Signing identity: $IDENTITY"

TEAM_ID="$(echo "$IDENTITY" | sed -E 's/.*\(([A-Z0-9]+)\)$/\1/')"
echo "Team ID:          $TEAM_ID"

[ -x "$RENPY_SDK/renpy.sh" ] || die "Ren'Py SDK not found at $RENPY_SDK (override with RENPY_SDK=...)"
[ -f "$ENTITLEMENTS" ]       || die "Missing entitlements file at $ENTITLEMENTS"

if [ "$NOTARIZE" -eq 1 ] && ! xcrun notarytool history --keychain-profile "$NOTARY_PROFILE" >/dev/null 2>&1; then
  die "No notarytool credentials stored under profile '$NOTARY_PROFILE'.
     Create them with (you will be prompted for an app-specific password):

       xcrun notarytool store-credentials $NOTARY_PROFILE \\
         --apple-id <your-apple-id-email> \\
         --team-id $TEAM_ID

     Generate the app-specific password at https://account.apple.com → Sign-In
     and Security → App-Specific Passwords. It is NOT your Apple ID password."
fi

VERSION="$(grep -E '^define config\.version' "$REPO_ROOT/game/options.rpy" \
  | sed -E 's/.*"([^"]+)".*/\1/')"
[ -n "$VERSION" ] || die "Could not read config.version from game/options.rpy"
echo "Version:          $VERSION"

DIST_DIR="$(dirname "$REPO_ROOT")/MOGMAX-$VERSION-dists"

# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
if [ "$SKIP_BUILD" -eq 0 ]; then
  step "Lint"
  "$RENPY_SDK/renpy.sh" "$REPO_ROOT" lint

  step "Build pc + mac packages"
  "$RENPY_SDK/renpy.sh" "$RENPY_SDK/launcher" distribute "$REPO_ROOT" \
    --package pc --package mac
fi

[ -d "$DIST_DIR" ] || die "dist dir not found: $DIST_DIR"
MAC_ZIP="$(ls "$DIST_DIR"/MOGMAX-*-mac.zip 2>/dev/null | head -n1)"
[ -n "$MAC_ZIP" ] || die "no mac zip in $DIST_DIR"
echo "Mac zip: $MAC_ZIP"

# ---------------------------------------------------------------------------
# Sign
# ---------------------------------------------------------------------------
step "Stage .app"
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT
ditto -x -k "$MAC_ZIP" "$STAGE"

APP="$(find "$STAGE" -maxdepth 2 -name '*.app' -type d | head -n1)"
[ -n "$APP" ] || die "no .app inside $MAC_ZIP"
echo "App: $APP"

# Finder/unzip metadata and quarantine flags make codesign emit "resource fork,
# Finder information, or similar detritus not allowed" and abort. Strip first.
xattr -cr "$APP"
find "$APP" -name '.DS_Store' -delete

step "Sign nested binaries (inside-out)"
# Nested code must be signed before its container, deepest first — signing the
# outer bundle seals a hash of everything inside it, so anything signed
# afterwards invalidates that seal. `codesign --deep` exists but Apple
# explicitly recommends against it for distribution signing because it applies
# the *same* entitlements everywhere and quietly skips some nested formats.
#
# -r reverses the depth-sorted list so children precede parents.
NESTED_COUNT=0
while IFS= read -r bin; do
  codesign --force --timestamp --options runtime \
    --entitlements "$ENTITLEMENTS" \
    --sign "$IDENTITY" "$bin" 2>/dev/null
  NESTED_COUNT=$((NESTED_COUNT + 1))
done < <(
  {
    # Loadable code that is not itself a bundle: dylibs, Python extension
    # modules, and any helper executables Ren'Py ships in the bundle.
    find "$APP" -type f \( -name '*.dylib' -o -name '*.so' \) -print
    find "$APP" -type f -perm +111 -print | while read -r f; do
      # `file` is the only reliable way to tell a Mach-O helper binary from a
      # shell script that merely happens to have the execute bit set.
      #
      # Deliberately `if ... grep -q` rather than the more natural `case`:
      # macOS ships bash 3.2.57, whose parser mis-handles a case statement
      # nested inside $(...) inside <(...) and dies with "syntax error near
      # unexpected token". Do not "clean this up" into a case.
      if file -b "$f" | grep -q 'Mach-O'; then
        echo "$f"
      fi
    done
    # Nested bundles (frameworks, plugins, helper .apps) sign as units.
    find "$APP" -depth -type d \( -name '*.framework' -o -name '*.bundle' \) -print
  } | awk '{ print gsub(/\//,"/") "\t" $0 }' | sort -rn | cut -f2- | awk '!seen[$0]++'
)
echo "Signed $NESTED_COUNT nested binaries."

step "Sign app bundle"
codesign --force --timestamp --options runtime \
  --entitlements "$ENTITLEMENTS" \
  --sign "$IDENTITY" "$APP"

step "Verify signature"
codesign --verify --deep --strict --verbose=2 "$APP"
# Confirm the hardened runtime actually stuck. Notarization rejects the upload
# without it, and the failure message from Apple is famously unhelpful.
codesign --display --verbose=2 "$APP" 2>&1 | grep -q 'flags=.*runtime' \
  || die "hardened runtime flag missing after signing"
echo "Hardened runtime: present"

# ---------------------------------------------------------------------------
# DMG
# ---------------------------------------------------------------------------
step "Build .dmg"
DMG="${MAC_ZIP%.zip}.dmg"

# Lay out a drag-to-install window: the .app next to an /Applications alias.
DMG_SRC="$(mktemp -d)"
trap 'rm -rf "$STAGE" "$DMG_SRC"' EXIT
ditto "$APP" "$DMG_SRC/$(basename "$APP")"
ln -s /Applications "$DMG_SRC/Applications"

hdiutil create \
  -volname "MOGMAX $VERSION" \
  -srcfolder "$DMG_SRC" \
  -ov -format UDZO \
  "$DMG" >/dev/null
echo "Created $DMG"

# The disk image itself is signed too, so the download carries a valid
# signature even before the ticket is stapled.
codesign --force --timestamp --sign "$IDENTITY" "$DMG"

if [ "$NOTARIZE" -eq 0 ]; then
  step "Done (signing only — NOT notarized)"
  echo "This build will STILL warn on other Macs. Re-run without --no-notarize."
  ls -lh "$DMG"
  exit 0
fi

# ---------------------------------------------------------------------------
# Notarize + staple
# ---------------------------------------------------------------------------
step "Notarize (uploads to Apple; usually 1-5 min)"
xcrun notarytool submit "$DMG" \
  --keychain-profile "$NOTARY_PROFILE" \
  --wait

step "Staple ticket"
# Stapling embeds the notarization ticket in the .dmg so Gatekeeper can
# validate it with no network connection. Without this a first launch on a
# machine that is offline (or behind a filtering proxy) still gets blocked.
xcrun stapler staple "$DMG"
xcrun stapler validate "$DMG"

step "Final Gatekeeper check"
# This is the actual assertion that matters: it evaluates the .dmg exactly the
# way Gatekeeper will on a player's Mac.
spctl -a -t open --context context:primary-signature -v "$DMG"

step "Done"
ls -lh "$DMG"
echo
echo "Upload this .dmg. It should open with no security warning on any Mac."
