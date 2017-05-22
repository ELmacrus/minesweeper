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

koordy = [NW, N, NE, E, SE, S, SW, W] #wykorzystywane do sprawdzania 8 sasiadow danego pola

#### funkcja tworzy plansze z wybranym polem
def stworz_plansze(rozmiar_planszy, pole):

    plansza_gry = []
    for i in range(rozmiar_planszy):
        wiersz_planszy = []
        for j in range(rozmiar_planszy):
            wiersz_planszy.append(pole)
        plansza_gry.append(wiersz_planszy)

    return plansza_gry

#funkcja losuje miny na planszy
def wylosuj_miny(plansza_gry, rozmiar_planszy, ile_min):

	pole_z_mina = sample(range(rozmiar_planszy*rozmiar_planszy), ile_min)
	for mina in pole_z_mina:
		wiersz = int(mina/rozmiar_planszy)
		kolumna = mina%rozmiar_planszy
		plansza_gry[wiersz][kolumna] = 'X'
	
	return plansza_gry

#funkcja liczy miny w sasiedztwie pola zeby powstaly pola z numerkiem
def policz_miny(plansza_gry, rozmiar_planszy):

	for wiersz in range(rozmiar_planszy):
		for kolumna in range(rozmiar_planszy):
			miny = []
			if plansza_gry[wiersz][kolumna] == 0:	
				for koord in koordy:
					nowy_wiersz = wiersz+koord[0]
					nowa_kolumna = kolumna+koord[1]
					if (nowy_wiersz > -1) and (nowa_kolumna > -1):
						try:
							miny.append(plansza_gry[wiersz+koord[0]][kolumna+koord[1]])
						except IndexError:
							pass			
				plansza_gry[wiersz][kolumna] = miny.count('X')

	return plansza_gry

#3 powyzsze kroki w jednej funkcji
def przygotuj_plansze(rozmiar_planszy, ile_min):
	
	plansza = stworz_plansze(rozmiar_planszy, 0)
	plansza = wylosuj_miny(plansza, rozmiar_planszy, ile_min)
	plansza = policz_miny(plansza, rozmiar_planszy)
	return plansza

#funkcja wyswietla plansze
def wyswietl_plansze(plansza_gry, rozmiar_planszy):
	
	for wiersz in range(rozmiar_planszy):
		linia = " "
		linia2 = ""
		for kolumna in range(rozmiar_planszy):
			linia += str(plansza_gry[wiersz][kolumna]) + " | "
			linia2 += "----"
		print linia
		print linia2

###czy tego nie wyjebac zastanowie sie####################
def szukaj_miny(plansza_gry, wiersz, kolumna):
	
	if wiersz <0 or kolumna <0:
		return -1
	else:	
		try:
			pole = plansza_gry[wiersz][kolumna]
			return pole
		except IndexError:
			return -2

###funkcja wrzuca wszystkie sasiadujace zera do jednej grupy
def pogrupuj_puste_pola(plansza_oryginal, rozmiar_planszy):

	zgrupowane_zera = [[[-1,-1]]] #losowa wartosc zeby zadzialala petla for grupa in zgrupowane_zera
	for wiersz in range(rozmiar_planszy):
		for kolumna in range(rozmiar_planszy):
			juz_jest = False
			if plansza_oryginal[wiersz][kolumna] == 0:

				for grupa in zgrupowane_zera:			
					if [wiersz, kolumna] in grupa:
						juz_jest = True

				if juz_jest == False:
					grupa_zer = []
					grupa_zer.append([wiersz, kolumna])
					####sprawdzamy 8 sasiadow
					grupa_zer = sprawdzaj_8(plansza_oryginal, grupa_zer, koordy, wiersz, kolumna)				
					zgrupowane_zera.append(grupa_zer)

	zgrupowane_zera[0].pop() ##wyrzucamy [-1 -1]

	#konwersja na numery pol zeby zrobic sety z [4, 6] na 46
	for grupa_zer in zgrupowane_zera:
		for i in range(len(grupa_zer)):
			wiersz = grupa_zer[i][0]
			kolumna = grupa_zer[i][1]
			grupa_zer[i] = (wiersz*rozmiar_planszy) + kolumna

	#tworzymy sety grup z zerami
	zgrupowane_zera_sety = [] ###lista w ktorej sa wszystkie sety(grupy)
	for grupa_zer in zgrupowane_zera:
		grupa_zer_set = set()
		for pole_z_zerem in grupa_zer:
			grupa_zer_set.add(pole_z_zerem)

		zgrupowane_zera_sety.append(grupa_zer_set)

	#sprawdzamy czy grupy pokrywaja sie ze soba, jeesli tak tworzy wieksza grupe
	L = len(zgrupowane_zera_sety)
	ile = L
	while(ile>0):
		for i in range(L):
			for j in range(i+1, L):
				wspolne_pola = zgrupowane_zera_sety[i].intersection(zgrupowane_zera_sety[j])
				if len(wspolne_pola) > 0:
					zgrupowane_zera_sety[i] = zgrupowane_zera_sety[i].union(zgrupowane_zera_sety[j])
		ile -= 1
	#zostawiamy tylko pelne grupy
	for i in range(L):
		for j in range(i+1, L):
			if zgrupowane_zera_sety[i].issuperset(zgrupowane_zera_sety[j]) == True:
				zgrupowane_zera_sety[j].clear()

	#do kazdej grupy z zerem dorzucamy jej niezerowe sasiedztwo ktore tez powinno sie wyswietlic
	grupy_zer = odkryj_sasiedztwo_zer(plansza_oryginal, zgrupowane_zera_sety, rozmiar_planszy)

	return grupy_zer

