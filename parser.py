"""Módulo para interpretar frases de conversión en lenguaje natural.

Convierte textos como '100 cm a mm' o '2,5 kilos en gramos' en tuplas
estructuradas (valor, unidad_origen, unidad_destino).
"""

import re
from typing import Union
from unidades import buscar_unidad

# Expresión regular para separar: [valor], [unidad origen], [conector], [unidad destino]
# Conectores admitidos: a, en, to, ->, →, =>
_PATRON_CONECTOR = r"(?:->|→|=>|\ba\b|\ben\b|\bto\b)"
_REGEX_CONVERSION = re.compile(
    rf"^\s*([+-]?\d+(?:[.,]\d+)?(?:[eE][+-]?\d+)?)\s*([^\s\d].*?)\s*{_PATRON_CONECTOR}\s*(.+?)\s*$",
    re.IGNORECASE,
)


def interpretar(frase: str) -> tuple[Union[int, float], str, str]:
    """Interpreta una frase de conversión como '100 cm a mm'.

    Devuelve una tupla (valor, simbolo_origen, simbolo_destino).
    Lanza ValueError si el formato no es válido o las unidades no existen.
    """
    if not frase or not isinstance(frase, str):
        raise ValueError(
            "Frase vacía. Formato esperado: '<valor> <origen> a <destino>' (ejemplo: '100 cm a mm')"
        )

    coincidencia = _REGEX_CONVERSION.match(frase.strip())
    if not coincidencia:
        raise ValueError(
            "No se pudo interpretar la frase. "
            "Formato esperado: '<valor> <origen> a <destino>' (ejemplo: '100 cm a mm')"
        )

    texto_valor, texto_origen, texto_destino = coincidencia.groups()

    # Procesar valor numérico admitiendo coma o punto decimal
    valor_float = float(texto_valor.replace(",", "."))
    if valor_float.is_integer() and "." not in texto_valor and "," not in texto_valor:
        valor_final: Union[int, float] = int(valor_float)
    else:
        valor_final = valor_float

    # Validar y resolver los símbolos canónicos de las unidades
    _, sim_origen = buscar_unidad(texto_origen.strip())
    _, sim_destino = buscar_unidad(texto_destino.strip())

    return valor_final, sim_origen, sim_destino

