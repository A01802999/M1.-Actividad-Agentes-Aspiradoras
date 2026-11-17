# Autores: Diego Sánchez Mancilla (A01802999) y Joshua Michel Martinez Orozco (A01798152)
# Actividad M1 - TC2008B Sistemas Multiagentes: capturas de la simulación

import os
import random

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from robot_limpieza import Agente, Habitacion, ejecutar_paso

SEMILLA_CAPTURA = 35
FILAS = 20
COLUMNAS = 20
NUM_AGENT = 20
PORCENTAJE_SUCIO = 30
TIEMPO_MAX = 10000
CARPETA_RESULTADOS = "resultados"
COLOR_LIMPIA = "#E3EEF9"
COLOR_SUCIA = "#F5A623"
COLOR_AGENTE = "#0B3D91"


def tomar_estado(paso, habitacion, agentes):
    return {
        "paso": paso,
        "sucias": set(habitacion.sucias),
        "posiciones": [(a.fila, a.columna) for a in agentes],
        "porcentaje_limpio": habitacion.porcentaje_limpio(),
        "movimientos": sum(a.movimientos for a in agentes),
    }


def registrar_simulacion():
    habitacion = Habitacion(FILAS, COLUMNAS, PORCENTAJE_SUCIO)
    agentes = [Agente() for _ in range(NUM_AGENT)]
    estados = [tomar_estado(0, habitacion, agentes)]
    paso = 0
    while not habitacion.esta_limpia() and paso < TIEMPO_MAX:
        paso += 1
        ejecutar_paso(habitacion, agentes)
        estados.append(tomar_estado(paso, habitacion, agentes))
    return estados


def dibujar_estado(eje, estado, titulo):
    cuadricula = [[1 if (f, c) in estado["sucias"] else 0 for c in range(COLUMNAS)]
                  for f in range(FILAS)]
    eje.imshow(cuadricula, cmap=ListedColormap([COLOR_LIMPIA, COLOR_SUCIA]), vmin=0, vmax=1,
               extent=(0, COLUMNAS, FILAS, 0), interpolation="nearest")
    eje.set_xticks(range(COLUMNAS + 1), minor=True)
    eje.set_yticks(range(FILAS + 1), minor=True)
    eje.grid(which="minor", color="white", linewidth=0.6)
    eje.tick_params(which="both", length=0, labelbottom=False, labelleft=False)
    columnas = [c + 0.5 for _, c in estado["posiciones"]]
    filas = [f + 0.5 for f, _ in estado["posiciones"]]
    eje.scatter(columnas, filas, s=38, color=COLOR_AGENTE, zorder=3)
    eje.set_title(titulo, fontsize=11)
    eje.set_xlabel(f"Pasos transcurridos: {estado['paso']}\n"
                   f"Porcentaje de limpieza: {estado['porcentaje_limpio']:.2f}%\n"
                   f"Movimientos totales: {estado['movimientos']}", fontsize=9)


def generar_captura():
    estados = registrar_simulacion()
    seleccion = [
        (estados[0], "Estado inicial (agentes en [1,1])"),
        (estados[len(estados) // 5], "Estado intermedio"),
        (estados[-1], "Estado final"),
    ]
    figura, ejes = plt.subplots(1, 3, figsize=(13, 5.2))
    for eje, (estado, titulo) in zip(ejes, seleccion):
        dibujar_estado(eje, estado, titulo)
    figura.suptitle(f"Simulación: habitación {FILAS}x{COLUMNAS}, {NUM_AGENT} agentes, "
                    f"{PORCENTAJE_SUCIO}% de celdas sucias (naranja: sucia, punto azul: agente)",
                    fontsize=11)
    figura.tight_layout()
    ruta = os.path.join(CARPETA_RESULTADOS, "captura_simulacion.png")
    figura.savefig(ruta, dpi=200, bbox_inches="tight")
    plt.close(figura)
    return ruta


if __name__ == "__main__":
    random.seed(SEMILLA_CAPTURA)
    os.makedirs(CARPETA_RESULTADOS, exist_ok=True)
    print(generar_captura())