#uzywane w pogrupuj puste pola
def sprawdzaj_8(plansza_oryginal, grupa_zer, koordy, wiersz, kolumna):

	for koord in koordy:					
		sprawdzane_pole = szukaj_miny(plansza_oryginal, wiersz+koord[0], kolumna+koord[1])
		if sprawdzane_pole == 0 and sprawdzane_pole not in grupa_zer:
			grupa_zer.append([wiersz+koord[0], kolumna+koord[1]])
	return grupa_zer



##uzywane w pogrupuj puste pola
def odkryj_sasiedztwo_zer(plansza_oryginal, grupy_zer_set, rozmiar_planszy):

	#zmieniamy sety na listy
	grupy_zer = []
	for secik in grupy_zer_set:
		grupy_zer.append(sorted(list(secik)))

	#przez zerowanie setow.clear w pogrupuj puste pola zostaja puste sety, trzeba sie ich pozbyc
	grupy_zer_bez_pustych = []
	for i in range(len(grupy_zer)):
		if len(grupy_zer[i])>0:
			grupy_zer_bez_pustych.append(grupy_zer[i])

	#zmieniamy notacje z 46 na [4, 6] zeby pasowalo do odkrytepola
	for i in range(len(grupy_zer_bez_pustych)):
		for j in range(len(grupy_zer_bez_pustych[i])):
			wiersz = int(grupy_zer_bez_pustych[i][j]/rozmiar_planszy)
			kolumna = grupy_zer_bez_pustych[i][j]%rozmiar_planszy
			grupy_zer_bez_pustych[i][j] = [wiersz, kolumna]

	#sprawdzamy otoczenie zer i dodajemy znalezione pola do grupy z zerami 
	grupy_zer_final = []
	for i in range(len(grupy_zer_bez_pustych)):
		grupa_zer_temp = grupy_zer_bez_pustych[i]

		for j in range(len(grupy_zer_bez_pustych[i])):
			#print len(grupa_zer)
			element = grupy_zer_bez_pustych[i][j]
			wiersz = element[0]
			kolumna = element[1]
			for koord in koordy:
				try:
					pole = plansza_oryginal[wiersz+koord[0]][kolumna+koord[1]]
				except IndexError:
					pole = -1

				nowy_wiersz = wiersz+koord[0]
				nowa_kolumna = kolumna+koord[1]
				if (nowy_wiersz>-1 and nowa_kolumna>-1):
					if pole > 0 and [nowy_wiersz, nowa_kolumna] not in grupa_zer_temp:
						grupa_zer_temp.append([nowy_wiersz, nowa_kolumna])

		grupy_zer_final.append(grupa_zer_temp)

	return grupy_zer_final


###SILNIK CALEJ GRY###	
def zrob_ruch(plansza_gracza, plansza_oryginal, odkryte_pola, rozmiar_planszy, ile_min, grupy_zer):

	while len(odkryte_pola)<=(rozmiar_planszy*rozmiar_planszy)-1-ile_min:
		
		os.system('cls')
		wyswietl_plansze(plansza_oryginal, rozmiar_planszy)
		print "\n"
		print len(odkryte_pola)
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
			print "KONIEC GRY, PRZEGRALES"
			break
		elif teraz_odkryte_pole == 0:
			###odszukaj odpowiednia grupe z tym polem
			for i in range(len(grupy_zer)):
				if [wiersz, kolumna] in grupy_zer[i]:
					trafiona_grupa = grupy_zer[i]
					for j in range(len(trafiona_grupa)):
						pole = trafiona_grupa[j]
						pole_wiersz = pole[0]
						pole_kolumna = pole[1]
						plansza_gracza[pole_wiersz][pole_kolumna] = plansza_oryginal[pole_wiersz][pole_kolumna]
						odkryte_pola.append([pole_wiersz, pole_kolumna])
					break

			wyswietl_plansze(plansza_oryginal, rozmiar_planszy)
			print "\n"
			wyswietl_plansze(plansza_gracza, rozmiar_planszy)
		else:
			odkryte_pola.append([wiersz, kolumna])

		if len(odkryte_pola)>(rozmiar_planszy*rozmiar_planszy)-1-ile_min:
			os.system('cls')
			print "WYGRALES W MORDE JEZA!!!!"
			wyswietl_plansze(plansza_oryginal, rozmiar_planszy)
			print "\n"
			wyswietl_plansze(plansza_gracza, rozmiar_planszy)

	






