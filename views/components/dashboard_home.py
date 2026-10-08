import customtkinter as ctk

from views.ui_theme import BarChart, COLORS, HeroBanner, SimpleDonut, card, font


class DashboardHomeView(ctk.CTkScrollableFrame):
    def __init__(self, parent, dashboard=None):
        super().__init__(parent, fg_color="transparent", corner_radius=0,
                         scrollbar_button_color=COLORS["border"],
                         scrollbar_button_hover_color=COLORS["blue_dark"])
        self.dashboard = dashboard
        self.grid_columnconfigure(0, weight=1)

        HeroBanner(
            self, "Bienvenido", "Bienvenido al Sistema Kardex",
            "Gestiona tu inventario de forma eficiente, precisa y segura.\n"
            "Selecciona un módulo en el menú o utiliza los accesos rápidos.",
            "Inventario hoy,\nun mejor mañana.",
        ).grid(row=0, column=0, sticky="ew", pady=(0, 12))

        self.summary = self._get_summary()
        self._build_kpis()
        self._build_middle()
        self._build_bottom()

    def _get_summary(self):
        fallback = {"productos": 128, "bodegas": 4, "alertas": 3, "movimientos": 24}
        try:
            from controllers.kardex_ctrl import obtener_resumen_dashboard
            data = obtener_resumen_dashboard()
            if data and data.get("productos"):
                fallback.update(data)
        except Exception:
            pass
        return fallback

    def _build_kpis(self):
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        row.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="kpi")
        items = (
            ("◇", self.summary["productos"], "Productos", "Total en inventario", COLORS["blue"]),
            ("▣", self.summary["bodegas"], "Bodegas", "Sucursales activas", "#1FB968"),
            ("△", self.summary["alertas"], "Productos en alerta", "Stock bajo o agotado", COLORS["yellow"]),
            ("↕", self.summary["movimientos"], "Movimientos (hoy)", "Entradas y salidas", COLORS["purple"]),
        )
        for col, item in enumerate(items):
            self._kpi(row, col, *item)

    def _kpi(self, parent, col, icon, value, title, subtitle, color):
        box = card(parent, height=104)
        box.grid(row=0, column=col, sticky="nsew",
                 padx=(0 if col == 0 else 6, 0 if col == 3 else 6))
        box.grid_propagate(False)
        box.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(box, text=icon, width=70, height=70, corner_radius=11,
                     fg_color=color, font=font(30, "bold"), text_color="white")\
            .grid(row=0, column=0, rowspan=3, padx=14, pady=16)
        ctk.CTkLabel(box, text=str(value), font=font(21, "bold"),
                     text_color=COLORS["text"], anchor="w")\
            .grid(row=0, column=1, sticky="sw", pady=(14, 0))
        ctk.CTkLabel(box, text=title, font=font(11, "bold"),
                     text_color=COLORS["text"], anchor="w")\
            .grid(row=1, column=1, sticky="nw")
        ctk.CTkLabel(box, text=subtitle, font=font(9), text_color=COLORS["muted"], anchor="w")\
            .grid(row=2, column=1, sticky="nw", pady=(0, 14))
        ctk.CTkLabel(box, text="›", font=font(23), text_color=COLORS["muted"])\
            .grid(row=0, column=2, rowspan=3, padx=12)

    def _build_middle(self):
        middle = ctk.CTkFrame(self, fg_color="transparent")
        middle.grid(row=2, column=0, sticky="nsew", pady=(0, 12))
        middle.grid_columnconfigure(0, weight=52, uniform="middle")
        middle.grid_columnconfigure(1, weight=25, uniform="middle")
        middle.grid_columnconfigure(2, weight=27, uniform="middle")

        graph = card(middle, height=268)
        graph.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        graph.grid_propagate(False)
        graph.grid_rowconfigure(1, weight=1)
        graph.grid_columnconfigure(0, weight=1)
        head = ctk.CTkFrame(graph, fg_color="transparent")
        head.grid(row=0, column=0, sticky="ew", padx=16, pady=(13, 5))
        head.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(head, text="▥   Movimientos de Inventario", font=font(13, "bold"),
                     text_color=COLORS["text"]).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(head, text="Últimos 7 días", font=font(9),
                     text_color=COLORS["muted"]).grid(row=1, column=0, sticky="w", padx=24)
        ctk.CTkButton(head, text="Entradas y Salidas    ﹀", width=155, height=34,
                      fg_color=COLORS["field"], hover_color=COLORS["card_alt"],
                      border_width=1, border_color=COLORS["border"], font=font(10))\
            .grid(row=0, column=1, rowspan=2)
        BarChart(graph).grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 8))

        stock = card(middle, height=268)
        stock.grid(row=0, column=1, sticky="nsew", padx=6)
        stock.grid_propagate(False)
        ctk.CTkLabel(stock, text="◇   Estado de Stock", font=font(12, "bold"),
                     text_color=COLORS["text"]).pack(anchor="w", padx=15, pady=(14, 3))
        SimpleDonut(stock, height=150, total=self.summary["productos"]).pack(fill="x", padx=20)
        for label, count, pct, color in (("Óptimo", 98, "76%", COLORS["green"]),
                                         ("Stock Bajo", 22, "17%", COLORS["yellow"]),
                                         ("Agotado", 8, "6%", COLORS["red"])):
            line = ctk.CTkFrame(stock, fg_color="transparent", height=20)
            line.pack(fill="x", padx=18)
            ctk.CTkLabel(line, text="●", text_color=color, font=font(11)).pack(side="left")
            ctk.CTkLabel(line, text=label, text_color=COLORS["text"], font=font(10)).pack(side="left", padx=7)
            ctk.CTkLabel(line, text=pct, text_color=COLORS["muted"], font=font(9)).pack(side="right")
            ctk.CTkLabel(line, text=str(count), text_color=COLORS["text"], font=font(9, "bold")).pack(side="right", padx=9)

        alerts = card(middle, height=268)
        alerts.grid(row=0, column=2, sticky="nsew", padx=(6, 0))
        alerts.grid_propagate(False)
        header = ctk.CTkFrame(alerts, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(13, 6))
        ctk.CTkLabel(header, text="Alertas de Stock", font=font(12, "bold"),
                     text_color=COLORS["text"]).pack(side="left")
        ctk.CTkButton(header, text="Ver todas", width=60, height=24,
                      fg_color="transparent", hover_color=COLORS["card_alt"],
                      text_color=COLORS["cyan"], font=font(9), command=self._go_inventory).pack(side="right")
        ctk.CTkFrame(alerts, height=1, fg_color=COLORS["border"]).pack(fill="x")
        self._alert(alerts, "Monitor LG 24 Pulgadas", "ELEC-002", "Stock Bajo", "8 / 10", COLORS["yellow"])
        self._alert(alerts, "Silla Ergonómica Ejecutiva", "MOB-001", "Agotado", "0 / 4", COLORS["red"])
        self._alert(alerts, "Teclado Mecánico RGB", "ELEC-005", "Stock Bajo", "2 / 5", COLORS["yellow"])

    def _alert(self, parent, name, code, status, stock, color):
        row = ctk.CTkFrame(parent, fg_color="transparent", height=62)
        row.pack(fill="x", padx=8)
        ctk.CTkLabel(row, text="◇", width=36, height=36, corner_radius=8,
                     fg_color=COLORS["card_alt"], text_color=COLORS["blue"], font=font(18))\
            .pack(side="left", padx=(0, 8))
        text = ctk.CTkFrame(row, fg_color="transparent")
        text.pack(side="left", fill="both", expand=True, pady=6)
        ctk.CTkLabel(text, text=name, font=font(9), text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(text, text=code, font=font(8), text_color=COLORS["muted"]).pack(anchor="w")
        stat = ctk.CTkFrame(text, fg_color="transparent")
        stat.pack(anchor="w")
        ctk.CTkLabel(stat, text=f"  {status}  ", height=20, corner_radius=10,
                     fg_color=color, text_color="#071421", font=font(8, "bold")).pack(side="left")
        ctk.CTkLabel(stat, text=stock, font=font(9, "bold"), text_color=COLORS["text"]).pack(side="left", padx=8)
        ctk.CTkButton(row, text="›", width=24, height=28, fg_color="transparent",
                      hover_color=COLORS["card_alt"], command=self._go_inventory).pack(side="right")
        ctk.CTkFrame(parent, height=1, fg_color=COLORS["border_soft"]).pack(fill="x", padx=8)

    def _build_bottom(self):
        bottom = ctk.CTkFrame(self, fg_color="transparent")
        bottom.grid(row=3, column=0, sticky="ew")
        bottom.grid_columnconfigure(0, weight=1)
        bottom.grid_columnconfigure(1, weight=1)

        quick = card(bottom, height=205)
        quick.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        quick.grid_propagate(False)
        ctk.CTkLabel(quick, text="ϟ   Accesos Rápidos", font=font(13, "bold"),
                     text_color=COLORS["text"]).pack(anchor="w", padx=16, pady=(14, 0))
        ctk.CTkLabel(quick, text="Accede a las funciones principales del sistema", font=font(9),
                     text_color=COLORS["muted"]).pack(anchor="w", padx=42)
        buttons = ctk.CTkFrame(quick, fg_color="transparent")
        buttons.pack(fill="both", expand=True, padx=12, pady=12)
        buttons.grid_columnconfigure((0, 1, 2), weight=1, uniform="quick")
        actions = (("▤\nConsultar\nInventario  ›", COLORS["blue"], self._go_inventory),
                   ("⇄\nRegistrar\nMovimiento  ›", "#1FB35E", self._go_movement),
                   ("⚙\nAdministración  ›", COLORS["purple"], self._go_admin))
        for col, (label, color, command) in enumerate(actions):
            ctk.CTkButton(buttons, text=label, height=118, corner_radius=10,
                          fg_color=color, hover_color=COLORS["blue_dark"],
                          font=font(12, "bold"), command=command)\
                .grid(row=0, column=col, sticky="nsew", padx=5)

        activity = card(bottom, height=205)
        activity.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
        activity.grid_propagate(False)
        head = ctk.CTkFrame(activity, fg_color="transparent")
        head.pack(fill="x", padx=16, pady=(13, 5))
        ctk.CTkLabel(head, text="◷   Actividad Reciente", font=font(12, "bold"),
                     text_color=COLORS["text"]).pack(side="left")
        ctk.CTkButton(head, text="Ver todas", width=62, height=24, fg_color="transparent",
                      hover_color=COLORS["card_alt"], text_color=COLORS["cyan"],
                      font=font(9), command=self._go_movement).pack(side="right")
        data = (("↑", "Entrada", "Laptop Dell Latitude 3420", "Hace 12 min", COLORS["green"]),
                ("↓", "Salida", "Resma de Papel Tamaño Carta", "Hace 28 min", COLORS["red"]),
                ("↑", "Entrada", "Monitor LG 24 Pulgadas", "Hace 1 hora", COLORS["green"]),
                ("↓", "Salida", "Silla Ergonómica Ejecutiva", "Hace 2 horas", COLORS["red"]),
                ("↑", "Entrada", "Mouse Inalámbrico Logitech", "Hace 3 horas", COLORS["green"]))
        for icon, kind, product, when, color in data:
            row = ctk.CTkFrame(activity, fg_color="transparent", height=26)
            row.pack(fill="x", padx=16)
            ctk.CTkLabel(row, text=icon, width=24, font=font(17, "bold"), text_color=color).pack(side="left")
            ctk.CTkLabel(row, text=kind, width=76, anchor="w", font=font(9), text_color=color).pack(side="left")
            ctk.CTkLabel(row, text=product, anchor="w", font=font(9), text_color=COLORS["text"]).pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(row, text=when, font=font(9), text_color=COLORS["muted"]).pack(side="right")
            ctk.CTkLabel(row, text="›", font=font(14), text_color=COLORS["muted"]).pack(side="right", padx=(8, 0))

    def _navigate(self, label, method_name):
        if self.dashboard and label in self.dashboard.nav_buttons:
            self.dashboard.navigate(label, getattr(self.dashboard, method_name))

    def _go_inventory(self):
        self._navigate("Consultar Inventario", "show_inventario")

    def _go_movement(self):
        self._navigate("Registrar Movimiento", "show_movimientos")

    def _go_admin(self):
        self._navigate("Administración", "show_admin")
