import f_przygotowanie as saper

rozmiar_planszy = 5
ile_min = 10
odkryte_pola = []

plansza_oryginal = saper.przygotuj_plansze(rozmiar_planszy, ile_min)
plansza_gracza = saper.stworz_plansze(rozmiar_planszy, " ")
grupy_zer = saper.pogrupuj_puste_pola(plansza_oryginal, rozmiar_planszy)
saper.zrob_ruch(plansza_gracza, plansza_oryginal, odkryte_pola, rozmiar_planszy, ile_min, grupy_zer)




