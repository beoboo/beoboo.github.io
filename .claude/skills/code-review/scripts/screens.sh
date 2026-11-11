#!/usr/bin/env bash
# Render the page in headless Chrome as the reviewers need to see it:
# full-height slices at phone, tablet and desktop widths in the site's one dark
# theme (add "<width> light" configs if a light theme returns), plus the print
# stylesheet as a PDF.
#
#   screens.sh <repo> <out-dir> [page]        page defaults to index.html
#
# Writes <out>/<width>-<theme>-<nn>.png (slices of 1600px, top to bottom),
# <out>/print.pdf and <out>/screens.txt (what was rendered, page heights).
# Chrome's headless window cannot be narrower than ~500px, so every page is
# rendered inside an iframe of the exact width; slices are taken by moving
# the iframe up, so no image library is needed.
set -euo pipefail

repo=$(cd "$1" && pwd)
out=$2
page=${3:-index.html}
mkdir -p "$out"

chrome="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
[ -x "$chrome" ] || { echo "Chrome not found at $chrome" >&2; exit 1; }
url="file://$repo/$page"
slice=1600
log="$out/screens.txt"
: > "$log"

# theme: light = preferredColorScheme 1, dark = 0
render() {
  local width=$1 theme=$2 scheme
  [ "$theme" = dark ] && scheme=0 || scheme=1

  # 1. measure the page height at this width
  cat > "$out/.measure.html" <<EOF
<!doctype html><html><body><iframe id="f" src="$url" style="width:${width}px;height:900px;border:0"></iframe>
<pre id="o">pending</pre><script>
document.getElementById('f').onload=function(){var o=document.getElementById('o'),d;try{d=this.contentWindow.document}catch(e){o.textContent='ERR '+e;return}
// measure after the web fonts load, or the page is measured at its fallback-font height
d.fonts.ready.then(function(){o.textContent='H='+d.documentElement.scrollHeight})}
</script></body></html>
EOF
  local height
  height=$("$chrome" --headless=new --disable-gpu --allow-file-access-from-files \
      --blink-settings=preferredColorScheme=$scheme --virtual-time-budget=4000 \
      --dump-dom "file://$out/.measure.html" 2>/dev/null | sed -n 's/.*<pre id="o">H=\([0-9]*\).*/\1/p')
  [ -n "$height" ] || { echo "$width $theme: could not measure height" >> "$log"; return; }

  # 2. slice it
  local win=$(( width > 500 ? width : 500 )) n=0 offset=0
  while [ "$offset" -lt "$height" ]; do
    cat > "$out/.slice.html" <<EOF
<!doctype html><html><body style="margin:0;background:#808080">
<div style="width:${width}px;height:${slice}px;overflow:hidden"><iframe src="$url" style="width:${width}px;height:${height}px;border:0;display:block;margin-top:-${offset}px"></iframe></div>
</body></html>
EOF
    "$chrome" --headless=new --disable-gpu --hide-scrollbars --allow-file-access-from-files \
      --blink-settings=preferredColorScheme=$scheme --virtual-time-budget=4000 \
      --window-size=$win,$slice --screenshot="$out/$width-$theme-$(printf %02d $n).png" \
      "file://$out/.slice.html" >/dev/null 2>&1
    n=$((n + 1)); offset=$((offset + slice))
  done
  echo "$width $theme: page ${height}px, $n slices (${width}-${theme}-00..$(printf %02d $((n - 1))).png)" >> "$log"
}

for cfg in "320 dark" "375 dark" "768 dark" "1440 dark"; do
  # shellcheck disable=SC2086
  render $cfg
done

"$chrome" --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=4000 \
  --print-to-pdf="$out/print.pdf" "$url" >/dev/null 2>&1 && echo "print: print.pdf" >> "$log"
rm -f "$out/.measure.html" "$out/.slice.html"
cat "$log"
