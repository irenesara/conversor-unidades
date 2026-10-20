"""Pruebas unitarias para la validación de entrada numérica."""

import unittest
from interfaz import App


class TestValidacionEntrada(unittest.TestCase):
    """Pruebas para comprobar que solo se permiten números en la casilla."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.app = App()
        cls.app.withdraw()  # Ocultar ventana durante los tests

    @classmethod
    def tearDownClass(cls) -> None:
        cls.app.destroy()

    def test_valores_validos(self) -> None:
        """Comprueba que se admitan enteros, decimales y signos válidos."""
        validos = [
            "",
            "-",
            ".",
            ",",
            "-.",
            "-,",
            "0",
            "100",
            "100.",
            "100,",
            "2.5",
            "2,5",
            "-40",
            "-40.5",
            "-40,5",
        ]
        for val in validos:
            with self.subTest(valor=val):
                self.assertTrue(
                    self.app._validar_numero(val),
                    f"El valor '{val}' debería ser considerado válido.",
                )

    def test_valores_invalidos(self) -> None:
        """Comprueba que se rechacen letras y formatos incorrectos."""
        invalidos = [
            "a",
            "abc",
            "100a",
            "a100",
            "1.2.3",
            "1,2,3",
            "1.2,3",
            "40-5",
            "--5",
            " ",
            "!",
            "100 patatas",
        ]
        for val in invalidos:
            with self.subTest(valor=val):
                self.assertFalse(
                    self.app._validar_numero(val),
                    f"El valor '{val}' debería ser rechazado.",
                )


if __name__ == "__main__":
    unittest.main()
