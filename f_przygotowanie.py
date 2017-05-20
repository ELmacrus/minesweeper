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

koordy = [NW, N, NE, E, SE, S, SW, W] #wykorzystywane w odkryj_puste_pola_2
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

	pole_z_mina = sample(range(rozmiar_planszy*rozmiar_planszy), 10)
	
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
		try:
			pole = plansza_gry[wiersz][kolumna]
			return pole
		except IndexError:
			return -2
		
def zrob_ruch(plansza_gracza, plansza_oryginal, odkryte_pola, rozmiar_planszy):

	while len(odkryte_pola)<=(rozmiar_planszy*rozmiar_planszy)-1-20:
		print sorted(odkryte_pola)
		print len(odkryte_pola)
		testy = raw_input()
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
			L1 = len(odkryte_pola)
			plansza_gracza, odkryte_pola = odkryj_puste_pola(plansza_gracza, plansza_oryginal, odkryte_pola)
			L2 = len(odkryte_pola)
			ile_odkryto = L2 - L1
			while ile_odkryto > 0:
				L2 = len(odkryte_pola)
				plansza_gracza, odkryte_pola = odkryj_puste_pola_2(plansza_gracza, plansza_oryginal, odkryte_pola, ile_odkryto)
				L3 = len(odkryte_pola)
				ile_odkryto = L3 - L2
			#testy = raw_input()
			wyswietl_plansze(plansza_oryginal, rozmiar_planszy)
			print "\n"
			wyswietl_plansze(plansza_gracza, rozmiar_planszy)
		else:
			odkryte_pola.append([wiersz, kolumna])

	print "WYGRALES W MORDE JEZA!!!!"
	wyswietl_plansze(plansza_gracza, rozmiar_planszy)

def odkryj_puste_pola(plansza_gracza, plansza_oryginal, odkryte_pola):

	
	def sprawdz_nastepne_w_poziomie(plansza_gracza, plansza_oryginal, odkryte_pola, pole, wiersz, kolumna, kierunek):

		while (pole == 0 or (pole != -1 and pole != -2)):
			#print pole
			if pole != 0:
				wiersz += kierunek[0]
				kolumna += kierunek[1]
				plansza_gracza[wiersz][kolumna] = plansza_oryginal[wiersz][kolumna]
				if [wiersz, kolumna] not in odkryte_pola:
					odkryte_pola.append([wiersz, kolumna])
					break

			elif pole == 'X':
				break

			else:
				wiersz += kierunek[0]
				kolumna += kierunek[1]
				try:
					plansza_gracza[wiersz][kolumna] = plansza_oryginal[wiersz][kolumna]
					if [wiersz, kolumna] not in odkryte_pola:
						odkryte_pola.append([wiersz, kolumna])
						pole = szukaj(plansza_oryginal, wiersz+kierunek[0], kolumna+kierunek[1])
				except IndexError:
					break

		return plansza_gracza, odkryte_pola

	def sprawdz_nastepne_w_pionie(plansza_gracza, plansza_oryginal, odkryte_pola, pole, wiersz, kolumna, kierunek):
    
		while pole == 0:

			wiersz += kierunek[0]
			kolumna += kierunek[1]
			plansza_gracza[wiersz][kolumna] = plansza_oryginal[wiersz][kolumna]
			if [wiersz, kolumna] not in odkryte_pola:
				odkryte_pola.append([wiersz, kolumna])

			##w lewo
			pole_lewo = szukaj(plansza_oryginal, wiersz+W[0], kolumna+W[1])
			plansza_gracza, odkryte_pola = sprawdz_nastepne_w_poziomie(plansza_gracza, plansza_oryginal, odkryte_pola, pole_lewo, wiersz, kolumna, W)

			##w prawo
			pole_prawo = szukaj(plansza_oryginal, wiersz+E[0], kolumna+E[1])
			plansza_gracza, odkryte_pola = sprawdz_nastepne_w_poziomie(plansza_gracza, plansza_oryginal, odkryte_pola, pole_prawo, wiersz, kolumna, E)

	            
			pole = szukaj(plansza_oryginal, wiersz+kierunek[0], kolumna+kierunek[1])

		return plansza_gracza, odkryte_pola

	wiersz = odkryte_pola[-1][0]
	kolumna = odkryte_pola[-1][1]
	szukaj = szukaj_miny
	

	###sprawdz biezacy wiersz w lewo
	pole_lewo = szukaj(plansza_oryginal, wiersz+W[0], kolumna+W[1])
	plansza_gracza, odkryte_pola = sprawdz_nastepne_w_poziomie(plansza_gracza, plansza_oryginal, odkryte_pola, pole_lewo, wiersz, kolumna, W)

	###sprawdz biezacy wiersz w prawo
	pole_prawo = szukaj(plansza_oryginal, wiersz+E[0], kolumna+E[1])
	plansza_gracza, odkryte_pola = sprawdz_nastepne_w_poziomie(plansza_gracza, plansza_oryginal, odkryte_pola, pole_prawo, wiersz, kolumna, E)


	###sprawdzaj wiersze w gore
	pole_gora = szukaj(plansza_oryginal, wiersz+N[0], kolumna+N[1])
	plansza_gracza, odkryte_pola = sprawdz_nastepne_w_pionie(plansza_gracza, plansza_oryginal, odkryte_pola, pole_gora, wiersz, kolumna, N)

	###sprawdzaj wiersze w dol
	pole_dol = szukaj(plansza_oryginal, wiersz+S[0], kolumna+S[1])
	plansza_gracza, odkryte_pola = sprawdz_nastepne_w_pionie(plansza_gracza, plansza_oryginal, odkryte_pola, pole_dol, wiersz, kolumna, S)

	return plansza_gracza, odkryte_pola

