import f_przygotowanie as saper

rozmiar_planszy = 10
odkryte_pola = []

plansza_oryginal = saper.przygotuj_plansze(rozmiar_planszy)
plansza_gracza = saper.stworz_plansze(rozmiar_planszy, " ")
saper.wyswietl_plansze(plansza_gracza, rozmiar_planszy)
saper.zrob_ruch(plansza_gracza, plansza_oryginal, odkryte_pola, rozmiar_planszy)




