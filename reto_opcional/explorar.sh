#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export OMP_PROC_BIND=spread OMP_PLACES=threads
out=reto_opcional/exploracion.csv
printf 'modo,N,p,param,t_seq,t_par,t_parte_seq\n' > "$out"
for n in 32768 65536 98304 131072 196608 262144 393216 524288 786432 1048576 2097152; do
    r=$((20000000 / n))
    ((r < 30)) && r=30
    for p in 2 4 6; do
        case "$p" in
            2) cpus=0,2 ;;
            4) cpus=0,2,4,6 ;;
            6) cpus=0,2,4,6,8,10 ;;
        esac
        taskset -c "$cpus" ./reto_opcional/lab12_reto reto "$n" "$p" "$r" \
            | tail -n +2 >> "$out"
    done
done
