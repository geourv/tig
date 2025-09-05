#!/usr/bin/env bash
set -Eeuo pipefail

# usage:
#   contrib/make-logos.sh assets/logo.svg assets/icons/docs_quarts_de_docs [--ico] [--pwa] [--og banner.svg|png]
# deps: inkscape (obligatori). ImageMagick (opcional) només si uses --ico o --og.

SRC=""
OUT="assets/icons"
DO_ICO=0
DO_PWA=0
OG_SRC=""

# posicionals
[[ $# -ge 1 && "${1#--}" == "$1" ]] && SRC="$1" && shift || true
[[ $# -ge 1 && "${1#--}" == "$1" ]] && OUT="$1" && shift || true

# opcions
while [[ $# -gt 0 ]]; do
  case "$1" in
    --ico) DO_ICO=1; shift;;
    --pwa) DO_PWA=1; shift;;
    --og)  OG_SRC="${2:-}"; shift 2;;
    *) echo "unknown option: $1" >&2; exit 2;;
  esac
done

[[ -n "$SRC" && -f "$SRC" ]] || { echo "usage: $0 logo.svg [out_dir] [--ico] [--pwa] [--og banner.svg|png]"; exit 1; }
mkdir -p "$OUT"

have(){ command -v "$1" >/dev/null 2>&1; }

INK="inkscape"
have "$INK" || { echo "ERROR: inkscape required"; exit 1; }

IM=""
if have magick; then IM="magick"; elif have convert; then IM="convert"; fi
if { [[ $DO_ICO -eq 1 ]] || [[ -n "$OG_SRC" ]]; } && [[ -z "$IM" ]]; then
  echo "warning: ImageMagick not found → skipping .ico/og-image"
  DO_ICO=0; OG_SRC=""
fi

INK_VER="$($INK --version 2>/dev/null | head -n1 || true)"

png_from_svg () {
  local src="$1" out="$2" w="$3" h="${4:-$3}"
  if [[ "$INK_VER" =~ Inkscape\ 0\.[0-9] ]]; then
    "$INK" "$src" --export-png="$out" --export-width="$w" --export-height="$h" >/dev/null
  else
    "$INK" "$src" --export-type=png --export-filename="$out" -w "$w" -h "$h" >/dev/null
  fi
}

plain_svg () {
  local src="$1" out="$2"
  "$INK" "$src" --export-plain-svg="$out" >/dev/null
}

echo "→ output: $OUT"

# essentials
plain_svg "$SRC" "$OUT/logo.svg"
png_from_svg "$SRC" "$OUT/favicon-32x32.png" 32
png_from_svg "$SRC" "$OUT/apple-touch-icon.png" 180
: > "$OUT/.nojekyll"

# optional: .ico
if [[ $DO_ICO -eq 1 ]]; then
  png_from_svg "$SRC" "$OUT/favicon-16x16.png" 16
  png_from_svg "$SRC" "$OUT/favicon-48.png" 48
  $IM "$OUT/favicon-16x16.png" "$OUT/favicon-32x32.png" "$OUT/favicon-48.png" "$OUT/favicon.ico"
  rm -f "$OUT/favicon-48.png"
fi

# optional: PWA icons
if [[ $DO_PWA -eq 1 ]]; then
  png_from_svg "$SRC" "$OUT/logo-192x192.png" 192
  png_from_svg "$SRC" "$OUT/logo-512x512.png" 512
  png_from_svg "$SRC" "$OUT/logo-maskable-192x192.png" 192
  png_from_svg "$SRC" "$OUT/logo-maskable-512x512.png" 512
fi

# optional: OG image from a dedicated banner (recommended)
if [[ -n "$OG_SRC" && -f "$OG_SRC" ]]; then
  TMP="$OUT/.ogtmp.png"
  case "$OG_SRC" in
    *.svg) png_from_svg "$OG_SRC" "$TMP" 1200 630 ;;
    *)     cp "$OG_SRC" "$TMP" ;;
  esac
  $IM "$TMP" -resize 1200x630^ -gravity center -extent 1200x630 "$OUT/og-1200x630.png"
  rm -f "$TMP"
fi

echo "done."
