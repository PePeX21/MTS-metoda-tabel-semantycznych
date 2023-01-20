"""Dane """
stale = ["a", "b", "c", "d", "e"]
zmienne = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
           "W", "X", "Y", "Z"]
funkcje = ["f", "g", "h", "i", "j", "k", "l", "m", "n"]
predykaty = ["p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "Z"]
operatory_kwantyfikatory = ["AND", "OR", "IFF", "XOR", "IMPLIES", "↓", "↑", "FORALL", "EXISTS"]
NOT = "NOT"

rules = {"AND": [["alfa", 1], ["", ""]],
         "NOT OR": [["alfa", 2], ["NOT", "NOT"]],
         "NOT IMPLIES": [["alfa", 2], ["", "NOT"]],
         "NOT ↑": [["alfa", 2], ["", ""]],
         "↓": [["alfa", 1], ["NOT", "NOT"]],
         "IFF": [["alfa", 1, "len[3] mean difference"], ["", ""]],  # TO GLOWNO JEST Z IMPLIESAMI W SRODKU
         "NOT XOR": [["alfa", 2, "len[3] mean difference"], ["", ""]],  # spojrz do tabli regolami alfa w wykladach
         # reguly alfa
         "NOT AND": [["beta", 2], ["NOT", "NOT"]],
         "OR": [["beta", 1], ["", ""]],
         "IMPLIES": [["beta", 1], ["NOT", ""]],
         "↑": [["beta", 1], ["NOT", "NOT"]],
         "NOT ↓": [["beta", 2], ["", ""]],
         "NOT IFF": [["beta", 2, "len[3] mean difference"], ["NOT", "NOT"]],  # TO GLOWNO JEST Z IMPLIESAMI W SRODKU
         "XOR": [["beta", 1, "len[3] mean difference"], ["NOT", "NOT"]],  # spojrz do tabli regolami beta w wykladach
         # reguly beta
         "FORALL": ["gamma", 1],
         "NOT EXISTS": ["gamma", 2],
         # reguly gamma
         "EXISTS": ["delta", 1],
         "NOT FORALL": ["delta", 2]}
# reguly delta

mode_0 = ["X Y Z p/3",
          "Z g/1  Z Z p/1 Z d q/2 r/2 FORALL OR NOT NOT NOT",
          "Z Z q/1 Z p/1 Z p/1 a q/1 b q/1 c p/1 d q/1 e r/1 AND AND AND AND NOT OR OR OR FORALL",
          "a q/1 b q/1 IFF NOT",
          "Z Z p/1 a q/1 AND FORALL",
          "Z Y Z p/1 Y q/1 EXISTS FORALL",
          "a p/1",
          "Z Z p/1 Z p/1 NOT AND FORALL"]

""" funkcje przygotowujace do MTS """


def MODE(mode_0):
    global tmp, mode

    if mode == "0":
        if tmp == len(mode_0):

            mode = input("czy chcesz wpisac wlasna formule ? wpisz: 1 \nzeby zakonczyc wpisz: 0\n")
            if mode == "0":
                return "0"
            else:
                mode = "1"
                return predicates_changing(replace(input()).split())
        else:
            tmp = tmp + 1
            print(mode_0[tmp - 1])
            return predicates_changing(replace(mode_0[tmp - 1]).split())

    else:
        return predicates_changing(replace(input()).split())


def replace(line):
    line = line.replace("&", "AND")
    line = line.replace("∧", "AND")
    line = line.replace("V", "OR")
    line = line.replace("|", "OR")
    line = line.replace("↔", "IFF")
    line = line.replace("⊕", "XOR")
    line = line.replace("→", "IMPLIES")

    line = line.replace("~", "NOT")
    line = line.replace("¬", "NOT")

    line = line.replace("∀", "FORALL")
    line = line.replace("∃", "EXISTS")

    return line


def predicates_changing(line):  # kod z twojego ONP, u mnie np: z Z p/1 robi p/Z,    z a b c q/2 robi q/abc

    stos = []
    lista_zmiennych = []
    for i in line:
        if (i[0] in funkcje or i[0] in predykaty) and (len(i) == 3):
            for l in range(int(i[2])):
                lista_zmiennych = lista_zmiennych + [stos.pop()]
            lista_zmiennych.reverse()
            funkcja = i[0:2]
            for zmienna in lista_zmiennych:
                funkcja = funkcja + zmienna
            stos.append(funkcja)
            funkcja = ""
            lista_zmiennych = []
        else:
            stos.append(i)
    return stos


""" funkcje MTS """


class Leaf:
    def __init__(self, gamma, lines, field):
        self.gamma = gamma
        self.lines = lines
        self.field = field

    def alfa_beta_role(self, value, line):
        print("Klucz:", value)  ################################################################################

        for i in range(value[0][1]):
            self.lines[line].pop()

        cut = 1
        index = 1
        while (True):
            if self.lines[line][-index][1] == "/":  # oznacza to ze trafilismy na predykat, ma on postac p"/"Z:
                break
            elif self.lines[line][-index] == NOT:
                cut = cut + 1
            elif self.lines[line][-index] in operatory_kwantyfikatory:
                cut = cut + 2
            index = index + 1

        line_1 = self.lines[line][:-cut]
        line_2 = self.lines[line][-cut:]

        if len(value[0]) == 3:  # zobacz komentarz w "dane" przy slownikow regol
            tmp_1 = line_1 + line_2 + ["IMPLIES"]
            tmp_2 = line_2 + line_1 + ["IMPLIES"]

            line_1 = tmp_1
            line_2 = tmp_2

        del self.lines[line]
        cut = 1

        if bool(value[1][0]):
            line_1.append(value[1][0])
        if bool(value[1][1]):
            line_2.append(value[1][1])

        print("linie po podziale", value[0][0], line_1,
              line_2)  ################################################################

        return line_1, line_2

    def gamma_delta_role(self, value, line):
        print("Klucz", value)  ########################################################

        if value[0] == "gamma":

            if value[1] != 0:  # value[1] == 0 gdy sztucznie wywoluje sie gamme pod koniec obliczen --> MTS pierwszy if
                self.lines[line].pop(-value[1])
                self.gamma.append(self.lines[line])  # xX!! mechhh !!Xx#

            for stala in self.fields[0]:  # moga powtarzac sie zmienne ktore podstawiam
                if value[1] == 0:  # ale moga tak jak w algorytmie:
                    tmp = " ".join(self.gamma[line])  # W książce ”Logika matematyczna w informatyce” M. Ben-Ari’ego
                else:  # wiem, brzmi madrze (tytul skopiowany z cwiczen lukasiewicza)
                    tmp = " ".join(self.lines[line])  # generalnie chodzi o to ze nie ma wplywa to na spelnialnosc
                tmp = tmp.replace(tmp[0], stala)
                tmp = tmp.split()
                tmp.pop(0)
                self.lines.append(tmp)

            if value[1] != 0:
                del self.lines[line]
                # slozy to rozpoznaniu przy kolejnym wywolaniu gamma
            self.fields[1] = self.fields[0].copy()  # czy zmienne byly juz wywolywane czy nie

        else:  # else czyli delta
            self.lines[line].pop(-value[1])

            new_stala = (list(filter(lambda x: x not in self.fields[0], stale)))
            if new_stala:
                new_stala = new_stala[0]
            else:
                new_stala = "a"  # zabezpieczenie przed skonczeniem sie stalych
            if new_stala not in self.fields[0]:  # zabezpieczenie przed nieskonczonym roznieniem sie
                self.fields[0].append(new_stala)  # leaf.fields[0] od leaf.fields[1]

            tmp = " ".join(self.lines[line])
            tmp = tmp.replace(tmp[0], new_stala)
            tmp = tmp.split()
            tmp.pop(0)
            self.lines[line] = tmp

    def leaf_checking(self):

        denied_predicate = []
        predicate = []
        for line in self.lines:
            if NOT in line:  # dziele na predykaty zaprzeczone i nie zaprzeczone
                denied_predicate = denied_predicate + line
            else:
                predicate = predicate + line

        denied_predicate = " ".join(denied_predicate)
        denied_predicate = denied_predicate.replace("NOT", "")
        denied_predicate = denied_predicate.split()

        #if not list(filter(lambda x: x in predicate, denied_predicate)):  # sprawdzam czy powtarzaja sie elementy


#Dane
stale = ["a", "b", "c", "d", "e"]
zmienne = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
           "W", "X", "Y", "Z"]
