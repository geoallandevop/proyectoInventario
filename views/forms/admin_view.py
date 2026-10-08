import customtkinter as ctk

from controllers.admin_ctrl import (
    actualizar_producto, actualizar_usuario, crear_producto, crear_usuario,
    obtener_catalogo, obtener_categorias, obtener_roles, obtener_unidades,
    obtener_usuarios, toggle_estado_producto, toggle_estado_usuario,
)
from views.ui_theme import COLORS, HeroBanner, VectorIcon, card, font


class AdminView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.current_tab = "users"
        self.id_usuario_editando = None
        self.id_producto_editando = None

        HeroBanner(
            self, "Administración", "Panel de Administración",
            "Gestiona usuarios, productos y aprobaciones del sistema.\n"
            "Mantén el control total de tu inventario con herramientas seguras y confiables.",
            "Personas, productos\ny procesos en armonía\npara un mejor control.",
        ).grid(row=0, column=0, sticky="ew", pady=(0, 12))
        self._build_tabs()
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.grid(row=2, column=0, sticky="nsew", pady=(12, 0))
        self.show_tab("users")

    def _build_tabs(self):
        nav = card(self, height=58)
        nav.grid(row=1, column=0, sticky="ew")
        nav.grid_propagate(False)
        nav.grid_columnconfigure((0, 1, 2), weight=1, uniform="tabs")
        self.tab_buttons = {}
        items = (("users", "Gestión de Usuarios"),
                 ("products", "Catálogo de Productos"),
                 ("approvals", "Aprobar Ajustes"))
        for col, (key, text) in enumerate(items):
            btn = ctk.CTkButton(nav, text=text, height=54, corner_radius=8,
                                fg_color="transparent", hover_color=COLORS["card_alt"],
                                font=font(12, "bold"), command=lambda k=key: self.show_tab(k))
            btn.grid(row=0, column=col, sticky="nsew", padx=2, pady=2)
            self.tab_buttons[key] = btn

    def show_tab(self, key):
        self.current_tab = key
        for name, btn in self.tab_buttons.items():
            btn.configure(fg_color=COLORS["blue_dark"] if name == key else "transparent",
                          text_color=COLORS["text"] if name == key else "#D4E3F5")
        for widget in self.content.winfo_children():
            widget.destroy()
        if key == "users":
            self._build_users()
        elif key == "products":
            self._build_products()
        else:
            self._build_approvals()

    # ----------------------------- users -----------------------------
    def _build_users(self):
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=1)
        self.roles = obtener_roles() or [
            {"id": 1, "nombre": "Administrador"},
            {"id": 2, "nombre": "Encargado de bodega"},
            {"id": 3, "nombre": "Consulta / supervisión"},
        ]
        self.role_values = [f"{r['id']} - {r['nombre']}" for r in self.roles]

        form = card(self.content, height=232)
        form.grid(row=0, column=0, sticky="ew")
        form.grid_propagate(False)
        form.grid_columnconfigure(0, weight=3)
        form.grid_columnconfigure(1, weight=3)
        form.grid_columnconfigure(2, weight=2)
        VectorIcon(form, "users", size=34, bg=COLORS["card"], fg=COLORS["blue"])\
            .grid(row=0, column=0, sticky="w", padx=24, pady=(14, 0))
        title = ctk.CTkFrame(form, fg_color="transparent")
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=66, pady=(13, 3))
        ctk.CTkLabel(title, text="Registrar Nuevo Usuario", font=font(16, "bold"),
                     text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(title, text="Completa la información para crear un nuevo usuario en el sistema.",
                     font=font(10), text_color=COLORS["muted"]).pack(anchor="w")

        self.u_nombre = self._labeled_entry(form, 1, 0, "Nombre Completo", "Ej. Juan Pérez García")
        self.u_correo = self._labeled_entry(form, 1, 1, "Correo Electrónico", "Ej. usuario@correo.com")
        self.u_pass = self._labeled_entry(form, 2, 0, "Contraseña", "Ingresa una contraseña segura", show="●")
        self.u_rol = self._labeled_option(form, 2, 1, "Rol de Usuario", self.role_values)

        aside = ctk.CTkFrame(form, fg_color="transparent", border_width=0)
        aside.grid(row=0, column=2, rowspan=3, sticky="nsew", padx=22, pady=15)
        ctk.CTkFrame(form, width=1, fg_color=COLORS["border"]).place(relx=.72, rely=.08, relheight=.84)
        icon_box = ctk.CTkFrame(aside, width=60, height=60, corner_radius=11, fg_color="#123F72")
        icon_box.pack(anchor="w", pady=(2, 8))
        icon_box.pack_propagate(False)
        VectorIcon(icon_box, "users", size=34, bg="#123F72", fg="#C7DFFF")\
            .place(relx=.5, rely=.5, anchor="center")
        self.user_form_title = ctk.CTkLabel(aside, text="Crear Usuario", font=font(15, "bold"),
                                            text_color=COLORS["text"])
        self.user_form_title.pack(anchor="w")
        ctk.CTkLabel(aside, text="Asigna un rol adecuado y asegúrate de que el usuario tenga acceso solo a lo necesario.",
                     wraplength=215, justify="left", font=font(10), text_color=COLORS["muted"])\
            .pack(anchor="w", pady=(3, 8))
        self.user_message = ctk.CTkLabel(aside, text="", height=18, font=font(9))
        self.user_message.pack(anchor="w")
        self.user_save = ctk.CTkButton(aside, text="＋   Guardar Nuevo", height=40,
                                       fg_color=COLORS["blue"], hover_color=COLORS["blue_dark"],
                                       font=font(11, "bold"), command=self.save_user)
        self.user_save.pack(fill="x", pady=(2, 0))

        users_box = card(self.content)
        users_box.grid(row=1, column=0, sticky="nsew", pady=(12, 0))
        users_box.grid_rowconfigure(2, weight=1)
        users_box.grid_columnconfigure(0, weight=1)
        head = ctk.CTkFrame(users_box, fg_color="transparent")
        head.grid(row=0, column=0, sticky="ew", padx=20, pady=(14, 8))
        head.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(head, text="☷", font=font(26), text_color=COLORS["blue"]).grid(row=0, column=0, rowspan=2, sticky="w")
        ctk.CTkLabel(head, text="Usuarios Existentes", font=font(15, "bold"),
                     text_color=COLORS["text"]).grid(row=0, column=0, sticky="w", padx=44)
        ctk.CTkLabel(head, text="Lista de usuarios registrados en el sistema.", font=font(9),
                     text_color=COLORS["muted"]).grid(row=1, column=0, sticky="w", padx=44)
        self.user_search = ctk.CTkEntry(head, width=390, height=38,
                                        placeholder_text="⌕   Buscar usuario por nombre, correo o rol...",
                                        fg_color=COLORS["field"], border_color=COLORS["border"], font=font(10))
        self.user_search.grid(row=0, column=1, rowspan=2, sticky="e")
        self.user_search.bind("<KeyRelease>", lambda _e: self.render_users())

        self._table_header(users_box, 1,
                           (("#", 5), ("Nombre Completo", 20), ("Correo Electrónico", 22),
                            ("Rol", 21), ("Estado", 12), ("Acciones", 20)))
        self.users_body = ctk.CTkScrollableFrame(users_box, fg_color="transparent", corner_radius=0,
                                                  scrollbar_button_color=COLORS["border"])
        self.users_body.grid(row=2, column=0, sticky="nsew", padx=14)
        self.users_body.grid_columnconfigure(0, weight=1)
        self.user_count = ctk.CTkLabel(users_box, text="", font=font(10), text_color=COLORS["muted"])
        self.user_count.grid(row=3, column=0, sticky="w", padx=18, pady=9)
        self.render_users()

    def render_users(self):
        for widget in self.users_body.winfo_children():
            widget.destroy()
        users = obtener_usuarios()
        if not users:
            users = [
                {"id": 1, "nombre": "Fernando Pichilla", "correo": "fernando@gmail.com", "id_rol": 1, "rol": "Administrador", "estado": True},
                {"id": 2, "nombre": "Fernando 2", "correo": "fernando2@gmail.com", "id_rol": 2, "rol": "Encargado de bodega", "estado": True},
                {"id": 3, "nombre": "Fernando Consultas", "correo": "consultas@gmail.com", "id_rol": 3, "rol": "Consulta / supervisión", "estado": True},
            ]
        query = self.user_search.get().strip().casefold()
        if query:
            users = [u for u in users if query in f"{u['nombre']} {u['correo']} {u['rol']}".casefold()]
        for idx, user in enumerate(users):
            row = ctk.CTkFrame(self.users_body, fg_color="transparent", height=48)
            row.grid(row=idx*2, column=0, sticky="ew")
            row.grid_propagate(False)
            for col, weight in enumerate((5, 20, 22, 21, 12, 20)):
                row.grid_columnconfigure(col, weight=weight, uniform="users")
            values = (f"[{user['id']}]", user["nombre"], user["correo"], user["rol"])
            for col, value in enumerate(values):
                ctk.CTkLabel(row, text=value, anchor="w", font=font(10),
                             text_color=COLORS["text"]).grid(row=0, column=col, sticky="ew", padx=7)
            state_color = COLORS["green"] if user["estado"] else COLORS["red"]
            state_bg = COLORS["green_bg"] if user["estado"] else COLORS["red_bg"]
            ctk.CTkLabel(row, text=" ●  Activo " if user["estado"] else " ●  Inactivo ",
                         height=28, corner_radius=14, fg_color=state_bg, text_color=state_color,
                         font=font(9)).grid(row=0, column=4, sticky="w", padx=6)
            actions = ctk.CTkFrame(row, fg_color="transparent")
            actions.grid(row=0, column=5, sticky="ew", padx=5)
            ctk.CTkButton(actions, text="✎   Editar", width=98, height=34,
                          fg_color="#506984", hover_color="#637D99", font=font(10),
                          command=lambda u=user: self.edit_user(u)).pack(side="left", padx=(0, 6))
            ctk.CTkButton(actions, text="▥   Desactivar" if user["estado"] else "✓   Activar",
                          width=122, height=34, fg_color=COLORS["red"] if user["estado"] else "#1DAD61",
                          hover_color="#D43143" if user["estado"] else "#178C4E", font=font(10),
                          command=lambda user_id=user["id"]: self.toggle_user(user_id)).pack(side="left")
            ctk.CTkFrame(self.users_body, height=1, fg_color=COLORS["border_soft"])\
                .grid(row=idx*2+1, column=0, sticky="ew")
        self.user_count.configure(text=f"Mostrando {len(users)} usuarios")

    def edit_user(self, user):
        self.id_usuario_editando = user["id"]
        for field, value in ((self.u_nombre, user["nombre"]), (self.u_correo, user["correo"])):
            field.delete(0, "end")
            field.insert(0, value)
        for role in self.role_values:
            if role.startswith(f"{user['id_rol']} -"):
                self.u_rol.set(role)
        self.user_form_title.configure(text="Editar Usuario")
        self.user_save.configure(text="✓   Actualizar Usuario")
        self.user_message.configure(text="Deja la contraseña vacía para conservarla.", text_color=COLORS["muted"])

    def save_user(self):
        name, email, password, role = (self.u_nombre.get().strip(), self.u_correo.get().strip(),
                                       self.u_pass.get(), self.u_rol.get())
        if not name or not email or "@" not in email or " - " not in role:
            self._user_msg("Completa un nombre y correo válidos.", False)
            return
        if not self.id_usuario_editando and not password:
            self._user_msg("La contraseña es obligatoria para usuarios nuevos.", False)
            return
        role_id = int(role.split(" - ", 1)[0])
        success = actualizar_usuario(self.id_usuario_editando, name, email, password, role_id) \
            if self.id_usuario_editando else crear_usuario(name, email, password, role_id)
        self._user_msg("Usuario actualizado correctamente." if self.id_usuario_editando else "Usuario creado correctamente.", success)
        if success:
            self.clear_user_form()
            self.render_users()

    def _user_msg(self, text, success):
        self.user_message.configure(text=("✓ " if success else "⚠ ") + text,
                                    text_color=COLORS["green"] if success else COLORS["red"])

    def clear_user_form(self):
        self.id_usuario_editando = None
        for field in (self.u_nombre, self.u_correo, self.u_pass):
            field.delete(0, "end")
        self.user_form_title.configure(text="Crear Usuario")
        self.user_save.configure(text="＋   Guardar Nuevo")
        self.user_message.configure(text="")

    def toggle_user(self, user_id):
        toggle_estado_usuario(user_id)
        self.render_users()

    # ---------------------------- products ----------------------------
    def _build_products(self):
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=1)
        categories = obtener_categorias() or [{"id": 1, "nombre": "Electrónica"}, {"id": 2, "nombre": "Mobiliario"}, {"id": 3, "nombre": "Papelería"}]
        units = obtener_unidades() or [{"id": 1, "nombre": "Unidad (Un)"}, {"id": 2, "nombre": "Caja (Cj)"}]
        self.category_values = [f"{x['id']} - {x['nombre']}" for x in categories]
        self.unit_values = [f"{x['id']} - {x['nombre']}" for x in units]

        form = card(self.content, height=220)
        form.grid(row=0, column=0, sticky="ew")
        form.grid_propagate(False)
        form.grid_columnconfigure((0, 1, 2), weight=1)
        ctk.CTkLabel(form, text="◇   Registrar / Editar Producto", font=font(16, "bold"),
                     text_color=COLORS["text"]).grid(row=0, column=0, columnspan=3, sticky="w", padx=22, pady=(14, 5))
        self.p_sku = self._labeled_entry(form, 1, 0, "Código Único", "Ej. ELEC-001")
        self.p_desc = self._labeled_entry(form, 1, 1, "Descripción", "Nombre del producto")
        self.p_cat = self._labeled_option(form, 1, 2, "Categoría", self.category_values)
        self.p_uni = self._labeled_option(form, 2, 0, "Unidad de Medida", self.unit_values)
        self.p_min = self._labeled_entry(form, 2, 1, "Stock Mínimo", "0")
        self.p_cost = self._labeled_entry(form, 2, 2, "Costo Promedio", "0.00")
        action = ctk.CTkFrame(form, fg_color="transparent")
        action.grid(row=3, column=0, columnspan=3, sticky="e", padx=22, pady=(4, 12))
        self.product_message = ctk.CTkLabel(action, text="", font=font(9))
        self.product_message.pack(side="left", padx=10)
        ctk.CTkButton(action, text="Limpiar", width=90, height=34, fg_color=COLORS["field"],
                      hover_color=COLORS["card_alt"], command=self.clear_product_form).pack(side="left", padx=5)
        self.product_save = ctk.CTkButton(action, text="＋  Guardar Producto", width=160, height=34,
                                           fg_color=COLORS["blue"], hover_color=COLORS["blue_dark"],
                                           command=self.save_product)
        self.product_save.pack(side="left")

        box = card(self.content)
        box.grid(row=1, column=0, sticky="nsew", pady=(12, 0))
        box.grid_rowconfigure(2, weight=1)
        box.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(box, text="☷   Catálogo de Productos", font=font(15, "bold"),
                     text_color=COLORS["text"]).grid(row=0, column=0, sticky="w", padx=20, pady=13)
        self._table_header(box, 1, (("Código", 12), ("Descripción", 31), ("Stock Mín.", 12),
                                             ("Costo", 12), ("Estado", 13), ("Acciones", 20)))
        self.products_body = ctk.CTkScrollableFrame(box, fg_color="transparent", corner_radius=0,
                                                     scrollbar_button_color=COLORS["border"])
        self.products_body.grid(row=2, column=0, sticky="nsew", padx=14)
        self.products_body.grid_columnconfigure(0, weight=1)
        self.render_products()

    def render_products(self):
        for widget in self.products_body.winfo_children():
            widget.destroy()
        products = obtener_catalogo()
        if not products:
            products = [
                {"id": 1, "codigo": "ELEC-001", "desc": "Laptop Dell Latitude 3420", "id_cat": 1, "id_uni": 1, "stock_min": 5, "costo": 5500, "estado": True},
                {"id": 2, "codigo": "ELEC-002", "desc": "Monitor LG 24 Pulgadas", "id_cat": 1, "id_uni": 1, "stock_min": 10, "costo": 1200, "estado": True},
                {"id": 3, "codigo": "MOB-001", "desc": "Silla Ergonómica Ejecutiva", "id_cat": 2, "id_uni": 1, "stock_min": 4, "costo": 850, "estado": True},
            ]
        for idx, product in enumerate(products):
            row = ctk.CTkFrame(self.products_body, fg_color="transparent", height=48)
            row.grid(row=idx*2, column=0, sticky="ew")
            row.grid_propagate(False)
            for col, weight in enumerate((12, 31, 12, 12, 13, 20)):
                row.grid_columnconfigure(col, weight=weight, uniform="products")
            values = (product["codigo"], product["desc"], f"{float(product['stock_min']):.1f}", f"${float(product['costo']):,.2f}")
            for col, value in enumerate(values):
                ctk.CTkLabel(row, text=value, anchor="w", font=font(10), text_color=COLORS["text"])\
                    .grid(row=0, column=col, sticky="ew", padx=7)
            color = COLORS["green"] if product["estado"] else COLORS["red"]
            bg = COLORS["green_bg"] if product["estado"] else COLORS["red_bg"]
            ctk.CTkLabel(row, text=" ●  Activo " if product["estado"] else " ●  Inactivo ",
                         height=28, corner_radius=14, fg_color=bg, text_color=color, font=font(9))\
                .grid(row=0, column=4, sticky="w", padx=7)
            actions = ctk.CTkFrame(row, fg_color="transparent")
            actions.grid(row=0, column=5, sticky="ew", padx=5)
            ctk.CTkButton(actions, text="✎  Editar", width=86, height=32, fg_color="#506984",
                          hover_color="#637D99", command=lambda p=product: self.edit_product(p)).pack(side="left", padx=(0, 5))
            ctk.CTkButton(actions, text="Desactivar" if product["estado"] else "Activar", width=98, height=32,
                          fg_color=COLORS["red"] if product["estado"] else "#1DAD61",
                          hover_color="#D43143", command=lambda p_id=product["id"]: self.toggle_product(p_id)).pack(side="left")
            ctk.CTkFrame(self.products_body, height=1, fg_color=COLORS["border_soft"])\
                .grid(row=idx*2+1, column=0, sticky="ew")

    def edit_product(self, product):
        self.id_producto_editando = product["id"]
        for entry, value in ((self.p_sku, product["codigo"]), (self.p_desc, product["desc"]),
                             (self.p_min, product["stock_min"]), (self.p_cost, product["costo"])):
            entry.delete(0, "end")
            entry.insert(0, str(value))
        for value in self.category_values:
            if value.startswith(f"{product['id_cat']} -"):
                self.p_cat.set(value)
        for value in self.unit_values:
            if value.startswith(f"{product['id_uni']} -"):
                self.p_uni.set(value)
        self.product_save.configure(text="✓  Actualizar Producto")

    def save_product(self):
        try:
            category_id = int(self.p_cat.get().split(" - ", 1)[0])
            unit_id = int(self.p_uni.get().split(" - ", 1)[0])
            minimum = float(self.p_min.get())
            cost = float(self.p_cost.get() or 0)
            if not self.p_sku.get().strip() or not self.p_desc.get().strip() or minimum < 0 or cost < 0:
                raise ValueError
        except (ValueError, IndexError):
            self._product_msg("Revisa los datos capturados.", False)
            return
        args = (self.p_sku.get().strip(), self.p_desc.get().strip(), category_id, unit_id, minimum, cost)
        success = actualizar_producto(self.id_producto_editando, *args) if self.id_producto_editando else crear_producto(*args)
        self._product_msg("Producto guardado correctamente.", success)
        if success:
            self.clear_product_form()
            self.render_products()

    def _product_msg(self, text, success):
        self.product_message.configure(text=("✓ " if success else "⚠ ") + text,
                                       text_color=COLORS["green"] if success else COLORS["red"])

    def clear_product_form(self):
        self.id_producto_editando = None
        for entry in (self.p_sku, self.p_desc, self.p_min, self.p_cost):
            entry.delete(0, "end")
        self.product_save.configure(text="＋  Guardar Producto")
        self.product_message.configure(text="")

    def toggle_product(self, product_id):
        toggle_estado_producto(product_id)
        self.render_products()

    # --------------------------- approvals ---------------------------
    def _build_approvals(self):
        self.content.grid_columnconfigure(0, weight=1)
        box = card(self.content)
        box.grid(row=0, column=0, sticky="nsew")
        ctk.CTkLabel(box, text="☑", width=74, height=74, corner_radius=14,
                     fg_color="#123F72", text_color="#CAE3FF", font=font(32))\
            .pack(pady=(85, 18))
        ctk.CTkLabel(box, text="No hay ajustes pendientes", font=font(21, "bold"),
                     text_color=COLORS["text"]).pack()
        ctk.CTkLabel(box, text="Cuando se registre un ajuste que requiera autorización, aparecerá en esta sección.",
                     font=font(11), text_color=COLORS["muted"], wraplength=520)\
            .pack(pady=(8, 100))

    # ---------------------------- helpers ----------------------------
    def _labeled_entry(self, parent, row, col, label, placeholder, show=None):
        box = ctk.CTkFrame(parent, fg_color="transparent")
        box.grid(row=row, column=col, sticky="ew", padx=(24 if col == 0 else 10, 10 if col < 2 else 24), pady=4)
        ctk.CTkLabel(box, text=label, font=font(10, "bold"), text_color=COLORS["text"]).pack(anchor="w", pady=(0, 3))
        entry = ctk.CTkEntry(box, placeholder_text=placeholder, show=show, height=38,
                             fg_color=COLORS["field"], border_color=COLORS["border"], font=font(10))
        entry.pack(fill="x")
        return entry

    def _labeled_option(self, parent, row, col, label, values):
        box = ctk.CTkFrame(parent, fg_color="transparent")
        box.grid(row=row, column=col, sticky="ew", padx=(24 if col == 0 else 10, 10 if col < 2 else 24), pady=4)
        ctk.CTkLabel(box, text=label, font=font(10, "bold"), text_color=COLORS["text"]).pack(anchor="w", pady=(0, 3))
        option = ctk.CTkOptionMenu(box, values=values, height=38, fg_color=COLORS["field"],
                                   button_color=COLORS["field"], button_hover_color=COLORS["card_alt"],
                                   font=font(10), dropdown_font=font(10))
        option.pack(fill="x")
        return option

    def _table_header(self, parent, row, columns):
        header = ctk.CTkFrame(parent, fg_color=COLORS["header"], height=40, corner_radius=8)
        header.grid(row=row, column=0, sticky="ew", padx=14)
        header.grid_propagate(False)
        for col, (label, weight) in enumerate(columns):
            header.grid_columnconfigure(col, weight=weight, uniform="header")
            ctk.CTkLabel(header, text=label, font=font(10, "bold"), text_color=COLORS["text"], anchor="w")\
                .grid(row=0, column=col, sticky="ew", padx=8, pady=10)
