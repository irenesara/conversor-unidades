"""Pruebas unitarias para el intérprete de frases de conversión."""

import unittest
from parser import interpretar


class TestParser(unittest.TestCase):
    """Casos de prueba para la función interpretar."""

    def test_frase_simple(self) -> None:
        """Prueba frase estándar '100 cm a mm'."""
        self.assertEqual(interpretar("100 cm a mm"), (100, "cm", "mm"))

    def test_frase_con_coma_y_alias(self) -> None:
        """Prueba frase con coma y alias '2,5 kilos en gramos'."""
        self.assertEqual(interpretar("2,5 kilos en gramos"), (2.5, "kg", "g"))

    def test_frase_sin_espacio_y_conector_to(self) -> None:
        """Prueba frase compacta con 'to': '100cm to mm'."""
        self.assertEqual(interpretar("100cm to mm"), (100, "cm", "mm"))

    def test_frase_con_flecha(self) -> None:
        """Prueba frase con flecha: '100 cm -> mm'."""
        self.assertEqual(interpretar("100 cm -> mm"), (100, "cm", "mm"))

    def test_frase_temperatura_negativa(self) -> None:
        """Prueba temperatura negativa: '-40 C a F'."""
        self.assertEqual(interpretar("-40 C a F"), (-40, "C", "F"))

    def test_frase_invalida_lanza_error(self) -> None:
        """Prueba que un texto no comprensible lance ValueError con ejemplo."""
        with self.assertRaises(ValueError) as contexto:
            interpretar("hola")
        self.assertIn("100 cm a mm", str(contexto.exception))

    def test_unidad_inexistente_lanza_error(self) -> None:
        """Prueba que una unidad desconocida lance ValueError."""
        with self.assertRaises(ValueError) as contexto:
            interpretar("100 patatas a mm")
        self.assertIn("patatas", str(contexto.exception).lower())


if __name__ == "__main__":
    unittest.main()

