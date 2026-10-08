import datetime
import customtkinter as ctk

from views.ui_theme import (
    BrandLogo, COLORS, VectorIcon, flat_button, font, get_theme, set_theme,
)


class MainDashboard(ctk.CTkToplevel):
    def __init__(self, parent, usuario_logueado, nombre_rol):
        super().__init__(parent)
        self.usuario = usuario_logueado
        self.rol = (nombre_rol or "USUARIO").upper()
        self.active_section = "Inicio / Dashboard"
        self.title(f"Sistema Kardex - Dashboard ({self.rol})")
        self.minsize(1120, 720)
        self.configure(fg_color=COLORS["app"])
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self._place_window()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self._build_shell()

    def _build_shell(self):
        self.configure(fg_color=COLORS["app"])
        self._build_sidebar()
        self._build_workspace()
        routes = {
            "Inicio / Dashboard": self.show_dashboard_home,
            "Consultar Inventario": self.show_inventario,
            "Registrar Movimiento": self.show_movimientos,
            "Administración": self.show_admin,
        }
        route = routes.get(self.active_section, self.show_dashboard_home)
        if self.active_section not in self.nav_buttons:
            self.active_section = next(iter(self.nav_buttons))
            route = routes[self.active_section]
        self.navigate(self.active_section, route)

    def _place_window(self):
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        width = min(1440, max(1120, sw - 60))
        height = min(900, max(720, sh - 90))
        self.geometry(f"{width}x{height}+{max(0,(sw-width)//2)}+{max(0,(sh-height)//2)}")

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=265, corner_radius=0,
                                    fg_color=COLORS["sidebar"])
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_columnconfigure(0, weight=1)
        self.sidebar.grid_rowconfigure(3, weight=1)

        BrandLogo(self.sidebar, compact=True).grid(row=0, column=0, sticky="w",
                                                   padx=28, pady=(30, 26))
        self._build_profile()

        nav = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav.grid(row=2, column=0, sticky="new", padx=15)
        nav.grid_columnconfigure(0, weight=1)
        self.nav_buttons = {}
        items = []
        if self.rol == "ADMINISTRADOR":
            items.append(("Inicio / Dashboard", "⌂", self.show_dashboard_home))
        items.append(("Consultar Inventario", "▤", self.show_inventario))
        if self.rol in ("ADMINISTRADOR", "ENCARGADO DE BODEGA"):
            items.append(("Registrar Movimiento", "⇄", self.show_movimientos))
        if self.rol == "ADMINISTRADOR":
            items.append(("Administración", "⚙", self.show_admin))

        for row, (name, icon, command) in enumerate(items):
            btn = flat_button(nav, f"  {icon}     {name}",
                              command=lambda n=name, c=command: self.navigate(n, c))
            btn.grid(row=row, column=0, sticky="ew", pady=5)
            self.nav_buttons[name] = btn

        utility = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        utility.grid(row=4, column=0, sticky="sew", padx=22, pady=(10, 22))
        utility.grid_columnconfigure(0, weight=1)
        ctk.CTkFrame(utility, height=1, fg_color=COLORS["border"]).grid(row=0, column=0, sticky="ew", pady=(0, 18))
        ctk.CTkButton(utility, text="⇥    Cerrar Sesión", command=self.logout,
                      height=44, corner_radius=8, fg_color="#DB3948",
                      hover_color="#B92D3A", font=font(13, "bold"))\
            .grid(row=1, column=0, sticky="ew")
        ctk.CTkLabel(utility, text="Tema Visual", font=font(10),
                     text_color=COLORS["muted"], anchor="w").grid(row=2, column=0, sticky="ew", pady=(96, 5))
        theme_border = ctk.CTkFrame(utility, height=42, corner_radius=8,
                                    fg_color=COLORS["border"])
        theme_border.grid(row=3, column=0, sticky="ew")
        theme_border.grid_propagate(False)
        theme_border.grid_columnconfigure(0, weight=1)
        self.theme_selector = ctk.CTkOptionMenu(
            theme_border, values=["Dark", "Light"], height=38, corner_radius=7,
            fg_color=COLORS["card"], button_color=COLORS["card"],
            button_hover_color=COLORS["card_alt"], dropdown_fg_color=COLORS["card"],
            dropdown_hover_color=COLORS["card_alt"], text_color=COLORS["text"],
            font=font(11), dropdown_font=font(10), command=self.change_theme)
        self.theme_selector.grid(row=0, column=0, sticky="ew", padx=1, pady=1)
        self.theme_selector.set(get_theme())
        ctk.CTkLabel(utility, text="KARDEX PRO   v1.0.0", font=font(9),
                     text_color=COLORS["muted"], anchor="w").grid(row=4, column=0, sticky="ew", pady=(24, 0))
        ctk.CTkLabel(utility, text="Control  •  Inventario  •  Resultados",
                     font=font(9), text_color=COLORS["muted_2"], anchor="w")\
            .grid(row=5, column=0, sticky="ew")

    def _build_profile(self):
        frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        frame.grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 24))
        name = getattr(self.usuario, "NOMBRE_COMPLETO", "Usuario Kardex")
        initials = "".join(part[0] for part in name.split()[:2]).upper() or "UK"
        ctk.CTkLabel(frame, text=initials, width=58, height=58, corner_radius=29,
                     fg_color="#193756", border_width=1, border_color="#4677A9",
                     font=font(16, "bold"), text_color="#CFE4FF")\
            .grid(row=0, column=0, rowspan=3, padx=(0, 14))
        ctk.CTkLabel(frame, text=name, font=font(12, "bold"),
                     text_color=COLORS["text"], anchor="w")\
            .grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(frame, text=f"[{self.rol}]", font=font(10),
                     text_color=COLORS["muted"], anchor="w")\
            .grid(row=1, column=1, sticky="w")
        ctk.CTkLabel(frame, text="●  En línea", font=font(10),
                     text_color=COLORS["green"], anchor="w")\
            .grid(row=2, column=1, sticky="w", pady=(3, 0))

    def _build_workspace(self):
        workspace = ctk.CTkFrame(self, fg_color=COLORS["app"], corner_radius=0)
        workspace.grid(row=0, column=1, sticky="nsew")
        workspace.grid_rowconfigure(1, weight=1)
        workspace.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(workspace, height=82, fg_color=COLORS["app"], corner_radius=0)
        header.grid(row=0, column=0, sticky="ew", padx=18)
        header.grid_propagate(False)
        header.grid_columnconfigure(0, weight=1)
        now = datetime.datetime.now()
        months = ("enero", "febrero", "marzo", "abril", "mayo", "junio",
                  "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre")
        weekdays = ("Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo")
        date_text = f"{weekdays[now.weekday()]}, {now.day} de {months[now.month-1]} de {now.year}\n{now.strftime('%I:%M %p').lower()}"
        right = ctk.CTkFrame(header, fg_color=COLORS["app"])
        right.grid(row=0, column=1, sticky="e", pady=15)
        VectorIcon(right, "calendar", size=30, bg=COLORS["app"], fg=COLORS["muted"])\
            .pack(side="left", padx=(0, 12))
        ctk.CTkLabel(right, text=date_text, font=font(10), justify="left",
                     text_color=COLORS["muted"]).pack(side="left")
        ctk.CTkFrame(right, width=1, height=38, fg_color=COLORS["border"])\
            .pack(side="left", padx=25)
        bell = ctk.CTkFrame(right, width=46, height=46, corner_radius=8,
                            fg_color=COLORS["app"])
        bell.pack(side="left")
        bell.pack_propagate(False)
        VectorIcon(bell, "bell", size=30, bg=COLORS["app"], fg=COLORS["text"],
                   command=self.show_notifications).place(relx=.5, rely=.53, anchor="center")
        ctk.CTkLabel(bell, text="1", width=17, height=17, corner_radius=9,
                     fg_color=COLORS["red"], text_color="white", font=font(8, "bold"))\
            .place(x=29, y=1)
        ctk.CTkFrame(right, width=1, height=38, fg_color=COLORS["border"])\
            .pack(side="left", padx=(14, 18))
        product = ctk.CTkFrame(right, fg_color=COLORS["app"])
        product.pack(side="left")
        ctk.CTkLabel(product, text="Sistema Kardex", font=font(11, "bold"),
                     text_color=COLORS["text"], anchor="w").pack(anchor="w")
        ctk.CTkLabel(product, text="Control que impulsa tu negocio", font=font(8),
                     text_color=COLORS["muted"], anchor="w").pack(anchor="w")

        self.content_frame = ctk.CTkFrame(workspace, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=(16, 14), pady=(0, 14))

    def navigate(self, name, command):
        self.active_section = name
        for label, button in self.nav_buttons.items():
            active = label == name
            button.configure(fg_color=COLORS["blue_dark"] if active else "transparent",
                             text_color=COLORS["text"],
                             border_width=1 if active else 0)
        command()
        suffix = "Dashboard" if name == "Inicio / Dashboard" else name
        self.title(f"Sistema Kardex - {suffix} ({self.rol})")

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_dashboard_home(self):
        self.clear_content()
        from views.components.dashboard_home import DashboardHomeView
        DashboardHomeView(self.content_frame, dashboard=self).pack(fill="both", expand=True)

    def show_inventario(self):
        self.clear_content()
        from views.components.kardex_table import InventarioView
        InventarioView(self.content_frame).pack(fill="both", expand=True)

    def show_movimientos(self):
        self.clear_content()
        from views.forms.movimiento_view import RegistroMovimientoView
        RegistroMovimientoView(self.content_frame, self.usuario).pack(fill="both", expand=True)

    def show_admin(self):
        self.clear_content()
        from views.forms.admin_view import AdminView
        AdminView(self.content_frame).pack(fill="both", expand=True)

    def show_notifications(self):
        pop = ctk.CTkToplevel(self)
        pop.title("Alertas de Kardex")
        pop.geometry("390x300")
        pop.resizable(False, False)
        pop.configure(fg_color=COLORS["app"])
        pop.transient(self)
        card_box = ctk.CTkFrame(pop, fg_color=COLORS["card"], corner_radius=12,
                                border_width=1, border_color=COLORS["border"])
        card_box.pack(fill="both", expand=True, padx=18, pady=18)
        ctk.CTkLabel(card_box, text="Alertas de stock", font=font(18, "bold"),
                     text_color=COLORS["text"]).pack(anchor="w", padx=20, pady=(18, 10))
        for product, detail, color in (("Monitor LG 24 Pulgadas", "Stock bajo: 8 / 10", COLORS["yellow"]),
                                       ("Silla Ergonómica Ejecutiva", "Agotado: 0 / 4", COLORS["red"])):
            row = ctk.CTkFrame(card_box, fg_color=COLORS["panel"], corner_radius=8)
            row.pack(fill="x", padx=18, pady=5)
            ctk.CTkLabel(row, text="●", text_color=color, font=font(14)).pack(side="left", padx=12)
            labels = ctk.CTkFrame(row, fg_color="transparent")
            labels.pack(side="left", fill="x", expand=True, pady=9)
            ctk.CTkLabel(labels, text=product, font=font(11, "bold"),
                         text_color=COLORS["text"]).pack(anchor="w")
            ctk.CTkLabel(labels, text=detail, font=font(10),
                         text_color=COLORS["muted"]).pack(anchor="w")
        ctk.CTkButton(card_box, text="Ver inventario", fg_color=COLORS["blue"],
                      hover_color=COLORS["blue_dark"], command=lambda: (pop.destroy(), self.navigate("Consultar Inventario", self.show_inventario)))\
            .pack(fill="x", padx=18, pady=15)

    def change_theme(self, selected):
        active = self.active_section
        set_theme(selected)
        self.active_section = active
        for widget in self.winfo_children():
            widget.destroy()
        self._build_shell()

    def on_closing(self):
        self.master.destroy()

    def logout(self):
        self.destroy()
        self.master.deiconify()
        self.master.entry_password.delete(0, "end")
        self.master.label_error.configure(text="")
        self.master.button_login.configure(state="normal", text="Iniciar Sesión                              →")
