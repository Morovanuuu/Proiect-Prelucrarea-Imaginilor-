"""
Modul: image_filters.py
Descriere: Contine logica matematica independenta pentru toate filtrele de procesare a imaginii.
Acest modul nu are dependente de interfata grafica (fara OpenCV/Pillow), facilitand testarea si reutilizarea.
"""

import math
import random
from collections import deque


def clamp(val):
    """
    Asigura ca valoarea unui pixel ramane strict in intervalul valid [0, 255].
    Preia o valoare calculata (care poate iesi din limite) si o trunchiaza.
    """
    return max(0, min(255, int(val)))


def get_grayscale(m):
    """Conversie RGB in tonuri de gri (Medie, Luma, Mid/Max)."""
    h, w = len(m), len(m[0])
    res1, res2, res3 = [], [], []
    for y in range(h):
        r1, r2, r3 = [], [], []
        for x in range(w):
            r, g, b = m[y][x]
            v1 = (r + g + b) // 3
            v2 = int(0.299 * r + 0.587 * g + 0.114 * b)
            v3 = (min(r, g, b) + max(r, g, b)) // 2
            r1.append([v1, v1, v1])
            r2.append([v2, v2, v2])
            r3.append([v3, v3, v3])
        res1.append(r1);
        res2.append(r2);
        res3.append(r3)
    return res1, res2, res3


def get_cmy(m):
    """Transforma spatiul aditiv RGB in spatiul substractiv CMY."""
    h, w = len(m), len(m[0])
    res_cmy = []
    for y in range(h):
        row = []
        for x in range(w):
            r, g, b = m[y][x]
            row.append([255 - r, 255 - g, 255 - b])
        res_cmy.append(row)
    return res_cmy


def get_yuv(m):
    """Conversie RGB -> YUV (luminozitate si crominanta)."""
    h, w = len(m), len(m[0])
    res_y, res_u, res_v = [], [], []
    for y in range(h):
        r_y, r_u, r_v = [], [], []
        for x in range(w):
            r, g, b = m[y][x]
            Y = 0.3 * r + 0.6 * g + 0.1 * b
            U = 0.74 * (r - Y) + 0.27 * (b - Y)
            V = 0.48 * (r - Y) + 0.41 * (b - Y)
            val_y, val_u, val_v = clamp(Y), clamp(U + 128), clamp(V + 128)
            r_y.append([val_y, val_y, val_y])
            r_u.append([val_u, val_u, val_u])
            r_v.append([val_v, val_v, val_v])
        res_y.append(r_y);
        res_u.append(r_u);
        res_v.append(r_v)
    return res_y, res_u, res_v


def get_ycbcr(m):
    """Conversie RGB -> YCbCr (folosita in compresia JPEG)."""
    h, w = len(m), len(m[0])
    res_y, res_cb, res_cr = [], [], []
    for y in range(h):
        r_y, r_cb, r_cr = [], [], []
        for x in range(w):
            r, g, b = m[y][x]
            Y = 0.299 * r + 0.587 * g + 0.114 * b
            Cb = -0.1687 * r - 0.3313 * g + 0.498 * b + 128
            Cr = 0.498 * r - 0.4187 * g - 0.0813 * b + 128
            val_y, val_cb, val_cr = clamp(Y), clamp(Cb), clamp(Cr)
            r_y.append([val_y, val_y, val_y])
            r_cb.append([val_cb, val_cb, val_cb])
            r_cr.append([val_cr, val_cr, val_cr])
        res_y.append(r_y);
        res_cb.append(r_cb);
        res_cr.append(r_cr)
    return res_y, res_cb, res_cr


