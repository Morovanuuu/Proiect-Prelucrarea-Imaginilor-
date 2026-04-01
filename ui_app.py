"""
Modul: ui_app.py
Descriere: Se gestioneaza exclusiv interfata grafica (GUI) si indruma datele catre modulele de procesare
"""

import tkinter as tk
from tkinter import filedialog
from bmp_io import read_bmp, write_bmp
import image_filters as filters


class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Photoshop V2")
        self.root.geometry("1300x900")

        self.bg_workspace = "#1E1E2E"
        self.bg_sidebar = "#282A36"
        self.text_color = "#F8F8F2"
        self.btn_bg, self.btn_hover, self.btn_text = "#FFFFFF", "#E2E8F0", "#1E1E2E"
        self.save_bg, self.save_hover, self.save_text = "#2E7D32", "#388E3C", "#FFFFFF"
        self.clear_bg, self.clear_hover, self.clear_text = "#DC3545", "#C82333", "#FFFFFF"

        self.root.configure(bg=self.bg_workspace)
        self.original_matrix = None
        self.display_matrix = None

        self.start_frame = tk.Frame(self.root, bg=self.bg_workspace)
        self.main_frame = tk.Frame(self.root, bg=self.bg_workspace)

        self.build_start_page()
        self.build_main_page()
        self.start_frame.pack(expand=True, fill="both")

    def add_hover(self, btn, normal_bg, hover_bg, normal_fg, hover_fg):
        """Adauga efecte vizuale de hover pentru butoanele Tkinter."""
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg, fg=hover_fg))
        btn.bind("<Leave>", lambda e: btn.config(bg=normal_bg, fg=normal_fg))

    def update_status(self, message, color="#F8F8F2"):
        """aici facem update la status, actualizeaza bara de status din stanga jos"""
        self.status_bar.config(text=f"  {message}", fg=color)
        self.root.update()

    def build_start_page(self):
        """Se construieste ecranul de start"""
        tk.Frame(self.start_frame, bg=self.bg_workspace).pack(pady=170)
        tk.Label(self.start_frame, text="Photoshop V2", font=("Helvetica", 48, "bold"), bg=self.bg_workspace,
                 fg=self.text_color).pack(pady=(0, 40))
        btn_start = tk.Button(self.start_frame, text="Start", font=("Helvetica", 16, "bold"), bg=self.btn_bg,
                              fg=self.btn_text, relief="flat", width=15, pady=10, command=self.show_main_page)
        btn_start.pack()
        self.add_hover(btn_start, self.btn_bg, self.btn_hover, self.btn_text, self.btn_text)

    def build_main_page(self):
        """Se onstruieste spatiul de lucru: top nav, status bar si containerele de imagini."""
        self.status_bar = tk.Label(self.main_frame, text="  Asteptare imagine...", bg=self.bg_sidebar,
                                   fg=self.text_color, font=("Arial", 10), anchor="w", pady=5)
        self.status_bar.pack(side="bottom", fill="x")

        self.top_nav = tk.Frame(self.main_frame, bg=self.bg_sidebar, bd=0)
        self.top_nav.pack(side="top", fill="x")

        btn_inapoi = tk.Button(self.top_nav, text="Start", bg=self.btn_bg, fg=self.btn_text, relief="flat",
                               font=("Arial", 11, "bold"), command=self.show_start_page, padx=10)
        btn_inapoi.pack(side="left", padx=10, pady=10)
        self.add_hover(btn_inapoi, self.btn_bg, self.btn_hover, self.btn_text, self.btn_text)

        tk.Frame(self.top_nav, width=1, bg="#44475A").pack(side="left", fill="y", pady=10, padx=5)

        btn_deschide = tk.Button(self.top_nav, text="Deschide", bg=self.btn_bg, fg=self.btn_text,
                                 font=("Arial", 11, "bold"), relief="flat", command=self.open_image, padx=10)
        btn_deschide.pack(side="left", padx=10, pady=10)
        self.add_hover(btn_deschide, self.btn_bg, self.btn_hover, self.btn_text, self.btn_text)

        tk.Frame(self.top_nav, width=1, bg="#44475A").pack(side="left", fill="y", pady=10, padx=5)

        tk.Label(self.top_nav, text="Filtru:", bg=self.bg_sidebar, fg=self.text_color, font=("Arial", 11, "bold")).pack(
            side="left", padx=(10, 5))

        self.filter_var = tk.StringVar(value="Grayscale")
        optiuni = ["Grayscale", "CMY", "YUV", "YCbCr", "HSV", "Invers RGB", "Binarizare", "Histograma",
                   "Momente Ordin 1", "Momente Ordin 2", "Matrice Covarianta", "Proiectii"]
        filter_menu = tk.OptionMenu(self.top_nav, self.filter_var, *optiuni)
        filter_menu.config(bg=self.btn_bg, fg=self.btn_text, activebackground=self.btn_hover,
                           activeforeground=self.btn_text, relief="flat", highlightthickness=0,
                           font=("Arial", 11, "bold"))
        filter_menu["menu"].config(bg=self.btn_bg, fg=self.btn_text, font=("Arial", 11))
        filter_menu.pack(side="left", padx=5, pady=10)

        btn_aplica = tk.Button(self.top_nav, text="Aplica", bg=self.btn_bg, fg=self.btn_text,
                               font=("Arial", 11, "bold"), relief="flat", command=self.apply_filter, padx=10)
        btn_aplica.pack(side="left", padx=10, pady=10)
        self.add_hover(btn_aplica, self.btn_bg, self.btn_hover, self.btn_text, self.btn_text)

        tk.Frame(self.top_nav, width=1, bg="#44475A").pack(side="left", fill="y", pady=10, padx=5)

        btn_salveaza = tk.Button(self.top_nav, text="Salveaza", bg=self.save_bg, fg=self.save_text,
                                 font=("Arial", 11, "bold"), relief="flat", command=self.save_image, padx=10)
        btn_salveaza.pack(side="left", padx=10, pady=10)
        self.add_hover(btn_salveaza, self.save_bg, self.save_hover, self.save_text, self.save_text)

        tk.Frame(self.top_nav, width=1, bg="#44475A").pack(side="left", fill="y", pady=10, padx=5)

        btn_inchide = tk.Button(self.top_nav, text="Curata Spatiul", bg=self.clear_bg, fg=self.clear_text,
                                font=("Arial", 11, "bold"), relief="flat", command=self.close_image, padx=10)
        btn_inchide.pack(side="left", padx=10, pady=10)
        self.add_hover(btn_inchide, self.clear_bg, self.clear_hover, self.clear_text, self.clear_text)

        self.content_frame = tk.Frame(self.main_frame, bg=self.bg_workspace)
        self.content_frame.pack(expand=True, fill="both", padx=20, pady=20)
        self.left_panel = tk.Frame(self.content_frame, bg=self.bg_workspace)
        self.left_panel.pack(side="left", expand=True, fill="both")
        self.right_panel = tk.Frame(self.content_frame, bg=self.bg_workspace)
        self.right_panel.pack(side="right", expand=True, fill="both")

        self.canvas_orig = tk.Label(self.left_panel, bg=self.bg_workspace)
        self.canvas_orig.pack(expand=True)
        self.canvas_g1 = tk.Label(self.right_panel, bg=self.bg_workspace)
        self.canvas_g2 = tk.Label(self.right_panel, bg=self.bg_workspace)
        self.canvas_g3 = tk.Label(self.right_panel, bg=self.bg_workspace)
        self.canvas_g4 = tk.Label(self.right_panel, bg=self.bg_workspace)
        self.canvas_cmy = tk.Label(self.right_panel, bg=self.bg_workspace)

    def resize_matrix(self, matrix, max_size=320):
        """Redimensioneaza o matrice pentru a fi afisata optim pe ecran, fara a suprasolicita Tkinter."""
        h, w = len(matrix), len(matrix[0])
        if w <= max_size and h <= max_size: return matrix
        scale = max(w / max_size, h / max_size)
        new_w, new_h = int(w / scale), int(h / scale)
        new_matrix = []
        for i in range(new_h):
            row = []
            for j in range(new_w): row.append(matrix[int(i * scale)][int(j * scale)])
            new_matrix.append(row)
        return new_matrix

    def matrix_to_tk(self, matrix, filename):
        """Converteste o matrice in format PPM (P6) pentru compatibilitate cu PhotoImage din Tkinter."""
        h, w = len(matrix), len(matrix[0])
        header = f"P6\n{w} {h}\n255\n".encode("ascii")
        data = bytearray()
        for row in matrix:
            for r, g, b in row: data.extend([int(r), int(g), int(b)])
        with open(filename, "wb") as f:
            f.write(header + data)
        return tk.PhotoImage(file=filename)

    def open_image(self):
        """Logica de deschidere a imaginii folosind File Dialog."""
        path = filedialog.askopenfilename(filetypes=[("BMP files", "*.bmp")])
        if path:
            self.original_matrix = read_bmp(path)
            h, w = len(self.original_matrix), len(self.original_matrix[0]) if len(self.original_matrix) > 0 else 0
            self.display_matrix = self.resize_matrix(self.original_matrix)
            self.tk_orig = self.matrix_to_tk(self.display_matrix, "t_orig.ppm")
            self.canvas_orig.config(image=self.tk_orig, text="Original", compound="top", fg=self.text_color,
                                    font=("Arial", 12, "bold"))
            self.update_status(f"Imagine incarcata cu succes: {w}x{h} pixeli", "#50FA7B")
            self.hide_all_canvases()

    def hide_all_canvases(self):
        for c in [self.canvas_g1, self.canvas_g2, self.canvas_g3, self.canvas_g4, self.canvas_cmy]:
            c.grid_forget()

    def apply_filter(self):
        """Metoda de rutare (Switch) catre functia corecta de procesare, in functie de dropdown."""
        if not self.display_matrix:
            self.update_status("Eroare: Deschide o imagine mai intai!", "#FF5555")
            return

        sel = self.filter_var.get()
        self.hide_all_canvases()
        m = self.display_matrix

        if sel == "Grayscale":
            r1, r2, r3 = filters.get_grayscale(m)
            self.tk_g1, self.tk_g2, self.tk_g3 = self.matrix_to_tk(r1, "t1.ppm"), self.matrix_to_tk(r2,
                                                                                                    "t2.ppm"), self.matrix_to_tk(
                r3, "t3.ppm")
            self._setup_canvas(self.canvas_g1, self.tk_g1, "Gray(1): Medie", 0, 0)
            self._setup_canvas(self.canvas_g2, self.tk_g2, "Gray(2): Luma", 0, 1)
            self._setup_canvas(self.canvas_g3, self.tk_g3, "Gray(3): Mid/Max", 1, 0, colspan=2)

        elif sel == "CMY":
            res = filters.get_cmy(m)
            self.tk_cmy = self.matrix_to_tk(res, "t_cmy.ppm")
            self._setup_canvas(self.canvas_cmy, self.tk_cmy, "Filtru CMY", 0, 0)

        elif sel == "YUV":
            y, u, v = filters.get_yuv(m)
            self.tk_g1, self.tk_g2, self.tk_g3 = self.matrix_to_tk(y, "t_y.ppm"), self.matrix_to_tk(u,
                                                                                                    "t_u.ppm"), self.matrix_to_tk(
                v, "t_v.ppm")
            self._setup_canvas(self.canvas_g1, self.tk_g1, "Canal Y", 0, 0, colspan=2)
            self._setup_canvas(self.canvas_g2, self.tk_g2, "Canal U", 1, 0)
            self._setup_canvas(self.canvas_g3, self.tk_g3, "Canal V", 1, 1)

        elif sel == "YCbCr":
            y, cb, cr = filters.get_ycbcr(m)
            self.tk_g1, self.tk_g2, self.tk_g3 = self.matrix_to_tk(y, "t_y.ppm"), self.matrix_to_tk(cb,
                                                                                                    "t_cb.ppm"), self.matrix_to_tk(
                cr, "t_cr.ppm")
            self._setup_canvas(self.canvas_g1, self.tk_g1, "Canal Y", 0, 0, colspan=2)
            self._setup_canvas(self.canvas_g2, self.tk_g2, "Canal Cb", 1, 0)
            self._setup_canvas(self.canvas_g3, self.tk_g3, "Canal Cr", 1, 1)

        elif sel == "HSV":
            h_mat, s_mat, v_mat = filters.get_hsv(m)
            self.tk_g1, self.tk_g2, self.tk_g3 = self.matrix_to_tk(h_mat, "t_h.ppm"), self.matrix_to_tk(s_mat,
                                                                                                        "t_s.ppm"), self.matrix_to_tk(
                v_mat, "t_v.ppm")
            self._setup_canvas(self.canvas_g1, self.tk_g1, "Canal H", 0, 0, colspan=2)
            self._setup_canvas(self.canvas_g2, self.tk_g2, "Canal S", 1, 0)
            self._setup_canvas(self.canvas_g3, self.tk_g3, "Canal V", 1, 1)

        elif sel == "Invers RGB":
            inv, r, g, b = filters.get_invers(m)
            self.tk_g1, self.tk_g2, self.tk_g3, self.tk_g4 = self.matrix_to_tk(inv, "t_inv.ppm"), self.matrix_to_tk(r,
                                                                                                                    "t_r.ppm"), self.matrix_to_tk(
                g, "t_g.ppm"), self.matrix_to_tk(b, "t_b.ppm")
            self._setup_canvas(self.canvas_g1, self.tk_g1, "Invers", 0, 0)
            self._setup_canvas(self.canvas_g2, self.tk_g2, "Rosu Invers", 0, 1)
            self._setup_canvas(self.canvas_g3, self.tk_g3, "Verde Invers", 1, 0)
            self._setup_canvas(self.canvas_g4, self.tk_g4, "Albastru Invers", 1, 1)

        elif sel == "Binarizare":
            res = filters.get_binarizare(m)
            self.tk_g1 = self.matrix_to_tk(res, "t_bin.ppm")
            self._setup_canvas(self.canvas_g1, self.tk_g1, "Binarizare", 0, 0)

        elif sel == "Histograma":
            res = filters.get_histogram(m)
            self.tk_g1 = self.matrix_to_tk(res, "t_hist.ppm")
            self._setup_canvas(self.canvas_g1, self.tk_g1, "Histograma", 0, 0)

        elif sel == "Momente Ordin 1":
            res, xc, yc, m00, m10, m01 = filters.get_moments1(m)
            if res is None:
                self.update_status("Eroare: Imagine complet alba!", "#FF5555")
                return
            self.tk_g1 = self.matrix_to_tk(res, "t_m1.ppm")
            self._setup_canvas(self.canvas_g1, self.tk_g1, f"Centru: X={xc}, Y={yc}", 0, 0)

        elif sel == "Momente Ordin 2":
            m20, m02, m11 = filters.get_moments2(m)
            self.tk_g1 = self.matrix_to_tk(m, "t_m2.ppm")
            self._setup_canvas(self.canvas_g1, self.tk_g1, f"M20={m20}, M02={m02}\nM11={m11}", 0, 0)

        elif sel == "Matrice Covarianta":
            cxx, cyy, cxy = filters.get_covariance(m)
            if cxx is None:
                self.update_status("Eroare: Imagine complet alba!", "#FF5555")
                return
            self.tk_g1 = self.matrix_to_tk(m, "t_cov.ppm")
            self._setup_canvas(self.canvas_g1, self.tk_g1,
                               f"Covarianta:\n[{cxx:.2f}, {cxy:.2f}]\n[{cxy:.2f}, {cyy:.2f}]", 0, 0)

        elif sel == "Proiectii":
            h_proj, v_proj = filters.get_projections(m)
            self.tk_g1, self.tk_g2 = self.matrix_to_tk(h_proj, "t_ph.ppm"), self.matrix_to_tk(v_proj, "t_pv.ppm")
            self._setup_canvas(self.canvas_g1, self.tk_g1, "Orizontala", 0, 0)
            self._setup_canvas(self.canvas_g2, self.tk_g2, "Verticala", 0, 1)

        self.update_status(f"Vizualizare '{sel}' generata cu succes!", "#50FA7B")

    def _setup_canvas(self, canvas, img, text, row, col, colspan=1):
        canvas.config(image=img, text=text, compound="top", fg=self.text_color, font=("Arial", 10, "bold"))
        canvas.grid(row=row, column=col, columnspan=colspan, padx=15, pady=15)

    def save_image(self):
        """Proceseaza salvarea imaginii procesate inapoi in format BMP, in functie de filtru."""
        if not self.original_matrix:
            self.update_status("Eroare: Deschide o imagine inainte!", "#FF5555")
            return

        sel = self.filter_var.get()
        no_save = ["Histograma", "Momente Ordin 1", "Momente Ordin 2", "Matrice Covarianta", "Proiectii"]
        if sel in no_save:
            self.update_status("Aceste vizualizari sunt doar preview!", "#FF5555")
            return

        base_path = filedialog.asksaveasfilename(defaultextension=".bmp", filetypes=[("BMP files", "*.bmp")])
        if not base_path: return

        self.update_status("Se proceseaza salvarea... Asteapta.", "#F8F8F2")
        m = self.original_matrix

        try:
            if sel == "Grayscale":
                r1, r2, r3 = filters.get_grayscale(m)
                write_bmp(r1, base_path.replace(".bmp", "_g1.bmp"))
                write_bmp(r2, base_path.replace(".bmp", "_g2.bmp"))
                write_bmp(r3, base_path.replace(".bmp", "_g3.bmp"))
            elif sel == "CMY":
                write_bmp(filters.get_cmy(m), base_path)
            elif sel == "YUV":
                y, u, v = filters.get_yuv(m)
                write_bmp(y, base_path.replace(".bmp", "_Y.bmp"))
                write_bmp(u, base_path.replace(".bmp", "_U.bmp"))
                write_bmp(v, base_path.replace(".bmp", "_V.bmp"))
            elif sel == "YCbCr":
                y, cb, cr = filters.get_ycbcr(m)
                write_bmp(y, base_path.replace(".bmp", "_Y.bmp"))
                write_bmp(cb, base_path.replace(".bmp", "_Cb.bmp"))
                write_bmp(cr, base_path.replace(".bmp", "_Cr.bmp"))
            elif sel == "HSV":
                h_m, s_m, v_m = filters.get_hsv(m)
                write_bmp(h_m, base_path.replace(".bmp", "_H.bmp"))
                write_bmp(s_m, base_path.replace(".bmp", "_S.bmp"))
                write_bmp(v_m, base_path.replace(".bmp", "_V.bmp"))
            elif sel == "Invers RGB":
                inv, r, g, b = filters.get_invers(m)
                write_bmp(inv, base_path.replace(".bmp", "_inv.bmp"))
                write_bmp(r, base_path.replace(".bmp", "_r.bmp"))
                write_bmp(g, base_path.replace(".bmp", "_g.bmp"))
                write_bmp(b, base_path.replace(".bmp", "_b.bmp"))
            elif sel == "Binarizare":
                write_bmp(filters.get_binarizare(m), base_path)

            self.update_status("Imagine salvata cu succes!", "#50FA7B")
        except Exception as e:
            self.update_status(f"Eroare la salvare: {e}", "#FF5555")

    def show_main_page(self):
        self.start_frame.pack_forget()
        self.main_frame.pack(expand=True, fill="both")

    def show_start_page(self):
        self.close_image()
        self.main_frame.pack_forget()
        self.start_frame.pack(expand=True, fill="both")

    def close_image(self):
        self.hide_all_canvases()
        for c in [self.canvas_orig, self.canvas_g1, self.canvas_g2, self.canvas_g3, self.canvas_g4, self.canvas_cmy]:
            c.config(image="", text="")
        self.original_matrix = self.display_matrix = None
        self.update_status("Spatiul de lucru a fost curatat.", self.text_color)