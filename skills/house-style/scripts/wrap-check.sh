#!/bin/sh
# Names each Markdown line over 100 characters, as FILE:LINE, and exits 1 if it names any.
# Usage: wrap-check.sh FILE...   such as: git ls-files -z '*.md' | xargs -0 wrap-check.sh
#
# Left out: frontmatter, fenced code and table rows. URLs aren't counted, so only a URL that
# pushes a line past 100 lets it run long. A fence closes only on its own mark, as long or
# longer, so a block can hold a shorter fence. LC_ALL=C makes every awk count bytes, and
# dropping UTF-8's continuation bytes leaves one per character.
LC_ALL=C
export LC_ALL
exec awk '
  FNR == 1 { fence = ""; front = /^---$/; if (front) next }
  front { if (/^---$/) front = 0; next }
  match($0, /^ *(```+|~~~+)/) {
    mark = substr($0, RSTART, RLENGTH); sub(/^ */, "", mark)
    if (fence == "") { fence = mark; next }
    if (substr(mark, 1, 1) == substr(fence, 1, 1) && length(mark) >= length(fence) &&
        /^ *[`~]+ *$/) { fence = ""; next }
  }
  fence != "" || /^ *\|/ { next }
  { line = $0; gsub(/https?:\/\/[^ )>]+/, "", line); gsub(/[\200-\277]/, "", line) }
  length(line) > 100 { print FILENAME ":" FNR; found = 1 }
  END { exit found }
' "$@"
