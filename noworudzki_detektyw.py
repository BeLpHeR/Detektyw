import time, random, sys

# Deklaracja stałych:
PODEJRZANI = [
    'SPRZEDAWCA CIASTEK',
    'NOWORUDZKI PATRIOTA',
    'URZĘDNIK GMINNY',
    'RADNY MIEJSKI',
    'PISARZ',
    'DENTYSTA',
    'REDAKTOR GAZETY',
    'BARMANKA',
    'NAUCZYCIELKA']
PRZEDMIOTY = [
    'LATARKA', 
    'ROLKA PAPIERU TOALETOWEGO', 
    'ŚRUBOKRĘT', 
    'WIERTARKA', 
    'PENDRIVE', 
    'SŁOIK OGÓRKÓW', 
    'TOREBKA LOUIS VUTTON', 
    'MIKROSKOP', 
    'KARTA PODARUNKOWA']
MIEJSCA = [
    'ZAUŁEK', 
    'SPALONY SZPITAL', 
    'ROSSMANN', 
    'URZĄD MIASTA', 
    'BIAŁA LOKOMOTYWA', 
    'NOWAR', 
    'LICEUM', 
    'DINO', 
    'POCZTA GŁÓWNA']
CZAS_GRY = 600  # 600 sekund (10 minut) na rozwiązanie zagadki.

# Pierwsze litery i najdłuższa nazwa miejsca są potrzebne do wyświetlania menu:
PIERWSZE_LITERY_MIEJSC = {}
NAJDLUZSZA_NAZWA = 0
for miejsce in MIEJSCA:
    PIERWSZE_LITERY_MIEJSC[miejsce[0]] = miejsce
    if len(miejsce) > NAJDLUZSZA_NAZWA:
        NAJDLUZSZA_NAZWA = len(miejsce)

# Podstawowe sprawdzenie, czy jest tyle samo miejsc, podejrzanych i przedmiotów:
assert len(PODEJRZANI) == 9
assert len(PRZEDMIOTY) == 9
assert len(MIEJSCA) == 9
# Pierwsze litery muszą być unikatowe:
assert len(PIERWSZE_LITERY_MIEJSC.keys()) == len(MIEJSCA)


znaniPodejrzaniIMiejsca = []
# Słownik odwiedzonych miejsc (visitedPlaces), gdzie kluczami są miejsca, a  wartościami podejrzani i przedmioty, które tam się znajdują.
odwiedzoneMiejsca = {}
aktualneMiejsce = 'TAXI'  # Rozpocznij grę na postoju taksówek.
obrazeniPodejrzai = []  # Oskarżeni podejrzani nie będą dawać wskazówek.
klamcy = random.sample(PODEJRZANI, random.randint(3, 4))
doOskarzenia = 3  # Możesz oskarżyć maksymalnie 3 osoby.
sprawca = random.choice(PODEJRZANI)

# Te same indeksy łączą podejrzanego, przedmiot i miejsce.
random.shuffle(PODEJRZANI)
random.shuffle(PRZEDMIOTY)
random.shuffle(MIEJSCA)

# Utwórz strukturę danych dla wskazówek o przedmiocie i podejrzanym,
# podanych przez osoby prawdomówne.
# Słownik ze wskazówkami (clues), gdzie klucze to podejrzani proszeni o wskazówkę, a wartościami słownik z daną wskazówką.
wskazowki = {}
for i, przesluchiwany in enumerate(PODEJRZANI):
    if przesluchiwany in klamcy:
        continue  # Na tym etapie pomiń kłamców.

    # Kluczami słownika wskazówek są przedmioty i podejrzani,
    # a wartością jest podana wskazówka.
    wskazowki[przesluchiwany] = {}
    wskazowki[przesluchiwany]['debug_liar'] = False  # Przydatne podczas rozwiązywania problemów.
    for obiekt in PRZEDMIOTY:  # Wybierz wskazówkę o każdym przedmiocie.
        if random.randint(0, 1) == 0:  # Powiedz, gdzie jest dany przedmiot:
            wskazowki[przesluchiwany][obiekt] = MIEJSCA[PRZEDMIOTY.index(obiekt)]
        else:  # Powiedz, kto ma dany przedmiot:
            wskazowki[przesluchiwany][obiekt] = PODEJRZANI[PRZEDMIOTY.index(obiekt)]
    for podejrzany in PODEJRZANI:  # Wybierz wskazówkę o każdym podejrzanym.
        if random.randint(0, 1) == 0:  # Powiedz, gdzie jest podejrzany:
            wskazowki[przesluchiwany][podejrzany] = MIEJSCA[PODEJRZANI.index(podejrzany)]
        else:  # Powiedz, jaki przedmiot ma dany podejrzany:
            wskazowki[przesluchiwany][podejrzany] = PRZEDMIOTY[PODEJRZANI.index(podejrzany)]

