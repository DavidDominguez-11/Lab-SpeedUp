### ✅ Entregables del Laboratorio

Cada pareja deberá entregar 4 archivos:

1. `reporte_lab12.pdf`
   - Datos del equipo: modelo de CPU, núcleos físicos y lógicos, núcleos de rendimiento/eficiencia, Hyper-Threading.
   - Predicción escrita antes de cada experimento y comparación con lo medido.
   - Tabla de la Parte 1 completa y cálculo a mano de S, E, C y F para al menos dos filas.
   - Respuestas numeradas de las Partes 1 a 4, incluidos los dos modelos que dedujeron.
   - Síntesis: qué fuga (η_f, η_c, η_b, η_r) explica la pérdida de cada parte, con el número medido, y qué no encaja en ninguna.

2. `evidencia_lab12.pdf`
   - Capturas de la salida de `lscpu` o `sysctl` con los datos del equipo.
   - Capturas de la compilación (`make`) y de la ejecución de cada uno de los 4 modos (`amdahl`, `suma`, `desbalance`, `gustafson`).
   - Las 7 gráficas generadas por `graficar.py`.

3. `resultados_lab12.zip`
   - Los 10 CSV originales: 5 de `amdahl`, 1 de `suma`, 3 de `desbalance` y 1 de `gustafson`.
   - Los archivos `*_con_S_E.csv` generados por `graficar.py`.

4. `lab12_speedup.c` *(solo si hacen el reto opcional)*
   - Versión modificada para buscar speedup superlineal, con comentarios que expliquen qué cambiaron y por qué.
   - Al menos 5 corridas que muestren que el resultado se repite.

**Entrega:** Por Canva.