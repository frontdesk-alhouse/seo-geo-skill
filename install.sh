#!/usr/bin/env bash
# Instala el skill seo-geo en Claude Code. / Installs the seo-geo skill in Claude Code.
# Uso: desde la carpeta del repo clonado, `bash install.sh` (español, por defecto)
# Usage: from the cloned repo folder, `bash install.sh --lang en` (English edition)
# Idempotente: se puede correr de nuevo para actualizar o para cambiar de idioma.

set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/seo-geo"
LANG_CHOICE="es"

# Archivos que cambian según el idioma; se borran al cambiar de edición.
LANG_SPECIFIC=(references templates examples SKILL.md checklist-lanzamiento.md launch-checklist.md README.en.md CHANGELOG.md install.sh .gitignore)

# Nombres viejos que ya no existen; se borran siempre. / Old names, always removed.
LEGACY=(webflow-hygiene-checklist.md)

usage() {
  echo "Uso / Usage: bash install.sh [--lang es|en]" >&2
}

while [ $# -gt 0 ]; do
  case "$1" in
    --lang) [ $# -ge 2 ] || { usage; exit 2; }; LANG_CHOICE="$2"; shift 2 ;;
    --lang=*) LANG_CHOICE="${1#--lang=}"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Error: argumento no reconocido / unknown argument: $1" >&2; usage; exit 2 ;;
  esac
done

case "$LANG_CHOICE" in
  es) EDITION="$SRC" ;;
  en) EDITION="$SRC/en" ;;
  *) echo "Error: --lang debe ser es o en / --lang must be es or en (got '$LANG_CHOICE')." >&2; exit 2 ;;
esac

if [ ! -f "$EDITION/SKILL.md" ]; then
  echo "Error: no encuentro / cannot find $EDITION/SKILL.md." >&2
  exit 1
fi

# Idioma instalado antes: .lang si existe; si no, español cuando ya hay un SKILL.md.
previous_lang() {
  if [ -f "$DEST/.lang" ]; then
    tr -d '[:space:]' < "$DEST/.lang"
  elif [ -f "$DEST/SKILL.md" ]; then
    echo "es"
  fi
}

remove_legacy() {
  local item
  for item in "${LEGACY[@]}"; do
    rm -rf "${DEST:?}/$item"
  done
}

remove_stale() {
  local item
  for item in "${LANG_SPECIFIC[@]}"; do
    rm -rf "${DEST:?}/$item"
  done
}

copy_es() {
  local item
  for item in "$SRC"/* "$SRC"/.[!.]*; do
    [ -e "$item" ] || continue
    case "$(basename "$item")" in
      .git|.github|.DS_Store|.lang|en) continue ;;
    esac
    cp -R "$item" "$DEST/"
  done
  rm -f "$DEST/.lang"
}

copy_en() {
  local item
  for item in "$SRC/en"/* "$SRC/en"/.[!.]*; do
    [ -e "$item" ] || continue
    case "$(basename "$item")" in
      .DS_Store|.lang) continue ;;
    esac
    cp -R "$item" "$DEST/"
  done
  cp -R "$SRC/scripts" "$DEST/"
  cp "$SRC/LICENSE" "$DEST/LICENSE"
  cp "$SRC/README.en.md" "$DEST/README.md"
  printf 'en\n' > "$DEST/.lang"
}

if [ "$SRC" = "$DEST" ]; then
  echo "El skill ya está en $DEST. Nada que copiar. / The skill is already in $DEST."
else
  mkdir -p "$DEST"
  PREV="$(previous_lang)"
  if [ -n "$PREV" ] && [ "$PREV" != "$LANG_CHOICE" ]; then
    remove_stale
  fi
  remove_legacy
  if [ "$LANG_CHOICE" = "en" ]; then copy_en; else copy_es; fi
  rm -rf "$DEST/scripts/__pycache__"
  if [ "$LANG_CHOICE" = "en" ]; then
    echo "Skill (English edition) copied to $DEST"
  else
    echo "Skill copiado a $DEST"
  fi
fi

if command -v python3 >/dev/null 2>&1; then
  if [ "$LANG_CHOICE" = "en" ]; then
    echo "python3 found: $(python3 --version 2>&1). The scripts need no dependencies."
  else
    echo "python3 encontrado: $(python3 --version 2>&1). Los scripts no necesitan dependencias."
  fi
elif [ "$LANG_CHOICE" = "en" ]; then
  echo "Warning: python3 not found. The skill works, but the scripts in scripts/ need it." >&2
else
  echo "Aviso: no encontré python3. El skill funciona, pero los scripts de scripts/ lo necesitan." >&2
fi

chmod +x "$DEST"/scripts/*.py 2>/dev/null || true

if [ "$LANG_CHOICE" = "en" ]; then
cat <<'USAGE'

Done. In Claude Code:

  /seo-geo medical https://example.com            build and launch (steps 1 to 6)
  /seo-geo saas https://example.com --gate        launch gate only
  /seo-geo generic https://example.com --measure  citation measurement in AI assistants

Standalone scripts (they print English; override with --lang es):

  python3 ~/.claude/skills/seo-geo/scripts/check_html_crudo.py --help
USAGE
else
cat <<'USAGE'

Listo. En Claude Code:

  /seo-geo medical https://ejemplo.com            construir y lanzar (pasos 1 a 6)
  /seo-geo saas https://ejemplo.com --gate        solo el gate de lanzamiento
  /seo-geo generic https://ejemplo.com --medir    medición de citación en asistentes

Scripts sueltos:

  python3 ~/.claude/skills/seo-geo/scripts/check_html_crudo.py --help
USAGE
fi
