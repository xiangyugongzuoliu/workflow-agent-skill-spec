#!/usr/bin/env bash
set -euo pipefail

target="${1:?target required}"
output="${2:?output json required}"

if [ ! -d "$target" ]; then
  printf '{"ok":false,"err":"target directory does not exist","recoverable":true}\n'
  exit 1
fi

mkdir -p "$(dirname "$output")"

file_count="$(find "$target" -maxdepth 4 -type f | wc -l | tr -d ' ')"
private_hits="$(grep -RInE '(/Users/|~/Downloads|token|secret|password|cookie|api_key|apikey)' "$target" 2>/dev/null | sed 's/"/\\"/g' || true)"
destructive_hits="$(grep -RInE '(rm -rf|git push|npm publish|curl .*-d|scp |rsync .*--delete)' "$target" 2>/dev/null | sed 's/"/\\"/g' || true)"

{
  printf '{\n'
  printf '  "ok": true,\n'
  printf '  "file_count": %s,\n' "$file_count"
  printf '  "private_pattern_hits": [\n'
  if [ -n "$private_hits" ]; then
    printf '%s\n' "$private_hits" | awk '{printf "    \"%s\"%s\n", $0, (NR==line_count ? "" : ",")}' line_count="$(printf '%s\n' "$private_hits" | wc -l | tr -d ' ')"
  fi
  printf '  ],\n'
  printf '  "destructive_hits": [\n'
  if [ -n "$destructive_hits" ]; then
    printf '%s\n' "$destructive_hits" | awk '{printf "    \"%s\"%s\n", $0, (NR==line_count ? "" : ",")}' line_count="$(printf '%s\n' "$destructive_hits" | wc -l | tr -d ' ')"
  fi
  printf '  ],\n'
  printf '  "skipped_checks": []\n'
  printf '}\n'
} > "$output"

printf '{"ok":true,"output":"%s","file_count":%s}\n' "$output" "$file_count"
