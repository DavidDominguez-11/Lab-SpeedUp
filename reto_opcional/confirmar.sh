#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export OMP_PROC_BIND=spread OMP_PLACES=threads
out=reto_opcional/confirmacion.csv
err=reto_opcional/confirmacion.stderr.txt
printf 'corrida,modo,N,p,param,t_seq,t_par,t_parte_seq\n' > "$out"
: > "$err"
for corrida in {1..10}; do
    for n in 393216 524288; do
        # Una invocacion nueva por corrida y por tamaño: no se reutiliza el proceso.
        taskset -c 0,2 ./reto_opcional/lab12_reto reto "$n" 2 100 \
            2>> "$err" | tail -n +2 | sed "s/^/$corrida,/" >> "$out"
    done
done
