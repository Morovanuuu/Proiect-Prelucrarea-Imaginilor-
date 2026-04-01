"""
Modul: image_filters.py
Descriere: Contine formulele matematice, independenta pentru toate filtrele de procesare a imaginii
Acest modul nu  depinde de interfata grafica, este pentru testarea si reutilizare
"""


def clamp(val):
    """
    Se asigura ca valoarea unui pixel ramane strict in intervalul valid [0, 255]
    Se preia o valoare calculata (care poate iesi din limite) si o trunchiaza
    """
    return max(0, min(255, int(val)))


def get_grayscale(m):
    """
    Se converteste matricea RGB in tonuri de gri folosind cele 3 metode din laborator:
    1. Media: Media aritmetica simpla (R + G + B) / 3
    2. Luma (NTSC): Metoda ponderata  mai mare la culoarea verde (0.299*R + 0.587*G + 0.114*B)
    3. Mid/Max (Desaturare): Media dintre canalul cel mai intens si cel mai slab
    """
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
    """
    Se transforma spatiul aditiv RGB in spatiul substractiv CMY (Cyan, Magenta, Yellow)
    Formula: C = 255 - R, M = 255 - G, Y = 255 - B
    """
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
    """
    Conversie RGB -> YUV
    Se separa informatia de luminozitate (Y) de informatia de culoare/crominanta (U si V)
    Valorile U si V sunt scalate si deplasate (+128) pentru a fi vizibile ca imagini pe 8 biti
    """
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
    """
    Conversie RGB -> YCbCr
    Y = Luminanta, Cb = Diferenta fata de Albastru, Cr = Diferenta fata de Rosu
    """
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
    """
    Conversie RGB -> HSV (Hue/Nuanta, Saturation/Saturatie, Value/Valoare)
    """
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
    """
    Se aplica filtrul de imagine negativa (inversare culori)
    Se returneaza negativul global, precum si negativul calculat separat pe fiecare canal RGB
    """
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
    """
    Binarizarea imaginii (Thresholding)
    Se transforma toti pixelii in negru (0) sau alb pur (255) in functie de o valoare
    """
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
    """
    Se calculeaza histograma imaginii (frecventa de aparitie a fiecarei intensitati luminoase, 0-255)
    Se returneaza o matrice grafica reprezentand barele histogramei scalate
    """
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
    """
    Se calculeaza momentele de ordin 1 (M00, M10, M01)
    Aceste momente sunt folosite pentru a determina Aria formei (M00) si
    coordonatele Centrului de Masa
    Se returneaza si matricea cu centrul marcat vizual
    """
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

    # Se deseneaza o cruce rosie pe centrul de masa
    for i in range(-15, 16):
        if 0 <= xc + i < w: res_moments[yc][xc + i] = [255, 85, 85]
        if 0 <= yc + i < h: res_moments[yc + i][xc] = [255, 85, 85]
    return res_moments, xc, yc, M00, M10, M01


def get_moments2(m):
    """
    Se calculeaza momentele spatiale de ordinul 2 (M20, M02, M11)
    Acestea descriu distributia masei/pixelilor fata de axele de coordonate
    (momente de inertie) si sunt esentiale pentru calculul orientarii obiectului
    """
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
    """
    Se extrage matricea de covarianta pe baza momentelor centrale de ordinul 2
    """
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
    """
    Se calculeaza proiectiile de intensitate pe axa orizontala
    si verticala;  Rezultatul este un grafic de intensitate
    """
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