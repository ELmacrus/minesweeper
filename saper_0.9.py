import f_przygotowanie as saper

rozmiar_planszy = 20
ile_min = 100
odkryte_pola = []


def graj(rozmiar_planszy, ile_min, odkryte_pola):

	plansza_oryginal = saper.przygotuj_plansze(rozmiar_planszy, ile_min)
	plansza_gracza = saper.stworz_plansze(rozmiar_planszy, " ")
	grupy_zer = saper.pogrupuj_puste_pola(plansza_oryginal, rozmiar_planszy)
	saper.zrob_ruch(plansza_gracza, plansza_oryginal, odkryte_pola, rozmiar_planszy, ile_min, grupy_zer)



graj(rozmiar_planszy, ile_min, odkryte_pola)


