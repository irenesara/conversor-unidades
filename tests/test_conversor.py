"""Pruebas unitarias para la lógica de conversión y formateo."""

import unittest
from conversor import convertir, formatear


class TestConversor(unittest.TestCase):
    """Casos de prueba para la función convertir y formatear."""

    def test_longitud_cm_a_mm(self) -> None:
        """Prueba conversión de 100 cm a mm."""
        resultado = convertir(100.0, "cm", "mm")
        self.assertAlmostEqual(resultado, 1000.0, places=4)

    def test_longitud_km_a_m(self) -> None:
        """Prueba conversión de 1 km a m."""
        resultado = convertir(1.0, "km", "m")
        self.assertAlmostEqual(resultado, 1000.0, places=4)

    def test_longitud_mi_a_km(self) -> None:
        """Prueba conversión de 1 mi a km."""
        resultado = convertir(1.0, "mi", "km")
        self.assertAlmostEqual(resultado, 1.609344, places=6)

    def test_longitud_in_a_ft(self) -> None:
        """Prueba conversión de 12 in a ft."""
        resultado = convertir(12.0, "in", "ft")
        self.assertAlmostEqual(resultado, 1.0, places=4)

    def test_masa_kg_a_lb(self) -> None:
        """Prueba conversión de 1 kg a lb (aprox 2.20462)."""
        resultado = convertir(1.0, "kg", "lb")
        self.assertAlmostEqual(resultado, 2.20462, places=4)

    def test_volumen_l_a_ml(self) -> None:
        """Prueba conversión de 1 l a ml."""
        resultado = convertir(1.0, "l", "ml")
        self.assertAlmostEqual(resultado, 1000.0, places=4)

    def test_tiempo_h_a_min(self) -> None:
        """Prueba conversión de 2 h a min."""
        resultado = convertir(2.0, "h", "min")
        self.assertAlmostEqual(resultado, 120.0, places=4)

    def test_datos_gb_a_mb(self) -> None:
        """Prueba conversión de 1 GB a MB."""
        resultado = convertir(1.0, "GB", "MB")
        self.assertAlmostEqual(resultado, 1024.0, places=4)

    def test_temperatura_c_a_f(self) -> None:
        """Prueba conversión de 0 C a F."""
        resultado = convertir(0.0, "C", "F")
        self.assertAlmostEqual(resultado, 32.0, places=4)

    def test_temperatura_c_a_k(self) -> None:
        """Prueba conversión de 100 C a K."""
        resultado = convertir(100.0, "C", "K")
        self.assertAlmostEqual(resultado, 373.15, places=4)

    def test_temperatura_negativa_c_a_f(self) -> None:
        """Prueba conversión de -40 C a F."""
        resultado = convertir(-40.0, "C", "F")
        self.assertAlmostEqual(resultado, -40.0, places=4)

    def test_misma_unidad(self) -> None:
        """Prueba conversión entre la misma unidad: 5 cm a cm."""
        resultado = convertir(5.0, "cm", "cm")
        self.assertAlmostEqual(resultado, 5.0, places=4)

    def test_magnitudes_distintas_lanza_error(self) -> None:
        """Prueba que convertir entre magnitudes incompatibles lance ValueError."""
        with self.assertRaises(ValueError) as contexto:
            convertir(1.0, "kg", "cm")
        self.assertIn("son magnitudes distintas", str(contexto.exception))

    def test_bajo_cero_absoluto_lanza_error(self) -> None:
        """Prueba que temperaturas bajo el cero absoluto lancen ValueError."""
        with self.assertRaises(ValueError) as contexto:
            convertir(-300.0, "C", "K")
        self.assertIn("cero absoluto", str(contexto.exception).lower())

    def test_formatear_estilo_espanol(self) -> None:
        """Prueba el formato numérico con coma decimal y punto de miles."""
        self.assertEqual(formatear(1000.0), "1.000")
        self.assertEqual(formatear(1609.344), "1.609,344")
        self.assertEqual(formatear(2.5), "2,5")
        self.assertEqual(formatear(0.0), "0")
        self.assertEqual(formatear(-40.0), "-40")


if __name__ == "__main__":
    unittest.main()

