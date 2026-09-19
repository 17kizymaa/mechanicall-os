#!/bin/sh
# alias-scaffold.sh — one standard folder per anphuni alias, from templates/alias/.
#
#   scripts/alias-scaffold.sh <alias> [--root DIR] [--templates DIR] [--dry-run]
#
# Creates  <root>/projects/<alias>/
#            POINTER.md  INTAKE.md  NOTES.md
#            MATERIAL/  PROPOSALS/OPENER.md  DELIVERED/  RECEIPTS/
#
# Rules (CURRENT.md share-urls-kit):
#   - idempotent: existing files are never overwritten (reported as "keep")
#   - never writes CURRENT.md (refuses if asked; no client CURRENT, no nested CURRENT)
#   - substitutes {alias} and {date} only; nothing else
#   - no mint, no deploy, no share, no rename, no delete
#
# Default root: $ANPHUNI_ROOT or ~/anphuni-project
set -eu

usage() { sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//'; exit "${1:-0}"; }

here=$(cd "$(dirname "$0")/.." && pwd)
root="${ANPHUNI_ROOT:-$HOME/anphuni-project}"
tpl="$here/templates/alias"
dry=0
alias_name=""

while [ $# -gt 0 ]; do
  case "$1" in
    -h|--help) usage 0 ;;
    --root) shift; root="$1" ;;
    --templates) shift; tpl="$1" ;;
    --dry-run) dry=1 ;;
    -*) echo "unknown flag: $1" >&2; usage 2 ;;
    *) if [ -z "$alias_name" ]; then alias_name="$1"; else echo "one alias at a time" >&2; exit 2; fi ;;
  esac
  shift
done

[ -n "$alias_name" ] || { echo "alias required" >&2; usage 2; }

# alias: lowercase slug only — memorable, non-sensitive, safe for folders/logs
case "$alias_name" in
  *[!a-z0-9-]*|-*|*-|'') echo "refuse: alias must match [a-z0-9-]+, no leading/trailing dash: '$alias_name'" >&2; exit 3 ;;
esac
case "$alias_name" in
  current|CURRENT) echo "refuse: '$alias_name' is not an alias" >&2; exit 3 ;;
esac

[ -d "$tpl" ] || { echo "templates dir missing: $tpl" >&2; exit 2; }
for f in POINTER.md INTAKE.md NOTES.md OPENER.md; do
  [ -f "$tpl/$f" ] || { echo "template missing: $tpl/$f" >&2; exit 2; }
done

dest="$root/projects/$alias_name"
today=$(date +%Y-%m-%d)

say() { printf '%s\n' "$*"; }
run() { if [ "$dry" -eq 1 ]; then say "  (dry) $*"; else "$@"; fi; }

mkd() {
  if [ -d "$1" ]; then say "keep  dir  $1"; else say "make  dir  $1"; run mkdir -p "$1"; fi
}

# render template -> target; never overwrite; never CURRENT.md
render() {
  src="$1"; out="$2"
  case "$(basename "$out")" in
    CURRENT.md) say "refuse     $out (never write CURRENT.md)"; return 0 ;;
  esac
  if [ -e "$out" ]; then say "keep  file $out"; return 0; fi
  say "write file $out"
  [ "$dry" -eq 1 ] && return 0
  sed -e "s/{alias}/$alias_name/g" -e "s/{date}/$today/g" "$src" > "$out.tmp.$$" && mv "$out.tmp.$$" "$out"
}

say "alias-scaffold: $alias_name -> $dest"
mkd "$dest"
for d in MATERIAL PROPOSALS DELIVERED RECEIPTS; do mkd "$dest/$d"; done
render "$tpl/POINTER.md" "$dest/POINTER.md"
render "$tpl/INTAKE.md"  "$dest/INTAKE.md"
render "$tpl/NOTES.md"   "$dest/NOTES.md"
render "$tpl/OPENER.md"  "$dest/PROPOSALS/OPENER.md"

if [ -e "$dest/CURRENT.md" ]; then
  say "FLAG  client CURRENT.md exists at $dest/CURRENT.md — not this kit's; CURRENT forbids nested/client CURRENT"
fi
say "done. no mint, no deploy, no share. Room id stays 'unminted' until the operator Next mints it."
