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


    def test_tamano_letra_aviso_y_resultado(self) -> None:
        """Comprueba que el aviso use tamaño de letra reducido y el resultado mantenga tamaño 32."""
        # 1. Al vaciar el campo de valor, se muestra el aviso con tamaño menor a 32
        self.app.entrada_valor.delete(0, "end")
        self.app.calcular()
        fuente_aviso = self.app.lbl_resultado_grande.cget("font")
        tam_aviso = (
            fuente_aviso.cget("size")
            if hasattr(fuente_aviso, "cget")
            else getattr(fuente_aviso, "_size", fuente_aviso[1] if isinstance(fuente_aviso, (tuple, list)) else 18)
        )
        self.assertLess(tam_aviso, 32, "El tamaño de letra del aviso debe ser menor que 32.")
        self.assertIn("Introduce un valor", self.app.lbl_resultado_grande.cget("text"))

        # 2. Al escribir un resultado numérico, debe mantener el tamaño actual (32)
        self.app.entrada_valor.insert(0, "100")
        self.app.calcular()
        fuente_res = self.app.lbl_resultado_grande.cget("font")
        tam_res = (
            fuente_res.cget("size")
            if hasattr(fuente_res, "cget")
            else getattr(fuente_res, "_size", fuente_res[1] if isinstance(fuente_res, (tuple, list)) else 32)
        )
        self.assertEqual(tam_res, 32, "El resultado numérico debe mantener tamaño de letra 32.")


if __name__ == "__main__":
    unittest.main()
