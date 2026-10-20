"""Módulo de lógica matemática de conversión y formateo numérico.

No contiene dependencias gráficas para permitir su ejecución en cualquier entorno
y facilitar las pruebas unitarias automatizadas.
"""

from unidades import CATEGORIAS, buscar_unidad


def _convertir_temperatura(valor: float, origen: str, destino: str) -> float:
    """Convierte temperaturas entre Celsius, Fahrenheit y Kelvin pasando por Celsius."""
    # 1. Convertir la unidad de origen a grados Celsius
    if origen == "C":
        celsius = valor
    elif origen == "F":
        celsius = (valor - 32.0) * 5.0 / 9.0
    elif origen == "K":
        celsius = valor - 273.15
    else:
        raise ValueError(f"Unidad de temperatura no soportada: '{origen}'")

    # 2. Validar que no esté por debajo del cero absoluto (0 Kelvin)
    kelvin = celsius + 273.15
    if kelvin < -1e-9:
        raise ValueError("La temperatura no puede estar por debajo del cero absoluto (0 K)")

    # 3. Convertir de Celsius a la unidad de destino
    if destino == "C":
        return celsius
    if destino == "F":
        return (celsius * 9.0 / 5.0) + 32.0
    if destino == "K":
        return celsius + 273.15
    raise ValueError(f"Unidad de temperatura no soportada: '{destino}'")


def convertir(valor: float, origen: str, destino: str) -> float:
    """Convierte un valor numérico de una unidad de origen a una de destino.

    Lanza ValueError si las unidades pertenecen a categorías diferentes, si
    no existen o si se intenta usar una temperatura por debajo de 0 K.
    """
    cat_origen, sim_origen = buscar_unidad(origen)
    cat_destino, sim_destino = buscar_unidad(destino)

    if cat_origen != cat_destino:
        raise ValueError(
            f"No se puede convertir {sim_origen} a {sim_destino}: son magnitudes distintas"
        )

    if cat_origen == "Temperatura":
        return _convertir_temperatura(valor, sim_origen, sim_destino)

    factor_origen = CATEGORIAS[cat_origen]["unidades"][sim_origen]["factor"]
    factor_destino = CATEGORIAS[cat_destino]["unidades"][sim_destino]["factor"]

    return valor * factor_origen / factor_destino


def _formatear_cientifico(abs_num: float, signo: str) -> str:
    """Formatea números muy grandes o muy pequeños en notación científica."""
    texto_cient = f"{abs_num:.6e}"
    mantisa, exponente = texto_cient.split("e")
    mantisa_limpia = mantisa.rstrip("0").rstrip(".")
    exp_int = int(exponente)
    mantisa_es = mantisa_limpia.replace(".", ",")
    return f"{signo}{mantisa_es}e{exp_int}"


def formatear(numero: float) -> str:
    """Formatea un número con estilo español (punto para miles, coma decimal).

    Aplica como máximo 6 decimales significativos sin ceros sobrantes.
    Usa notación científica para valores muy grandes o muy pequeños.
    """
    if numero is None:
        return ""

    if abs(numero) < 1e-12:
        return "0"

    signo = "-" if numero < 0 else ""
    abs_num = abs(numero)

    # Notación científica para magnitudes fuera del rango habitual
    if abs_num >= 1e12 or abs_num < 1e-4:
        return _formatear_cientifico(abs_num, signo)

    # Redondear a un máximo de 6 decimales
    redondeado = round(abs_num, 6)
    partes = f"{redondeado:.6f}".split(".")
    parte_entera = partes[0]
    parte_decimal = partes[1].rstrip("0")

    entero_formateado = f"{int(parte_entera):,}".replace(",", ".")
    if parte_decimal:
        return f"{signo}{entero_formateado},{parte_decimal}"
    return f"{signo}{entero_formateado}"

