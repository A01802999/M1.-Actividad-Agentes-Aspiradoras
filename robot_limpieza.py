# Autores: Diego Sánchez Mancilla (A01802999) y Joshua Michel Martinez Orozco (A01798152)
# Actividad M1 - TC2008B Sistemas Multiagentes: robot de limpieza reactivo

import random

PARAMETROS_DEFECTO = {
    "filas": 10,
    "columnas": 10,
    "num_agent": 1,
    "porcentaje_sucio": 30.0,
    "tiempo_max": 200,
}

DIRECCIONES = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1), (0, 1),
    (1, -1), (1, 0), (1, 1),
]


def es_entero(valor):
    return isinstance(valor, int) and not isinstance(valor, bool)


def es_numero(valor):
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


def validar_parametros(filas, columnas, num_agent, porcentaje_sucio, tiempo_max):
    reglas = {
        "filas": (filas, lambda v: es_entero(v) and v >= 2),
        "columnas": (columnas, lambda v: es_entero(v) and v >= 2),
        "num_agent": (num_agent, lambda v: es_entero(v) and v >= 1),
        "porcentaje_sucio": (porcentaje_sucio, lambda v: es_numero(v) and 0 <= v <= 100),
        "tiempo_max": (tiempo_max, lambda v: es_entero(v) and v >= 1),
    }
    validados = {}
    for nombre, (valor, es_valido) in reglas.items():
        if es_valido(valor):
            validados[nombre] = valor
        else:
            validados[nombre] = PARAMETROS_DEFECTO[nombre]
            print(f"Valor inválido para {nombre}: {valor}. "
                  f"Se usa el valor por defecto {PARAMETROS_DEFECTO[nombre]}.")
    return validados


class Habitacion:
    def __init__(self, filas, columnas, porcentaje_sucio):
        self.filas = filas
        self.columnas = columnas
        self.total_celdas = filas * columnas
        cantidad_sucias = int(self.total_celdas * porcentaje_sucio / 100 + 0.5)
        indices = random.sample(range(self.total_celdas), cantidad_sucias)
        self.sucias = {(i // columnas, i % columnas) for i in indices}

    def esta_sucia(self, fila, columna):
        return (fila, columna) in self.sucias

    def limpiar(self, fila, columna):
        self.sucias.discard((fila, columna))

    def esta_dentro(self, fila, columna):
        return 0 <= fila < self.filas and 0 <= columna < self.columnas

    def esta_limpia(self):
        return len(self.sucias) == 0

    def porcentaje_limpio(self):
        return 100.0 * (self.total_celdas - len(self.sucias)) / self.total_celdas


class Agente:
    def __init__(self, fila=0, columna=0):
        self.fila = fila
        self.columna = columna
        self.movimientos = 0
        self.limpiezas = 0

    def actuar(self, habitacion):
        if habitacion.esta_sucia(self.fila, self.columna):
            habitacion.limpiar(self.fila, self.columna)
            self.limpiezas += 1
            return
        d_fila, d_columna = random.choice(DIRECCIONES)
        nueva_fila = self.fila + d_fila
        nueva_columna = self.columna + d_columna
        if habitacion.esta_dentro(nueva_fila, nueva_columna):
            self.fila = nueva_fila
            self.columna = nueva_columna
            self.movimientos += 1


def ejecutar_paso(habitacion, agentes):
    for agente in agentes:
        agente.actuar(habitacion)
        if habitacion.esta_limpia():
            break


def simular(filas=PARAMETROS_DEFECTO["filas"],
            columnas=PARAMETROS_DEFECTO["columnas"],
            num_agent=PARAMETROS_DEFECTO["num_agent"],
            porcentaje_sucio=PARAMETROS_DEFECTO["porcentaje_sucio"],
            tiempo_max=PARAMETROS_DEFECTO["tiempo_max"]):
    p = validar_parametros(filas, columnas, num_agent, porcentaje_sucio, tiempo_max)
    habitacion = Habitacion(p["filas"], p["columnas"], p["porcentaje_sucio"])
    agentes = [Agente() for _ in range(p["num_agent"])]

    tiempo = 0
    while not habitacion.esta_limpia() and tiempo < p["tiempo_max"]:
        tiempo += 1
        ejecutar_paso(habitacion, agentes)

    return {
        "tiempo": tiempo,
        "porcentaje_limpio": habitacion.porcentaje_limpio(),
        "movimientos": sum(a.movimientos for a in agentes),
        "completo": habitacion.esta_limpia(),
    }


if __name__ == "__main__":
    print(simular())
