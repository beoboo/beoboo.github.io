#!/usr/bin/env bash
# Collect the sources the content lens checks the page against.
#
#   sources.sh <repo> <out-dir>
#
# - the README and metadata of every GitHub repo the page links to
#   (beoboo/* and other owners), via the gh CLI;
# - the live Music Practice Tracker landing page, as text;
# - the CV PDF, which is kept OUT of the public repo: pass its path as
#   CV_PDF=<path>; the lens reads it itself.
set -uo pipefail
repo=$(cd "$1" && pwd)
out=$2
mkdir -p "$out"

grep -oE 'https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+' "$repo/index.html" | sort -u | while read -r url; do
  slug=${url#https://github.com/}
  file="$out/readme-${slug//\//__}.md"
  {
    gh api "repos/$slug" --jq '"# \(.full_name) — \(.description // "no description") (\(.language // "-"), pushed \(.pushed_at[0:10]), \(.visibility))"' 2>&1
    gh api "repos/$slug/readme" --jq '.content' 2>/dev/null | base64 -d 2>/dev/null || echo "(no README)"
  } > "$file"
  echo "repo   $slug -> $file"
done

app="https://music-tracker-data.web.app/"
if curl -s --max-time 15 "$app" -o "$out/music-tracker-landing.html"; then
  sed -E 's/<script.*<\/script>//g; s/<[^>]+>/ /g' "$out/music-tracker-landing.html" | tr -s ' \n' > "$out/music-tracker-landing.txt"
  echo "app    $app -> $out/music-tracker-landing.txt"
fi

if [ -n "${CV_PDF:-}" ] && [ -e "$CV_PDF" ]; then
  echo "cv     $CV_PDF (read it with the Read tool)"
else
  echo "cv     none: ask the user for the current CV (it is not published); until then the last report is the record of what was confirmed"
fi
