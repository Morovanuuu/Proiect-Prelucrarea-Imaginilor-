"""
Modul: ui_app.py
Descriere: Se gestioneaza exclusiv interfata grafica (GUI) folosind un Meniu Clasic (MenuBar).
Rutarea datelor catre modulele de procesare si interactiunea cu utilizatorul.
"""

import tkinter as tk
from tkinter import filedialog, simpledialog
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

        self.root.configure(bg=self.bg_workspace)
        self.original_matrix = None
        self.display_matrix = None
        self.current_filter = None
        self.target_label = None
        self.morph_iterations = 1  # Pastram numarul de repetari pentru salvare

        self.start_frame = tk.Frame(self.root, bg=self.bg_workspace)
        self.main_frame = tk.Frame(self.root, bg=self.bg_workspace)

        self.build_start_page()
        self.build_main_page()
        self.create_menu()

        self.start_frame.pack(expand=True, fill="both")

    def add_hover(self, btn, normal_bg, hover_bg, normal_fg, hover_fg):
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg, fg=hover_fg))
        btn.bind("<Leave>", lambda e: btn.config(bg=normal_bg, fg=normal_fg))

    def update_status(self, message, color="#F8F8F2"):
        self.status_bar.config(text=f"  {message}", fg=color)
        self.root.update()

    def build_start_page(self):
        tk.Frame(self.start_frame, bg=self.bg_workspace).pack(pady=170)
        tk.Label(self.start_frame, text="Photoshop V2", font=("Helvetica", 48, "bold"), bg=self.bg_workspace,
                 fg=self.text_color).pack(pady=(0, 40))
        btn_start = tk.Button(self.start_frame, text="Start", font=("Helvetica", 16, "bold"), bg=self.btn_bg,
                              fg=self.btn_text, relief="flat", width=15, pady=10, command=self.show_main_page)
        btn_start.pack()
        self.add_hover(btn_start, self.btn_bg, self.btn_hover, self.btn_text, self.btn_text)

    def build_main_page(self):
        self.status_bar = tk.Label(self.main_frame, text="  Asteptare imagine...", bg=self.bg_sidebar,
                                   fg=self.text_color, font=("Arial", 10), anchor="w", pady=5)
        self.status_bar.pack(side="bottom", fill="x")

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

    def create_menu(self):
        self.menubar = tk.Menu(self.root)

        menu_fisier = tk.Menu(self.menubar, tearoff=0)
        menu_fisier.add_command(label="Deschide Imagine...", command=self.open_image)
        menu_fisier.add_command(label="Salveaza Rezultatul", command=self.save_image)
        menu_fisier.add_separator()
        menu_fisier.add_command(label="Curata Spatiul", command=self.close_image)
        menu_fisier.add_command(label="Inapoi la Start", command=self.show_start_page)
        menu_fisier.add_separator()
        menu_fisier.add_command(label="Iesire", command=self.root.quit)
        self.menubar.add_cascade(label="Fisier", menu=menu_fisier)

        menu_culori = tk.Menu(self.menubar, tearoff=0)
        for f in ["Grayscale", "CMY", "YUV", "YCbCr", "HSV", "Invers RGB"]:
            menu_culori.add_command(label=f, command=lambda sel=f: self.apply_filter(sel))
        self.menubar.add_cascade(label="Conversii Culoare", menu=menu_culori)

        menu_analiza = tk.Menu(self.menubar, tearoff=0)
        for f in ["Binarizare", "Histograma", "Egalizare Histograma", "Momente Ordin 1", "Momente Ordin 2",
                  "Matrice Covarianta", "Proiectii"]:
            menu_analiza.add_command(label=f, command=lambda sel=f: self.apply_filter(sel))
        self.menubar.add_cascade(label="Analiza & Statistica", menu=menu_analiza)

        # Meniu Nou pentru Filtre Spatiale (Lab 7)
        menu_spatiale = tk.Menu(self.menubar, tearoff=0)
        for f in ["Mediere (Blur)", "Median (Zgomot)", "Minim (Intunecare)", "Maxim (Luminare)",
                  "Accentuare (Sharpen)"]:
            menu_spatiale.add_command(label=f, command=lambda sel=f: self.apply_filter(sel))
        self.menubar.add_cascade(label="Filtre Spatiale", menu=menu_spatiale)

        menu_morfologie = tk.Menu(self.menubar, tearoff=0)
        for f in ["Dilatare", "Eroziune", "Deschidere", "Inchidere"]:
            menu_morfologie.add_command(label=f, command=lambda sel=f: self.apply_filter(sel))
        self.menubar.add_cascade(label="Morfologie", menu=menu_morfologie)

        menu_avansat = tk.Menu(self.menubar, tearoff=0)
        for f in ["Sobel (Directie)", "Etichetare (BFS)", "Selecteaza Obiect (Dupa Eticheta)"]:
            menu_avansat.add_command(label=f, command=lambda sel=f: self.apply_filter(sel))
        self.menubar.add_cascade(label="Filtre Avansate", menu=menu_avansat)

    def resize_matrix(self, matrix, max_size=320):
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
        h, w = len(matrix), len(matrix[0])
        header = f"P6\n{w} {h}\n255\n".encode("ascii")
        data = bytearray()
        for row in matrix:
            for r, g, b in row: data.extend([int(r), int(g), int(b)])
        with open(filename, "wb") as f:
            f.write(header + data)
        return tk.PhotoImage(file=filename)

    def open_image(self):
        path = filedialog.askopenfilename(filetypes=[("BMP files", "*.bmp")])
        if path:
            self.original_matrix = read_bmp(path)
            h, w = len(self.original_matrix), len(self.original_matrix[0]) if len(self.original_matrix) > 0 else 0
            self.display_matrix = self.resize_matrix(self.original_matrix)
            self.tk_orig = self.matrix_to_tk(self.display_matrix, "t_orig.ppm")
            self.canvas_orig.config(image=self.tk_orig, text="Original", compound="top", fg=self.text_color,
                                    font=("Arial", 12, "bold"))
            self.update_status(f"Imagine incarcata: {w}x{h} pixeli. Alege un filtru din meniul de sus.", "#50FA7B")
            self.hide_all_canvases()
            self.current_filter = None

    def hide_all_canvases(self):
        for c in [self.canvas_g1, self.canvas_g2, self.canvas_g3, self.canvas_g4, self.canvas_cmy]:
            c.grid_forget()

    def apply_filter(self, filter_name):
        if not self.display_matrix:
            self.update_status("Eroare: Deschide o imagine mai intai din meniul Fisier!", "#FF5555")
            return

        self.current_filter = filter_name
        self.hide_all_canvases()
        m = self.display_matrix

        if filter_name == "Grayscale":
            r1, r2, r3 = filters.get_grayscale(m)
            self.tk_g1, self.tk_g2, self.tk_g3 = self.matrix_to_tk(r1, "t1.ppm"), self.matrix_to_tk(r2,
                                                                                                    "t2.ppm"), self.matrix_to_tk(
                r3, "t3.ppm")
            self._setup_canvas(self.canvas_g1, self.tk_g1, "Gray(1): Medie", 0, 0)
            self._setup_canvas(self.canvas_g2, self.tk_g2, "Gray(2): Luma", 0, 1)
            self._setup_canvas(self.canvas_g3, self.tk_g3, "Gray(3): Mid/Max", 1, 0, colspan=2)

        elif filter_name == "CMY":
            res = filters.get_cmy(m)
            self.tk_cmy = self.matrix_to_tk(res, "t_cmy.ppm")
            self._setup_canvas(self.canvas_cmy, self.tk_cmy, "Filtru CMY", 0, 0)

        elif filter_name == "YUV":
            y, u, v = filters.get_yuv(m)
            self.tk_g1, self.tk_g2, self.tk_g3 = self.matrix_to_tk(y, "t_y.ppm"), self.matrix_to_tk(u,
                                                                                                    "t_u.ppm"), self.matrix_to_tk(
                v, "t_v.ppm")
            self._setup_canvas(self.canvas_g1, self.tk_g1, "Canal Y", 0, 0, colspan=2)
            self._setup_canvas(self.canvas_g2, self.tk_g2, "Canal U", 1, 0)
            self._setup_canvas(self.canvas_g3, self.tk_g3, "Canal V", 1, 1)

        elif filter_name == "YCbCr":
            y, cb, cr = filters.get_ycbcr(m)
            self.tk_g1, self.tk_g2, self.tk_g3 = self.matrix_to_tk(y, "t_y.ppm"), self.matrix_to_tk(cb,
                                                                                                    "t_cb.ppm"), self.matrix_to_tk(
                cr, "t_cr.ppm")
            self._setup_canvas(self.canvas_g1, self.tk_g1, "Canal Y", 0, 0, colspan=2)
            self._setup_canvas(self.canvas_g2, self.tk_g2, "Canal Cb", 1, 0)
            self._setup_canvas(self.canvas_g3, self.tk_g3, "Canal Cr", 1, 1)

        elif filter_name == "HSV":
            h_mat, s_mat, v_mat = filters.get_hsv(m)
            self.tk_g1, self.tk_g2, self.tk_g3 = self.matrix_to_tk(h_mat, "t_h.ppm"), self.matrix_to_tk(s_mat,
                                                                                                        "t_s.ppm"), self.matrix_to_tk(
                v_mat, "t_v.ppm")
            self._setup_canvas(self.canvas_g1, self.tk_g1, "Canal H", 0, 0, colspan=2)
            self._setup_canvas(self.canvas_g2, self.tk_g2, "Canal S", 1, 0)
            self._setup_canvas(self.canvas_g3, self.tk_g3, "Canal V", 1, 1)

        elif filter_name == "Invers RGB":
            inv, r, g, b = filters.get_invers(m)
            self.tk_g1, self.tk_g2, self.tk_g3, self.tk_g4 = self.matrix_to_tk(inv, "t_inv.ppm"), self.matrix_to_tk(r,
                                                                                                                    "t_r.ppm"), self.matrix_to_tk(
                g, "t_g.ppm"), self.matrix_to_tk(b, "t_b.ppm")
            self._setup_canvas(self.canvas_g1, self.tk_g1, "Invers", 0, 0)
            self._setup_canvas(self.canvas_g2, self.tk_g2, "Rosu Invers", 0, 1)
            self._setup_canvas(self.canvas_g3, self.tk_g3, "Verde Invers", 1, 0)
            self._setup_canvas(self.canvas_g4, self.tk_g4, "Albastru Invers", 1, 1)

        elif filter_name == "Binarizare":
            res = filters.get_binarizare(m)
            self.tk_g1 = self.matrix_to_tk(res, "t_bin.ppm")
            self._setup_canvas(self.canvas_g1, self.tk_g1, "Binarizare", 0, 0)

        elif filter_name == "Histograma":
            res = filters.get_histogram(m)
            self.tk_g1 = self.matrix_to_tk(res, "t_hist.ppm")
            self._setup_canvas(self.canvas_g1, self.tk_g1, "Histograma", 0, 0)

        elif filter_name == "Egalizare Histograma":
            res = filters.get_egalizare_histograma(m)
            self.tk_g1 = self.matrix_to_tk(res, "t_eq.ppm")
            self._setup_canvas(self.canvas_g1, self.tk_g1, "Egalizare Histograma", 0, 0)

        # LAB 7: Filtre Spatiale
        elif filter_name == "Mediere (Blur)":
            res = filters.get_mediere(m)
            self.tk_g1 = self.matrix_to_tk(res, "t_med.ppm")
            self._setup_canvas(self.canvas_g1, self.tk_g1, "Filtru Mediere", 0, 0)

        elif filter_name == "Median (Zgomot)":
            res = filters.get_median(m)
            self.tk_g1 = self.matrix_to_tk(res, "t_median.ppm")
            self._setup_canvas(self.canvas_g1, self.tk_g1, "Filtru Median", 0, 0)

        elif filter_name == "Minim (Intunecare)":
            res = filters.get_minim(m)
            self.tk_g1 = self.matrix_to_tk(res, "t_min.ppm")
            self._setup_canvas(self.canvas_g1, self.tk_g1, "Filtru Minim", 0, 0)

        elif filter_name == "Maxim (Luminare)":
            res = filters.get_maxim(m)
            self.tk_g1 = self.matrix_to_tk(res, "t_max.ppm")
            self._setup_canvas(self.canvas_g1, self.tk_g1, "Filtru Maxim", 0, 0)

        elif filter_name == "Accentuare (Sharpen)":
            res = filters.get_accentuare(m)
            self.tk_g1 = self.matrix_to_tk(res, "t_sharp.ppm")
            self._setup_canvas(self.canvas_g1, self.tk_g1, "Accentuare (Sharpen)", 0, 0)

        elif filter_name in ["Dilatare", "Eroziune", "Deschidere", "Inchidere"]:
            iters = simpledialog.askinteger("Operatie Morfologica",
                                            f"De cate ori doriti sa aplicati iteratia de {filter_name}?\nRecomandat: 1, 2 sau 3",
                                            minvalue=1, maxvalue=20, initialvalue=1)
            if iters is None:
                self.update_status("Operatie morfologica anulata.", "#F8F8F2")
                return

            self.morph_iterations = iters
            if filter_name == "Dilatare":
                res = filters.get_dilatare(m, iters)
            elif filter_name == "Eroziune":
                res = filters.get_eroziune(m, iters)
            elif filter_name == "Deschidere":
                res = filters.get_deschidere(m, iters)
            elif filter_name == "Inchidere":
                res = filters.get_inchidere(m, iters)

            self.tk_g1 = self.matrix_to_tk(res, "t_morph.ppm")
            self._setup_canvas(self.canvas_g1, self.tk_g1, f"{filter_name} (x{iters})", 0, 0)

        elif filter_name == "Momente Ordin 1":
            res, xc, yc, m00, m10, m01 = filters.get_moments1(m)
            if res is None:
                self.update_status("Eroare: Imagine complet alba!", "#FF5555")
                return
            self.tk_g1 = self.matrix_to_tk(res, "t_m1.ppm")
            self._setup_canvas(self.canvas_g1, self.tk_g1, f"Centru: X={xc}, Y={yc}", 0, 0)

        elif filter_name == "Momente Ordin 2":
            m20, m02, m11 = filters.get_moments2(m)
            self.tk_g1 = self.matrix_to_tk(m, "t_m2.ppm")
            self._setup_canvas(self.canvas_g1, self.tk_g1, f"M20={m20}, M02={m02}\nM11={m11}", 0, 0)

        elif filter_name == "Matrice Covarianta":
            cxx, cyy, cxy = filters.get_covariance(m)
            if cxx is None:
                self.update_status("Eroare: Imagine complet alba!", "#FF5555")
                return
            self.tk_g1 = self.matrix_to_tk(m, "t_cov.ppm")
            self._setup_canvas(self.canvas_g1, self.tk_g1,
                               f"Covarianta:\n[{cxx:.2f}, {cxy:.2f}]\n[{cxy:.2f}, {cyy:.2f}]", 0, 0)

        elif filter_name == "Proiectii":
            h_proj, v_proj = filters.get_projections(m)
            self.tk_g1, self.tk_g2 = self.matrix_to_tk(h_proj, "t_ph.ppm"), self.matrix_to_tk(v_proj, "t_pv.ppm")
            self._setup_canvas(self.canvas_g1, self.tk_g1, "Orizontala", 0, 0)
            self._setup_canvas(self.canvas_g2, self.tk_g2, "Verticala", 0, 1)

        elif filter_name == "Sobel (Directie)":
            res_sobel, angle, max_mag = filters.get_sobel(m)
            self.tk_g1 = self.matrix_to_tk(res_sobel, "t_sobel.ppm")
            info_text = f"Filtru Sobel (Muchii)\nUnghi Alungire: {angle:.2f} grade"
            self._setup_canvas(self.canvas_g1, self.tk_g1, info_text, 0, 0)

        elif filter_name == "Etichetare (BFS)":
            res_labels, obj_count = filters.get_connected_components(m)
            self.tk_g1 = self.matrix_to_tk(res_labels, "t_labels.ppm")
            info_text = f"Obiecte gasite: {obj_count}\n(Colorate distinct)"
            self._setup_canvas(self.canvas_g1, self.tk_g1, info_text, 0, 0)

        elif filter_name == "Selecteaza Obiect (Dupa Eticheta)":
            _, obj_count = filters.get_connected_components(m)
            if obj_count == 0:
                self.update_status("Eroare: Imaginea nu contine niciun obiect (este complet alba)!", "#FF5555")
                return
            target = simpledialog.askinteger("Selectie Obiect", f"Introdu numarul obiectului cautat (1 - {obj_count}):",
                                             minvalue=1, maxvalue=obj_count)
            if target is not None:
                self.target_label = target
                res_iso = filters.get_isolated_object(m, target)
                self.tk_g1 = self.matrix_to_tk(res_iso, "t_iso.ppm")
                self._setup_canvas(self.canvas_g1, self.tk_g1, f"Obiect Izolat: #{target}", 0, 0)
            else:
                self.update_status("Selectia obiectului a fost anulata.", "#F8F8F2")
                return

        self.update_status(f"Vizualizare '{filter_name}' generata cu succes!", "#50FA7B")

    def _setup_canvas(self, canvas, img, text, row, col, colspan=1):
        canvas.config(image=img, text=text, compound="top", fg=self.text_color, font=("Arial", 10, "bold"))
        canvas.grid(row=row, column=col, columnspan=colspan, padx=15, pady=15)

    def save_image(self):
        if not self.original_matrix:
            self.update_status("Eroare: Deschide o imagine inainte!", "#FF5555")
            return

        if not self.current_filter:
            self.update_status("Eroare: Aplica un filtru inainte de a salva!", "#FF5555")
            return

        sel = self.current_filter
        no_save = ["Histograma", "Momente Ordin 1", "Momente Ordin 2", "Matrice Covarianta", "Proiectii"]
        if sel in no_save:
            self.update_status("Aceste vizualizari sunt doar preview si nu pot fi salvate ca imagine BMP!", "#FF5555")
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
            elif sel == "Binarizare":
                write_bmp(filters.get_binarizare(m), base_path)
            elif sel == "Egalizare Histograma":
                write_bmp(filters.get_egalizare_histograma(m), base_path)

            # LAB 7 Salvari
            elif sel == "Mediere (Blur)":
                write_bmp(filters.get_mediere(m), base_path)
            elif sel == "Median (Zgomot)":
                write_bmp(filters.get_median(m), base_path)
            elif sel == "Minim (Intunecare)":
                write_bmp(filters.get_minim(m), base_path)
            elif sel == "Maxim (Luminare)":
                write_bmp(filters.get_maxim(m), base_path)
            elif sel == "Accentuare (Sharpen)":
                write_bmp(filters.get_accentuare(m), base_path)

            elif sel == "Dilatare":
                write_bmp(filters.get_dilatare(m, self.morph_iterations), base_path)
            elif sel == "Eroziune":
                write_bmp(filters.get_eroziune(m, self.morph_iterations), base_path)
            elif sel == "Deschidere":
                write_bmp(filters.get_deschidere(m, self.morph_iterations), base_path)
            elif sel == "Inchidere":
                write_bmp(filters.get_inchidere(m, self.morph_iterations), base_path)

            elif sel == "Sobel (Directie)":
                res_sobel, _, _ = filters.get_sobel(m)
                write_bmp(res_sobel, base_path.replace(".bmp", "_sobel.bmp"))
            elif sel == "Etichetare (BFS)":
                res_labels, _ = filters.get_connected_components(m)
                write_bmp(res_labels, base_path.replace(".bmp", "_etichetat.bmp"))
            elif sel == "Selecteaza Obiect (Dupa Eticheta)":
                if hasattr(self, 'target_label') and self.target_label:
                    res_iso = filters.get_isolated_object(m, self.target_label)
                    write_bmp(res_iso, base_path.replace(".bmp", f"_obiect_{self.target_label}.bmp"))
            else:
                self.update_status(f"Acest filtru nu este inca configurat pentru salvare.", "#FF5555")
                return

            self.update_status(f"Imaginea a fost salvata cu succes!", "#50FA7B")
        except Exception as e:
            self.update_status(f"Eroare la salvare: {e}", "#FF5555")

    def show_main_page(self):
        self.start_frame.pack_forget()
        self.main_frame.pack(expand=True, fill="both")
        self.root.config(menu=self.menubar)

    def show_start_page(self):
        self.close_image()
        self.main_frame.pack_forget()
        self.start_frame.pack(expand=True, fill="both")
        self.root.config(menu="")

    def close_image(self):
        self.hide_all_canvases()
        for c in [self.canvas_orig, self.canvas_g1, self.canvas_g2, self.canvas_g3, self.canvas_g4, self.canvas_cmy]:
            c.config(image="", text="")
        self.original_matrix = self.display_matrix = None
        self.current_filter = None
        self.target_label = None
        self.update_status("Spatiul de lucru a fost curatat.", self.text_color)