def get_hsv(m):
    """Conversie RGB -> HSV (Hue, Saturation, Value)."""
    h, w = len(m), len(m[0])
    res_h, res_s, res_v = [], [], []
    for y in range(h):
        r_h, r_s, r_v = [], [], []
        for x in range(w):
            R, G, B = m[y][x]
            r_norm, g_norm, b_norm = R / 255.0, G / 255.0, B / 255.0
            cmax = max(r_norm, g_norm, b_norm)
            cmin = min(r_norm, g_norm, b_norm)
            diff = cmax - cmin
            V = cmax
            S = diff / cmax if cmax != 0 else 0
            if diff == 0:
                H = 0
            elif cmax == r_norm:
                H = (60 * ((g_norm - b_norm) / diff) + 360) % 360
            elif cmax == g_norm:
                H = (60 * ((b_norm - r_norm) / diff) + 120) % 360
            elif cmax == b_norm:
                H = (60 * ((r_norm - g_norm) / diff) + 240) % 360
            H_val, S_val, V_val = int(H * 255 / 360), int(S * 255), int(V * 255)
            r_h.append([H_val, H_val, H_val])
            r_s.append([S_val, S_val, S_val])
            r_v.append([V_val, V_val, V_val])
        res_h.append(r_h);
        res_s.append(r_s);
        res_v.append(r_v)
    return res_h, res_s, res_v


def get_invers(m):
    """Aplica filtrul de imagine negativa (inversare culori)."""
    h, w = len(m), len(m[0])
    res_inv, res_r, res_g, res_b = [], [], [], []
    for y in range(h):
        row_inv, row_r, row_g, row_b = [], [], [], []
        for x in range(w):
            r, g, b = m[y][x]
            r_inv, g_inv, b_inv = 255 - r, 255 - g, 255 - b
            row_inv.append([r_inv, g_inv, b_inv])
            row_r.append([r_inv, 0, 0])
            row_g.append([0, g_inv, 0])
            row_b.append([0, 0, b_inv])
        res_inv.append(row_inv);
        res_r.append(row_r);
        res_g.append(row_g);
        res_b.append(row_b)
    return res_inv, res_r, res_g, res_b


