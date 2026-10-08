"""Shared visual language for the Kardex Pro desktop interface."""

import tkinter as tk
import customtkinter as ctk


DARK_COLORS = {
    "app": "#071421",
    "sidebar": "#0B1D2D",
    "panel": "#0D1C2B",
    "card": "#102131",
    "card_alt": "#13283A",
    "field": "#102437",
    "border": "#244057",
    "border_soft": "#1A3348",
    "text": "#F3F7FF",
    "muted": "#9CB7D7",
    "muted_2": "#6F8CAB",
    "blue": "#078DF4",
    "blue_dark": "#056CD7",
    "cyan": "#0AA8FF",
    "green": "#22DD79",
    "green_bg": "#0B4A36",
    "yellow": "#FFBF17",
    "yellow_bg": "#4C4219",
    "red": "#FF4655",
    "red_bg": "#521E29",
    "purple": "#7B43E8",
    "header": "#10283D",
}

LIGHT_COLORS = {
    "app": "#EDF3F8",
    "sidebar": "#E3EDF5",
    "panel": "#F7FAFD",
    "card": "#FFFFFF",
    "card_alt": "#E7F0F8",
    "field": "#F1F6FA",
    "border": "#B8CCDD",
    "border_soft": "#D5E1EA",
    "text": "#102438",
    "muted": "#526F89",
    "muted_2": "#7890A5",
    "blue": "#078DF4",
    "blue_dark": "#056CD7",
    "cyan": "#008FE5",
    "green": "#0DA95A",
    "green_bg": "#D9F6E6",
    "yellow": "#BC8400",
    "yellow_bg": "#FFF0BE",
    "red": "#E23849",
    "red_bg": "#FFE0E4",
    "purple": "#7040D6",
    "header": "#DFEBF4",
}

COLORS = dict(DARK_COLORS)
CURRENT_THEME = "Dark"

FONT = "Segoe UI"
FONT_DISPLAY = "Segoe UI"


def set_theme(mode):
    """Apply a complete palette, including widgets with explicit colors."""
    global CURRENT_THEME
    normalized = "Light" if str(mode).lower().startswith("light") else "Dark"
    CURRENT_THEME = normalized
    COLORS.clear()
    COLORS.update(LIGHT_COLORS if normalized == "Light" else DARK_COLORS)
    ctk.set_appearance_mode(normalized)
    return normalized


def get_theme():
    return CURRENT_THEME


def font(size=13, weight="normal", slant="roman"):
    return ctk.CTkFont(family=FONT, size=size, weight=weight, slant=slant)


def card(parent, **kwargs):
    defaults = dict(
        fg_color=COLORS["card"], corner_radius=12,
        border_width=1, border_color=COLORS["border"],
    )
    defaults.update(kwargs)
    return ctk.CTkFrame(parent, **defaults)


def flat_button(parent, text, command=None, active=False, **kwargs):
    defaults = dict(
        text=text, command=command, height=46, corner_radius=8,
        font=font(13, "bold" if active else "normal"), anchor="w",
        fg_color=COLORS["blue_dark"] if active else "transparent",
        hover_color=COLORS["card_alt"],
        text_color=COLORS["text"],
        border_width=1 if active else 0,
        border_color=COLORS["cyan"],
    )
    defaults.update(kwargs)
    return ctk.CTkButton(parent, **defaults)