def odkryj_puste_pola_2(plansza_gracza, plansza_oryginal, odkryte_pola, ile_nowych):

	def sprawdzaj_gora_dol(plansza_gracza, plansza_oryginal,odkryte_pola, biezacy_rzad, koordy):

		szukaj = szukaj_miny
		for pole in biezacy_rzad:
			wiersz = pole[0]
			kolumna = pole[1]
			sprawdzane_pola = dict()

			if plansza_oryginal[wiersz][kolumna] == 0:
				sprawdzane_pola['0'] = []
				sprawdzane_pola['0'].append(szukaj(plansza_oryginal, wiersz+koordy[0][0], kolumna+koordy[0][1]))
				sprawdzane_pola['0'].append([wiersz+koordy[0][0], kolumna+koordy[0][1]])

				sprawdzane_pola['1'] = []
				sprawdzane_pola['1'].append(szukaj(plansza_oryginal, wiersz+koordy[1][0], kolumna+koordy[1][1]))
				sprawdzane_pola['1'].append([wiersz+koordy[1][0], kolumna+koordy[1][1]])

				sprawdzane_pola['2'] = []
				sprawdzane_pola['2'].append(szukaj(plansza_oryginal, wiersz+koordy[2][0], kolumna+koordy[2][1]))
				sprawdzane_pola['2'].append([wiersz+koordy[2][0], kolumna+koordy[2][1]])

				sprawdzane_pola['3'] = []
				sprawdzane_pola['3'].append(szukaj(plansza_oryginal, wiersz+koordy[3][0], kolumna+koordy[3][1]))
				sprawdzane_pola['3'].append([wiersz+koordy[3][0], kolumna+koordy[3][1]])

				sprawdzane_pola['4'] = []
				sprawdzane_pola['4'].append(szukaj(plansza_oryginal, wiersz+koordy[4][0], kolumna+koordy[4][1]))
				sprawdzane_pola['4'].append([wiersz+koordy[4][0], kolumna+koordy[4][1]])

				sprawdzane_pola['5'] = []
				sprawdzane_pola['5'].append(szukaj(plansza_oryginal, wiersz+koordy[5][0], kolumna+koordy[5][1]))
				sprawdzane_pola['5'].append([wiersz+koordy[5][0], kolumna+koordy[5][1]])

				sprawdzane_pola['6'] = []
				sprawdzane_pola['6'].append(szukaj(plansza_oryginal, wiersz+koordy[6][0], kolumna+koordy[6][1]))
				sprawdzane_pola['6'].append([wiersz+koordy[6][0], kolumna+koordy[6][1]])

				sprawdzane_pola['7'] = []
				sprawdzane_pola['7'].append(szukaj(plansza_oryginal, wiersz+koordy[7][0], kolumna+koordy[7][1]))
				sprawdzane_pola['7'].append([wiersz+koordy[7][0], kolumna+koordy[7][1]])

			for key in sprawdzane_pola:

				if (sprawdzane_pola[key][0] != -1 and sprawdzane_pola[key][0] != -2 and sprawdzane_pola[key][1] not in odkryte_pola):
					
					if sprawdzane_pola[key][0] == 0:
						odkryte_pola.append(sprawdzane_pola[key][1])
						plansza_gracza[sprawdzane_pola[key][1][0]][sprawdzane_pola[key][1][1]] = plansza_oryginal[sprawdzane_pola[key][1][0]][sprawdzane_pola[key][1][1]]
						plansza_gracza, odkryte_pola = odkryj_puste_pola(plansza_gracza, plansza_oryginal, odkryte_pola)

					else:
						odkryte_pola.append(sprawdzane_pola[key][1])
						plansza_gracza[sprawdzane_pola[key][1][0]][sprawdzane_pola[key][1][1]] = plansza_oryginal[sprawdzane_pola[key][1][0]][sprawdzane_pola[key][1][1]]


		return plansza_gracza, odkryte_pola

	odkryte_pola_temp = []
	for i in range(1, ile_nowych+2):
		odkryte_pola_temp.append(odkryte_pola[-i])

	odkryte_pola_temp = sorted(odkryte_pola_temp)
	najwyzszy_rzad = odkryte_pola_temp[1][0]
	najnizszy_rzad = odkryte_pola_temp[-1][0]
	najwyzszy_rzad_pola = []
	najnizszy_rzad_pola = []

	for pole in odkryte_pola_temp:
		if najwyzszy_rzad == najnizszy_rzad:
			if pole[0] == najwyzszy_rzad:
				najwyzszy_rzad_pola.append(pole)
				najnizszy_rzad_pola.append(pole)

		else:
			if pole[0] == najwyzszy_rzad:
				najwyzszy_rzad_pola.append(pole)
			elif pole[0] == najnizszy_rzad:
				najnizszy_rzad_pola.append(pole)
	
	####################SZUKAJ W GORE
	plansza_gracza, odkryte_pola = sprawdzaj_gora_dol(plansza_gracza, plansza_oryginal, odkryte_pola, najwyzszy_rzad_pola, koordy)
	#################SZUKAJ W DOL
	plansza_gracza, odkryte_pola = sprawdzaj_gora_dol(plansza_gracza, plansza_oryginal, odkryte_pola, najnizszy_rzad_pola, koordy)
	
	#test = raw_input(">")
	return plansza_gracza, odkryte_pola