funkcje = ["f", "g", "h", "i", "j", "k", "l", "m", "n"]
predykaty = ["p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "Z"]
operatory_kwantyfikatory = ["AND", "OR", "IFF", "XOR", "IMPLIES", "↓", "↑", "FORALL", "EXISTS"]
NOT = "NOT"

rules = {"AND": [["alfa", 1], ["", ""]],
         "NOT OR": [["alfa", 2], ["NOT", "NOT"]],
         "NOT IMPLIES": [["alfa", 2], ["", "NOT"]],
         "NOT ↑": [["alfa", 2], ["", ""]],
         "↓": [["alfa", 1], ["NOT", "NOT"]],
         "IFF": [["alfa", 1, "len[3] mean difference"], ["", ""]],
         "NOT XOR": [["alfa", 2, "len[3] mean difference"], ["", ""]],
         # reguly alfa
         "NOT AND": [["beta", 2], ["NOT", "NOT"]],
         "OR": [["beta", 1], ["", ""]],
         "IMPLIES": [["beta", 1], ["NOT", ""]],
         "↑": [["beta", 1], ["NOT", "NOT"]],
         "NOT ↓": [["beta", 2], ["", ""]],
         "NOT IFF": [["beta", 2, "len[3] mean difference"], ["NOT", "NOT"]],
         "XOR": [["beta", 1, "len[3] mean difference"], ["NOT", "NOT"]],
         # reguly beta
         "FORALL": ["gamma", 1],
         "NOT EXISTS": ["gamma", 2],
         # reguly gamma
         "EXISTS": ["delta", 1],
         "NOT FORALL": ["delta", 2]}
# reguly delta

mode_0 = ["X Y Z p/3",
          "Z g/1  Z Z p/1 Z d q/2 r/2 FORALL OR NOT NOT NOT",
          "Z Z q/1 Z p/1 Z p/1 a q/1 b q/1 c p/1 d q/1 e r/1 AND AND AND AND NOT OR OR OR FORALL",
          "a q/1 b q/1 IFF NOT",
          "Z Z p/1 a q/1 AND FORALL",
          "Z Y Z p/1 Y q/1 EXISTS FORALL",
          "a p/1",
          "Z Z p/1 Z p/1 NOT AND FORALL",
          "z p/1 z p/1 NOT OR NOT"]

""" funkcje przygotowujace do MTS """


def MODE(mode_0):
    global tmp, mode

    if mode == "0":
        if tmp == len(mode_0):

            mode = input("czy chcesz wpisac wlasna formule ? wpisz: 1 \nzeby zakonczyc wpisz: 0\n")
            if mode == "0":
                return "0"
            else:
                mode = "1"
                return predicates_changing(replace(input()).split())
        else:
            tmp = tmp + 1
            print(mode_0[tmp - 1])
            return predicates_changing(replace(mode_0[tmp - 1]).split())

    else:
        return predicates_changing(replace(input()).split())


def replace(line):
    line = line.replace("&", "AND")
    line = line.replace("∧", "AND")
    line = line.replace("V", "OR")
    line = line.replace("|", "OR")
    line = line.replace("↔", "IFF")
    line = line.replace("⊕", "XOR")
    line = line.replace("→", "IMPLIES")

    line = line.replace("~", "NOT")
    line = line.replace("¬", "NOT")

    line = line.replace("∀", "FORALL")
    line = line.replace("∃", "EXISTS")

    return line


def predicates_changing(line):  # kod :z a b c q/2 robi q/abc

    stos = []
    lista_zmiennych = []
    for i in line:
        if (i[0] in funkcje or i[0] in predykaty) and (len(i) == 3):
            for l in range(int(i[2])):
                lista_zmiennych = lista_zmiennych + [stos.pop()]
            lista_zmiennych.reverse()
            funkcja = i[0:2]
            for zmienna in lista_zmiennych:
                funkcja = funkcja + zmienna
            stos.append(funkcja)
            funkcja = ""
            lista_zmiennych = []
        else:
            stos.append(i)
    return stos


""" funkcje MTS """


class Leaf:
    def __init__(self, gamma, lines, field):
        self.gamma = gamma
        self.lines = lines
        self.field = field

    def alfa_beta_role(self, value, line):

        for i in range(value[0][1]):
            self.lines[line].pop()

        cut = 1
        index = 1
        while (True):
            if self.lines[line][-index][1] == "/":  # oznacza to ze trafilismy na predykat, ma on postac p"/"Z:
                break
            elif self.lines[line][-index] == NOT:
                cut = cut + 1
            elif self.lines[line][-index] in operatory_kwantyfikatory:
                cut = cut + 2
            index = index + 1

        line_1 = self.lines[line][:-cut]
        line_2 = self.lines[line][-cut:]

        if len(value[0]) == 3:
            tmp_1 = line_1 + line_2 + ["IMPLIES"]
            tmp_2 = line_2 + line_1 + ["IMPLIES"]

            line_1 = tmp_1
            line_2 = tmp_2

        del self.lines[line]
        cut = 1

        if bool(value[1][0]):
            line_1.append(value[1][0])
        if bool(value[1][1]):
            line_2.append(value[1][1])

        return line_1, line_2

    def gamma_delta_role(self, value, line):

        if value[0] == "gamma":

            if value[1] != 0:  # value[1] == 0 gdy sztucznie wywoluje sie gamme pod koniec obliczen --> MTS pierwszy if
                self.lines[line].pop(-value[1])
                self.gamma.append(self.lines[line])  # xX!! mechhh !!Xx#

            for stala in self.fields[0]:  # moga powtarzac sie zmienne ktore podstawiam
                if value[1] == 0:  # ale moga tak jak w algorytmie:
                    tmp = " ".join(self.gamma[line])  # W książce ”Logika matematyczna w informatyce” M. Ben-Ari’ego
                else:
                    tmp = " ".join(self.lines[line])
                tmp = tmp.replace(tmp[0], stala)
                tmp = tmp.split()
                tmp.pop(0)
                self.lines.append(tmp)

            if value[1] != 0:
                del self.lines[line]
                # slozy to rozpoznaniu przy kolejnym wywolaniu gamma
            self.fields[1] = self.fields[0].copy()  # czy zmienne byly juz wywolywane czy nie

        else:  # else czyli delta
            self.lines[line].pop(-value[1])

            new_stala = (list(filter(lambda x: x not in self.fields[0], stale)))
            if new_stala:
                new_stala = new_stala[0]
            else:
                new_stala = "a"  # zabezpieczenie przed skonczeniem sie stalych
            if new_stala not in self.fields[0]:  # zabezpieczenie przed nieskonczonym roznieniem sie
                self.fields[0].append(new_stala)  # leaf.fields[0] od leaf.fields[1]

            tmp = " ".join(self.lines[line])
            tmp = tmp.replace(tmp[0], new_stala)
            tmp = tmp.split()
            tmp.pop(0)
            self.lines[line] = tmp

    def leaf_checking(self):

        denied_predicate = []
        predicate = []
        for line in self.lines:
            if NOT in line:  # dziele na predykaty zaprzeczone i nie zaprzeczone
                denied_predicate = denied_predicate + line
            else:
                predicate = predicate + line

        denied_predicate = " ".join(denied_predicate)
        denied_predicate = denied_predicate.replace("NOT", "")
        denied_predicate = denied_predicate.split()

        if not list(filter(lambda x: x in predicate, denied_predicate)):
            three.append(1)
        else:
            three.append(0)

        print("predykaty zaprzeczone:", denied_predicate, "predykaty:", predicate)


def MTS(leaf):
    while (True):
        gamma_time = 0
        for line in range(len(leaf.lines)):

            if leaf.lines[line][-1] == NOT and leaf.lines[line][-2] == NOT:
                leaf.lines[line].pop()
                leaf.lines[line].pop()

            if not list(filter(lambda x: x in operatory_kwantyfikatory, leaf.lines[
                line])):  # oznacza to ze w tym lisciu nie ma juz operatory_kwantyfikatory, (liscie zostaly doprowadzone do konca obliczen)

                gamma_time = gamma_time + 1
                if gamma_time == len(
                        leaf.lines):  # leaf.fields[0] to dziedzina formuly, leaf.fields[1] ro dziedzina gammy

                    if leaf.fields[0] != leaf.fields[
                        1] and leaf.gamma:  # and leaf.gamma poniewaz zbior nie moze byc pusty
                        for i in range(len(leaf.gamma)):  # uruchamiana dla kazdego wyrazania z gamma
                            leaf.gamma_delta_role(["gamma", 0], i)  # ["gamma", 0] = value, to jest jak rules(key)
                    else:
                        leaf.leaf_checking()
                        return 0
                else:
                    continue
            # w tym ifie jest gamma_time i return

            elif leaf.lines[line][-1] == NOT and leaf.lines[line][-2] in operatory_kwantyfikatory:

                value = rules[leaf.lines[line][-1] + " " + leaf.lines[line][-2]]  # rules[key]
                if value[0][0] == "alfa" or value[0][0] == "beta":

                    line_1, line_2 = leaf.alfa_beta_role(value, line)
                    if value[0][0] == "alfa":
                        leaf.lines.append(line_1)
                        leaf.lines.append(line_2)

                    elif value[0][0] == "beta":
                        leaf.lines.append(line_1)
                        MTS(leaf)  # rozgalezienie
                        leaf.lines.pop()

                        leaf.lines.append(line_2)
                else:
                    leaf.gamma_delta_role(value, line)

            elif leaf.lines[line][-1] in operatory_kwantyfikatory:

                value = rules[leaf.lines[line][-1]]  # rules[key]
                if value[0][0] == "alfa" or value[0][0] == "beta":

                    line_1, line_2 = leaf.alfa_beta_role(value, line)
                    if value[0][0] == "alfa":
                        leaf.lines.append(line_1)
                        leaf.lines.append(line_2)

                    elif value[0][0] == "beta":
                        leaf.lines.append(line_1)
                        MTS(leaf)  # rozgalezienie
                        leaf.lines.pop()

                        leaf.lines.append(line_2)
                else:
                    leaf.gamma_delta_role(value, line)


""" MAIN """

print("            ##############################")
print("            # METODA TABEL SEMANTYCZNYCH #")
print("            ##############################\n")

leaf = Leaf(None, None, None)  # lisc ma postac .gamma .lines .field
three, lines, fields = [], [], []  # three - wartosci wszystkich lisci
tmp, line, field = 0, None, None

mode = input("0 : formuly przykladowe z MOODLE \n1 : wpisz wlasna formule \n")
if mode != "0":
    print("jezeli chcialbys zakonczyc prace wpisz: 0")

while (True):

    while (True):
        line = MODE(mode_0)
        test_line = " ".join(line)
        if "/" in test_line or test_line == "0":
            break
        else:
            print("nie poprawne dane, wpisz ponownie")

    if line[0] == "0":
        break

    lines = [line]
    leaf.lines = lines

    field = list(filter(lambda x: x in stale, "".join(line)))
    if not bool(field):
        field = ["a"]

    fields = [field, field.copy()]  # 2 st field jest dla dziedziny gamma
    leaf.fields = fields

    leaf.gamma = []

    MTS(leaf)

    print("MAIN:    gamma:", leaf.gamma, "  lines:", leaf.lines, "  fields:", leaf.fields, "\n")

    if sum(three):
        print("SPELNIALNA", three, "\n0 oznacza lisc zamkniety, 1 oznacza lisc otwarty")
        if 0 not in three:
            print("a do tego PRAWDZIWA\n")
        else:
            print("\n")
    else:
        print("NIESPELNIALNA", three, "\n0 oznacza lisc zamkniety, 1 oznacza lisc otwarty\n")

    leaf = Leaf(None, None, None)
    three, lines, field = [], [], []
