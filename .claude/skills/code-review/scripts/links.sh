#!/usr/bin/env bash
# Every link on the page, followed, plus what the live site serves.
#
#   links.sh <repo> [page]
#
# External links: final HTTP status after redirects. LinkedIn answers bots
# with 999 — that is its bot wall, not a broken link. Local files: present
# or missing. Then the live site: the page, robots.txt, sitemap.xml, a
# missing path (should be a 404 with the site's own page), and headers.
set -uo pipefail
repo=$(cd "$1" && pwd)
page=${2:-index.html}
site="https://beoboo.github.io"
ua="Mozilla/5.0 (compatible; site-review-link-check)"

echo "[links on $page]"
grep -oE '(href|src)="[^"]+"' "$repo/$page" | sed -E 's/^(href|src)="//; s/"$//' | sort -u | while read -r url; do
  case "$url" in
    http://*|https://*)
      code=$(curl -s -o /dev/null -L --max-time 15 -A "$ua" -w '%{http_code}' "$url")
      echo "  $code  $url" ;;
    mailto:*) echo "  mail $url" ;;
    \#*) ;;   # anchors are checked by scan.py
    data:*) echo "  data (inline)" ;;
    *) [ -e "$repo/${url%%[#?]*}" ] && echo "  file $url" || echo "  MISSING $url" ;;
  esac
done

echo "[live site]"
for path in / /robots.txt /sitemap.xml /this-page-does-not-exist; do
  code=$(curl -s -o /dev/null --max-time 15 -A "$ua" -w '%{http_code} %{content_type}' "$site$path")
  echo "  $code  $site$path"
done
echo "[live headers for /]"
curl -sI --max-time 15 -A "$ua" "$site/" | grep -iE '^(cache-control|content-type|content-encoding|last-modified|age|x-cache)' | sed 's/^/  /'
