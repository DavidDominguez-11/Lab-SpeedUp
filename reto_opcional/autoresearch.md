# Reto opcional: experimento acotado

Hipótesis: un arreglo que supera la caché privada de un núcleo, dividido entre varios
núcleos físicos, podría dar S > p por efectos de memoria. Se prueban 11 tamaños de
32 Ki a 2 Mi elementos y p=2,4,6. El criterio para afirmar S > p exige cinco
ejecuciones independientes bajo el mismo código y configuración, cada una con
cinco pares de mediciones, y mediana S > p en todas. Se publicarán también los
resultados que contradigan la hipótesis. Ningún resultado se copiará al informe
principal ni a `Entrega` sin evidencia.

Compilación: `gcc -O2 -Wall -Wextra -fopenmp -o reto_opcional/lab12_reto reto_opcional/lab12_speedup.c -lm`.
Afinidad: CPUs lógicas pares 0,2,4,6,8,10 (un hilo por núcleo físico según `lscpu -e`).
Variables: `OMP_PROC_BIND=spread OMP_PLACES=threads`. El orden de las fases
secuencial/paralela se alterna en cada par. Se verifica igualdad de sumas con
error relativo <= 1e-10.

## Resultado observado

El barrido (33 configuraciones, 5 pares cada una) produjo dos medianas
aparentemente superlineales: N=393216, p=2, S=2.0035 y N=524288, p=2,
S=2.0006. Al repetir cada caso en diez procesos independientes con cinco pares
por proceso, solo 4/10 y 2/10 procesos, respectivamente, mantuvieron una mediana
S>2. Las medianas agregadas fueron 1.9917 y 1.9727. Se rechaza la hipótesis de
speedup superlineal reproducible para estas configuraciones. Los datos completos
están en `exploracion.csv` y `confirmacion.csv`; el informe se genera directamente
de esos datos. `autoresearch.sh` recompila y repite las mediciones; el PDF se
regenera en Windows con `python reto_opcional/generar_informe.py` y ReportLab.
