# Especificación del proyecto: Conversor de Unidades en Python

> **Instrucciones para el agente (Antigravity):** lee este documento completo antes de empezar. Genera **todo** el proyecto descrito aquí: estructura de carpetas, código, tests, `requirements.txt` y `README.md`. El código debe estar **comentado en español**, ser claro y fácil de entender para un estudiante. Al terminar, ejecuta los tests y comprueba que la aplicación arranca sin errores.

---

## 1. Objetivo

Crear una aplicación de escritorio en Python que convierta valores entre unidades de medida. Debe tener una **interfaz gráfica moderna y bonita**.

El usuario puede convertir de dos maneras:

1. **Modo selector:** elige la categoría, la unidad de origen y la de destino en menús desplegables, y escribe el valor.
2. **Modo texto rápido:** escribe una frase como `100 cm a mm` y el programa la interpreta.

Ejemplo de resultado: `100 cm = 1000 mm`

---

## 2. Tecnologías

| Elemento | Elección |
|---|---|
| Lenguaje | Python 3.10 o superior |
| Interfaz gráfica | **CustomTkinter** (`pip install customtkinter`) |
| Tests | `unittest` (incluido en Python) |
| Otras librerías | Ninguna más. La lógica de conversión se programa a mano. |

---

## 3. Estructura de archivos

```
conversor/
├── main.py              # Punto de entrada: arranca la aplicación
├── unidades.py          # Tablas de unidades, nombres y factores
├── conversor.py         # Lógica de conversión (sin interfaz)
├── parser.py            # Interpreta frases como "100 cm a mm"
├── interfaz.py          # Ventana y componentes gráficos
├── tests/
│   ├── __init__.py
│   ├── test_conversor.py
│   └── test_parser.py
├── requirements.txt
└── README.md
```

**Separa la lógica de la interfaz.** `conversor.py`, `unidades.py` y `parser.py` no deben importar nada gráfico, para poder probarlos con tests.

---

## 4. Categorías y unidades

Cada categoría tiene una **unidad base**. Cada unidad guarda su **factor**, es decir, cuántas unidades base equivalen a 1 de esa unidad.

**Algoritmo general:** `resultado = valor × factor_origen ÷ factor_destino`

### 4.1 Longitud (base: metro)
| Símbolo | Nombre | Factor |
|---|---|---|
| mm | milímetro | 0.001 |
| cm | centímetro | 0.01 |
| dm | decímetro | 0.1 |
| m | metro | 1 |
| km | kilómetro | 1000 |
| in | pulgada | 0.0254 |
| ft | pie | 0.3048 |
| yd | yarda | 0.9144 |
| mi | milla | 1609.344 |

### 4.2 Masa (base: gramo)
| Símbolo | Nombre | Factor |
|---|---|---|
| mg | miligramo | 0.001 |
| g | gramo | 1 |
| kg | kilogramo | 1000 |
| t | tonelada | 1 000 000 |
| oz | onza | 28.349523125 |
| lb | libra | 453.59237 |

### 4.3 Volumen (base: litro)
| Símbolo | Nombre | Factor |
|---|---|---|
| ml | mililitro | 0.001 |
| cl | centilitro | 0.01 |
| l | litro | 1 |
| m3 | metro cúbico | 1000 |
| gal | galón (EE. UU.) | 3.785411784 |

### 4.4 Tiempo (base: segundo)
| Símbolo | Nombre | Factor |
|---|---|---|
| ms | milisegundo | 0.001 |
| s | segundo | 1 |
| min | minuto | 60 |
| h | hora | 3600 |
| d | día | 86400 |
| sem | semana | 604800 |

### 4.5 Datos (base: byte)
| Símbolo | Nombre | Factor |
|---|---|---|
| B | byte | 1 |
| KB | kilobyte | 1024 |
| MB | megabyte | 1024² |
| GB | gigabyte | 1024³ |
| TB | terabyte | 1024⁴ |

### 4.6 Temperatura (caso especial, sin factores)
Unidades: `C` (Celsius), `F` (Fahrenheit), `K` (Kelvin).

Convierte siempre pasando por Celsius:
- F → C: `(F − 32) × 5/9`
- K → C: `K − 273.15`
- C → F: `C × 9/5 + 32`
- C → K: `C + 273.15`

Valida que el resultado no quede por debajo del cero absoluto (0 K). Si queda por debajo, lanza un error con un mensaje claro.

