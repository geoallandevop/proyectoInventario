import customtkinter as ctk

from controllers.kardex_ctrl import (
    obtener_bodegas, obtener_productos, obtener_stock_producto, registrar_movimiento,
)
from views.ui_theme import COLORS, HeroBanner, card, font


class RegistroMovimientoView(ctk.CTkScrollableFrame):
    def __init__(self, parent, usuario):
        super().__init__(parent, fg_color="transparent", corner_radius=0,
                         scrollbar_button_color=COLORS["border"])
        self.usuario = usuario
        self.grid_columnconfigure(0, weight=1)
        self.bodegas_data = obtener_bodegas()
        self.productos_data = obtener_productos()

        HeroBanner(
            self, "Movimientos", "Registrar Movimiento",
            "Registra entradas, salidas y devoluciones con trazabilidad completa.\n"
            "El stock se valida y actualiza automáticamente al confirmar.",
            "Cada movimiento,\nbajo control.",
        ).grid(row=0, column=0, sticky="ew", pady=(0, 12))
        self._build_content()

    def _build_content(self):
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.grid(row=1, column=0, sticky="nsew")
        content.grid_columnconfigure(0, weight=3)
        content.grid_columnconfigure(1, weight=1)

        form = card(content)
        form.grid(row=0, column=0, sticky="nsew", padx=(0, 7))
        form.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkLabel(form, text="⇄", font=font(28, "bold"), text_color=COLORS["blue"])\
            .grid(row=0, column=0, sticky="w", padx=(24, 0), pady=(20, 0))
        title = ctk.CTkFrame(form, fg_color="transparent")
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=68, pady=(18, 16))
        ctk.CTkLabel(title, text="Datos del Movimiento", font=font(17, "bold"),
                     text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(title, text="Completa los datos para actualizar el inventario.",
                     font=font(10), text_color=COLORS["muted"]).pack(anchor="w")

        self.cb_tipo = self._field_option(form, 1, 0, "Tipo de Movimiento",
                                          ["Entrada", "Salida", "Devolución"])
        bodegas = [f"{b['id']} - {b['nombre']}" for b in self.bodegas_data] or ["No hay bodegas disponibles"]
        self.cb_bodega = self._field_option(form, 1, 1, "Bodega", bodegas, self.actualizar_stock)
        productos = [f"{p['id']} - {p['codigo']} · {p['nombre']}" for p in self.productos_data] or ["No hay productos disponibles"]
        self.cb_producto = self._field_option(form, 2, 0, "Producto", productos, self.actualizar_stock)
        self.entry_doc = self._field_entry(form, 2, 1, "Documento de Referencia", "Factura, remisión o recibo")
        self.entry_cant = self._field_entry(form, 3, 0, "Cantidad", "0")
        self.entry_costo = self._field_entry(form, 3, 1, "Costo Unitario", "0.00")

        ctk.CTkLabel(form, text="Observaciones", font=font(10, "bold"),
                     text_color=COLORS["text"], anchor="w")\
            .grid(row=4, column=0, columnspan=2, sticky="ew", padx=24, pady=(12, 4))
        self.observaciones = ctk.CTkTextbox(form, height=84, corner_radius=8,
                                            fg_color=COLORS["field"], border_width=1,
                                            border_color=COLORS["border"], font=font(11))
        self.observaciones.grid(row=5, column=0, columnspan=2, sticky="ew", padx=24)

        self.lbl_mensaje = ctk.CTkLabel(form, text="", height=26, font=font(10), anchor="w")
        self.lbl_mensaje.grid(row=6, column=0, columnspan=2, sticky="ew", padx=24, pady=(8, 0))
        actions = ctk.CTkFrame(form, fg_color="transparent")
        actions.grid(row=7, column=0, columnspan=2, sticky="ew", padx=24, pady=(8, 22))
        actions.grid_columnconfigure(0, weight=1)
        ctk.CTkButton(actions, text="Limpiar", width=120, height=44,
                      fg_color=COLORS["field"], hover_color=COLORS["card_alt"],
                      border_width=1, border_color=COLORS["border"],
                      command=self.limpiar).grid(row=0, column=0, sticky="e", padx=(0, 8))
        self.btn_guardar = ctk.CTkButton(actions, text="＋  Guardar Movimiento", width=205,
                                         height=44, fg_color=COLORS["blue"],
                                         hover_color=COLORS["blue_dark"],
                                         font=font(11, "bold"), command=self.guardar)
        self.btn_guardar.grid(row=0, column=1)

        side = card(content)
        side.grid(row=0, column=1, sticky="nsew", padx=(7, 0))
        ctk.CTkLabel(side, text="◇", width=68, height=68, corner_radius=12,
                     fg_color="#123F72", font=font(30), text_color="#C9E1FF")\
            .pack(pady=(36, 12))
        ctk.CTkLabel(side, text="Stock Disponible", font=font(16, "bold"),
                     text_color=COLORS["text"]).pack()
        self.lbl_stock_actual = ctk.CTkLabel(side, text="--", font=font(38, "bold"),
                                             text_color=COLORS["green"])
        self.lbl_stock_actual.pack(pady=(10, 0))
        ctk.CTkLabel(side, text="unidades en la bodega seleccionada", font=font(10),
                     wraplength=210, text_color=COLORS["muted"]).pack(padx=20)
        ctk.CTkFrame(side, height=1, fg_color=COLORS["border"]).pack(fill="x", padx=24, pady=28)
        ctk.CTkLabel(side, text="Validación automática", font=font(11, "bold"),
                     text_color=COLORS["text"]).pack(anchor="w", padx=24)
        ctk.CTkLabel(side, text="Las salidas que superen el stock disponible serán bloqueadas.",
                     font=font(10), wraplength=230, justify="left",
                     text_color=COLORS["muted"]).pack(anchor="w", padx=24, pady=(6, 0))
        self.actualizar_stock()

    def _field_option(self, parent, row, col, label, values, command=None):
        box = ctk.CTkFrame(parent, fg_color="transparent")
        box.grid(row=row, column=col, sticky="ew", padx=(24 if col == 0 else 10, 10 if col == 0 else 24), pady=8)
        ctk.CTkLabel(box, text=label, font=font(10, "bold"), text_color=COLORS["text"]).pack(anchor="w", pady=(0, 4))
        control = ctk.CTkOptionMenu(box, values=values, height=42, corner_radius=8,
                                    fg_color=COLORS["field"], button_color=COLORS["field"],
                                    button_hover_color=COLORS["card_alt"],
                                    font=font(10), dropdown_font=font(10), command=command)
        control.pack(fill="x")
        return control

    def _field_entry(self, parent, row, col, label, placeholder):
        box = ctk.CTkFrame(parent, fg_color="transparent")
        box.grid(row=row, column=col, sticky="ew", padx=(24 if col == 0 else 10, 10 if col == 0 else 24), pady=8)
        ctk.CTkLabel(box, text=label, font=font(10, "bold"), text_color=COLORS["text"]).pack(anchor="w", pady=(0, 4))
        control = ctk.CTkEntry(box, placeholder_text=placeholder, height=42,
                               fg_color=COLORS["field"], border_color=COLORS["border"],
                               font=font(10))
        control.pack(fill="x")
        return control

    def _selected_ids(self):
        warehouse = self.cb_bodega.get()
        product = self.cb_producto.get()
        if " - " not in warehouse or " - " not in product:
            return None, None
        try:
            return int(warehouse.split(" - ", 1)[0]), int(product.split(" - ", 1)[0])
        except ValueError:
            return None, None

    def actualizar_stock(self, _choice=None):
        warehouse_id, product_id = self._selected_ids()
        if warehouse_id is None:
            self.lbl_stock_actual.configure(text="--", text_color=COLORS["muted"])
            return
        stock = obtener_stock_producto(product_id, warehouse_id)
        self.lbl_stock_actual.configure(text=f"{float(stock):.1f}",
                                        text_color=COLORS["red"] if float(stock) <= 0 else COLORS["green"])

    def guardar(self):
        warehouse_id, product_id = self._selected_ids()
        if warehouse_id is None:
            self._message("No hay una bodega y un producto válidos.", False)
            return
        try:
            quantity = float(self.entry_cant.get())
            cost = float(self.entry_costo.get() or 0)
            if quantity <= 0 or cost < 0:
                raise ValueError
        except ValueError:
            self._message("Cantidad y costo deben ser números válidos.", False)
            return
        kind = self.cb_tipo.get()
        type_id = {"Entrada": 1, "Salida": 2, "Devolución": 3}.get(kind, 1)
        origin = warehouse_id if kind == "Salida" else None
        destination = warehouse_id if kind != "Salida" else None
        user_id = getattr(self.usuario, "ID_USUARIO", None)
        if user_id is None:
            self._message("No se pudo identificar al usuario de la sesión.", False)
            return
        self.btn_guardar.configure(state="disabled", text="Guardando...")
        self.update_idletasks()
        success, message = registrar_movimiento(
            user_id, type_id, origin, destination, self.entry_doc.get().strip(),
            [{"id_producto": product_id, "cantidad": quantity, "costo_unitario": cost}],
            observaciones=self.observaciones.get("1.0", "end").strip(),
        )
        self.btn_guardar.configure(state="normal", text="＋  Guardar Movimiento")
        self._message(message, success)
        if success:
            self.entry_cant.delete(0, "end")
            self.actualizar_stock()

    def _message(self, message, success):
        self.lbl_mensaje.configure(text=("✓  " if success else "⚠  ") + message,
                                   text_color=COLORS["green"] if success else COLORS["red"])

    def limpiar(self):
        for entry in (self.entry_doc, self.entry_cant, self.entry_costo):
            entry.delete(0, "end")
        self.observaciones.delete("1.0", "end")
        self.lbl_mensaje.configure(text="")
        self.actualizar_stock()

