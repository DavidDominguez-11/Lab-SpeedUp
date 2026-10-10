#!/usr/bin/env bash
# Reproduce las mediciones; sobreescribe los CSV existentes con nuevas corridas.
set -euo pipefail
cd "$(dirname "$0")/.."
gcc -O2 -Wall -Wextra -fopenmp -o reto_opcional/lab12_reto reto_opcional/lab12_speedup.c -lm
bash reto_opcional/explorar.sh
bash reto_opcional/confirmar.sh
bash reto_opcional/ambiente.sh
printf 'Mediciones guardadas. En Windows, regenere tablas e informe con: python reto_opcional/generar_informe.py\n' >&2
