from random import sample
import os
import time

#koordynaty sasiednich pol
NW = [-1, -1]
N = [-1, 0]
NE = [-1, 1]
E = [0, 1]
SE = [1, 1]
S = [1, 0]
SW = [1, -1]
W = [0, -1]
####

def stworz_plansze(rozmiar_planszy, pole):

    plansza_gry = []

    for i in range(rozmiar_planszy):
        wiersz_planszy = []
        for j in range(rozmiar_planszy):
            wiersz_planszy.append(pole)
        plansza_gry.append(wiersz_planszy)

    return plansza_gry


def wylosuj_miny(plansza_gry, rozmiar_planszy):

	pole_z_mina = sample(range(rozmiar_planszy*rozmiar_planszy), 20)
	
	for mina in pole_z_mina:
		wiersz = int(mina/rozmiar_planszy)
		kolumna = mina%rozmiar_planszy
		plansza_gry[wiersz][kolumna] = 'X'

	#print sorted(pole_z_mina)
	return plansza_gry

def policz_miny(plansza_gry, rozmiar_planszy):

	for wiersz in range(rozmiar_planszy):
		for kolumna in range(rozmiar_planszy):
			bomby = []

			if plansza_gry[wiersz][kolumna] == 0:				
				try:
					bomby.append(szukaj_miny(plansza_gry, wiersz+NW[0], kolumna+NW[1])) #NW
				except IndexError:
					pass

				try:
					bomby.append(szukaj_miny(plansza_gry, wiersz+N[0], kolumna+N[1])) #N
				except IndexError:
					pass

				try:
					bomby.append(szukaj_miny(plansza_gry, wiersz+NE[0], kolumna+NE[1])) #NE
				except IndexError:
					pass

				try:
					bomby.append(szukaj_miny(plansza_gry, wiersz+E[0], kolumna+E[1])) #E
				except IndexError:
					pass

				try:
					bomby.append(szukaj_miny(plansza_gry, wiersz+SE[0], kolumna+SE[1])) #SE
				except IndexError:
					pass

				try:
					bomby.append(szukaj_miny(plansza_gry, wiersz+S[0], kolumna+S[1])) #S
				except IndexError:
					pass

				try:
					bomby.append(szukaj_miny(plansza_gry, wiersz+SW[0], kolumna+SW[1])) #SW
				except IndexError:
					pass

				try:
					bomby.append(szukaj_miny(plansza_gry, wiersz+W[0], kolumna+W[1])) #W
				except IndexError:
					pass
				
				plansza_gry[wiersz][kolumna] = bomby.count('X')

	return plansza_gry



def przygotuj_plansze(rozmiar_planszy):
	
	plansza = stworz_plansze(rozmiar_planszy, 0)
	plansza = wylosuj_miny(plansza, rozmiar_planszy)
	plansza = policz_miny(plansza, rozmiar_planszy)
	return plansza



def wyswietl_plansze(plansza_gry, rozmiar_planszy):

	#os.system('cls')
	for wiersz in range(rozmiar_planszy):
		linia = " "
		linia2 = ""
		for kolumna in range(rozmiar_planszy):
			linia += str(plansza_gry[wiersz][kolumna]) + " | "
			linia2 += "----"
		print linia
		print linia2


def szukaj_miny(plansza_gry, wiersz, kolumna):
	
	if wiersz <0 or kolumna <0:
		return -1
	else:
		pole = plansza_gry[wiersz][kolumna]
		return pole


def zrob_ruch(plansza_gracza, plansza_oryginal, odkryte_pola, rozmiar_planszy):

	while len(odkryte_pola)<=99:

		os.system('cls')
		wyswietl_plansze(plansza_oryginal, rozmiar_planszy)
		print "\n"
		wyswietl_plansze(plansza_gracza, rozmiar_planszy)
		wiersz = int(raw_input("Podaj wiersz: > ")) - 1
		kolumna = int(raw_input("Podaj kolumne: > ")) - 1
		teraz_odkryte_pole = plansza_oryginal[wiersz][kolumna]
		plansza_gracza[wiersz][kolumna] = teraz_odkryte_pole
		

		if [wiersz, kolumna] in odkryte_pola:
			print "To pole jest juz odkryte! Odkryj inne"
			time.sleep(3)
		elif teraz_odkryte_pole == 'X':
			odkryte_pola.append([wiersz, kolumna])
			os.system('cls')
			wyswietl_plansze(plansza_oryginal, rozmiar_planszy)
			print "\n"
			wyswietl_plansze(plansza_gracza, rozmiar_planszy)
			print "KONIEC GRY"
			break
		elif teraz_odkryte_pole == 0:
			odkryte_pola.append([wiersz, kolumna])
			plansza_gracza, odkryte_pola = odkryj_puste_pola(plansza_gracza, plansza_oryginal, odkryte_pola, rozmiar_planszy)
			wyswietl_plansze(plansza_oryginal, rozmiar_planszy)
			print "\n"
			wyswietl_plansze(plansza_gracza, rozmiar_planszy)
		else:
			odkryte_pola.append([wiersz, kolumna])


def odkryj_puste_pola(plansza_gracza, plansza_oryginal, odkryte_pola, rozmiar_planszy):

	wiersz = odkryte_pola[-1][0]
	kolumna = odkryte_pola[-1][1]
	szukaj = szukaj_miny
	pole = szukaj(plansza_oryginal, wiersz+W[0], kolumna+W[1])

	###sprawdz biezacy wiersz w lewo
	while (pole == 0 or pole != -1):
		print wiersz, kolumna
		if pole == 1:
			wiersz += W[0]
			kolumna += W[1]
			odkryte_pola.append([wiersz, kolumna])
			plansza_gracza[wiersz][kolumna] = plansza_oryginal[wiersz][kolumna]
			break

		elif pole == 'X':
			break

		else:
			wiersz += W[0]
			kolumna += W[1]
			odkryte_pola.append([wiersz, kolumna])
			plansza_gracza[wiersz][kolumna] = plansza_oryginal[wiersz][kolumna]
			pole = szukaj(plansza_oryginal, wiersz+W[0], kolumna+W[1])

	return plansza_gracza, odkryte_pola