class BrandLogo(ctk.CTkFrame):
    def __init__(self, parent, compact=False, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        size = 42 if compact else 58
        mark = ctk.CTkFrame(self, width=size, height=size, corner_radius=10,
                            fg_color=COLORS["cyan"])
        mark.pack(side="left", padx=(0, 14))
        mark.pack_propagate(False)
        inner = ctk.CTkFrame(mark, width=int(size * .47), height=int(size * .47),
                             corner_radius=4, fg_color="#071B2B")
        inner.place(relx=.5, rely=.5, anchor="center")

        text_box = ctk.CTkFrame(self, fg_color="transparent")
        text_box.pack(side="left")
        title = ctk.CTkFrame(text_box, fg_color="transparent")
        title.pack(anchor="w")
        ctk.CTkLabel(title, text="KARDEX", font=font(22 if compact else 31, "bold"),
                     text_color=COLORS["text"]).pack(side="left")
        ctk.CTkLabel(title, text=" PRO", font=font(22 if compact else 31, "bold"),
                     text_color=COLORS["cyan"]).pack(side="left")
        ctk.CTkLabel(text_box, text="Sistema de Inventario", font=font(11 if compact else 17),
                     text_color=COLORS["muted"]).pack(anchor="w")


class VectorIcon(tk.Canvas):
    """Small line icons drawn consistently, independent from installed emoji fonts."""

    def __init__(self, parent, kind, size=28, bg=None, fg=None, command=None, **kwargs):
        self.size = size
        self.kind = kind
        self.fg = fg or COLORS["muted"]
        self.command = command
        super().__init__(parent, width=size, height=size, bg=bg or COLORS["panel"],
                         highlightthickness=0, bd=0, cursor="hand2" if command else "arrow", **kwargs)
        self.bind("<Configure>", self._draw)
        if command:
            self.bind("<Button-1>", lambda _event: command())

    def _draw(self, _event=None):
        self.delete("all")
        s, c, w = self.size, self.fg, max(1, self.size // 14)
        if self.kind == "eye":
            self.create_arc(s*.14, s*.28, s*.86, s*.76, start=18, extent=144, style="arc", outline=c, width=w)
            self.create_arc(s*.14, s*.24, s*.86, s*.72, start=198, extent=144, style="arc", outline=c, width=w)
            self.create_oval(s*.42, s*.38, s*.58, s*.58, outline=c, width=w)
        elif self.kind == "user":
            self.create_oval(s*.36, s*.14, s*.64, s*.42, outline=c, width=w)
            self.create_arc(s*.20, s*.38, s*.80, s*.88, start=0, extent=180, style="arc", outline=c, width=w)
        elif self.kind == "lock":
            self.create_arc(s*.30, s*.12, s*.70, s*.55, start=0, extent=180, style="arc", outline=c, width=w)
            self.create_rectangle(s*.22, s*.38, s*.78, s*.82, outline=c, width=w)
            self.create_oval(s*.47, s*.55, s*.53, s*.61, fill=c, outline=c)
        elif self.kind == "calendar":
            self.create_rectangle(s*.18, s*.24, s*.82, s*.82, outline=c, width=w)
            self.create_line(s*.18, s*.39, s*.82, s*.39, fill=c, width=w)
            self.create_line(s*.34, s*.14, s*.34, s*.31, fill=c, width=w)
            self.create_line(s*.66, s*.14, s*.66, s*.31, fill=c, width=w)
        elif self.kind == "bell":
            self.create_arc(s*.23, s*.20, s*.77, s*.73, start=0, extent=180, style="arc", outline=c, width=w)
            self.create_line(s*.23, s*.46, s*.18, s*.72, s*.82, s*.72, s*.77, s*.46, fill=c, width=w, smooth=True)
            self.create_arc(s*.40, s*.65, s*.60, s*.88, start=180, extent=180, style="arc", outline=c, width=w)
        elif self.kind == "box":
            self.create_polygon(s*.18, s*.32, s*.50, s*.14, s*.82, s*.32, s*.50, s*.50,
                                fill="", outline=c, width=w)
            self.create_polygon(s*.18, s*.32, s*.50, s*.50, s*.50, s*.86, s*.18, s*.67,
                                fill="", outline=c, width=w)
            self.create_polygon(s*.50, s*.50, s*.82, s*.32, s*.82, s*.67, s*.50, s*.86,
                                fill="", outline=c, width=w)
        elif self.kind == "users":
            self.create_oval(s*.18, s*.18, s*.42, s*.42, outline=c, width=w)
            self.create_oval(s*.58, s*.18, s*.82, s*.42, outline=c, width=w)
            self.create_oval(s*.38, s*.10, s*.62, s*.36, outline=c, width=w)
            self.create_arc(s*.10, s*.37, s*.48, s*.80, start=0, extent=180, style="arc", outline=c, width=w)
            self.create_arc(s*.52, s*.37, s*.90, s*.80, start=0, extent=180, style="arc", outline=c, width=w)
            self.create_arc(s*.28, s*.30, s*.72, s*.82, start=0, extent=180, style="arc", outline=c, width=w)


class CubeArt(tk.Canvas):
    """Lightweight isometric decoration used by the supplied mockups."""

    def __init__(self, parent, bg=None, width=320, height=155, **kwargs):
        bg = bg or COLORS["panel"]
        super().__init__(parent, width=width, height=height, bg=bg,
                         highlightthickness=0, bd=0, **kwargs)
        self.bind("<Configure>", self._draw)

    def _cube(self, x, y, s, shade=0):
        top = "#174E91" if shade == 0 else "#123D70"
        left = "#0B2D53" if shade == 0 else "#092640"
        right = "#123F75" if shade == 0 else "#0D3158"
        self.create_polygon(x, y, x+s, y-s*.42, x+s*2, y,
                            x+s, y+s*.42, fill=top, outline="#2868AE", width=1)
        self.create_polygon(x, y, x+s, y+s*.42, x+s, y+s*1.55,
                            x, y+s*1.12, fill=left, outline="#174D83", width=1)
        self.create_polygon(x+s, y+s*.42, x+s*2, y, x+s*2, y+s*1.12,
                            x+s, y+s*1.55, fill=right, outline="#235C9B", width=1)

    def _draw(self, _event=None):
        self.delete("all")
        w, h = self.winfo_width(), self.winfo_height()
        self.create_polygon(0, h, w*.48, h*.08, w, h*.08, w, h,
                            fill=COLORS["app"], outline="")
        self._cube(w*.22, h*.46, min(w, h)*.20, 1)
        self._cube(w*.47, h*.19, min(w, h)*.27, 0)
        self._cube(w*.66, h*.53, min(w, h)*.22, 0)
        self._cube(w*.43, h*.70, min(w, h)*.15, 1)


class HeroBanner(ctk.CTkFrame):
    def __init__(self, parent, eyebrow, title, lines, quote, **kwargs):
        super().__init__(parent, height=150, fg_color=COLORS["panel"], corner_radius=12,
                         border_width=1, border_color=COLORS["border"], **kwargs)
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=6)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=2)
        self.grid_rowconfigure(0, weight=1)

        copy = ctk.CTkFrame(self, fg_color="transparent")
        copy.grid(row=0, column=0, sticky="nsew", padx=(22, 5), pady=18)
        ctk.CTkLabel(copy, text=eyebrow.upper(), font=font(10, "bold"),
                     text_color=COLORS["blue_dark"], anchor="w").pack(fill="x")
        ctk.CTkLabel(copy, text=title, font=font(31, "bold"),
                     text_color=COLORS["text"], anchor="w").pack(fill="x", pady=(5, 3))
        ctk.CTkLabel(copy, text=lines, font=font(13), justify="left",
                     text_color=COLORS["muted"], anchor="w").pack(fill="x")

        art_holder = ctk.CTkFrame(self, fg_color="transparent")
        art_holder.grid(row=0, column=1, sticky="nsew")
        art = CubeArt(art_holder, bg=COLORS["panel"], height=146)
        art.pack(fill="both", expand=True)

        quote_box = ctk.CTkFrame(self, fg_color="transparent")
        quote_box.grid(row=0, column=2, sticky="nsew", padx=(0, 18), pady=34)
        ctk.CTkLabel(quote_box, text=quote, font=font(12, slant="italic"),
                     text_color=COLORS["text"], justify="left", anchor="w").pack(anchor="w")
        ctk.CTkFrame(quote_box, height=3, width=50, fg_color=COLORS["cyan"],
                     corner_radius=2).pack(anchor="w", pady=(12, 0))


