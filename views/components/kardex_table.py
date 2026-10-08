import math
import customtkinter as ctk

from controllers.kardex_ctrl import obtener_inventario
from views.ui_theme import COLORS, HeroBanner, card, font, status_style


class InventarioView(ctk.CTkFrame):
    PAGE_SIZE = 8

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.current_page = 1
        self.sort_key = None
        self.sort_reverse = False
        self.all_rows = self._load_rows()
        self.filtered_rows = list(self.all_rows)

        HeroBanner(
            self, "Inventario", "Inventario Actual (Semáforos)",
            "Consulta el stock actual de productos con indicadores de estado.\n"
            "Visualiza, busca y filtra tu inventario de forma rápida y sencilla.",
            "Inventario\nsiempre bajo control.",
        ).grid(row=0, column=0, sticky="ew", pady=(0, 12))
        self._build_filters()
        self._build_table()
        self._apply_filters()

    def _load_rows(self):
        try:
            source = obtener_inventario()
        except Exception:
            source = []
        if not source:
            source = [
                ("ELEC-001", "Laptop Dell Latitude 3420", 5.0, "Bodega Central", 15.0),
                ("ELEC-002", "Monitor LG 24 Pulgadas", 10.0, "Bodega Central", 8.0),
                ("MOB-001", "Silla Ergonómica Ejecutiva", 4.0, "Bodega Central", 0.0),
                ("PAP-001", "Resma de Papel Tamaño Carta", 20.0, "Bodega Sucursal Norte", 50.0),
            ]
        rows = []
        for item in source:
            values = tuple(item)
            if len(values) >= 6:
                code, product, _category, minimum, warehouse, current = values[:6]
            else:
                code, product, minimum, warehouse, current = values[:5]
            state, color, bg = status_style(current, minimum)
            rows.append({"code": str(code), "product": str(product), "warehouse": str(warehouse),
                         "minimum": float(minimum or 0), "current": float(current or 0),
                         "state": state, "color": color, "state_bg": bg})
        return rows

    def _build_filters(self):
        filters = card(self, height=66)
        filters.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        filters.grid_propagate(False)
        filters.grid_columnconfigure(0, weight=2)
        filters.grid_columnconfigure(1, weight=1)
        filters.grid_columnconfigure(2, weight=1)

        self.search = ctk.CTkEntry(filters, placeholder_text="⌕   Buscar por código, producto o bodega...",
                                   height=42, corner_radius=8, fg_color=COLORS["field"],
                                   border_width=1, border_color=COLORS["border"],
                                   placeholder_text_color=COLORS["muted"], font=font(11))
        self.search.grid(row=0, column=0, sticky="ew", padx=(14, 7), pady=12)
        self.search.bind("<KeyRelease>", lambda _e: self._apply_filters(reset=True))

        warehouses = ["Todas las bodegas"] + sorted({r["warehouse"] for r in self.all_rows})
        self.warehouse_filter = ctk.CTkOptionMenu(
            filters, values=warehouses, height=42, corner_radius=8,
            fg_color=COLORS["field"], button_color=COLORS["field"],
            button_hover_color=COLORS["card_alt"], text_color=COLORS["text"],
            font=font(11), dropdown_font=font(11), command=lambda _v: self._apply_filters(reset=True))
        self.warehouse_filter.grid(row=0, column=1, sticky="ew", padx=7, pady=12)

        self.state_filter = ctk.CTkOptionMenu(
            filters, values=["Todos los estados", "Óptimo", "Bajo", "Agotado"],
            height=42, corner_radius=8, fg_color=COLORS["field"],
            button_color=COLORS["field"], button_hover_color=COLORS["card_alt"],
            text_color=COLORS["text"], font=font(11), dropdown_font=font(11),
            command=lambda _v: self._apply_filters(reset=True))
        self.state_filter.grid(row=0, column=2, sticky="ew", padx=7, pady=12)
        ctk.CTkButton(filters, text="⟳  Limpiar filtros", height=42, width=155,
                      fg_color="#123253", hover_color="#19436B", border_width=1,
                      border_color="#225280", corner_radius=8, font=font(10, "bold"),
                      command=self.clear_filters).grid(row=0, column=3, padx=(7, 14), pady=12)

    def _build_table(self):
        self.table = card(self)
        self.table.grid(row=2, column=0, sticky="nsew")
        self.table.grid_rowconfigure(1, weight=1)
        self.table.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(self.table, fg_color=COLORS["header"], height=50, corner_radius=11)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        columns = (("Código", "code", 13), ("Producto", "product", 22),
                   ("Bodega", "warehouse", 18), ("Stock Mín.", "minimum", 11),
                   ("Stock Actual", "current", 12), ("Estado", "state", 14),
                   ("Acciones", None, 10))
        for i, (label, key, weight) in enumerate(columns):
            header.grid_columnconfigure(i, weight=weight, uniform="table")
            command = (lambda k=key: self.sort_by(k)) if key else None
            ctk.CTkButton(header, text=f"{label}   ↕" if key else label, command=command,
                          height=48, fg_color="transparent", hover_color=COLORS["card_alt"],
                          text_color=COLORS["text"], font=font(10, "bold"),
                          anchor="w" if i < 6 else "center")\
                .grid(row=0, column=i, sticky="ew", padx=5)

        self.body = ctk.CTkScrollableFrame(self.table, fg_color="transparent", corner_radius=0,
                                            scrollbar_button_color=COLORS["border"])
        self.body.grid(row=1, column=0, sticky="nsew")
        self.body.grid_columnconfigure(0, weight=1)

        footer = ctk.CTkFrame(self.table, height=64, fg_color="transparent")
        footer.grid(row=2, column=0, sticky="ew")
        footer.grid_propagate(False)
        footer.grid_columnconfigure(0, weight=1)
        self.count_label = ctk.CTkLabel(footer, text="", font=font(10),
                                        text_color=COLORS["muted"])
        self.count_label.grid(row=0, column=0, sticky="w", padx=20, pady=17)
        pager = ctk.CTkFrame(footer, fg_color="transparent")
        pager.grid(row=0, column=1, sticky="e", padx=18, pady=12)
        self.prev_btn = ctk.CTkButton(pager, text="‹  Anterior", width=112, height=38,
                                      fg_color=COLORS["panel"], hover_color=COLORS["card_alt"],
                                      border_width=1, border_color=COLORS["border"],
                                      text_color=COLORS["muted"], command=lambda: self.change_page(-1))
        self.prev_btn.pack(side="left", padx=4)
        self.page_label = ctk.CTkLabel(pager, text="1", width=46, height=38, corner_radius=7,
                                       fg_color=COLORS["blue_dark"], font=font(11, "bold"))
        self.page_label.pack(side="left", padx=4)
        self.next_btn = ctk.CTkButton(pager, text="Siguiente  ›", width=112, height=38,
                                      fg_color=COLORS["panel"], hover_color=COLORS["card_alt"],
                                      border_width=1, border_color=COLORS["border"],
                                      text_color=COLORS["muted"], command=lambda: self.change_page(1))
        self.next_btn.pack(side="left", padx=4)

    def _apply_filters(self, reset=False):
        if reset:
            self.current_page = 1
        query = self.search.get().strip().casefold() if hasattr(self, "search") else ""
        warehouse = self.warehouse_filter.get() if hasattr(self, "warehouse_filter") else "Todas las bodegas"
        state = self.state_filter.get() if hasattr(self, "state_filter") else "Todos los estados"
        rows = []
        for row in self.all_rows:
            searchable = f"{row['code']} {row['product']} {row['warehouse']}".casefold()
            if query and query not in searchable:
                continue
            if warehouse != "Todas las bodegas" and row["warehouse"] != warehouse:
                continue
            if state != "Todos los estados" and row["state"] != state:
                continue
            rows.append(row)
        self.filtered_rows = rows
        self._render_rows()

    def _render_rows(self):
        for widget in self.body.winfo_children():
            widget.destroy()
        pages = max(1, math.ceil(len(self.filtered_rows) / self.PAGE_SIZE))
        self.current_page = min(self.current_page, pages)
        start = (self.current_page - 1) * self.PAGE_SIZE
        visible = self.filtered_rows[start:start+self.PAGE_SIZE]
        for index, item in enumerate(visible):
            row = ctk.CTkFrame(self.body, fg_color="transparent", height=62)
            row.grid(row=index*2, column=0, sticky="ew")
            row.grid_propagate(False)
            for col, weight in enumerate((13, 22, 18, 11, 12, 14, 10)):
                row.grid_columnconfigure(col, weight=weight, uniform="table")

            code_box = ctk.CTkFrame(row, fg_color="transparent")
            code_box.grid(row=0, column=0, sticky="w", padx=13)
            ctk.CTkLabel(code_box, text="▱", width=38, height=38, corner_radius=8,
                         fg_color="#15395C", text_color="#CDE2FF", font=font(17))\
                .pack(side="left", padx=(0, 10))
            ctk.CTkLabel(code_box, text=item["code"], font=font(10),
                         text_color=COLORS["text"]).pack(side="left")
            ctk.CTkLabel(row, text=item["product"], font=font(10), text_color=COLORS["text"],
                         anchor="w").grid(row=0, column=1, sticky="ew", padx=5)
            ctk.CTkLabel(row, text=item["warehouse"], font=font(10), text_color=COLORS["text"],
                         anchor="w").grid(row=0, column=2, sticky="ew", padx=5)
            ctk.CTkLabel(row, text=f"{item['minimum']:.1f}", font=font(10),
                         text_color=COLORS["text"], anchor="w").grid(row=0, column=3, sticky="ew", padx=5)
            ctk.CTkLabel(row, text=f"{item['current']:.1f}", font=font(10),
                         text_color=COLORS["text"], anchor="w").grid(row=0, column=4, sticky="ew", padx=5)
            ctk.CTkLabel(row, text=f"  ●   {item['state']}  ", height=36, corner_radius=8,
                         fg_color=item["state_bg"], text_color=item["color"], font=font(10))\
                .grid(row=0, column=5, sticky="ew", padx=5)
            ctk.CTkButton(row, text="⋮", width=38, height=36, corner_radius=8,
                          fg_color=COLORS["field"], hover_color=COLORS["card_alt"],
                          border_width=1, border_color=COLORS["border"], font=font(18),
                          command=lambda data=item: self.show_actions(data))\
                .grid(row=0, column=6, padx=14)
            ctk.CTkFrame(self.body, height=1, fg_color=COLORS["border_soft"])\
                .grid(row=index*2+1, column=0, sticky="ew")

        if not visible:
            ctk.CTkLabel(self.body, text="No se encontraron productos con esos filtros.",
                         text_color=COLORS["muted"], font=font(12))\
                .grid(row=0, column=0, pady=80)
        self.count_label.configure(text=f"Mostrando {len(visible)} de {len(self.filtered_rows)} productos")
        self.page_label.configure(text=str(self.current_page))
        self.prev_btn.configure(state="normal" if self.current_page > 1 else "disabled")
        self.next_btn.configure(state="normal" if self.current_page < pages else "disabled")

    def sort_by(self, key):
        if self.sort_key == key:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_key, self.sort_reverse = key, False
        self.filtered_rows.sort(key=lambda item: item[key], reverse=self.sort_reverse)
        self.current_page = 1
        self._render_rows()

    def change_page(self, delta):
        pages = max(1, math.ceil(len(self.filtered_rows) / self.PAGE_SIZE))
        self.current_page = min(pages, max(1, self.current_page + delta))
        self._render_rows()

    def clear_filters(self):
        self.search.delete(0, "end")
        self.warehouse_filter.set("Todas las bodegas")
        self.state_filter.set("Todos los estados")
        self._apply_filters(reset=True)

    def show_actions(self, item):
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Detalle - {item['code']}")
        dialog.geometry("430x330")
        dialog.resizable(False, False)
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()
        dialog.configure(fg_color=COLORS["app"])
        box = card(dialog)
        box.pack(fill="both", expand=True, padx=18, pady=18)
        ctk.CTkLabel(box, text=item["product"], font=font(18, "bold"),
                     text_color=COLORS["text"]).pack(anchor="w", padx=22, pady=(22, 4))
        ctk.CTkLabel(box, text=f"Código: {item['code']}\nBodega: {item['warehouse']}\n"
                                      f"Stock mínimo: {item['minimum']:.1f}\nStock actual: {item['current']:.1f}",
                     justify="left", font=font(12), text_color=COLORS["muted"])\
            .pack(anchor="w", padx=22, pady=12)
        ctk.CTkLabel(box, text=f"  ●   {item['state']}  ", height=36, corner_radius=8,
                     fg_color=item["state_bg"], text_color=item["color"], font=font(11, "bold"))\
            .pack(anchor="w", padx=22, pady=5)
        ctk.CTkButton(box, text="Cerrar", height=40, fg_color=COLORS["blue"],
                      hover_color=COLORS["blue_dark"], command=dialog.destroy)\
            .pack(fill="x", padx=22, pady=(18, 22))
