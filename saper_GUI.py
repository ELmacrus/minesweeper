import f_przygotowanie_GUI as saper
from Tkinter import *

import tkMessageBox



class GUI:

    def __init__(self, root, wiersz, kolumna):
        self.root = root
        self.wiersz = wiersz
        self.kolumna = kolumna
        self.przycisk = Button(self.root, text = ' ', width = 2, height = 1, bg = 'snow')
        self.przycisk.grid(row = self.wiersz+1, column = self.kolumna+1)

    
def graj(rozmiar_planszy, ile_min):

    def zrob_ruch(obiekty_GUI, jeden_obiekt_GUI):
        wiersz = jeden_obiekt_GUI.wiersz
        kolumna = jeden_obiekt_GUI.kolumna
        teraz_odkryte_pole = plansza_oryginal[wiersz][kolumna]        
        ustaw_kolor(teraz_odkryte_pole, jeden_obiekt_GUI.przycisk)

        if [wiersz, kolumna] in odkryte_pola:
            pass

        elif teraz_odkryte_pole == 'X':
            for obiekt in obiekty_GUI:
                obiekt.przycisk.config(state = DISABLED)


            tkMessageBox.showinfo("KONIEC GRY", "PRZEGRALES")


        elif teraz_odkryte_pole == 0:
            for i in range(len(grupy_zer)):
                if [wiersz, kolumna] in grupy_zer[i]:
                    trafiona_grupa = grupy_zer[i]
                    for j in range(len(trafiona_grupa)):
                        pole = trafiona_grupa[j]
                        pole_wiersz = pole[0]
                        pole_kolumna = pole[1]

                        ustaw_kolor(plansza_oryginal[pole_wiersz][pole_kolumna], obiekty_GUI[(pole_wiersz*rozmiar_planszy)+pole_kolumna].przycisk)
                        if [pole_wiersz, pole_kolumna] not in odkryte_pola:
                            odkryte_pola.append([pole_wiersz, pole_kolumna])
                    break
        
        else: 
            odkryte_pola.append([wiersz, kolumna])

        if len(odkryte_pola)>(rozmiar_planszy*rozmiar_planszy)-1-ile_min:
            for obiekt in obiekty_GUI:
                obiekt.przycisk.config(state = DISABLED)

            tkMessageBox.showinfo("GRATULACJE", "PRZESZEDLES TEGO SAPERA")

    def ustaw_kolor(teraz_odkryte_pole, przycisk):
        ##kolory i grafiki
        if teraz_odkryte_pole != 0 and teraz_odkryte_pole != 'X':
            if teraz_odkryte_pole == 1:
                kolor = 'navy'
            elif teraz_odkryte_pole == 2:
                kolor = 'dark green'
            elif teraz_odkryte_pole == 3:
                kolor = 'indian red'
            elif teraz_odkryte_pole == 4:
                kolor = 'dark violet'
            elif teraz_odkryte_pole == 5:
                kolor = 'cyan2'
            elif teraz_odkryte_pole == 6:
                kolor = 'OrangeRed2'
            elif teraz_odkryte_pole == 7:
                kolor = 'OliveDrab1'
            else:
                kolor = 'gray5'

            przycisk.config(text = teraz_odkryte_pole, fg = kolor)

        elif teraz_odkryte_pole == 0:
            przycisk.config(bg = 'antique white', relief = SUNKEN)
        elif teraz_odkryte_pole == 'X':
            przycisk.config(text = teraz_odkryte_pole)



    
    global L1
    L1.destroy()
    L2 = Label(root)

    plansza_oryginal = saper.przygotuj_plansze(rozmiar_planszy, ile_min) #1
    saper.wyswietl_plansze(plansza_oryginal, rozmiar_planszy)
    przyciski_planszy = [] #2
    grupy_zer = saper.pogrupuj_puste_pola(plansza_oryginal, rozmiar_planszy) #3

    
    for wiersz in range(rozmiar_planszy):
	    for kolumna in range(rozmiar_planszy):
		    przycisk = GUI(L2, wiersz, kolumna)
		    przyciski_planszy.append(przycisk)

    L2.pack(anchor = S)
    
    for element in przyciski_planszy:
        element.przycisk.config(command = lambda obiekty_GUI = przyciski_planszy, jeden_obiekt_GUI = element: zrob_ruch(obiekty_GUI, jeden_obiekt_GUI))
	
    odkryte_pola = [] #5




sec = 0

root = Tk()

L1 = Label(root)

B1 = Button(L1, text = "Poziom latwy", command = lambda rozmiar_planszy = 10, ile_min = 20: graj(rozmiar_planszy, ile_min))
B2 = Button(L1, text = "Poziom sredni", command = lambda rozmiar_planszy = 15, ile_min = 45: graj(rozmiar_planszy, ile_min))
B3 = Button(L1, text = "Poziom trudny", command = lambda rozmiar_planszy = 20, ile_min = 80: graj(rozmiar_planszy, ile_min))
B4 = Button(L1, text = "Poziom ekspert", command = lambda rozmiar_planszy = 25, ile_min = 125: graj(rozmiar_planszy, ile_min))
B5 = Button(L1, text = "test", command = lambda rozmiar_planszy = 5, ile_min = 5: graj(rozmiar_planszy, ile_min))

B1.pack(anchor = W)
B2.pack(anchor = W)
B3.pack(anchor = W)
B4.pack(anchor = W)
B5.pack(anchor = W)

L1.pack(anchor = W)
root.mainloop()












