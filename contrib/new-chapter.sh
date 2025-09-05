#!/usr/bin/env bash
set -euo pipefail

read -p "Language code (ca/es/en): " -e LANG
read -p "Chapter title: " -e TITLE
read -p "Weight (order, integer): " -e WEIGHT

# normalitza el nom de fitxer
SLUG=$(echo -n "$TITLE" | sed 's/ /-/g' | tr "[:upper:]" "[:lower:]" | sed 's/[^a-z0-9-]//g')

# directori de sortida
OUTDIR="_chapters/$LANG"
mkdir -p "$OUTDIR"

FILENAME="$OUTDIR/$WEIGHT-$SLUG.md"

if [ -f "$FILENAME" ]; then
  echo "File already exists: $FILENAME"
else
  TODAY=$(date +%Y-%m-%d)
  cat > "$FILENAME" <<EOF
---
lang: $LANG
permalink: /:title/$LANG/
title: $TITLE
author: Benito Zaragozí
date: $TODAY
category: guia
weight: $WEIGHT
layout: chapter
mermaid: false
---

# $TITLE

Esborrany del capítol.
EOF
  echo "Created new chapter draft: $FILENAME"
fi

# obre amb l’editor gràfic si vols
gedit "$FILENAME" 2>/dev/null || true
