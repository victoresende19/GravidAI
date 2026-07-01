#!/usr/bin/env bash
set -euo pipefail

# Script para baixar a cartilha para ./data/
DATA_DIR="$(dirname "$0")/../data"
TARGET_DIR="/workspaces/demand-1/repository/data"
URL="https://www.defensoria.df.gov.br/wp-content/uploads/2023/01/Cartilha-Os-Direitos-da-Crianca-e-do-Adolescente.pdf"
OUT_FILE="$TARGET_DIR/direitos_crianca_adolescente.pdf"

mkdir -p "$TARGET_DIR"

echo "Baixando cartilha para $OUT_FILE"
if command -v curl >/dev/null 2>&1; then
  curl -fSL "$URL" -o "$OUT_FILE"
  echo "Download concluído"
else
  echo "curl não encontrado. Baixe manualmente: $URL"
  exit 1
fi