def get_binarizare(m, prag=127):
    """Binarizarea imaginii (Thresholding). Alb pur sau negru pur."""
    h, w = len(m), len(m[0])
    res_bin = []
    for y in range(h):
        row = []
        for x in range(w):
            r, g, b = m[y][x]
            val = 255 if ((r + g + b) // 3) > prag else 0
            row.append([val, val, val])
        res_bin.append(row)
    return res_bin


def get_histogram(m):
    """Calculeaza histograma imaginii (0-255)."""
    h, w = len(m), len(m[0])
    hist = [0] * 256
    for y in range(h):
        for x in range(w):
            r, g, b = m[y][x]
            hist[(r + g + b) // 3] += 1
    max_val = max(hist) if max(hist) > 0 else 1
    res_hist = [[[40, 42, 54] for _ in range(256)] for _ in range(256)]
    for x in range(256):
        bar_height = int((hist[x] / max_val) * 250)
        for y in range(256 - bar_height, 256):
            res_hist[y][x] = [189, 147, 249]
    return res_hist


def get_moments1(m):
    """Calculeaza momentele de ordin 1 (M00, M10, M01) si centrul de masa."""
    h, w = len(m), len(m[0])
    M00, M10, M01 = 0, 0, 0
    for y in range(h):
        for x in range(w):
            r, g, b = m[y][x]
            I = 255 - ((r + g + b) // 3)
            M00 += I;
            M10 += x * I;
            M01 += y * I

    if M00 == 0: return None, 0, 0, 0, 0, 0

    xc, yc = int(M10 / M00), int(M01 / M00)
    res_moments = []
    for y in range(h):
        row = []
        for x in range(w): row.append(list(m[y][x]))
        res_moments.append(row)

    for i in range(-15, 16):
        if 0 <= xc + i < w: res_moments[yc][xc + i] = [255, 85, 85]
        if 0 <= yc + i < h: res_moments[yc + i][xc] = [255, 85, 85]
    return res_moments, xc, yc, M00, M10, M01


def get_moments2(m):
    """Calculeaza momentele spatiale de ordinul 2."""
    h, w = len(m), len(m[0])
    M20, M02, M11 = 0, 0, 0
    for y in range(h):
        for x in range(w):
            r, g, b = m[y][x]
            I = 255 - ((r + g + b) // 3)
            M20 += (x ** 2) * I
            M02 += (y ** 2) * I
            M11 += x * y * I
    return M20, M02, M11


def get_covariance(m):
    """Extrage matricea de covarianta."""
    h, w = len(m), len(m[0])
    M00, M10, M01 = 0, 0, 0
    for y in range(h):
        for x in range(w):
            gray = 255 - ((m[y][x][0] + m[y][x][1] + m[y][x][2]) // 3)
            M00 += gray;
            M10 += x * gray;
            M01 += y * gray
    if M00 == 0: return None, None, None

    xc, yc = M10 / M00, M01 / M00
    mu20, mu02, mu11 = 0, 0, 0
    for y in range(h):
        for x in range(w):
            gray = 255 - ((m[y][x][0] + m[y][x][1] + m[y][x][2]) // 3)
            mu20 += ((x - xc) ** 2) * gray
            mu02 += ((y - yc) ** 2) * gray
            mu11 += (x - xc) * (y - yc) * gray
    return mu20 / M00, mu02 / M00, mu11 / M00


def get_projections(m):
    """Calculeaza proiectiile de intensitate pe axa orizontala si verticala."""
    h, w = len(m), len(m[0])
    proj_h, proj_v = [0] * h, [0] * w
    for y in range(h):
        for x in range(w):
            gray = 255 - ((m[y][x][0] + m[y][x][1] + m[y][x][2]) // 3)
            proj_h[y] += gray
            proj_v[x] += gray

    max_h = max(proj_h) if max(proj_h) > 0 else 1
    res_h = [[[40, 42, 54] for _ in range(200)] for _ in range(h)]
    for y in range(h):
        bar_len = int((proj_h[y] / max_h) * 200)
        for x in range(bar_len): res_h[y][x] = [139, 233, 253]

    max_v = max(proj_v) if max(proj_v) > 0 else 1
    res_v = [[[40, 42, 54] for _ in range(w)] for _ in range(200)]
    for x in range(w):
        bar_len = int((proj_v[x] / max_v) * 200)
        for y in range(200 - bar_len, 200): res_v[y][x] = [80, 250, 123]

    return res_h, res_v


# =========================================================
# FILTRE LABORATOR 5 (Sobel si Etichetare BFS)
# =========================================================

def get_sobel(m):
    """
    Aplica operatorul Sobel pentru a detecta muchiile si a calcula
    directia de alungire (orientarea gradientului maxim).
    Returneaza matricea cu muchiile evidentiate si unghiul maxim.
    """
    h, w = len(m), len(m[0])
    # Initializam imaginea rezultata cu negru (0, 0, 0)
    res_sobel = [[[0, 0, 0] for _ in range(w)] for _ in range(h)]

    max_mag = 0
    orientation_rad = 0

    # Functie rapida pentru a calcula intensitatea (gri) a unui pixel
    def intensity(x, y):
        r, g, b = m[y][x]
        return (r + g + b) // 3

    # Ignoram marginile pentru a nu iesi din matrice
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            # Gradient pe X (Detecteaza linii verticale)
            gx = (intensity(x + 1, y - 1) + 2 * intensity(x + 1, y) + intensity(x + 1, y + 1)) - \
                 (intensity(x - 1, y - 1) + 2 * intensity(x - 1, y) + intensity(x - 1, y + 1))

            # Gradient pe Y (Detecteaza linii orizontale)
            gy = (intensity(x - 1, y + 1) + 2 * intensity(x, y + 1) + intensity(x + 1, y + 1)) - \
                 (intensity(x - 1, y - 1) + 2 * intensity(x, y - 1) + intensity(x + 1, y - 1))

            # Magnitudinea gradientului
            mag = math.sqrt(gx ** 2 + gy ** 2)

            # Salvam valoarea pentru imaginea de preview (limitata la 255)
            val = clamp(mag)
            res_sobel[y][x] = [val, val, val]

            # Cautam magnitudinea maxima pentru a gasi orientarea
            if mag > max_mag:
                max_mag = mag
                orientation_rad = math.atan2(gy, gx)

    # Convertim radianii in grade
    orientation_deg = math.degrees(orientation_rad)

    return res_sobel, orientation_deg, max_mag


def get_connected_components(m, prag=127):
    """
    Functie care primeste o imagine binarizata/grayscale si gaseste obiectele conexe.
    PASUL 1: Creeaza matricea de etichete folosind algoritmul BFS (fara OpenCV).
    PASUL 2: Asociaza fiecarei etichete (fiecarui obiect) o culoare RGB unica.
    PASUL 3: Returneaza matricea finala colorata gata de afisare.
    """
    h, w = len(m), len(m[0])

    # Initializam matricea de etichete cu 0 (0 inseamna neetichetat / fundal)
    labels = [[0 for _ in range(w)] for _ in range(h)]
    numar_obiecte = 0

    # Functie interna pentru a verifica daca un pixel face parte dintr-un obiect (e inchis la culoare)
    def este_obiect(x, y):
        r, g, b = m[y][x]
        intensitate = (r + g + b) // 3
        return intensitate < prag

    # PARTEA 1: ETICHETAREA (Breadth-First Search)
    for y in range(h):
        for x in range(w):
            # Daca pixelul e un obiect si inca nu i-am dat o eticheta
            if labels[y][x] == 0 and este_obiect(x, y):
                # Am gasit o forma noua, ii dam un numar nou (1, 2, 3...)
                numar_obiecte += 1
                labels[y][x] = numar_obiecte

                # Folosim deque pentru o coada eficienta (mai rapida decat o lista simpla)
                coada = deque([(x, y)])

                while coada:
                    cx, cy = coada.popleft()

                    # Verificam toti cei 8 vecini din jurul pixelului curent
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue  # Sarim peste el insusi

                            nx, ny = cx + dx, cy + dy

                            # Daca vecinul e in interiorul imaginii
                            if 0 <= nx < w and 0 <= ny < h:
                                # Daca vecinul e obiect si nu are eticheta inca, il adaugam in coada
                                if labels[ny][nx] == 0 and este_obiect(nx, ny):
                                    labels[ny][nx] = numar_obiecte
                                    coada.append((nx, ny))

    # PARTEA 2: COLORAREA OBIECTELOR
    # Cream un dictionar pentru culori. Cheia este eticheta, valoarea e o lista [R, G, B]
    culori_obiecte = {}
    for i in range(1, numar_obiecte + 1):
        # Generam o culoare aleatoare pentru fiecare obiect (evitam albul)
        culori_obiecte[i] = [random.randint(20, 230), random.randint(20, 230), random.randint(20, 230)]

    # Construim imaginea finala colorata (initializata cu Alb pentru fundal)
    imagine_colorata = [[[255, 255, 255] for _ in range(w)] for _ in range(h)]

    # Pictam imaginea finala conform etichetelor
    for y in range(h):
        for x in range(w):
            eticheta_curenta = labels[y][x]
            if eticheta_curenta > 0:
                imagine_colorata[y][x] = culori_obiecte[eticheta_curenta]

    return imagine_colorata, numar_obiecte


def get_isolated_object(m, target_label, prag=127):
    """
    Ruleaza etichetarea BFS si izoleaza un singur obiect cerut de utilizator (target_label).
    Obiectul selectat este colorat cu Rosu, iar restul imaginii ramane alb (fundal).
    """
    h, w = len(m), len(m[0])
    labels = [[0 for _ in range(w)] for _ in range(h)]
    numar_obiecte = 0

    def este_obiect(x, y):
        r, g, b = m[y][x]
        intensitate = (r + g + b) // 3
        return intensitate < prag

    # Parcurgem imaginea cu BFS la fel ca la etichetarea normala
    for y in range(h):
        for x in range(w):
            if labels[y][x] == 0 and este_obiect(x, y):
                numar_obiecte += 1
                labels[y][x] = numar_obiecte
                coada = deque([(x, y)])

                while coada:
                    cx, cy = coada.popleft()
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if dx == 0 and dy == 0: continue
                            nx, ny = cx + dx, cy + dy

                            if 0 <= nx < w and 0 <= ny < h:
                                if labels[ny][nx] == 0 and este_obiect(nx, ny):
                                    labels[ny][nx] = numar_obiecte
                                    coada.append((nx, ny))

    # Construim o imagine complet alba
    imagine_izolata = [[[255, 255, 255] for _ in range(w)] for _ in range(h)]

    # Coloram DOAR pixelii care apartin etichetei cautate (target_label)
    for y in range(h):
        for x in range(w):
            if labels[y][x] == target_label:
                imagine_izolata[y][x] = [255, 50, 50]  # Rosu aprins pentru vizibilitate

    return imagine_izolata