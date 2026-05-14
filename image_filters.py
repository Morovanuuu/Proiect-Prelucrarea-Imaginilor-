"""
Modul: image_filters.py
Descriere: Contine logica matematica independenta pentru toate filtrele de procesare a imaginii.
"""

import math
import random
from collections import deque
import numpy as np


def clamp(val):
    """Asigura ca valoarea unui pixel ramane strict in intervalul valid [0, 255]."""
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


def get_sobel(m):
    """Aplica operatorul Sobel pentru a detecta muchiile."""
    h, w = len(m), len(m[0])
    res_sobel = [[[0, 0, 0] for _ in range(w)] for _ in range(h)]
    max_mag = 0
    orientation_rad = 0

    def intensity(x, y):
        r, g, b = m[y][x]
        return (r + g + b) // 3

    for y in range(1, h - 1):
        for x in range(1, w - 1):
            gx = (intensity(x + 1, y - 1) + 2 * intensity(x + 1, y) + intensity(x + 1, y + 1)) - \
                 (intensity(x - 1, y - 1) + 2 * intensity(x - 1, y) + intensity(x - 1, y + 1))
            gy = (intensity(x - 1, y + 1) + 2 * intensity(x, y + 1) + intensity(x + 1, y + 1)) - \
                 (intensity(x - 1, y - 1) + 2 * intensity(x, y - 1) + intensity(x + 1, y - 1))
            mag = math.sqrt(gx ** 2 + gy ** 2)
            val = clamp(mag)
            res_sobel[y][x] = [val, val, val]
            if mag > max_mag:
                max_mag = mag
                orientation_rad = math.atan2(gy, gx)

    orientation_deg = math.degrees(orientation_rad)
    return res_sobel, orientation_deg, max_mag


def get_connected_components(m, prag=127):
    """Etichetarea componentelor conexe (BFS)."""
    h, w = len(m), len(m[0])
    labels = [[0 for _ in range(w)] for _ in range(h)]
    numar_obiecte = 0

    def este_obiect(x, y):
        r, g, b = m[y][x]
        intensitate = (r + g + b) // 3
        return intensitate < prag

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

    culori_obiecte = {}
    for i in range(1, numar_obiecte + 1):
        culori_obiecte[i] = [random.randint(20, 230), random.randint(20, 230), random.randint(20, 230)]

    imagine_colorata = [[[255, 255, 255] for _ in range(w)] for _ in range(h)]
    for y in range(h):
        for x in range(w):
            eticheta_curenta = labels[y][x]
            if eticheta_curenta > 0:
                imagine_colorata[y][x] = culori_obiecte[eticheta_curenta]
    return imagine_colorata, numar_obiecte


def get_isolated_object(m, target_label, prag=127):
    """Izoleaza un singur obiect cerut de utilizator."""
    h, w = len(m), len(m[0])
    labels = [[0 for _ in range(w)] for _ in range(h)]
    numar_obiecte = 0

    def este_obiect(x, y):
        r, g, b = m[y][x]
        intensitate = (r + g + b) // 3
        return intensitate < prag

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

    imagine_izolata = [[[255, 255, 255] for _ in range(w)] for _ in range(h)]
    for y in range(h):
        for x in range(w):
            if labels[y][x] == target_label:
                imagine_izolata[y][x] = [255, 50, 50]
    return imagine_izolata


# FILTRE  (Egalizare Histograma si Morfologie)


def get_egalizare_histograma(m):
    """
    Egalizarea histogramei pentru accentuarea contrastului.
    """
    h, w = len(m), len(m[0])
    hist = [0] * 256
    gray_m = [[0] * w for _ in range(h)]

    for y in range(h):
        for x in range(w):
            r, g, b = m[y][x]
            gray = (r + g + b) // 3
            gray_m[y][x] = gray
            hist[gray] += 1

    hc = [0] * 256
    hc[0] = hist[0]
    for i in range(1, 256):
        hc[i] = hc[i - 1] + hist[i]

    hc_min = hc[0]
    total_pixels = w * h

    res = [[[0, 0, 0] for _ in range(w)] for _ in range(h)]
    for y in range(h):
        for x in range(w):
            nivel_vechi = gray_m[y][x]
            nivel_nou = int(((hc[nivel_vechi] - hc_min) / (total_pixels - hc_min)) * 255)
            nivel_nou = clamp(nivel_nou)
            res[y][x] = [nivel_nou, nivel_nou, nivel_nou]

    return res


