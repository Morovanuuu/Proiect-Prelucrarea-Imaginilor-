"""
Modul: bmp_io.py
Descriere: Se gestioneaza citirea, decodificarea si salvarea fisierelor BMP necomprimate,
la nivel de byte, folosind modulul standard 'struct'.
"""

import struct

def read_bmp(file_path):
    """
    Se citeste un fisier BMP si  se extrage pixelii intr-o matrice 2D.
    Se pot incarca  imagini pe 8 biti (cu paleta) si pe 24 de biti (TrueColor).
    """
    with open(file_path, "rb") as f:
        file_header = f.read(14)
        if len(file_header) < 14:
            raise ValueError("Fisier prea mic pentru a fi BMP.")
        if file_header[0:2] != b"BM":
            raise ValueError("Nu este un fisier BMP valid.")

        data_offset = struct.unpack("<I", file_header[10:14])[0]
        info_header = f.read(40)
        if len(info_header) < 40:
            raise ValueError("Header DIB incomplet.")

        width = struct.unpack("<i", info_header[4:8])[0]
        height = struct.unpack("<i", info_header[8:12])[0]
        bit_count = struct.unpack("<H", info_header[14:16])[0]
        compression = struct.unpack("<I", info_header[16:20])[0]

        if compression != 0:
            raise ValueError("Aplicatia suporta doar imagini necomprimate.")

        bottom_up = height > 0
        abs_height = abs(height)

        palette = []
        if bit_count == 8:
            f.seek(54)
            for _ in range(256):
                bgra = f.read(4)
                palette.append([bgra[2], bgra[1], bgra[0]])

        f.seek(data_offset)
        pixels = []

        if bit_count == 24:
            row_size = ((width * 3 + 3) // 4) * 4
            for _ in range(abs_height):
                row_data = f.read(row_size)
                row_pixels = []
                for x in range(width):
                    b, g, r = row_data[x * 3], row_data[x * 3 + 1], row_data[x * 3 + 2]
                    row_pixels.append([r, g, b])
                pixels.append(row_pixels)
        elif bit_count == 8:
            row_size = ((width + 3) // 4) * 4
            for _ in range(abs_height):
                row_data = f.read(row_size)
                row_pixels = []
                for x in range(width):
                    idx = row_data[x]
                    row_pixels.append(list(palette[idx]))
                pixels.append(row_pixels)

        if bottom_up:
            pixels.reverse()
        return pixels


def write_bmp(matrix, filename):
    """
    Se salveaza o matrice 2D RGB intr-un fisier BMP (24-bit TrueColor),
    calculand padding-ul necesar pentru alinierea la 4 bytes.
    """
    height = len(matrix)
    width = len(matrix[0]) if height > 0 else 0
    row_size = ((width * 3 + 3) // 4) * 4
    image_size = row_size * height
    file_size = 54 + image_size

    with open(filename, "wb") as f:
        f.write(b"BM")
        f.write(struct.pack("<I", file_size))
        f.write(b"\x00\x00\x00\x00")
        f.write(struct.pack("<I", 54))
        f.write(struct.pack("<I", 40))
        f.write(struct.pack("<i", width))
        f.write(struct.pack("<i", height))
        f.write(struct.pack("<H", 1))
        f.write(struct.pack("<H", 24))
        f.write(struct.pack("<I", 0))
        f.write(struct.pack("<I", image_size))
        f.write(struct.pack("<i", 0))
        f.write(struct.pack("<i", 0))
        f.write(struct.pack("<I", 0))
        f.write(struct.pack("<I", 0))

        padding = b"\x00" * (row_size - width * 3)
        for row in reversed(matrix):
            row_data = bytearray()
            for r, g, b in row:
                row_data.extend([int(b), int(g), int(r)])
            f.write(row_data)
            f.write(padding)


def clamp(val):
    """Se asigura ca o valoare se incadreaza in intervalul valid pentru un pixel (0-255)."""
    return max(0, min(255, int(val)))