### 4.7 Alias
El parser debe aceptar variantes, sin distinguir mayúsculas y minúsculas salvo en los datos (B, KB…). Ejemplos:
- `cm`, `centimetro`, `centímetro`, `centimetros`, `centímetros`
- `kg`, `kilo`, `kilos`, `kilogramo`, `kilogramos`
- `°C`, `ºC`, `c`, `celsius`, `grados`
- `l`, `litro`, `litros`
- `h`, `hora`, `horas`

Guarda los alias en `unidades.py` como un diccionario `alias → símbolo`.

---

## 5. Módulos

### `unidades.py`
- Constante `CATEGORIAS`: diccionario con cada categoría, sus unidades (símbolo, nombre, factor) y un icono emoji (📏 Longitud, ⚖️ Masa, 🧪 Volumen, ⏱️ Tiempo, 💾 Datos, 🌡️ Temperatura).
- Constante `ALIAS`.
- Función `buscar_unidad(texto) -> (categoria, simbolo)`. Lanza `ValueError` si no existe.

### `conversor.py`
- Función `convertir(valor: float, origen: str, destino: str) -> float`.
- Si las unidades son de categorías distintas, lanza `ValueError("No se puede convertir kg a cm: son magnitudes distintas")`.
- Función `formatear(numero) -> str`: como máximo 6 decimales significativos y sin ceros sobrantes (`1000` y no `1000.000000`). Para números muy grandes o muy pequeños usa notación científica. Usa la coma como separador decimal y el punto para miles (estilo español): `1.609,344`.

### `parser.py`
- Función `interpretar(frase: str) -> (valor, origen, destino)`.
- Formatos aceptados:
  - `100 cm a mm`
  - `100cm a mm`
  - `100 cm en mm`
  - `100 cm to mm`
  - `100 cm -> mm`
  - `2,5 kg a g` (acepta coma decimal)
  - `-40 C a F`
- Usa expresiones regulares (`re`).
- Si la frase no se entiende, lanza `ValueError` con un mensaje que incluya un ejemplo correcto.

---

## 6. Interfaz gráfica (`interfaz.py`), lo más importante: que sea bonita

### Estilo general
- Tema **oscuro** por defecto (`ctk.set_appearance_mode("dark")`), con un **interruptor** para cambiar a modo claro.
- Color de acento: **azul violeta `#6C63FF`**. Usa un tono más claro, `#8B85FF`, para el efecto *hover* de los botones.
- Esquinas redondeadas en todos los elementos (`corner_radius` entre 10 y 15).
- Fuente: `"Segoe UI"` (en Windows) o la predeterminada. Título de 26 px en negrita y resultado de 32 px en negrita.
- Ventana de 900 × 600 px, centrada en la pantalla, redimensionable con un tamaño mínimo de 800 × 550.
- Título de la ventana: `Conversor de Unidades`.

### Distribución
```
┌──────────────┬─────────────────────────────────────────┬────────────────┐
│  BARRA       │   ZONA PRINCIPAL                        │  HISTORIAL     │
│  LATERAL     │                                         │                │
│              │   📏 Longitud                           │  100 cm → mm   │
│ 📏 Longitud  │                                         │  = 1000 mm     │
│ ⚖️ Masa      │   [ Valor: 100        ]                 │  ───────────   │
│ 🧪 Volumen   │   [ De: cm ▼ ]  ⇄  [ A: mm ▼ ]          │  5 kg → lb     │
│ ⏱️ Tiempo    │                                         │  = 11,0231 lb  │
│ 💾 Datos     │   ┌─────────────────────────────┐       │                │
│ 🌡️ Temp.     │   │      1.000 mm               │       │                │
│              │   │  100 centímetros =          │       │                │
│              │   │  1.000 milímetros           │       │                │
│              │   └─────────────────────────────┘       │                │
│              │                                         │ [Borrar]       │
│ ☀️/🌙 Tema   │   ⚡ Modo rápido: [100 cm a mm ] [→]     │                │
└──────────────┴─────────────────────────────────────────┴────────────────┘
```