# Utwórz strukturę danych dla wskazówek podanych przez kłamców
# na temat każdego przedmiotu i podejrzanego:
for i, przesluchiwany in enumerate(PODEJRZANI):
    if przesluchiwany not in klamcy:
        continue  # Już mamy obsługę osób prawdomównych.

    # Kluczami słownika wskazówek są przedmioty i podejrzani,
    # a wartością jest podana wskazówka.
    wskazowki[przesluchiwany] = {}
    wskazowki[przesluchiwany]['debug_liar'] = True  # Przydatne podczas rozwiązywania problemów.

    # Ten podejrzany jest kłamcą i podaje błędne wskazówki:
    for obiekt in PRZEDMIOTY:
        if random.randint(0, 1) == 0:
            while True:  # Wybierz losowe (błędne) miejsce związane ze wskazówką.
                # Kłamie na temat miejsca przedmiotu.
                wskazowki[przesluchiwany][obiekt] = random.choice(MIEJSCA)
                if wskazowki[przesluchiwany][obiekt] != MIEJSCA[PRZEDMIOTY.index(obiekt)]:
                    # Wyjdź z pętli po wybraniu błędnej wskazówki.
                    break
        else:
            while True:  # Wybierz losowego (błędnego) podejrzanego związanego ze wskazówką.
                wskazowki[przesluchiwany][obiekt] = random.choice(PODEJRZANI)
                if wskazowki[przesluchiwany][obiekt] != PODEJRZANI[PRZEDMIOTY.index(obiekt)]:
                    # Wyjdź z pętli po wybraniu błędnej wskazówki.
                    break
    for podejrzany in PODEJRZANI:
        if random.randint(0, 1) == 0:
            while True:  # Wybierz losowe (błędne) miejsce związane ze wskazówką.
                wskazowki[przesluchiwany][podejrzany] = random.choice(MIEJSCA)
                if wskazowki[przesluchiwany][podejrzany] != MIEJSCA[PRZEDMIOTY.index(obiekt)]:
                    # Wyjdź z pętli po wybraniu błędnej wskazówki.
                    break
        else:
            while True:  # Wybierz losowy (błędny) przedmiot związany ze wskazówką.
                wskazowki[przesluchiwany][podejrzany] = random.choice(PRZEDMIOTY)
                if wskazowki[przesluchiwany][podejrzany] != PRZEDMIOTY[PODEJRZANI.index(podejrzany)]:
                    # Wyjdź z pętli po wybraniu błędnej wskazówki.
                    break

# Utwórz strukturę danych dla wskazówek otrzymanych po zapytaniu o kota Mruczekek:
kocieWskazowki = {}
for przesluchiwany in random.sample(PODEJRZANI, random.randint(3, 4)):
    rodzajWskazowki = random.randint(1, 3)
    if rodzajWskazowki == 1:
        if przesluchiwany not in klamcy:
            # Oni Ci powiedzą, gdzie jest Mruczek
            kocieWskazowki[przesluchiwany] = sprawca
        elif przesluchiwany in klamcy:
            while True:
                # Wybierz błędną wskazówkę podejrzanego.
                kocieWskazowki[przesluchiwany] = random.choice(PODEJRZANI)
                if kocieWskazowki[przesluchiwany] != sprawca:
                    # Wyjdź z pętli po wybraniu błędnej wskazówki.
                    break

    elif rodzajWskazowki == 2:
        if przesluchiwany not in klamcy:
            # Oni Ci powiedzą, gdzie jest Mruczek
            kocieWskazowki[przesluchiwany] = MIEJSCA[PODEJRZANI.index(sprawca)]
        elif przesluchiwany in klamcy:
            while True:
                # Wybierz błędną wskazówkę na temat miejsca.
                kocieWskazowki[przesluchiwany] = random.choice(MIEJSCA)
                if kocieWskazowki[przesluchiwany] != MIEJSCA[PODEJRZANI.index(sprawca)]:
                    # Wyjdź z pętli po wybraniu błędnej wskazówki.
                    break
    elif rodzajWskazowki == 3:
        if przesluchiwany not in klamcy:
            # Oni Ci powiedzą, jaki przedmiot znajduje się blisko Mruczek
            kocieWskazowki[przesluchiwany] = PRZEDMIOTY[PODEJRZANI.index(sprawca)]
        elif przesluchiwany in klamcy:
            while True:
                # Wybierz błędną wskazówkę na temat przedmiotu.
                kocieWskazowki[przesluchiwany] = random.choice(PRZEDMIOTY)
                if kocieWskazowki[przesluchiwany] != PRZEDMIOTY[PODEJRZANI.index(sprawca)]:
                    # Wyjdź z pętli, gdy zostanie wybrana błędna wskazówka.
                    break

