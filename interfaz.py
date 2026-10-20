"""Módulo de la interfaz gráfica de usuario con CustomTkinter.

Implementa una interfaz moderna, responsiva, con tema oscuro/claro,
conversión en tiempo real, modo rápido, historial y atajos de teclado.
"""

from typing import Any, Optional
import tkinter
import customtkinter as ctk

from conversor import convertir, formatear
from parser import interpretar
from unidades import CATEGORIAS, buscar_unidad, obtener_nombre_unidad

# Constantes de diseño visual
COLOR_ACENTO = "#6C63FF"
COLOR_ACENTO_HOVER = "#8B85FF"
COLOR_ERROR = "#FF6B6B"
FUENTE_FAMILIA = "Segoe UI"


class App(ctk.CTk):
    """Ventana principal del conversor de unidades."""

    def __init__(self) -> None:
        super().__init__()
        ctk.set_appearance_mode("dark")
        self._configurar_ventana()

        self.categoria_actual: str = "Longitud"
        self.botones_categoria: dict[str, ctk.CTkButton] = {}
        self.historial: list[dict[str, Any]] = []
        self.ultimo_resultado_copia: str = ""
        self._timer_copiado: Optional[str] = None

        self._crear_estructura()
        self._configurar_atajos()
        self.seleccionar_categoria("Longitud")

    def _configurar_ventana(self) -> None:
        """Configura propiedades y centrado de la ventana principal."""
        self.title("Conversor de Unidades")
        self.minsize(800, 550)
        self._centrar_ventana(900, 600)
        self.lift()
        self.attributes("-topmost", True)
        self.after(250, lambda: self.attributes("-topmost", False))
        self.focus_force()

    def _centrar_ventana(self, ancho: int, alto: int) -> None:
        """Centra la ventana en la pantalla del usuario."""
        self.update_idletasks()
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        pos_x = max(0, (pantalla_ancho - ancho) // 2)
        pos_y = max(0, (pantalla_alto - alto) // 2)
        self.geometry(f"{ancho}x{alto}+{pos_x}+{pos_y}")

    def _crear_estructura(self) -> None:
        """Crea el diseño de tres columnas: barra lateral, zona principal e historial."""
        self.grid_columnconfigure(0, weight=0, minsize=180)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0, minsize=240)
        self.grid_rowconfigure(0, weight=1)

        self._crear_barra_lateral()
        self._crear_zona_principal()
        self._crear_panel_historial()

    def _crear_barra_lateral(self) -> None:
        """Construye la barra lateral con categorías y el interruptor de tema."""
        self.frame_lateral = ctk.CTkFrame(self, corner_radius=0)
        self.frame_lateral.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.frame_lateral.grid_rowconfigure(len(CATEGORIAS) + 2, weight=1)

        titulo_lateral = ctk.CTkLabel(
            self.frame_lateral,
            text="Conversor",
            font=ctk.CTkFont(family=FUENTE_FAMILIA, size=20, weight="bold"),
        )
        titulo_lateral.grid(row=0, column=0, padx=20, pady=(25, 15), sticky="w")

        for indice, (cat_nombre, cat_datos) in enumerate(CATEGORIAS.items(), start=1):
            texto_btn = f"{cat_datos['icono']}  {cat_nombre}"
            btn = ctk.CTkButton(
                self.frame_lateral,
                text=texto_btn,
                anchor="w",
                corner_radius=12,
                height=40,
                font=ctk.CTkFont(family=FUENTE_FAMILIA, size=14),
                command=lambda c=cat_nombre: self.seleccionar_categoria(c),
            )
            btn.grid(row=indice, column=0, padx=14, pady=5, sticky="ew")
            self.botones_categoria[cat_nombre] = btn

        self.switch_tema = ctk.CTkSwitch(
            self.frame_lateral,
            text="Modo oscuro",
            command=self._cambiar_tema,
            font=ctk.CTkFont(family=FUENTE_FAMILIA, size=13),
            progress_color=COLOR_ACENTO,
        )
        self.switch_tema.select()
        self.switch_tema.grid(
            row=len(CATEGORIAS) + 3, column=0, padx=16, pady=20, sticky="s"
        )

    def _cambiar_tema(self) -> None:
        """Alterna la apariencia general entre modo oscuro y claro."""
        if self.switch_tema.get() == 1:
            ctk.set_appearance_mode("dark")
            self.switch_tema.configure(text="Modo oscuro")
        else:
            ctk.set_appearance_mode("light")
            self.switch_tema.configure(text="Modo claro")
        self._actualizar_estilo_botones_categoria()

    def _actualizar_estilo_botones_categoria(self) -> None:
        """Resalta la categoría activa y atenúa las demás."""
        for nombre, boton in self.botones_categoria.items():
            if nombre == self.categoria_actual:
                boton.configure(
                    fg_color=COLOR_ACENTO,
                    hover_color=COLOR_ACENTO_HOVER,
                    text_color="#FFFFFF",
                )
            else:
                boton.configure(
                    fg_color="transparent",
                    hover_color=("gray85", "#2E2D4D"),
                    text_color=("gray10", "gray90"),
                )

    def _crear_zona_principal(self) -> None:
        """Crea el panel central con controles, tarjeta de resultado y modo rápido."""
        self.frame_principal = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_principal.grid(row=0, column=1, sticky="nsew", padx=25, pady=20)
        self.frame_principal.grid_columnconfigure(0, weight=1)

        self._crear_cabecera()
        self._crear_fila_valor()
        self._crear_fila_selectores()
        self._crear_tarjeta_resultado()
        self._crear_seccion_rapida()

    def _crear_cabecera(self) -> None:
        """Muestra el título de la categoría actualmente seleccionada."""
        self.etiqueta_cabecera = ctk.CTkLabel(
            self.frame_principal,
            text="📏 Longitud",
            font=ctk.CTkFont(family=FUENTE_FAMILIA, size=26, weight="bold"),
            anchor="w",
        )
        self.etiqueta_cabecera.grid(row=0, column=0, sticky="w", pady=(5, 15))

    def _crear_fila_valor(self) -> None:
        """Crea el campo de entrada para el valor numérico a convertir."""
        frame_valor = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        frame_valor.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        frame_valor.grid_columnconfigure(1, weight=1)

        etiq_valor = ctk.CTkLabel(
            frame_valor,
            text="Valor:",
            font=ctk.CTkFont(family=FUENTE_FAMILIA, size=15, weight="bold"),
        )
        etiq_valor.grid(row=0, column=0, padx=(0, 10), sticky="w")

        self.entrada_valor = ctk.CTkEntry(
            frame_valor,
            height=42,
            corner_radius=12,
            font=ctk.CTkFont(family=FUENTE_FAMILIA, size=16),
            placeholder_text="Escribe un número (ej. 100)",
        )
        self.entrada_valor.insert(0, "100")
        self.entrada_valor.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        self.entrada_valor.bind("<KeyRelease>", lambda _: self.calcular())
        self.entrada_valor.bind("<Return>", lambda _: self.guardar_en_historial())

        self.btn_guardar = ctk.CTkButton(
            frame_valor,
            text="💾 Guardar",
            width=90,
            height=42,
            corner_radius=12,
            fg_color=COLOR_ACENTO,
            hover_color=COLOR_ACENTO_HOVER,
            command=self.guardar_en_historial,
            font=ctk.CTkFont(family=FUENTE_FAMILIA, size=13),
        )
        self.btn_guardar.grid(row=0, column=2, sticky="e")

    def _crear_fila_selectores(self) -> None:
        """Crea los menús desplegables de origen y destino con el botón de intercambio."""
        frame_combos = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        frame_combos.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        frame_combos.grid_columnconfigure(1, weight=1)
        frame_combos.grid_columnconfigure(4, weight=1)

        ctk.CTkLabel(
            frame_combos,
            text="De:",
            font=ctk.CTkFont(family=FUENTE_FAMILIA, size=14, weight="bold"),
        ).grid(row=0, column=0, padx=(0, 8), sticky="w")

        self.combo_origen = ctk.CTkOptionMenu(
            frame_combos,
            height=38,
            corner_radius=12,
            fg_color=COLOR_ACENTO,
            button_color=COLOR_ACENTO,
            button_hover_color=COLOR_ACENTO_HOVER,
            command=lambda _: self.calcular(),
            font=ctk.CTkFont(family=FUENTE_FAMILIA, size=13),
        )
        self.combo_origen.grid(row=0, column=1, sticky="ew")

        btn_swap = ctk.CTkButton(
            frame_combos,
            text="⇄",
            width=46,
            height=38,
            corner_radius=12,
            fg_color=("gray80", "#2D2E3D"),
            hover_color=("gray70", "#3E3F52"),
            text_color=("black", "white"),
            font=ctk.CTkFont(family=FUENTE_FAMILIA, size=18, weight="bold"),
            command=self._intercambiar_unidades,
        )
        btn_swap.grid(row=0, column=2, padx=12)

        ctk.CTkLabel(
            frame_combos,
            text="A:",
            font=ctk.CTkFont(family=FUENTE_FAMILIA, size=14, weight="bold"),
        ).grid(row=0, column=3, padx=(0, 8), sticky="w")

        self.combo_destino = ctk.CTkOptionMenu(
            frame_combos,
            height=38,
            corner_radius=12,
            fg_color=COLOR_ACENTO,
            button_color=COLOR_ACENTO,
            button_hover_color=COLOR_ACENTO_HOVER,
            command=lambda _: self.calcular(),
            font=ctk.CTkFont(family=FUENTE_FAMILIA, size=13),
        )
        self.combo_destino.grid(row=0, column=4, sticky="ew")

    def _crear_tarjeta_resultado(self) -> None:
        """Crea la tarjeta destacada que muestra el resultado grande y el botón de copiar."""
        self.tarjeta_resultado = ctk.CTkFrame(
            self.frame_principal,
            corner_radius=15,
            fg_color=("gray90", "#1E1F2B"),
        )
        self.tarjeta_resultado.grid(row=3, column=0, sticky="ew", pady=(0, 20))
        self.tarjeta_resultado.grid_columnconfigure(0, weight=1)

        self.lbl_resultado_grande = ctk.CTkLabel(
            self.tarjeta_resultado,
            text="1.000 mm",
            font=ctk.CTkFont(family=FUENTE_FAMILIA, size=32, weight="bold"),
            anchor="w",
        )
        self.lbl_resultado_grande.grid(row=0, column=0, padx=25, pady=(20, 5), sticky="w")

        self.lbl_resultado_detalle = ctk.CTkLabel(
            self.tarjeta_resultado,
            text="100 centímetros = 1.000 milímetros",
            font=ctk.CTkFont(family=FUENTE_FAMILIA, size=14),
            text_color=("gray40", "gray65"),
            anchor="w",
        )
        self.lbl_resultado_detalle.grid(row=1, column=0, padx=25, pady=(0, 20), sticky="w")

        self.btn_copiar = ctk.CTkButton(
            self.tarjeta_resultado,
            text="📋 Copiar",
            width=110,
            height=36,
            corner_radius=10,
            fg_color=COLOR_ACENTO,
            hover_color=COLOR_ACENTO_HOVER,
            command=self.copiar_resultado,
            font=ctk.CTkFont(family=FUENTE_FAMILIA, size=13),
        )
        self.btn_copiar.grid(row=0, column=1, rowspan=2, padx=20, pady=20, sticky="e")

    def _crear_seccion_rapida(self) -> None:
        """Construye la sección inferior para el modo texto rápido."""
        frame_rapido = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        frame_rapido.grid(row=4, column=0, sticky="ew", pady=(10, 0))
        frame_rapido.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            frame_rapido,
            text="⚡ Modo rápido:",
            font=ctk.CTkFont(family=FUENTE_FAMILIA, size=14, weight="bold"),
        ).grid(row=0, column=0, padx=(0, 10), sticky="w")

        self.entrada_rapida = ctk.CTkEntry(
            frame_rapido,
            height=40,
            corner_radius=12,
            font=ctk.CTkFont(family=FUENTE_FAMILIA, size=14),
            placeholder_text="Escribe ej: 100 cm a mm y presiona Enter",
        )
        self.entrada_rapida.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        self.entrada_rapida.bind("<Return>", lambda _: self.ejecutar_modo_rapido())

        btn_flecha = ctk.CTkButton(
            frame_rapido,
            text="→",
            width=46,
            height=40,
            corner_radius=12,
            fg_color=COLOR_ACENTO,
            hover_color=COLOR_ACENTO_HOVER,
            command=self.ejecutar_modo_rapido,
            font=ctk.CTkFont(family=FUENTE_FAMILIA, size=18, weight="bold"),
        )
        btn_flecha.grid(row=0, column=2, sticky="e")

    def _crear_panel_historial(self) -> None:
        """Construye el panel derecho con la lista de conversiones recientes."""
        self.frame_historial = ctk.CTkFrame(self, corner_radius=0)
        self.frame_historial.grid(row=0, column=2, sticky="nsew", padx=0, pady=0)
        self.frame_historial.grid_columnconfigure(0, weight=1)
        self.frame_historial.grid_rowconfigure(1, weight=1)

        cabecera_hist = ctk.CTkFrame(self.frame_historial, fg_color="transparent")
        cabecera_hist.grid(row=0, column=0, sticky="ew", padx=16, pady=(20, 10))
        cabecera_hist.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            cabecera_hist,
            text="📜 Historial",
            font=ctk.CTkFont(family=FUENTE_FAMILIA, size=16, weight="bold"),
        ).grid(row=0, column=0, sticky="w")

        btn_borrar = ctk.CTkButton(
            cabecera_hist,
            text="Borrar",
            width=65,
            height=28,
            corner_radius=8,
            fg_color=("gray75", "#2D2E3D"),
            hover_color=("gray65", "#3E3F52"),
            text_color=("black", "white"),
            font=ctk.CTkFont(family=FUENTE_FAMILIA, size=12),
            command=self.borrar_historial,
        )
        btn_borrar.grid(row=0, column=1, sticky="e")

        self.scroll_historial = ctk.CTkScrollableFrame(
            self.frame_historial, fg_color="transparent"
        )
        self.scroll_historial.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 15))
        self.scroll_historial.grid_columnconfigure(0, weight=1)
        self._renderizar_historial()

    def seleccionar_categoria(self, nombre_categoria: str) -> None:
        """Selecciona una categoría, actualiza desplegables y recalcula."""
        if nombre_categoria not in CATEGORIAS:
            return

        self.categoria_actual = nombre_categoria
        icono = CATEGORIAS[nombre_categoria]["icono"]
        self.etiqueta_cabecera.configure(text=f"{icono} {nombre_categoria}")
        self._actualizar_estilo_botones_categoria()

        unidades_dict = CATEGORIAS[nombre_categoria]["unidades"]
        opciones = [f"{sim} - {info['nombre']}" for sim, info in unidades_dict.items()]

        self.combo_origen.configure(values=opciones)
        self.combo_destino.configure(values=opciones)

        # Seleccionar por defecto la primera y segunda unidad disponible
        if len(opciones) > 1:
            self.combo_origen.set(opciones[1] if nombre_categoria == "Longitud" else opciones[0])
            self.combo_destino.set(opciones[0] if nombre_categoria == "Longitud" else opciones[1])
        elif opciones:
            self.combo_origen.set(opciones[0])
            self.combo_destino.set(opciones[0])

        self.calcular()

    def _intercambiar_unidades(self) -> None:
        """Intercambia las unidades de los desplegables de origen y destino."""
        origen_actual = self.combo_origen.get()
        destino_actual = self.combo_destino.get()
        self.combo_origen.set(destino_actual)
        self.combo_destino.set(origen_actual)
        self.calcular()

    @staticmethod
    def _extraer_simbolo(texto_opcion: str) -> str:
        """Extrae el símbolo de una opción del desplegable tipo 'cm - centímetro'."""
        if not texto_opcion:
            return ""
        return texto_opcion.split(" - ")[0].strip()

    def _establecer_unidad_menu(
        self, menu: ctk.CTkOptionMenu, simbolo_objetivo: str
    ) -> None:
        """Fija la opción adecuada en el CTkOptionMenu según el símbolo canónico."""
        valores = menu.cget("values")
        for valor in valores:
            if valor.startswith(f"{simbolo_objetivo} -") or valor == simbolo_objetivo:
                menu.set(valor)
                return
        if valores:
            menu.set(valores[0])

    def calcular(self) -> None:
        """Ejecuta la conversión en tiempo real y actualiza la tarjeta de resultado."""
        texto_valor = self.entrada_valor.get().strip()
        if not texto_valor:
            self._mostrar_error("⚠️ Introduce un número válido")
            return

        try:
            valor = float(texto_valor.replace(",", "."))
        except ValueError:
            self._mostrar_error("⚠️ Introduce un número válido")
            return

        sim_origen = self._extraer_simbolo(self.combo_origen.get())
        sim_destino = self._extraer_simbolo(self.combo_destino.get())

        try:
            resultado = convertir(valor, sim_origen, sim_destino)
            self._mostrar_exito(valor, sim_origen, sim_destino, resultado)
        except ValueError as err:
            self._mostrar_error(f"⚠️ {str(err)}")

    def _mostrar_error(self, mensaje: str) -> None:
        """Muestra un mensaje de error amable en la tarjeta de resultado."""
        self.lbl_resultado_grande.configure(text=mensaje, text_color=COLOR_ERROR)
        self.lbl_resultado_detalle.configure(text="")
        self.btn_copiar.configure(state="disabled")
        self.ultimo_resultado_copia = ""

    def _mostrar_exito(
        self, valor: float, origen: str, destino: str, resultado: float
    ) -> None:
        """Muestra el resultado formateado y la explicación detallada."""
        formato_res = formatear(resultado)
        formato_val = formatear(valor)

        nombre_origen = obtener_nombre_unidad(origen, plural=(abs(valor) != 1.0))
        nombre_destino = obtener_nombre_unidad(destino, plural=(abs(resultado) != 1.0))

        color_texto = "gray10" if ctk.get_appearance_mode() == "Light" else "gray90"
        self.lbl_resultado_grande.configure(
            text=f"{formato_res} {destino}",
            text_color=color_texto,
        )
        self.lbl_resultado_detalle.configure(
            text=f"{formato_val} {nombre_origen} =\n{formato_res} {nombre_destino}",
            text_color=("gray40", "gray65"),
        )
        self.btn_copiar.configure(state="normal")
        self.ultimo_resultado_copia = f"{formato_res} {destino}"

    def copiar_resultado(self) -> None:
        """Copia el resultado actual al portapapeles y notifica al usuario."""
        if not self.ultimo_resultado_copia:
            return

        self.clipboard_clear()
        self.clipboard_append(self.ultimo_resultado_copia)

        if self._timer_copiado:
            self.after_cancel(self._timer_copiado)

        self.btn_copiar.configure(text="✓ ¡Copiado!")
        self._timer_copiado = self.after(
            1500, lambda: self.btn_copiar.configure(text="📋 Copiar")
        )

    def ejecutar_modo_rapido(self) -> None:
        """Procesa el texto del modo rápido, ajusta la GUI y calcula."""
        frase = self.entrada_rapida.get().strip()
        if not frase:
            return

        try:
            valor, sim_origen, sim_destino = interpretar(frase)
            cat_origen, _ = buscar_unidad(sim_origen)

            self.seleccionar_categoria(cat_origen)
            self._establecer_unidad_menu(self.combo_origen, sim_origen)
            self._establecer_unidad_menu(self.combo_destino, sim_destino)

            self.entrada_valor.delete(0, "end")
            self.entrada_valor.insert(0, str(valor))

            self.calcular()
            self.guardar_en_historial()
            self.entrada_rapida.delete(0, "end")
        except ValueError as err:
            self._mostrar_error(f"⚠️ {str(err)}")

    def guardar_en_historial(self) -> None:
        """Registra la conversión actual en la lista del historial."""
        if not self.ultimo_resultado_copia:
            return

        texto_valor = self.entrada_valor.get().strip()
        try:
            valor = float(texto_valor.replace(",", "."))
        except ValueError:
            return

        sim_origen = self._extraer_simbolo(self.combo_origen.get())
        sim_destino = self._extraer_simbolo(self.combo_destino.get())
        valor_guardar = int(valor) if valor.is_integer() else valor

        entrada = {
            "categoria": self.categoria_actual,
            "valor": valor_guardar,
            "origen": sim_origen,
            "destino": sim_destino,
            "res_texto": self.ultimo_resultado_copia,
            "etiqueta": f"{formatear(valor)} {sim_origen} → {sim_destino}",
        }

        # Evitar duplicar exactamente la última entrada
        if self.historial and self.historial[0] == entrada:
            return

        self.historial.insert(0, entrada)
        if len(self.historial) > 20:
            self.historial.pop()

        self._renderizar_historial()

    def _renderizar_historial(self) -> None:
        """Dibuja los elementos del historial en el panel desplegable."""
        for widget in self.scroll_historial.winfo_children():
            widget.destroy()

        if not self.historial:
            ctk.CTkLabel(
                self.scroll_historial,
                text="Sin conversiones aún",
                text_color=("gray50", "gray55"),
                font=ctk.CTkFont(family=FUENTE_FAMILIA, size=13),
            ).pack(pady=20)
            return

        for entrada in self.historial:
            self._crear_item_historial(entrada)

    def _crear_item_historial(self, entrada: dict[str, Any]) -> None:
        """Crea una tarjeta cliqueable para una entrada del historial."""
        tarjeta = ctk.CTkFrame(
            self.scroll_historial,
            corner_radius=10,
            fg_color=("gray85", "#21222D"),
        )
        tarjeta.pack(fill="x", pady=4, padx=2)

        lbl_arr = ctk.CTkLabel(
            tarjeta,
            text=entrada["etiqueta"],
            font=ctk.CTkFont(family=FUENTE_FAMILIA, size=12),
            anchor="w",
        )
        lbl_arr.pack(fill="x", padx=10, pady=(6, 1))

        lbl_aba = ctk.CTkLabel(
            tarjeta,
            text=f"= {entrada['res_texto']}",
            font=ctk.CTkFont(family=FUENTE_FAMILIA, size=13, weight="bold"),
            text_color=COLOR_ACENTO,
            anchor="w",
        )
        lbl_aba.pack(fill="x", padx=10, pady=(0, 6))

        for elemento in (tarjeta, lbl_arr, lbl_aba):
            elemento.bind(
                "<Button-1>", lambda _, e=entrada: self._cargar_conversion_historial(e)
            )

    def _cargar_conversion_historial(self, entrada: dict[str, Any]) -> None:
        """Restaura una conversión guardada al hacer clic en el historial."""
        self.seleccionar_categoria(entrada["categoria"])
        self._establecer_unidad_menu(self.combo_origen, entrada["origen"])
        self._establecer_unidad_menu(self.combo_destino, entrada["destino"])

        self.entrada_valor.delete(0, "end")
        self.entrada_valor.insert(0, str(entrada["valor"]))
        self.calcular()

    def borrar_historial(self) -> None:
        """Limpia todo el historial de conversiones."""
        self.historial.clear()
        self._renderizar_historial()

    def _configurar_atajos(self) -> None:
        """Vincula los atajos de teclado solicitados (Ctrl+L, Ctrl+C, Esc)."""
        self.bind_all("<Control-l>", self._atajo_modo_rapido)
        self.bind_all("<Control-L>", self._atajo_modo_rapido)
        self.bind_all("<Control-c>", self._atajo_copiar)
        self.bind_all("<Control-C>", self._atajo_copiar)
        self.bind_all("<Escape>", self._atajo_limpiar)

    def _atajo_modo_rapido(self, _event: Optional[Any] = None) -> str:
        """Atajo Ctrl+L: enfoca el campo de texto rápido."""
        self.entrada_rapida.focus_set()
        self.entrada_rapida.select_range(0, "end")
        return "break"

    def _atajo_copiar(self, _event: Optional[Any] = None) -> Optional[str]:
        """Atajo Ctrl+C: copia el resultado si el foco no está en un campo de texto."""
        widget = self.focus_get()
        if isinstance(widget, (tkinter.Entry, ctk.CTkEntry)):
            return None
        self.copiar_resultado()
        return "break"

    def _atajo_limpiar(self, _event: Optional[Any] = None) -> str:
        """Atajo Esc: limpia el campo del valor principal."""
        self.entrada_valor.delete(0, "end")
        self.calcular()
        return "break"


if __name__ == "__main__":
    app = App()
    app.mainloop()