def _apply_morphology(m, op_type, iterations=1, prag=127):
    """
    Functie de baza comuna pentru operatiile morfologice.
    """
    h, w = len(m), len(m[0])
    current = [[0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            r, g, b = m[y][x]
            current[y][x] = 0 if ((r + g + b) // 3) < prag else 255

    for _ in range(iterations):
        temp = [[255] * w for _ in range(h)]
        for y in range(h):
            for x in range(w):
                neighbors = []
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h:
                            neighbors.append(current[ny][nx])
                        else:
                            neighbors.append(255)

                if op_type == 'dilatare':
                    temp[y][x] = min(neighbors)
                elif op_type == 'eroziune':
                    temp[y][x] = max(neighbors)

        current = temp

    res = [[[val, val, val] for val in row] for row in current]
    return res


def get_dilatare(m, iteratii):
    return _apply_morphology(m, 'dilatare', iteratii)


def get_eroziune(m, iteratii):
    return _apply_morphology(m, 'eroziune', iteratii)


def get_deschidere(m, iteratii):
    eroded = _apply_morphology(m, 'eroziune', iteratii)
    return _apply_morphology(eroded, 'dilatare', iteratii)


def get_inchidere(m, iteratii):
    dilated = _apply_morphology(m, 'dilatare', iteratii)
    return _apply_morphology(dilated, 'eroziune', iteratii)



# FILTRE  (Filtre Spatiale 3x3 si DFT)

def _apply_3x3_window(m, func_type):
    h, w = len(m), len(m[0])
    res = [[[0, 0, 0] for _ in range(w)] for _ in range(h)]

    for y in range(h):
        for x in range(w):
            if y == 0 or y == h - 1 or x == 0 or x == w - 1:
                res[y][x] = m[y][x]
                continue

            r_vals, g_vals, b_vals = [], [], []

            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    r, g, b = m[y + dy][x + dx]
                    r_vals.append(r)
                    g_vals.append(g)
                    b_vals.append(b)

            if func_type == 'mediere':
                res[y][x] = [sum(r_vals) // 9, sum(g_vals) // 9, sum(b_vals) // 9]

            elif func_type == 'median':
                r_vals.sort();
                g_vals.sort();
                b_vals.sort()
                res[y][x] = [r_vals[4], g_vals[4], b_vals[4]]

            elif func_type == 'minim':
                res[y][x] = [min(r_vals), min(g_vals), min(b_vals)]

            elif func_type == 'maxim':
                res[y][x] = [max(r_vals), max(g_vals), max(b_vals)]

    return res


def get_mediere(m):
    return _apply_3x3_window(m, 'mediere')


def get_median(m):
    return _apply_3x3_window(m, 'median')


def get_minim(m):
    return _apply_3x3_window(m, 'minim')


def get_maxim(m):
    return _apply_3x3_window(m, 'maxim')


def get_accentuare(m):
    h, w = len(m), len(m[0])
    res = [[[0, 0, 0] for _ in range(w)] for _ in range(h)]

    kernel = [
        [0.0, -0.25, 0.0],
        [-0.25, 1.0, -0.25],
        [0.0, -0.25, 0.0]
    ]

    for y in range(1, h - 1):
        for x in range(1, w - 1):
            sum_r, sum_g, sum_b = 0.0, 0.0, 0.0

            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    r, g, b = m[y + dy][x + dx]
                    weight = kernel[dy + 1][dx + 1]
                    sum_r += weight * r
                    sum_g += weight * g
                    sum_b += weight * b

            orig_r, orig_g, orig_b = m[y][x]
            new_r = clamp(orig_r + 0.6 * sum_r)
            new_g = clamp(orig_g + 0.6 * sum_g)
            new_b = clamp(orig_b + 0.6 * sum_b)

            res[y][x] = [new_r, new_g, new_b]

    for x in range(w):
        res[0][x], res[h - 1][x] = m[0][x], m[h - 1][x]
    for y in range(h):
        res[y][0], res[y][w - 1] = m[y][0], m[y][w - 1]

    return res


#  Transformata Fourier (Numpy)

def get_fourier_transform(m):

    h, w = len(m), len(m[0])

    # 1. Convertim imaginea intr-o matrice 2D NumPy, cu numere reale
    # Transformata Fourier se aplica pe imagini alb-negru (grayscale)
    gray = np.zeros((h, w), dtype=np.float64)
    for y in range(h):
        for x in range(w):
            r, g, b = m[y][x]
            # Formula standard de conversie in tonuri de gri
            gray[y][x] = 0.299 * r + 0.587 * g + 0.114 * b

    # 2. Aplicam Transformata Fourier Rapida 2D (FFT2) din Numpy
    f = np.fft.fft2(gray)

    # 3. Mutam componenta de frecventa zero (cea mai luminoasa, numita DC)
    fshift = np.fft.fftshift(f)

    # 4. Numerele rezultate sunt complexe (au o parte reala si una imaginara
    # Pentru a le afisa pe ecran, trebuie sa le calculam distanta absoluta
    magnitude = np.abs(fshift)

    # 5. Aplicam o scara logaritmica.
    magnitude_log = np.log(1 + magnitude)

    # 6. Normalizam valorile matematice ca sa se incadreze in intervalul de culoare 0-255
    max_mag = np.max(magnitude_log)
    if max_mag == 0:
        max_mag = 1  # Evitam impartirea la zero

    res = [[[0, 0, 0] for _ in range(w)] for _ in range(h)]
    for y in range(h):
        for x in range(w):
            val = int((magnitude_log[y, x] / max_mag) * 255)
            val = clamp(val)
            res[y][x] = [val, val, val]

    return res


#  Dithering (Floyd-Steinberg)
def get_floyd_steinberg(m):
    """
    Foloseste o paleta de culori fixata si difuzeaza eroarea pe canalele R, G si B
    conform matricii standard (7/16, 3/16, 5/16, 1/16).
    """
    h, w = len(m), len(m[0])

    # Definim Paleta de culori (RGB + CMY + Alb/Negru)
    palette = [
        [0, 0, 0],  # Negru
        [255, 255, 255],  # Alb
        [255, 0, 0],  # Rosu
        [0, 255, 0],  # Verde
        [0, 0, 255],  # Albastru
        [255, 255, 0],  # Galben
        [0, 255, 255],  # Cyan
        [255, 0, 255]  # Magenta
    ]

    def nearest_color(r, g, b):
        min_dist = float('inf')
        best_c = palette[0]
        for pr, pg, pb in palette:
            dist = math.sqrt((r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2)
            if dist < min_dist:
                min_dist = dist
                best_c = [pr, pg, pb]
        return best_c

    # Cream o copie float a imaginii pentru a nu pierde din precizie la calculul erorii
    float_m = [[[float(c) for c in pixel] for pixel in row] for row in m]

    for y in range(h):
        for x in range(w):
            old_r, old_g, old_b = float_m[y][x]

            # Gasim culoarea din paleta
            new_r, new_g, new_b = nearest_color(old_r, old_g, old_b)
            float_m[y][x] = [new_r, new_g, new_b]

            # Calculam eroarea
            err_r = old_r - new_r
            err_g = old_g - new_g
            err_b = old_b - new_b

            # Functie pentru a distribui eroarea la vecini
            def add_error(nx, ny, factor):
                if 0 <= nx < w and 0 <= ny < h:
                    float_m[ny][nx][0] += err_r * factor
                    float_m[ny][nx][1] += err_g * factor
                    float_m[ny][nx][2] += err_b * factor

            # Matricea de difuzie a erorii Floyd-Steinberg
            add_error(x + 1, y, 7.0 / 16.0)  # Dreapta
            add_error(x - 1, y + 1, 3.0 / 16.0)  # Stanga-Jos
            add_error(x, y + 1, 5.0 / 16.0)  # Jos
            add_error(x + 1, y + 1, 1.0 / 16.0)  # Dreapta-Jos

    # Reconstruim imaginea aplicand clamp (0-255) pentru a o putea afisa
    res = [[[0, 0, 0] for _ in range(w)] for _ in range(h)]
    for y in range(h):
        for x in range(w):
            r, g, b = float_m[y][x]
            res[y][x] = [clamp(r), clamp(g), clamp(b)]

    return res


def get_laplacian(m):

    # Iau o imagine si creez o matrice noua goala pentru rezultat, apoi aplic filtrul Laplacian (3x3) pentru detectarea martignilor
    #
    h, w = len(m), len(m[0])
    res = [[[0, 0, 0] for _ in range(w)] for _ in range(h)]

    # Definesc o matrice mica 3x3 (kernel) care are 8 in mijloc si -1 in rest
    kernel = [
        [-1, -1, -1],
        [-1, 8, -1],
        [-1, -1, -1]
    ]
    # Am mers  cu un dublu for prin toti pixelii imaginii, dar sar peste marginile extreme (x=0, y=0)
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            sum_val = 0

            # Parcurgem vecinii
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    r, g, b = m[y + dy][x + dx]
                    # Calculam intensitatea pixelului curent
                    gray = (r + g + b) // 3
                    weight = kernel[dy + 1][dx + 1]
                    sum_val += gray * weight

            # Din cauza valorilor de -1, suma poate fi negativa.
            # Functia 'clamp' taie tot ce e sub 0 si peste 255.
            final_val = clamp(sum_val)
            res[y][x] = [final_val, final_val, final_val]

    return res


def get_eliminare_zgomot_gaussian(m):

 # Pregatesc o matrice noua pentru rezultat si setez dimensiunea kernelului la 3 ( vecini intre -1 si 1)
 # Pentru fiecare pixel, fac un for prin zona lui de vecini 3x3
 # Pentru a nu iesi in afara imaginii la margini, folosesc min si max ca sa ma mentin in limitele (0, width) si (0, height)
 # Adun separat valorile pentru rosu, verde si albastru de la toti cei 9 vecini
 # Am impartit sumele la 9  sa aflu media aritmetica
    h, w = len(m), len(m[0])
    res = [[[0, 0, 0] for _ in range(w)] for _ in range(h)]

    kernel_size = 3
    half_kernel = kernel_size // 2  # este  1

    for y in range(h):
        for x in range(w):
            sum_r, sum_g, sum_b = 0, 0, 0

            # Parcurgem kernel 3x3
            for i in range(-half_kernel, half_kernel + 1):
                for j in range(-half_kernel, half_kernel + 1):

                    offset_x = max(0, min(x + i, w - 1))
                    offset_y = max(0, min(y + j, h - 1))

                    r, g, b = m[offset_y][offset_x]
                    sum_r += r
                    sum_g += g
                    sum_b += b

            # Calculam media valorilor
            avg_r = sum_r // (kernel_size * kernel_size)
            avg_g = sum_g // (kernel_size * kernel_size)
            avg_b = sum_b // (kernel_size * kernel_size)

            # Setam noua valoare a pixelului
            res[y][x] = [avg_r, avg_g, avg_b]

    return res

def get_snr_single(m):

    # Creez doua variabile pentru suma_semnal si suma_zgomot (pornite de la 0)
    # Am trecut  prin fiecare pixel al imaginii
    # Setez semnalul ca fiind valoarea de rosu a pixelului
    # Calculez zgomotul scazand semnalul din 255 (valoarea maxima posibila)
    # Adun semnalul si zgomotul la sumele mele totale
    # Dupa ce termin pixelii, calculez media pentru semnal si media pentru zgomot impartind la numarul total de pixeli
    # Aplic formula  10 * log10 ( (media_semnal la patrat) / (media_zgomot la patrat) )
    # Calcul SNR (Signal-to-Noise Ratio)

    h, w = len(m), len(m[0])
    signal_sum = 0
    noise_sum = 0

    for y in range(h):
        for x in range(w):
            r, g, b = m[y][x]
            signal = r
            noise = abs(255 - signal)

            signal_sum += signal
            noise_sum += noise

    pixels = w * h
    signal_mean = signal_sum / pixels
    noise_mean = noise_sum / pixels

    # Prevenim impartirea la zero daca cumva imaginea e complet alba/neagra
    if noise_mean == 0:
        return float('inf')

    snr = 10 * math.log10((signal_mean * signal_mean) / (noise_mean * noise_mean))
    return snr


def _java_getRGB(r, g, b):

    val = 0xFF000000 | (r << 16) | (g << 8) | b
    if val >= 0x80000000:
        val -= 0x100000000
    return val


def get_snr_double(m1, m2):

    # Iau dimensiunea minima dintre cele 2 imagini (ca sa nu dea eroare daca una e mai mare)
    # Initializez sumele pentru semnal si zgomot cu 0
    # Parcurg pixelii comuni din ambele imagini deodata
    # Transform culorile RGB in numere intregi pe 32 de biti
    # Semnalul e diferenta absoluta intre pixelul din prima poza si cel din a doua
    # Zgomotul e valoarea absoluta a pixelului din prima poza
    # Adaug la sumele totale, calculez mediile pe toata imaginea
    # O pun in formula: 10 * log10((media_semnal^2) / (media_zgomot^2)) si returnez rezultatul

    h = min(len(m1), len(m2))
    w = min(len(m1[0]), len(m2[0]))

    signal_sum = 0
    noise_sum = 0

    for y in range(h):
        for x in range(w):
            r1, g1, b1 = m1[y][x]
            r2, g2, b2 = m2[y][x]

            rgb1 = _java_getRGB(r1, g1, b1)
            rgb2 = _java_getRGB(r2, g2, b2)

            signal = abs(rgb1 - rgb2)
            noise = abs(rgb1)

            signal_sum += signal
            noise_sum += noise

    pixels = w * h
    signal_mean = signal_sum / pixels
    noise_mean = noise_sum / pixels

    if noise_mean == 0:
        return float('inf')

    snr = 10 * math.log10((signal_mean * signal_mean) / (noise_mean * noise_mean))
    return snr


# Definesc matricile 3x3 (kernel-urile) pentru Vertical, Orizontal, Sobel si Scharr
# Merg pixel cu pixel prin imagine (fara marginile extreme)
# Pentru fiecare pixel, aplic convolutia separat pe R, G si B, inmultind vecinii cu valorile din kernel
# Apoi adun cele 3 rezultate intr-o singura valoare totala
# Daca valoarea e negativa, o fac pozitiva (modul/abs). Daca e peste 255, o limitez la 255
# Salvez valoarea ca ton de gri [val, val, val] in imaginea rezultat

def get_edge_detection(m, filter_type):

    h, w = len(m), len(m[0])
    res = [[[0, 0, 0] for _ in range(w)] for _ in range(h)]

    # Definim mastile (kernel-urile) in functie de tipul selectat
    if filter_type == "Filtru Vertical":
        kernel = [[1, 0, -1], [1, 0, -1], [1, 0, -1]]
    elif filter_type == "Filtru Orizontal":
        kernel = [[1, 1, 1], [0, 0, 0], [-1, -1, -1]]
    elif filter_type == "Sobel Vertical":
        kernel = [[1, 0, -1], [2, 0, -2], [1, 0, -1]]
    elif filter_type == "Sobel Orizontal":
        kernel = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
    elif filter_type == "Scharr Vertical":
        kernel = [[3, 0, -3], [10, 0, -10], [3, 0, -3]]
    elif filter_type == "Scharr Orizontal":
        kernel = [[3, 10, 3], [0, 0, 0], [-3, -10, -3]]
    else:
        return m

    for y in range(1, h - 1):
        for x in range(1, w - 1):
            sum_r, sum_g, sum_b = 0, 0, 0

            # Aplicam convolutia (produsul cu kernel-ul 3x3)
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    r, g, b = m[y + dy][x + dx]
                    weight = kernel[dy + 1][dx + 1]

                    sum_r += r * weight
                    sum_g += g * weight
                    sum_b += b * weight

            # combinam canalele
            total_sum = sum_r + sum_g + sum_b

            # Functia "fixOutOfRangeRGBValues"
            final_val = abs(total_sum)
            if final_val > 255:
                final_val = 255

            final_val = int(final_val)
            res[y][x] = [final_val, final_val, final_val]

    return res