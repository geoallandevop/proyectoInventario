import customtkinter as ctk

from views.ui_theme import (
    BrandLogo, COLORS, CubeArt, VectorIcon, card, font, get_theme, set_theme,
)


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class LoginWindow(ctk.CTk):
    """Access screen reproduced from the Kardex Pro mockup."""

    def __init__(self):
        super().__init__()
        self.title("Sistema Kardex - Acceso")
        self.minsize(1100, 700)
        self.configure(fg_color=COLORS["app"])
        self._place_initial_window()

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=39)
        self.grid_columnconfigure(1, weight=61)
        self.show_password = False
        self._build_window()
        self.bind("<Return>", self.login_event)

    def _build_window(self):
        self.configure(fg_color=COLORS["app"])
        self._build_brand_panel()
        self._build_login_panel()
        self._build_footer()

    def _place_initial_window(self):
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        width = min(1440, max(1100, sw - 60))
        height = min(900, max(700, sh - 90))
        x, y = max(0, (sw-width)//2), max(0, (sh-height)//2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _build_brand_panel(self):
        panel = ctk.CTkFrame(self, fg_color=COLORS["sidebar"], corner_radius=0)
        panel.grid(row=0, column=0, sticky="nsew")
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(3, weight=1)

        BrandLogo(panel).grid(row=0, column=0, sticky="w", padx=58, pady=(64, 44))

        copy = ctk.CTkFrame(panel, fg_color="transparent")
        copy.grid(row=1, column=0, sticky="ew", padx=58)
        ctk.CTkLabel(copy, text="Control que impulsa", font=font(25),
                     text_color=COLORS["text"], anchor="w").pack(fill="x")
        ctk.CTkLabel(copy, text="tu negocio", font=font(25, "bold"),
                     text_color=COLORS["cyan"], anchor="w").pack(fill="x")
        ctk.CTkFrame(copy, width=60, height=4, corner_radius=2,
                     fg_color=COLORS["cyan"]).pack(anchor="w", pady=(26, 22))
        ctk.CTkLabel(copy, text="Gestiona tu inventario de forma\neficiente, precisa y segura.",
                     font=font(17), text_color=COLORS["muted"], justify="left",
                     anchor="w").pack(fill="x")

        artwork = CubeArt(panel, bg=COLORS["sidebar"], height=280)
        artwork.grid(row=2, column=0, sticky="nsew", padx=34, pady=(8, 0))

        benefits = ctk.CTkFrame(panel, fg_color="transparent")
        benefits.grid(row=3, column=0, sticky="sew", padx=45, pady=(0, 28))
        benefits.grid_columnconfigure((0, 1, 2), weight=1)
        items = (("◇", "Seguro", "y confiable"),
                 ("▥", "Inventario", "en tiempo real"),
                 ("◎", "Diseñado", "para tu negocio"))
        for col, (icon, title, subtitle) in enumerate(items):
            item = ctk.CTkFrame(benefits, fg_color="transparent")
            item.grid(row=0, column=col, sticky="ew", padx=8)
            ctk.CTkLabel(item, text=icon, width=56, height=56, corner_radius=10,
                         fg_color=COLORS["card_alt"], text_color=COLORS["blue"],
                         font=font(26)).pack()
            ctk.CTkLabel(item, text=title, font=font(13, "bold"),
                         text_color=COLORS["text"]).pack(pady=(8, 0))
            ctk.CTkLabel(item, text=subtitle, font=font(12),
                         text_color=COLORS["muted"]).pack()

    def _build_login_panel(self):
        panel = ctk.CTkFrame(self, fg_color=COLORS["app"], corner_radius=0)
        panel.grid(row=0, column=1, sticky="nsew")
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(0, weight=1)

        form_card = card(panel, width=705, height=610, fg_color=COLORS["panel"])
        form_card.grid(row=0, column=0, padx=70, pady=70, sticky="nsew")
        form_card.grid_propagate(False)
        form_card.grid_columnconfigure(0, weight=1)
        form_card.grid_rowconfigure(8, weight=1)

        ctk.CTkLabel(form_card, text="B I E N V E N I D O", font=font(14, "bold"),
                     text_color=COLORS["muted"]).grid(row=0, column=0, pady=(58, 12))
        ctk.CTkLabel(form_card, text="Sistema Kardex", font=font(43, "bold"),
                     text_color=COLORS["text"]).grid(row=1, column=0)
        ctk.CTkLabel(form_card,
                     text="Inicia sesión para continuar y acceder\na tu sistema de inventario.",
                     font=font(17), text_color=COLORS["muted"], justify="center")\
            .grid(row=2, column=0, pady=(10, 32))

        self.entry_email = self._login_entry(form_card, 3, "user", "Usuario")
        self.entry_password = self._login_entry(form_card, 4, "lock", "Contraseña", password=True)

        self.label_error = ctk.CTkLabel(form_card, text="", height=24,
                                        font=font(12), text_color=COLORS["red"])
        self.label_error.grid(row=5, column=0, sticky="w", padx=72, pady=(4, 0))

        self.button_login = ctk.CTkButton(
            form_card, text="Iniciar Sesión                              →",
            height=62, corner_radius=9, fg_color=COLORS["blue"],
            hover_color=COLORS["blue_dark"], font=font(18, "bold"),
            command=self.login_event)
        self.button_login.grid(row=6, column=0, sticky="ew", padx=72, pady=(4, 0))

        help_row = ctk.CTkFrame(form_card, fg_color="transparent")
        help_row.grid(row=7, column=0, sticky="ew", padx=72, pady=(42, 0))
        help_row.grid_columnconfigure((0, 2), weight=1)
        ctk.CTkFrame(help_row, height=1, fg_color=COLORS["border"]).grid(row=0, column=0, sticky="ew")
        ctk.CTkLabel(help_row, text="¿Necesitas ayuda?", font=font(12),
                     text_color=COLORS["muted"]).grid(row=0, column=1, padx=14)
        ctk.CTkFrame(help_row, height=1, fg_color=COLORS["border"]).grid(row=0, column=2, sticky="ew")
        ctk.CTkLabel(form_card, text="Contacta al administrador del sistema.",
                     font=font(12), text_color=COLORS["muted"]).grid(row=8, column=0, sticky="n", pady=(8, 0))

    def _build_footer(self):
        footer = ctk.CTkFrame(self, fg_color=COLORS["sidebar"], corner_radius=0,
                              height=78, border_width=1, border_color=COLORS["border_soft"])
        footer.grid(row=1, column=0, columnspan=2, sticky="ew")
        footer.grid_propagate(False)
        footer.grid_columnconfigure(0, weight=1)
        brand = ctk.CTkFrame(footer, fg_color="transparent")
        brand.grid(row=0, column=0, sticky="w", padx=42, pady=16)
        ctk.CTkLabel(brand, text="KARDEX PRO   v1.0.0", font=font(11),
                     text_color=COLORS["muted"]).pack(anchor="w")
        ctk.CTkLabel(brand, text="Control  •  Inventario  •  Resultados",
                     font=font(10), text_color=COLORS["muted_2"]).pack(anchor="w")
        theme = ctk.CTkFrame(footer, fg_color="transparent")
        theme.grid(row=0, column=1, sticky="e", padx=42)
        ctk.CTkLabel(theme, text="◕", width=42, height=42, corner_radius=21,
                     fg_color=COLORS["card"], font=font(22),
                     text_color=COLORS["text"]).pack(side="left", padx=(0, 12))
        text = ctk.CTkFrame(theme, fg_color="transparent")
        text.pack(side="left")
        ctk.CTkLabel(text, text="Tema Visual", font=font(10),
                     text_color=COLORS["muted"]).pack(anchor="w")
        self.theme_selector = ctk.CTkOptionMenu(
            text, values=["Dark", "Light"], width=92, height=28,
            fg_color=COLORS["sidebar"], button_color=COLORS["sidebar"],
            button_hover_color=COLORS["card_alt"], dropdown_fg_color=COLORS["card"],
            dropdown_hover_color=COLORS["card_alt"], text_color=COLORS["text"],
            font=font(12, "bold"), dropdown_font=font(11), command=self.change_theme)
        self.theme_selector.set(get_theme())
        self.theme_selector.pack(anchor="w")

    def _login_entry(self, parent, row, icon, placeholder, password=False):
        shell = ctk.CTkFrame(parent, height=58, corner_radius=9,
                             fg_color=COLORS["field"], border_width=1,
                             border_color=COLORS["border"])
        shell.grid(row=row, column=0, sticky="ew", padx=72, pady=(18 if row == 4 else 0, 0))
        shell.pack_propagate(False)
        VectorIcon(shell, icon, size=26, bg=COLORS["field"], fg=COLORS["muted"])\
            .pack(side="left", padx=(18, 10))
        entry = ctk.CTkEntry(shell, placeholder_text=placeholder,
                             show="" if password and self.show_password else ("●" if password else ""),
                             height=52, corner_radius=0, fg_color="transparent",
                             border_width=0, text_color=COLORS["text"],
                             placeholder_text_color=COLORS["muted"], font=font(16))
        entry.pack(side="left", fill="both", expand=True, pady=2)
        if password:
            VectorIcon(shell, "eye", size=28, bg=COLORS["field"], fg=COLORS["muted"],
                       command=self.toggle_password).pack(side="right", padx=(8, 18))
        return entry

    def toggle_password(self):
        self.show_password = not self.show_password
        self.entry_password.configure(show="" if self.show_password else "●")

    def change_theme(self, selected):
        email = self.entry_email.get() if hasattr(self, "entry_email") else ""
        password = self.entry_password.get() if hasattr(self, "entry_password") else ""
        set_theme(selected)
        for widget in self.winfo_children():
            widget.destroy()
        self._build_window()
        self.entry_email.insert(0, email)
        self.entry_password.insert(0, password)

    def login_event(self, _event=None):
        email = self.entry_email.get().strip()
        password = self.entry_password.get()
        if not email or not password:
            self.label_error.configure(text="Ingresa tu usuario y contraseña.")
            return

        self.button_login.configure(state="disabled", text="Validando credenciales...")
        self.label_error.configure(text="")
        self.update_idletasks()
        from controllers.auth_ctrl import authenticate_user, get_user_role
        from views.main_dashboard import MainDashboard

        usuario, mensaje = authenticate_user(email, password)
        if usuario:
            rol = get_user_role(usuario)
            self.withdraw()
            MainDashboard(self, usuario, rol)
        else:
            self.label_error.configure(text=mensaje)
            self.button_login.configure(state="normal", text="Iniciar Sesión                              →")


if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()
