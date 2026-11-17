# Autores: Diego Sánchez Mancilla (A01802999) y Joshua Michel Martinez Orozco (A01798152)
# Actividad M1 - TC2008B Sistemas Multiagentes: experimentos del robot de limpieza

import csv
import os
import random
import statistics

from robot_limpieza import simular

SEMILLA_EXPERIMENTOS = 2026
REPETICIONES = 300
AGENTES = [1, 2, 3, 4, 5, 10, 15, 20, 30, 50, 100]
FILAS_BASE = 10
COLUMNAS_BASE = 10
SUCIO_BASE = 30
TIEMPO_SIN_LIMITE = 5000
TIEMPO_DEFECTO = 200
CARPETA_RESULTADOS = "resultados"


def correr_configuracion(filas, columnas, num_agent, porcentaje_sucio, tiempo_max, repeticiones):
    corridas = [simular(filas, columnas, num_agent, porcentaje_sucio, tiempo_max)
                for _ in range(repeticiones)]
    tiempos = [c["tiempo"] for c in corridas]
    movimientos = [c["movimientos"] for c in corridas]
    limpios = [c["porcentaje_limpio"] for c in corridas]
    completos = [c["completo"] for c in corridas]
    return {
        "filas": filas,
        "columnas": columnas,
        "num_agent": num_agent,
        "porcentaje_sucio": porcentaje_sucio,
        "tiempo_max": tiempo_max,
        "repeticiones": repeticiones,
        "tiempo_media": statistics.mean(tiempos),
        "tiempo_desv": statistics.stdev(tiempos),
        "movimientos_media": statistics.mean(movimientos),
        "movimientos_desv": statistics.stdev(movimientos),
        "limpio_media": statistics.mean(limpios),
        "limpio_desv": statistics.stdev(limpios),
        "tasa_completado": 100.0 * sum(completos) / repeticiones,
    }


def guardar_csv(nombre, filas_resultado):
    ruta = os.path.join(CARPETA_RESULTADOS, nombre)
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(filas_resultado[0].keys()))
        escritor.writeheader()
        escritor.writerows(filas_resultado)


def experimento_agentes_sin_limite():
    resultados = [correr_configuracion(FILAS_BASE, COLUMNAS_BASE, n, SUCIO_BASE,
                                       TIEMPO_SIN_LIMITE, REPETICIONES)
                  for n in AGENTES]
    base = resultados[0]["tiempo_media"]
    for r in resultados:
        r["aceleracion"] = base / r["tiempo_media"]
        r["eficiencia"] = r["aceleracion"] / r["num_agent"]
        r["agente_pasos"] = r["num_agent"] * r["tiempo_media"]
    guardar_csv("agentes_sin_limite.csv", resultados)
    return resultados


def experimento_agentes_tiempo_defecto():
    resultados = [correr_configuracion(FILAS_BASE, COLUMNAS_BASE, n, SUCIO_BASE,
                                       TIEMPO_DEFECTO, REPETICIONES)
                  for n in AGENTES]
    guardar_csv("agentes_tiempo_200.csv", resultados)
    return resultados


def experimento_porcentaje_sucio():
    resultados = []
    for porcentaje in [10, 30, 50, 80, 100]:
        for n in [1, 5, 20]:
            resultados.append(correr_configuracion(FILAS_BASE, COLUMNAS_BASE, n, porcentaje,
                                                   TIEMPO_SIN_LIMITE, REPETICIONES))
    guardar_csv("porcentaje_sucio.csv", resultados)
    return resultados


def experimento_tamano():
    resultados = []
    for lado in [5, 10, 20, 30]:
        for n in [1, 5, 20]:
            resultados.append(correr_configuracion(lado, lado, n, SUCIO_BASE,
                                                   100000, 100))
    guardar_csv("tamano_habitacion.csv", resultados)
    return resultados


def principal():
    random.seed(SEMILLA_EXPERIMENTOS)
    os.makedirs(CARPETA_RESULTADOS, exist_ok=True)
    experimento_agentes_sin_limite()
    experimento_agentes_tiempo_defecto()
    experimento_porcentaje_sucio()
    experimento_tamano()


if __name__ == "__main__":
    principal()