# EKSPERYMENT: Usuń znaczniki komentarz z przed tego bloku kodu, by zobaczyć strukturę danych dla wskazówek:
#import pprint
#pprint.pprint(clues)
#pprint.pprint(MruczekekClues)
#print('culprit =', culprit)

# POCZĄTEK GRY
print("""OSKARŻAM! (gra detektywistyczna)")
Program zainspirowany grą Where's the EGG?

Jesteś światowej sławy detektywem, Henrykiem Wścibskim. 
Zaginął kot Mruczek, a Ty musisz dokładnie zbadać wszystkie wskazówki.
Podejrzani albo zawsze kłamią, albo zawsze mówią prawdę. Zadawaj im pytania
o innych ludzi, miejsca i przedmioty, by określić, czy szczegóły
przez nich podawane są godne zaufania i zgodne z Twoimi obserwacjami.
Dzięki temu będziesz wiedzieć, czy ich wskazówka o kocie Mruczek jest prawdziwa, czy nie. 
Czy znajdziesz kota Mruczek na czas i oskarżysz winnego?
""")
input('Naciśnij Enter, aby rozpocząć...')


CzasPoczatkowy = time.time()
CzasKoncowy = CzasPoczatkowy + CZAS_GRY

while True:  # Główna pętla gry.
    if time.time() > CzasKoncowy or doOskarzenia == 0:
        # Obsługa warunku końca gry:
        if time.time() > CzasKoncowy:
            print('Skończył Ci się czas!')
        elif doOskarzenia == 0:
            print('Oskarżyłeś zbyt wielu niewinnych ludzi!')
        IndeksOskarzonych = PODEJRZANI.index(sprawca)
        print('Kota porwał {} w miejscu: {} z: {}!'.format(sprawca, MIEJSCA[IndeksOskarzonych], PRZEDMIOTY[IndeksOskarzonych]))
        print('Może następnym razem będziesz miał więcej szczęścia, Detektywie.')
        sys.exit()

    print()
    ileMinut = int(CzasKoncowy - time.time()) // 60
    ileSekund = int(CzasKoncowy - time.time()) % 60
    print('Pozostało: {} min, {} sek.'.format(ileMinut, ileSekund))

    if aktualneMiejsce == 'TAXI':
        print('  Jesteś w swojej TAXI. Dokąd chcesz jechać?')
        for miejsce in sorted(MIEJSCA):
            InfoOMiejscu = ''
            if miejsce in odwiedzoneMiejsca:
                InfoOMiejscu = odwiedzoneMiejsca[miejsce]
            nameLabel = '(' + miejsce[0] + ')' + miejsce[1:]
            spacing = " " * (NAJDLUZSZA_NAZWA - len(miejsce))
            print('{} {}{}'.format(nameLabel, spacing, InfoOMiejscu))
        print('(K)ONIEC GRY')
        while True:  # Pytaj, dopóki nie zostanie podana odpowiednia odpowiedź.
            odpowiedz = input('> ').upper()
            if odpowiedz == '':
                continue  # Zapytaj ponownie.
            if odpowiedz == 'K':
                print('Dziękujemy za grę!')
                sys.exit()
            if odpowiedz in PIERWSZE_LITERY_MIEJSC.keys():
                break
        aktualneMiejsce = PIERWSZE_LITERY_MIEJSC[odpowiedz]
        continue  # Wróć do początku głównej pętli gry.

    # Będąc na miejscu, gracz może pytać o wskazówki.
    print('  Jesteś w miejscu o nazwie: {}.'.format(aktualneMiejsce))
    numerAktualnegoMiejsca = MIEJSCA.index(aktualneMiejsce)
    osobyTutaj = PODEJRZANI[numerAktualnegoMiejsca]
    rzeczyTutaj = PRZEDMIOTY[numerAktualnegoMiejsca]
    print('  Jest tutaj {} i ma obok siebie: {}.'.format(osobyTutaj, rzeczyTutaj))

    # Dodaj podejrzanego i przedmiot znajdujących się w tym miejscu do naszej listy
    # znanych nam już podejrzanych i przedmiotów:
    if osobyTutaj not in znaniPodejrzaniIMiejsca:
        znaniPodejrzaniIMiejsca.append(osobyTutaj)
    if PRZEDMIOTY[numerAktualnegoMiejsca] not in znaniPodejrzaniIMiejsca:
        znaniPodejrzaniIMiejsca.append(PRZEDMIOTY[numerAktualnegoMiejsca])
    if aktualneMiejsce not in odwiedzoneMiejsca.keys():
        odwiedzoneMiejsca[aktualneMiejsce] = '({}, {})'.format(osobyTutaj.lower(), rzeczyTutaj.lower())

    # Jeśli gracz wcześniej niesłusznie oskarżył tę osobę,
    # to nie otrzyma od niej wskazówki:
    if osobyTutaj in obrazeniPodejrzai:
        print('Są obrażeni, że ich oskarżyłeś,')
        print('dlatego nie pomogą Ci w Twoim śledztwie.')
        print('Wracasz do swojej TAXI.')
        print()
        input('Naciśnij Enter, aby kontynuować...')
        aktualneMiejsce = 'TAXI'
        continue  # Wróć do początku głównej pętli gry.

    # Wyświetl menu z podejrzanymi i przedmiotami, o które gracz może spytać:
    print()
    print('(O) "OSKARŻAM!" (Pozostało {} oskarżeń)'.format(doOskarzenia))
    print('(Z) Zapytaj, czy wiedzą, gdzie jest kot Mruczek.')
    print('(T) Wróć do TAXI.')
    for i, suspectOrItem in enumerate(znaniPodejrzaniIMiejsca):
        print('({}) Zapytaj o: {}'.format(i + 1, suspectOrItem))

    while True:  # Pytaj, dopóki nie zostanie podana odpowiednia odpowiedź.
        odpowiedz = input('> ').upper()
        if odpowiedz in 'OZT' or (odpowiedz.isdecimal() and 0 < int(odpowiedz) <= len(znaniPodejrzaniIMiejsca)):
            break

    if odpowiedz == 'O':  # Gracz oskarża tego podejrzanego.
        doOskarzenia -= 1  # Zużył jedno oskarżenie.
        if osobyTutaj == sprawca:
            # Gracz słusznie oskarżył podejrzanego.
            print('Rozwiązałeś sprawę, Detektywie!')
            print('Kota Mruczek porwał(a) {}.'.format(sprawca))
            minutesTaken = int(time.time() - CzasPoczatkowy) // 60
            secondsTaken = int(time.time() - CzasPoczatkowy) % 60
            print('Dobra robota! Rozwiązałeś sprawę w {} min, {} sek.'.format(minutesTaken, secondsTaken))
            sys.exit()
        else:
            # Gracz niesłusznie oskarżył daną osobę.
            obrazeniPodejrzai.append(osobyTutaj)
            print('Oskarżyłeś niewinną osobę, Detektywie!')
            print('Nie otrzymasz od niej już żadnych wskazówek.')
            print('Wracasz do swojej TAXI.')
            aktualneMiejsce = 'TAXI'

    elif odpowiedz == 'Z':  # Gracz pyta o Mruczek.
        if osobyTutaj not in kocieWskazowki:
            print('"Nic nie wiem o kocie Mruczek."')
        elif osobyTutaj in kocieWskazowki:
            print('  Podejrzany daje Ci taką wskazówkę: "{}"'.format(kocieWskazowki[osobyTutaj]))
            # Dodaj wskazówkę niezwiązaną z miejscem do listy znanych rzeczy:
            if kocieWskazowki[osobyTutaj] not in znaniPodejrzaniIMiejsca and kocieWskazowki[osobyTutaj] not in MIEJSCA:
                znaniPodejrzaniIMiejsca.append(kocieWskazowki[osobyTutaj])

    elif odpowiedz == 'T':  # Gracz wraca do taksówki.
        aktualneMiejsce = 'TAXI'
        continue  # Wróć do początku głównej pętli gry.

    else:  # Gracz pyta o podejrzanego lub przedmiot.
        rzeczOKtoraPytasz = znaniPodejrzaniIMiejsca[int(odpowiedz) - 1]
        if rzeczOKtoraPytasz in (osobyTutaj, rzeczyTutaj):
            print('  Zapytana osoba nie będzie tego komentować.')
        else:
            print('  Otrzymujesz następującą wskazówkę: "{}"'.format(wskazowki[osobyTutaj][rzeczOKtoraPytasz]))
            # Dodaj wskazówkę niezwiązaną z miejscem do listy znanych rzeczy:
            if wskazowki[osobyTutaj][rzeczOKtoraPytasz] not in znaniPodejrzaniIMiejsca and wskazowki[osobyTutaj][rzeczOKtoraPytasz] not in MIEJSCA:
                znaniPodejrzaniIMiejsca.append(wskazowki[osobyTutaj][rzeczOKtoraPytasz])

    input('Naciśnij Enter, by kontynuować...')
