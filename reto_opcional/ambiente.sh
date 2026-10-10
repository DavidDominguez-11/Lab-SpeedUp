#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
{
    date -Iseconds
    gcc --version | head -n 1
    lscpu | grep -E 'Model name:|CPU\(s\):|Thread\(s\) per core:|Core\(s\) per socket:|L2 cache:|L3 cache:'
    lscpu -C
    lscpu -e=CPU,CORE,SOCKET,ONLINE
    sha256sum reto_opcional/lab12_speedup.c reto_opcional/lab12_reto
} > reto_opcional/ambiente.txt
