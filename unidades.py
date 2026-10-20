"""Módulo de definición de unidades de medida, categorías y alias.

Define las magnitudes soportadas, sus factores respecto a la unidad base
y el sistema de búsqueda de alias para admitir lenguaje natural.
"""

from typing import Any

# Estructura principal de categorías, iconos y factores de conversión.
# Cada categoría define su unidad base y el factor relativo de cada unidad.
CATEGORIAS: dict[str, dict[str, Any]] = {
    "Longitud": {
        "icono": "📏",
        "unidad_base": "m",
        "unidades": {
            "mm": {"nombre": "milímetro", "plural": "milímetros", "factor": 0.001},
            "cm": {"nombre": "centímetro", "plural": "centímetros", "factor": 0.01},
            "dm": {"nombre": "decímetro", "plural": "decímetros", "factor": 0.1},
            "m": {"nombre": "metro", "plural": "metros", "factor": 1.0},
            "km": {"nombre": "kilómetro", "plural": "kilómetros", "factor": 1000.0},
            "in": {"nombre": "pulgada", "plural": "pulgadas", "factor": 0.0254},
            "ft": {"nombre": "pie", "plural": "pies", "factor": 0.3048},
            "yd": {"nombre": "yarda", "plural": "yardas", "factor": 0.9144},
            "mi": {"nombre": "milla", "plural": "millas", "factor": 1609.344},
        },
    },
    "Masa": {
        "icono": "⚖️",
        "unidad_base": "g",
        "unidades": {
            "mg": {"nombre": "miligramo", "plural": "miligramos", "factor": 0.001},
            "g": {"nombre": "gramo", "plural": "gramos", "factor": 1.0},
            "kg": {"nombre": "kilogramo", "plural": "kilogramos", "factor": 1000.0},
            "t": {"nombre": "tonelada", "plural": "toneladas", "factor": 1000000.0},
            "oz": {"nombre": "onza", "plural": "onzas", "factor": 28.349523125},
            "lb": {"nombre": "libra", "plural": "libras", "factor": 453.59237},
        },
    },
    "Volumen": {
        "icono": "🧪",
        "unidad_base": "l",
        "unidades": {
            "ml": {"nombre": "mililitro", "plural": "mililitros", "factor": 0.001},
            "cl": {"nombre": "centilitro", "plural": "centilitros", "factor": 0.01},
            "l": {"nombre": "litro", "plural": "litros", "factor": 1.0},
            "m3": {"nombre": "metro cúbico", "plural": "metros cúbicos", "factor": 1000.0},
            "gal": {"nombre": "galón (EE. UU.)", "plural": "galones (EE. UU.)", "factor": 3.785411784},
        },
    },
    "Tiempo": {
        "icono": "⏱️",
        "unidad_base": "s",
        "unidades": {
            "ms": {"nombre": "milisegundo", "plural": "milisegundos", "factor": 0.001},
            "s": {"nombre": "segundo", "plural": "segundos", "factor": 1.0},
            "min": {"nombre": "minuto", "plural": "minutos", "factor": 60.0},
            "h": {"nombre": "hora", "plural": "horas", "factor": 3600.0},
            "d": {"nombre": "día", "plural": "días", "factor": 86400.0},
            "sem": {"nombre": "semana", "plural": "semanas", "factor": 604800.0},
        },
    },
    "Datos": {
        "icono": "💾",
        "unidad_base": "B",
        "unidades": {
            "B": {"nombre": "byte", "plural": "bytes", "factor": 1.0},
            "KB": {"nombre": "kilobyte", "plural": "kilobytes", "factor": 1024.0},
            "MB": {"nombre": "megabyte", "plural": "megabytes", "factor": 1024.0**2},
            "GB": {"nombre": "gigabyte", "plural": "gigabytes", "factor": 1024.0**3},
            "TB": {"nombre": "terabyte", "plural": "terabytes", "factor": 1024.0**4},
        },
    },
    "Temperatura": {
        "icono": "🌡️",
        "unidad_base": "C",
        "unidades": {
            "C": {"nombre": "grado Celsius", "plural": "grados Celsius", "factor": None},
            "F": {"nombre": "grado Fahrenheit", "plural": "grados Fahrenheit", "factor": None},
            "K": {"nombre": "Kelvin", "plural": "Kelvin", "factor": None},
        },
    },
}

