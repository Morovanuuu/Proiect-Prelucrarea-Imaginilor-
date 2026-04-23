# Photoshop V2 - Proiect Prelucrarea Imaginilor

## Descriere
Photoshop V2 este o aplicatie simpla ce este dezvoltata in Python pentru procesarea si analiza imaginilor. Proiectul implementeaza propriile functii de parsare la nivel de byte pentru fisierele de tip `.bmp` (fara a folosi biblioteci externe de procesare a imaginii precum OpenCV sau Pillow) si ofera o interfata grafica interactiva construita cu `tkinter`.

## Functionalitati Implementate
Aplicatia permite incarcarea imaginilor BMP necomprimate, procesarea acestora si salvarea rezultatelor. Filtrele si algoritmii implementati includ:

* **Conversii de spatiu de culoare:** Grayscale (3 metode: Medie, Luma, Mid/Max), CMY, YUV, YCbCr, HSV.
* **Filtre de baza:** Invers RGB (Negativ global si pe canale), Binarizare (Thresholding).
* **Analiza si Statistica:**
    * Histograma de intensitate luminoasa.
    * Momente de ordin 1 (Calculul ariei si afisarea vizuala a centrului de masa).
    * Momente spatiale de ordin 2 (Momente de inertie).
    * Matricea de Covarianta.
    * Proiectii de intensitate (Orizontala si Verticala).

## Structura Proiectului
Am impartit in 4 module principale aplicatia :

1.  `main.py` - Punctul de intrare in aplicatie (Entry Point). Initializeaza si ruleaza interfata grafica.
2.  `bmp_io.py` - Modul dedicat exclusiv decodificarii (citirii) si codificarii (scrierii) fisierelor `.bmp` la nivel de bytes, manipuland direct header-ele si calculand padding-ul necesar.
3.  `image_filters.py` - Inima matematica a aplicatiei. Contine exclusiv functiile care aplica transformarile pe matricele de pixeli, independent de interfata grafica.
4.  `ui_app.py` - Modulul care defineste clasa `ImageApp`, responsabila pentru randarea interfetei grafice (GUI), gestiunea evenimentelor si rutarea datelor catre filtrele matematice.

## Cerinte de Sistem si Instalare
Proiectul foloseste strict bibliotecile standard din Python. **Nu necesita instalarea de pachete externe via pip.**

* Python 3.x instalat pe sistem.
* Biblioteci standard utilizate: `tkinter`, `struct`, `filedialog`.

## Instructiuni de Rulare
1. Asigurati-va ca va aflati in directorul proiectului (acolo unde se afla fisierele `.py`).
2. Rulati urmatoarea comanda in terminal:
   ```bash
   python main.py