class SimpleDonut(tk.Canvas):
    def __init__(self, parent, values=(76, 17, 7), total=128, **kwargs):
        super().__init__(parent, bg=COLORS["card"], highlightthickness=0, **kwargs)
        self.values = values
        self.total = total
        self.bind("<Configure>", self._draw)

    def _draw(self, _event=None):
        self.delete("all")
        w, h = self.winfo_width(), self.winfo_height()
        s = min(w, h) - 28
        x0, y0 = (w-s)/2, (h-s)/2
        start = 90
        for value, color in zip(self.values, (COLORS["green"], COLORS["yellow"], COLORS["red"])):
            extent = -360 * value / sum(self.values)
            self.create_arc(x0, y0, x0+s, y0+s, start=start, extent=extent,
                            fill=color, outline=color)
            start += extent
        inner = s * .62
        ix, iy = (w-inner)/2, (h-inner)/2
        self.create_oval(ix, iy, ix+inner, iy+inner, fill=COLORS["card"], outline=COLORS["card"])
        self.create_text(w/2, h/2-8, text=str(self.total), fill=COLORS["text"],
                         font=(FONT, 22, "bold"))
        self.create_text(w/2, h/2+17, text="Productos", fill=COLORS["muted"],
                         font=(FONT, 10))


class BarChart(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLORS["card"], highlightthickness=0, **kwargs)
        self.bind("<Configure>", self._draw)

    def _draw(self, _event=None):
        self.delete("all")
        w, h = self.winfo_width(), self.winfo_height()
        left, right, top, bottom = 34, w-10, 12, h-34
        for i in range(5):
            y = bottom - (bottom-top)*i/4
            self.create_line(left, y, right, y, fill=COLORS["border_soft"])
            self.create_text(left-10, y, text=str(i*10), fill=COLORS["muted"], font=(FONT, 8))
        incoming = (18, 27, 19, 27, 25, 29, 28)
        outgoing = (12, 18, 28, 21, 15, 21, 20)
        labels = ("21 May", "22 May", "23 May", "24 May", "25 May", "26 May", "27 May")
        section = (right-left)/7
        for i, (a, b) in enumerate(zip(incoming, outgoing)):
            x = left + i*section + section*.24
            scale = (bottom-top)/40
            self.create_rectangle(x, bottom-a*scale, x+section*.23, bottom, fill=COLORS["blue"], outline="")
            self.create_rectangle(x+section*.28, bottom-b*scale, x+section*.51, bottom, fill=COLORS["green"], outline="")
            self.create_text(left+(i+.5)*section, bottom+14, text=labels[i], fill=COLORS["muted"], font=(FONT, 8))


def status_style(current, minimum):
    current = float(current or 0)
    minimum = float(minimum or 0)
    if current <= 0:
        return "Agotado", COLORS["red"], COLORS["red_bg"]
    if current <= minimum:
        return "Bajo", COLORS["yellow"], COLORS["yellow_bg"]
    return "Óptimo", COLORS["green"], COLORS["green_bg"]
