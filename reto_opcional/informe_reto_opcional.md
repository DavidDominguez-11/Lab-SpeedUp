# Reto opcional: comprobación de un speedup superlineal aparente

**Resultado:** los valores aislados con S > p no fueron repetibles según el criterio fijado antes de confirmar. No se afirma un speedup superlineal real.

## Equipo y método

AMD Ryzen 5 4600H, 6 núcleos físicos/12 lógicos; L2 512 KiB por núcleo y L3 4 MiB según `lscpu` de Ubuntu 24.04 en WSL. GCC con `-O2 -Wall -Wextra -fopenmp`. Se fijaron los hilos a CPUs lógicas pares (núcleos físicos distintos) con `taskset` y `OMP_PROC_BIND=spread OMP_PLACES=threads`. Se usó exactamente el mismo arreglo y número de sumas secuenciales/paralelas. El código comprueba las sumas con error relativo <= 1e-10 y alterna el orden de medición en cada par. `S=t_seq/t_par`, calculado con tiempos crudos.

El criterio previo fue exigir mediana S > p en **cinco procesos independientes** para la misma configuración. Se hicieron diez procesos independientes por cada uno de dos tamaños; cada proceso produjo cinco pares de tiempos (100 pares de confirmación en total).

## Barrido exploratorio

11 tamaños por p=2,4,6: 33 configuraciones, cinco pares cada una. Las únicas medianas que superaron p fueron: N=393216, p=2, S=2.0035; N=524288, p=2, S=2.0006. Esos candidatos se eligieron para confirmación; el barrido no constituye prueba independiente.

## Confirmación

| N | p | Pares | Mediana global S | Pares con S>p | Corridas con mediana S>p |
|---:|---:|---:|---:|---:|---:|
| 393216 | 2 | 50 | 1.9917 | 20/50 | 4/10 |
| 524288 | 2 | 50 | 1.9727 | 18/50 | 2/10 |

| N | Corrida | Mediana S | Mínimo S | Máximo S | Pares con S>2 |
|---:|---:|---:|---:|---:|---:|
| 393216 | 1 | 1.9738 | 1.9193 | 2.0303 | 1/5 |
| 393216 | 2 | 2.0528 | 1.7274 | 2.1446 | 3/5 |
| 393216 | 3 | 1.9305 | 1.9254 | 2.0034 | 1/5 |
| 393216 | 4 | 2.0122 | 1.9309 | 2.0374 | 3/5 |
| 393216 | 5 | 1.9917 | 1.8740 | 2.1319 | 2/5 |
| 393216 | 6 | 1.9586 | 1.9390 | 2.0634 | 1/5 |
| 393216 | 7 | 2.0142 | 1.9810 | 2.0328 | 3/5 |
| 393216 | 8 | 1.9917 | 1.9136 | 2.0946 | 1/5 |
| 393216 | 9 | 2.0185 | 1.9518 | 2.0743 | 3/5 |
| 393216 | 10 | 1.9684 | 1.8502 | 2.0190 | 2/5 |
| 524288 | 1 | 1.9775 | 1.9126 | 2.0815 | 2/5 |
| 524288 | 2 | 1.9487 | 1.9061 | 2.0112 | 1/5 |
| 524288 | 3 | 1.9484 | 1.8918 | 2.1240 | 1/5 |
| 524288 | 4 | 1.9757 | 1.9125 | 2.0383 | 2/5 |
| 524288 | 5 | 1.9637 | 1.8873 | 2.0904 | 1/5 |
| 524288 | 6 | 1.9289 | 1.8455 | 2.0762 | 2/5 |
| 524288 | 7 | 1.9549 | 1.8873 | 2.0188 | 1/5 |
| 524288 | 8 | 1.9541 | 1.8654 | 2.0232 | 2/5 |
| 524288 | 9 | 2.0382 | 1.9730 | 2.0565 | 3/5 |
| 524288 | 10 | 2.0074 | 1.8134 | 2.0723 | 3/5 |

## Interpretación

Los dos casos del barrido cruzaron p por un margen cercano al ruido de medición. En la confirmación, varias corridas y la mediana global quedaron por debajo de 2. Por ello, los picos individuales no cumplen el criterio de repetibilidad del reto. Esto demuestra que el S>p observado en el barrido era aparente bajo este protocolo; no prueba que ningún otro programa o equipo pueda lograr S>p.

La hipótesis de caché tampoco explica esos picos: N=393216 ocupa 3 MiB y N=524288 ocupa 4 MiB; cada mitad para p=2 ocupa 1.5 o 2 MiB, más que los 512 KiB de L2 privada. En tamaños donde cada mitad sí cabe en L2, el barrido no mostró una mediana S>2. La fluctuación de frecuencia, planificación o estado de caché es una explicación plausible de la dispersión, pero este experimento no identifica su causa exacta.

## Reproducción y archivos

`explorar.sh` y `confirmar.sh` ejecutan el binario compilado desde la copia `lab12_speedup.c` del reto. `exploracion.csv` y `confirmacion.csv` guardan cada par crudo; `resumen_corridas.csv` se genera de estos datos. `ambiente.txt` registra la topología, versión de GCC y SHA-256. `confirmacion.stderr.txt` conserva un checksum por proceso. Para regenerar este informe: `python reto_opcional/generar_informe.py`.

Limitación: WSL comparte recursos con Windows; la carga y la frecuencia del CPU no se controlaron externamente. La conclusión se restringe a estas configuraciones y corridas.
