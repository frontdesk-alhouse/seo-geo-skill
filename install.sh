#!/usr/bin/env bash
# Instala el skill seo-geo en Claude Code.
# Uso: desde la carpeta del repo clonado, `bash install.sh`
# Idempotente: se puede correr de nuevo para actualizar.

set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/seo-geo"

if [ ! -f "$SRC/SKILL.md" ]; then
  echo "Error: no encuentro SKILL.md junto a install.sh ($SRC)." >&2
  exit 1
fi

if [ "$SRC" = "$DEST" ]; then
  echo "El skill ya está en $DEST. Nada que copiar."
else
  mkdir -p "$DEST"
  # Copia el contenido (no la carpeta .git) sobre la instalación anterior.
  for item in "$SRC"/* "$SRC"/.[!.]*; do
    [ -e "$item" ] || continue
    case "$(basename "$item")" in
      .git|.github|.DS_Store) continue ;;
    esac
    cp -R "$item" "$DEST/"
  done
  echo "Skill copiado a $DEST"
fi

if command -v python3 >/dev/null 2>&1; then
  echo "python3 encontrado: $(python3 --version 2>&1). Los scripts no necesitan dependencias."
else
  echo "Aviso: no encontré python3. El skill funciona, pero los scripts de scripts/ lo necesitan." >&2
fi

chmod +x "$DEST"/scripts/*.py 2>/dev/null || true

cat <<'EOF'

Listo. En Claude Code:

  /seo-geo medical https://ejemplo.com            construir y lanzar (pasos 1 a 6)
  /seo-geo saas https://ejemplo.com --gate        solo el gate de lanzamiento
  /seo-geo generic https://ejemplo.com --medir    medición de citación en asistentes

Scripts sueltos:

  python3 ~/.claude/skills/seo-geo/scripts/check_html_crudo.py --help
EOF
