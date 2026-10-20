# 📐 Conversor de Unidades en Python

Una aplicación de escritorio moderna, intuitiva y atractiva para convertir unidades de medida entre diferentes magnitudes físicas y digitales. Construida en **Python 3.10+** con **CustomTkinter**, cuenta con conversión en tiempo real, modo rápido por texto natural, historial de conversiones, tema oscuro/claro y atajos de teclado.

---

## 🚀 Características principales

- **Interfaz gráfica moderna:** Diseño limpio con esquinas redondeadas, color de acento `#6C63FF` y soporte completo para modo oscuro y claro.
- **Conversión en tiempo real:** Los cálculos se actualizan de forma instantánea al escribir o cambiar cualquier unidad.
- **⚡ Modo rápido (lenguaje natural):** Escribe frases cotidianas como `100 cm a mm` o `2,5 kilos en gramos` y el sistema detectará automáticamente la magnitud, configurará los selectores y calculará el resultado.
- **📜 Historial interactivo:** Guarda hasta 20 conversiones recientes con un clic para recargarlas en cualquier momento.
- **📋 Copiado rápido:** Copia el resultado formateado al portapapeles con un clic o atajo de teclado.
- **Manejo de errores amable:** Notificaciones visuales claras ante entradas numéricas inválidas o temperaturas físicamente imposibles (bajo el cero absoluto, 0 K).
- **Atajos de teclado rápidos:**
  - `Ctrl + L`: Lleva el foco al campo de **Modo rápido**.
  - `Ctrl + C`: Copia el resultado actual (cuando no se está editando un campo de texto).
  - `Esc`: Limpia el valor actual.

---

## 📦 Instalación

1. Clona o descarga este repositorio:
   ```bash
   cd conversor_medidas
   ```

2. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🖥️ Ejecución

Para iniciar la aplicación de escritorio:

```bash
python main.py
```

---

## 🧪 Ejecución de Tests

Las pruebas unitarias automatizadas cubren toda la lógica matemática del conversor, el formateo numérico en notación española y el parser de lenguaje natural:

```bash
python -m unittest discover tests
```

---

## 📏 Unidades Soportadas

| Categoría | Icono | Unidad Base | Unidades y Símbolos |
|---|:---:|:---:|---|
| **Longitud** | 📏 | metro (m) | `mm` (milímetro), `cm` (centímetro), `dm` (decímetro), `m` (metro), `km` (kilómetro), `in` (pulgada), `ft` (pie), `yd` (yarda), `mi` (milla) |
| **Masa** | ⚖️ | gramo (g) | `mg` (miligramo), `g` (gramo), `kg` (kilogramo), `t` (tonelada), `oz` (onza), `lb` (libra) |
| **Volumen** | 🧪 | litro (l) | `ml` (mililitro), `cl` (centilitro), `l` (litro), `m3` (metro cúbico), `gal` (galón EE. UU.) |
| **Tiempo** | ⏱️ | segundo (s) | `ms` (milisegundo), `s` (segundo), `min` (minuto), `h` (hora), `d` (día), `sem` (semana) |
| **Datos** | 💾 | byte (B) | `B` (byte), `KB` (kilobyte), `MB` (megabyte), `GB` (gigabyte), `TB` (terabyte) |
| **Temperatura** | 🌡️ | Celsius (°C) | `C` (Celsius), `F` (Fahrenheit), `K` (Kelvin) *(con validación de cero absoluto)* |

---

## ⚡ Ejemplos de uso del Modo Rápido

Puedes ingresar frases en el campo inferior y presionar `Enter` o el botón `→`:

- `100 cm a mm` → `1.000 mm`
- `2,5 kilos en gramos` → `2.500 g`
- `100cm to mm` → `1.000 mm`
- `100 cm en mm` → `1.000 mm`
- `100 cm -> mm` → `1.000 mm`
- `-40 C a F` → `-40 F`
- `1 GB a MB` → `1.024 MB`
- `2 h a min` → `120 min`

---

## 📂 Estructura del Proyecto

```
conversor_medidas/
├── main.py              # Punto de entrada de la aplicación
├── unidades.py          # Definición de categorías, factores y diccionario de alias
├── conversor.py         # Lógica matemática de conversión y formateador numérico
├── parser.py            # Analizador sintáctico por expresiones regulares
├── interfaz.py          # Ventana y componentes visuales en CustomTkinter
├── tests/
│   ├── __init__.py
│   ├── test_conversor.py
│   └── test_parser.py
├── requirements.txt     # Dependencias del proyecto
├── README.md            # Documentación general
└── ESPECIFICACION.md    # Especificación técnica del proyecto
```