# Diccionario de alias para reconocer variaciones escritas de cada unidad.
ALIAS: dict[str, str] = {
    # Longitud
    "mm": "mm", "milimetro": "mm", "milímetro": "mm", "milimetros": "mm", "milímetros": "mm",
    "cm": "cm", "centimetro": "cm", "centímetro": "cm", "centimetros": "cm", "centímetros": "cm",
    "dm": "dm", "decimetro": "dm", "decímetro": "dm", "decimetros": "dm", "decímetros": "dm",
    "m": "m", "metro": "m", "metros": "m",
    "km": "km", "kilometro": "km", "kilómetro": "km", "kilometros": "km", "kilómetros": "km",
    "in": "in", "pulgada": "in", "pulgadas": "in", "inch": "in", "inches": "in", '"': "in",
    "ft": "ft", "pie": "ft", "pies": "ft", "foot": "ft", "feet": "ft", "'": "ft",
    "yd": "yd", "yarda": "yd", "yardas": "yd", "yard": "yd", "yards": "yd",
    "mi": "mi", "milla": "mi", "millas": "mi", "mile": "mi", "miles": "mi",

    # Masa
    "mg": "mg", "miligramo": "mg", "milígramo": "mg", "miligramos": "mg", "milígramos": "mg",
    "g": "g", "gramo": "g", "gramos": "g", "gr": "g", "grs": "g",
    "kg": "kg", "kilo": "kg", "kilos": "kg", "kilogramo": "kg", "kilogramos": "kg",
    "t": "t", "tonelada": "t", "toneladas": "t", "ton": "t", "tons": "t",
    "oz": "oz", "onza": "oz", "onzas": "oz", "ounce": "oz", "ounces": "oz",
    "lb": "lb", "libra": "lb", "libras": "lb", "lbs": "lb", "pound": "lb", "pounds": "lb",

    # Volumen
    "ml": "ml", "mililitro": "ml", "mililitros": "ml",
    "cl": "cl", "centilitro": "cl", "centilitros": "cl",
    "l": "l", "litro": "l", "litros": "l", "lt": "l", "lts": "l",
    "m3": "m3", "m³": "m3", "metro cubico": "m3", "metro cúbico": "m3",
    "metros cubicos": "m3", "metros cúbicos": "m3",
    "gal": "gal", "galon": "gal", "galón": "gal", "galones": "gal", "gallon": "gal",

    # Tiempo
    "ms": "ms", "milisegundo": "ms", "milisegundos": "ms",
    "s": "s", "seg": "s", "segundo": "s", "segundos": "s", "sec": "s", "secs": "s",
    "min": "min", "minuto": "min", "minutos": "min", "mins": "min",
    "h": "h", "hr": "h", "hrs": "h", "hora": "h", "horas": "h", "hour": "h", "hours": "h",
    "d": "d", "dia": "d", "día": "d", "dias": "d", "días": "d", "day": "d", "days": "d",
    "sem": "sem", "semana": "sem", "semanas": "sem", "week": "sem", "weeks": "sem",

    # Datos (sensible a mayúsculas para B, KB, MB, GB, TB)
    "B": "B", "byte": "B", "bytes": "B", "b": "B",
    "KB": "KB", "kilobyte": "KB", "kilobytes": "KB", "kb": "KB",
    "MB": "MB", "megabyte": "MB", "megabytes": "MB", "mb": "MB",
    "GB": "GB", "gigabyte": "GB", "gigabytes": "GB", "gb": "GB",
    "TB": "TB", "terabyte": "TB", "terabytes": "TB", "tb": "TB",

    # Temperatura
    "C": "C", "c": "C", "°C": "C", "ºC": "C", "°c": "C", "ºc": "C",
    "celsius": "C", "grados": "C", "grado": "C", "grados celsius": "C", "grado celsius": "C",
    "F": "F", "f": "F", "°F": "F", "ºF": "F", "°f": "F", "ºf": "F",
    "fahrenheit": "F", "grados fahrenheit": "F", "grado fahrenheit": "F",
    "K": "K", "k": "K", "°K": "K", "ºK": "K", "°k": "K", "ºk": "K",
    "kelvin": "K", "kelvins": "K", "grados kelvin": "K", "grado kelvin": "K",
}

# Mapa auxiliar en minúsculas para búsquedas insensibles a mayúsculas
_ALIAS_MINUSCULAS: dict[str, str] = {clave.lower(): valor for clave, valor in ALIAS.items()}


def buscar_unidad(texto: str) -> tuple[str, str]:
    """Busca y resuelve una unidad a partir de su símbolo o alias textual.

    Devuelve una tupla (categoría, símbolo_oficial).
    Lanza ValueError si el texto no corresponde a ninguna unidad registrada.
    """
    limpio = texto.strip()

    # 1. Búsqueda exacta (respetando mayúsculas, importante para B/KB/MB...)
    simbolo = ALIAS.get(limpio)

    # 2. Búsqueda en minúsculas para variantes generales
    if simbolo is None:
        simbolo = _ALIAS_MINUSCULAS.get(limpio.lower())

    # 3. Búsqueda directa entre los símbolos oficiales si no estuviera en alias
    if simbolo is None:
        for categoria, datos in CATEGORIAS.items():
            if limpio in datos["unidades"]:
                return categoria, limpio
        raise ValueError(f"Unidad desconocida: '{texto}'")

    # Identificar a qué categoría pertenece el símbolo resuelto
    for categoria, datos in CATEGORIAS.items():
        if simbolo in datos["unidades"]:
            return categoria, simbolo

    raise ValueError(f"Unidad desconocida: '{texto}'")


def obtener_nombre_unidad(simbolo: str, plural: bool = False) -> str:
    """Retorna el nombre descriptivo (singular o plural) de una unidad."""
    for datos in CATEGORIAS.values():
        if simbolo in datos["unidades"]:
            info = datos["unidades"][simbolo]
            if plural:
                return info.get("plural", info["nombre"] + "s")
            return info["nombre"]
    return simbolo