### Comportamiento
- **Barra lateral:** un botón por categoría con su emoji. El botón activo se resalta con el color de acento. Al pulsarlo se actualizan los desplegables con las unidades de esa categoría.
- **Conversión en tiempo real:** el resultado se actualiza mientras el usuario escribe o cambia una unidad, sin necesidad de pulsar un botón.
- **Botón ⇄:** intercambia las unidades de origen y destino.
- **Tarjeta de resultado:** fondo ligeramente distinto al de la ventana. Muestra el número grande y debajo, más pequeño, la frase completa con los nombres de las unidades.
- **Botón 📋 Copiar:** copia el resultado al portapapeles y muestra durante 1,5 s el texto "¡Copiado!".
- **Modo rápido:** un campo de texto donde escribir `100 cm a mm`. Al pulsar Enter o el botón →, la interfaz cambia automáticamente a la categoría correcta, rellena los campos y muestra el resultado.
- **Historial:** panel derecho con desplazamiento que muestra las últimas 20 conversiones, la más reciente arriba. Solo se añade una entrada al pulsar Enter, usar el modo rápido o el botón "Guardar". No se añade una entrada por cada tecla. Al hacer clic en una entrada se vuelve a cargar esa conversión. Incluye un botón "Borrar historial".
- **Errores:** nunca deben cerrar el programa. Se muestran en la tarjeta de resultado en color rojo suave (`#FF6B6B`) con un mensaje amable. Por ejemplo: "⚠️ Introduce un número válido".
- **Atajos de teclado:**
  - `Ctrl+L` pone el foco en el modo rápido.
  - `Ctrl+C`, con el foco fuera de un campo de texto, copia el resultado.
  - `Esc` limpia el campo del valor.

---

## 7. `main.py`
Debe ser corto: importa la clase de la ventana desde `interfaz.py` y la ejecuta.

```python
from interfaz import App

if __name__ == "__main__":
    app = App()
    app.mainloop()
```

---

## 8. Tests

Usa `unittest`. Los tests deben ejecutarse con `python -m unittest discover tests`.

Casos obligatorios (para comparar decimales usa `assertAlmostEqual`):

| Entrada | Resultado esperado |
|---|---|
| 100 cm → mm | 1000 |
| 1 km → m | 1000 |
| 1 mi → km | 1.609344 |
| 12 in → ft | 1 |
| 1 kg → lb | 2.20462 (aprox.) |
| 1 l → ml | 1000 |
| 2 h → min | 120 |
| 1 GB → MB | 1024 |
| 0 C → F | 32 |
| 100 C → K | 373.15 |
| -40 C → F | -40 |
| 5 cm → cm | 5 |
| kg → cm | lanza `ValueError` |
| -300 C → K | lanza `ValueError` (bajo el cero absoluto) |

Tests del parser:
- `"100 cm a mm"` → `(100, "cm", "mm")`
- `"2,5 kilos en gramos"` → `(2.5, "kg", "g")`
- `"100cm to mm"` → `(100, "cm", "mm")`
- `"hola"` → lanza `ValueError`
- `"100 patatas a mm"` → lanza `ValueError`

---

## 9. Calidad del código
- Comentarios y *docstrings* en **español**.
- Nombres de variables y funciones en español y en `snake_case` (`convertir_valor`, `unidad_origen`).
- Usa *type hints* en las funciones.
- Ninguna función debe superar unas 40 líneas. Si es más larga, divídela.
- No dejes código repetido. Las unidades se leen siempre de `unidades.py`, nunca se escriben a mano en la interfaz.
- Para añadir una unidad nueva debe bastar con añadir una línea en `unidades.py`.

---

## 10. Archivos extra

**`requirements.txt`**
```
customtkinter>=5.2
```

**`README.md`** con:
- Descripción breve del proyecto.
- Cómo instalarlo (`pip install -r requirements.txt`).
- Cómo ejecutarlo (`python main.py`).
- Cómo pasar los tests.
- Lista de unidades soportadas.
- Ejemplos de uso del modo rápido.

---

## 11. Criterios de aceptación (comprueba todo antes de terminar)
- [ ] `python main.py` abre la ventana sin errores.
- [ ] Todos los tests pasan.
- [ ] Escribir `100 cm a mm` en el modo rápido muestra `1.000 mm`.
- [ ] Cambiar de categoría actualiza los desplegables.
- [ ] El botón ⇄ intercambia las unidades y recalcula.
- [ ] Escribir letras en el campo del valor muestra un error amable y no rompe el programa.
- [ ] El historial guarda las conversiones y permite recargarlas.
- [ ] El interruptor de tema cambia entre modo oscuro y claro.
- [ ] El código está comentado en español.
