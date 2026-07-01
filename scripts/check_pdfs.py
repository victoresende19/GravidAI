#!/usr/bin/env python3
"""
Lista e valida PDFs no diretório ./data/ — simples checagem sem dependências do projeto.
Uso: python scripts/check_pdfs.py
"""
import os
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / 'data'

if not DATA_DIR.exists():
    print(f"Pasta não existe: {DATA_DIR}")
    raise SystemExit(1)

pdfs = [p for p in DATA_DIR.iterdir() if p.is_file() and p.suffix.lower() == '.pdf']
if not pdfs:
    print(f"Nenhum PDF encontrado em {DATA_DIR}")
    raise SystemExit(2)

print(f"Encontrados {len(pdfs)} PDF(s) em {DATA_DIR}:\n")
for p in pdfs:
    size = p.stat().st_size
    print(f"- {p.name} — {size} bytes")

print('\nCheque concluído.')
