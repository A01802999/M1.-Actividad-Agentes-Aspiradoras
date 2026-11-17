# Actividad M1: robot de limpieza reactivo (TC2008B)

Simulación multiagente de robots de limpieza reactivos y análisis del efecto del número de agentes.

## Archivos

- `robot_limpieza.py`: modelo (habitación, agente, simulación y validación de parámetros). No requiere librerías externas.
- `experimentos.py`: corre los experimentos A, B, C y D y guarda los resultados en CSV dentro de `resultados/`. No requiere librerías externas.
- `visualizacion.py`: dibuja los estados inicial, intermedio y final de una corrida (`resultados/captura_simulacion.png`). Requiere `matplotlib`.
- `Informe_Robot_Limpieza_Reactivo.pdf`: informe de la actividad.

## Cómo ejecutar

```
python robot_limpieza.py
python experimentos.py
pip install matplotlib
python visualizacion.py
```

Ejemplo de uso del modelo:

```python
from robot_limpieza import simular

simular(filas=10, columnas=10, num_agent=5, porcentaje_sucio=30, tiempo_max=200)
```

Devuelve un diccionario con `tiempo`, `porcentaje_limpio`, `movimientos` y `completo`.
