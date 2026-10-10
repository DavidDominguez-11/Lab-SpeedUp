#!/usr/bin/env python3
"""Genera el informe y las tablas directamente desde los CSV medidos."""
import csv
import statistics as stats
from collections import defaultdict
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

BASE = Path(__file__).resolve().parent
RAW = BASE / "confirmacion.csv"
SWEEP = BASE / "exploracion.csv"

groups = defaultdict(list)
with RAW.open(newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        key = int(row["N"]), int(row["p"]), int(row["corrida"])
        groups[key].append(float(row["t_seq"]) / float(row["t_par"]))
if len(groups) != 20 or any(len(v) != 5 for v in groups.values()):
    raise ValueError("Se esperaban 10 corridas independientes x 2 tamaños x 5 pares")

summary = []
for (n, p, run), values in sorted(groups.items()):
    summary.append((n, p, run, len(values), stats.median(values),
                    min(values), max(values), sum(v > p for v in values)))
with (BASE / "resumen_corridas.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["N", "p", "corrida", "pares", "mediana_S", "min_S", "max_S", "pares_S_mayor_p"])
    writer.writerows(summary)

sweep_groups = defaultdict(list)
with SWEEP.open(newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        n, p = int(row["N"]), int(row["p"])
        sweep_groups[n, p].append(float(row["t_seq"]) / float(row["t_par"]))
if len(sweep_groups) != 33 or any(len(v) != 5 for v in sweep_groups.values()):
    raise ValueError("Barrido incompleto: se esperaban 33 configuraciones x 5 pares")
apparent = [(n, p, stats.median(v)) for (n, p), v in sorted(sweep_groups.items())
            if stats.median(v) > p]

aggregates = {}
for n in (393216, 524288):
    values = [x for (nn, _, _), vv in groups.items() if nn == n for x in vv]
    runs_above = sum(r[4] > 2 for r in summary if r[0] == n)
    aggregates[n] = (stats.median(values), min(values), max(values),
                     sum(v > 2 for v in values), runs_above)

lines = [
    "# Reto opcional: comprobación de un speedup superlineal aparente",
    "",
    "**Resultado:** los valores aislados con S > p no fueron repetibles según el criterio fijado antes de confirmar. "
    "No se afirma un speedup superlineal real.",
    "",
    "## Equipo y método",
    "",
    "AMD Ryzen 5 4600H, 6 núcleos físicos/12 lógicos; L2 512 KiB por núcleo y L3 4 MiB "
    "según `lscpu` de Ubuntu 24.04 en WSL. GCC con `-O2 -Wall -Wextra -fopenmp`. "
    "Se fijaron los hilos a CPUs lógicas pares (núcleos físicos distintos) con `taskset` y "
    "`OMP_PROC_BIND=spread OMP_PLACES=threads`. Se usó exactamente el mismo arreglo y número "
    "de sumas secuenciales/paralelas. El código comprueba las sumas con error relativo <= 1e-10 "
    "y alterna el orden de medición en cada par. `S=t_seq/t_par`, calculado con tiempos crudos.",
    "",
    "El criterio previo fue exigir mediana S > p en **cinco procesos independientes** para la "
    "misma configuración. Se hicieron diez procesos independientes por cada uno de dos tamaños; "
    "cada proceso produjo cinco pares de tiempos (100 pares de confirmación en total).",
    "",
    "## Barrido exploratorio",
    "",
    "11 tamaños por p=2,4,6: 33 configuraciones, cinco pares cada una. Las únicas medianas "
    "que superaron p fueron: " + "; ".join(f"N={n}, p={p}, S={s:.4f}" for n, p, s in apparent) + ". "
    "Esos candidatos se eligieron para confirmación; el barrido no constituye prueba independiente.",
    "",
    "## Confirmación",
    "",
    "| N | p | Pares | Mediana global S | Pares con S>p | Corridas con mediana S>p |",
    "|---:|---:|---:|---:|---:|---:|",
]
for n, (median, low, high, count, runs_above) in aggregates.items():
    lines.append(f"| {n} | 2 | 50 | {median:.4f} | {count}/50 | {runs_above}/10 |")
lines += [
    "",
    "| N | Corrida | Mediana S | Mínimo S | Máximo S | Pares con S>2 |",
    "|---:|---:|---:|---:|---:|---:|",
]
for n, p, run, count, median, low, high, above in summary:
    lines.append(f"| {n} | {run} | {median:.4f} | {low:.4f} | {high:.4f} | {above}/5 |")
lines += [
    "",
    "## Interpretación",
    "",
    "Los dos casos del barrido cruzaron p por un margen cercano al ruido de medición. "
    "En la confirmación, varias corridas y la mediana global quedaron por debajo de 2. "
    "Por ello, los picos individuales no cumplen el criterio de repetibilidad del reto. "
    "Esto demuestra que el S>p observado en el barrido era aparente bajo este protocolo; "
    "no prueba que ningún otro programa o equipo pueda lograr S>p.",
    "",
    "La hipótesis de caché tampoco explica esos picos: N=393216 ocupa 3 MiB y N=524288 "
    "ocupa 4 MiB; cada mitad para p=2 ocupa 1.5 o 2 MiB, más que los 512 KiB de L2 "
    "privada. En tamaños donde cada mitad sí cabe en L2, el barrido no mostró una mediana S>2. "
    "La fluctuación de frecuencia, planificación o estado de caché es una explicación plausible "
    "de la dispersión, pero este experimento no identifica su causa exacta.",
    "",
    "## Reproducción y archivos",
    "",
    "`explorar.sh` y `confirmar.sh` ejecutan el binario compilado desde la copia "
    "`lab12_speedup.c` del reto. `exploracion.csv` y `confirmacion.csv` guardan cada par crudo; "
    "`resumen_corridas.csv` se genera de estos datos. `ambiente.txt` registra la topología, "
    "versión de GCC y SHA-256. `confirmacion.stderr.txt` conserva un checksum por proceso. "
    "Para regenerar este informe: `python reto_opcional/generar_informe.py`.",
    "",
    "Limitación: WSL comparte recursos con Windows; la carga y la frecuencia del CPU no se "
    "controlaron externamente. La conclusión se restringe a estas configuraciones y corridas.",
]
(BASE / "informe_reto_opcional.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

styles = getSampleStyleSheet()
styles["Title"].fontSize = 14
styles["Title"].leading = 17
styles["Title"].spaceAfter = 7
styles["Heading2"].fontSize = 10
styles["Heading2"].spaceBefore = 7
styles["Heading2"].spaceAfter = 3
styles.add(ParagraphStyle(name="Tight", parent=styles["BodyText"], fontSize=8,
                          leading=10, spaceAfter=4))
styles.add(ParagraphStyle(name="SmallCenter", parent=styles["BodyText"], fontSize=8,
                          leading=9, alignment=TA_CENTER))
story = []
def para(value):
    story.append(Paragraph(value, styles["Tight"]))

story.append(Paragraph("Reto opcional: speedup superlineal aparente", styles["Title"]))
para("Resultado: los valores aislados S &gt; p no fueron repetibles. No se afirma un speedup superlineal real.")
story.append(Paragraph("Equipo y método", styles["Heading2"]))
para("AMD Ryzen 5 4600H: 6 núcleos físicos, 12 lógicos; L2 512 KiB por núcleo y L3 4 MiB "
     "(lscpu, Ubuntu 24.04 en WSL). GCC -O2 -Wall -Wextra -fopenmp. Afinidad a núcleos físicos "
     "distintos mediante taskset, OMP_PROC_BIND=spread y OMP_PLACES=threads.")
para("El arreglo y el número de sumas son iguales en ambos caminos. Se alterna el orden "
     "secuencial/paralelo y se comprueba error relativo &lt;= 1e-10. S=t_seq/t_par. "
     "Criterio previo: mediana S &gt; p en cinco procesos independientes para una misma configuración.")
story.append(Paragraph("Barrido y confirmación", styles["Heading2"]))
para("Barrido: 11 tamaños por p=2,4,6; 33 configuraciones y 165 pares. Solo dos medianas "
     "aparentes S &gt; p: " + "; ".join(f"N={n}, p={p}, S={s:.4f}" for n,p,s in apparent) + ".")
agg_table = [["N", "p", "Pares", "Mediana S", "S>p", "Corridas >p"]]
for n, (median, _, _, count, runs_above) in aggregates.items():
    agg_table.append([str(n), "2", "50", f"{median:.4f}", f"{count}/50", f"{runs_above}/10"])
def table(data, widths):
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#e5eaf0")),
        ("GRID", (0,0), (-1,-1), 0.3, colors.HexColor("#c9d1d9")),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("FONTSIZE", (0,0), (-1,-1), 7.5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
        ("TOPPADDING", (0,0), (-1,-1), 2),
    ]))
    return t
story.append(table(agg_table, [80,35,55,100,75,100]))
story.append(Spacer(1, 0.15*cm))
para("Cada tamaño se confirmó con 10 procesos independientes y 5 pares por proceso. "
     "La tabla siguiente conserva la mediana de cada proceso; los tiempos crudos están en confirmacion.csv.")
run_table = [["N", "Corrida", "Mediana S", "Mín. S", "Máx. S", "Pares S>2"]]
for n,p,run,count,median,low,high,above in summary:
    run_table.append([str(n), str(run), f"{median:.4f}", f"{low:.4f}",
                      f"{high:.4f}", f"{above}/5"])
story.append(table(run_table, [80,65,85,75,75,85]))
story.append(Paragraph("Interpretación", styles["Heading2"]))
para("Varias corridas y ambas medianas globales quedaron por debajo de p=2. "
     "Los picos no satisfacen el criterio de repetibilidad. Las mitades de los arreglos "
     "confirmados ocupan 1.5 y 2 MiB, más que L2 (512 KiB), de modo que la hipótesis "
     "de caché privada no justifica esos picos. La dispersión puede deberse a frecuencia, "
     "planificación o caché, pero no se aisló su causa.")
para("La conclusión se limita a estas configuraciones en WSL. Código, CSV crudos, "
     "checksums, ambiente y pasos de reproducción acompañan este PDF. No se modificó Entrega.")
doc = SimpleDocTemplate(str(BASE / "informe_reto_opcional.pdf"), pagesize=A4,
                        leftMargin=1.2*cm, rightMargin=1.2*cm,
                        topMargin=1.0*cm, bottomMargin=1.0*cm)
doc.build(story)
package = ["informe_reto_opcional.md", "informe_reto_opcional.pdf",
           "exploracion.csv", "confirmacion.csv", "resumen_corridas.csv",
           "confirmacion.stderr.txt", "ambiente.txt", "lab12_speedup.c",
           "autoresearch.md", "autoresearch.jsonl", "autoresearch.sh",
           "explorar.sh", "confirmar.sh", "ambiente.sh", "analizar.py",
           "generar_informe.py"]
with ZipFile(BASE / "reto_opcional_entregable.zip", "w", ZIP_DEFLATED) as archive:
    for name in package:
        archive.write(BASE / name, arcname=f"reto_opcional/{name}")
print(f"Generados informe_reto_opcional.md/pdf, resumen_corridas.csv y ZIP ({len(summary)} corridas)")
