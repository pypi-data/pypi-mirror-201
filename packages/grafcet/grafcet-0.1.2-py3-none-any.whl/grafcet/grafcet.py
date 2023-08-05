from multipledispatch import dispatch
from typing import List
from time import time
from grafcet.temporisation import *


class Etape:
    """
    La classe Etape représente une étape dans un processus.

    Attributes:
        trace (bool): Indique si le mode de trace est activé ou non.
        un_front (int): Compteur global pour les fronts montants.

    Args:
        name (int, optional): Le nom de l'étape. Par défaut -1.
        etape_initiale (bool, optional): Indique si l'étape est initiale ou non. Par défaut False.
        tempo (Temporisation, optional): L'objet de temporisation associé à l'étape. Par défaut Temporisation(0).

    Attributes:
        name (int): Le nom de l'étape.
        state (int): L'état actuel de l'étape (0 pour inactif, 1 pour actif).
        etape_initiale (bool): Indique si l'étape est initiale ou non.
        front_montant (int): Indique s'il y a un front montant (1 pour vrai, 0 pour faux).
        tempo (Temporisation): L'objet de temporisation associé à l'étape.
        fin_temporisation (int): Indique si la temporisation est terminée (1 pour vrai, 0 pour faux).
    """
    trace: bool = False
    un_front: int = 0

    def __init__(self, name: int = -1, etape_initiale: bool = False, tempo: [Temporisation, None] = None):
        self.name: int = name
        self.state: int = 0
        self.etape_initiale: bool = etape_initiale
        self.front_montant: int = 0
        if isinstance(tempo, Temporisation):
            self.tempo: Temporisation = tempo
        else:
            self.tempo: Temporisation = Temporisation(0)
        self.tempo.stop()
        self.fin_temporisation: int = 0

    def is_off(self) -> bool:
        """
        Vérifie si l'étape est inactif.

        Returns:
            bool: True si l'étape est inactif, False sinon.
        """
        return self.state == 0

    def is_on(self) -> bool:
        """
        Vérifie si l'étape est actif.

        Returns:
            bool: True si l'étape est actif, False sinon.
        """
        return self.state == 1

    def desactive(self) -> None:
        """
        Désactive l'étape.
        """
        self.force(0)
        self.front_montant = 0
        self.fin_temporisation = 0
        self.tempo.stop()

    def active(self, etape_precedente: "Etape", transition: bool) -> int:
        """
        Active l'étape en fonction de l'état de l'étape précédente et de l'état' d'une transition.

        :param etape_precedente: L'étape précédente.
        :type etape_precedente: Etape
        :param transition: Indique s'il y a une transition depuis l'étape précédente.
        :type transition: bool
        :return: Un booléen indiquant si le front montant a été détecté (1) ou non (0).
        :rtype: int
        """
        if self.front_montant:
            self.front_montant = 0
        # print(self.name, self.state, transition,etape_precedente.is_on(), self.tempo.state(), self.tempo.is_on())
        if self.state == 0 and transition and etape_precedente.is_on():
            self.force(1)
            etape_precedente.desactive()
            self.front_montant = 1
            Etape.un_front = 1
        if self.state == 1 and self.tempo.valid() and self.tempo.is_off() and self.fin_temporisation == 0:
            self.fin_temporisation = 1
            Etape.un_front = 1

        if Etape.trace:
            if self.etape_initiale:
                print("****************")
            print(self.__str__())
            if self.etape_initiale:
                print(" INIT")
            else:
                print("")
        return self.front_montant

    def force(self, value: int) -> None:
        """
        Force l'état de l'étape.

        :param value: La valeur de l'état à forcer (0 ou 1).
        :type value: int
        """
        if value == 0 or value == 1:
            self.state = value
            self.front_montant = value
            if self.tempo.valid():
                if self.state:
                    self.tempo.start()
                else:
                    self.tempo.stop()

    def front(self) -> bool:
        """
        Vérifie si le front montant a été détecté.

        :return: Un booléen indiquant si le front montant a été détecté (True) ou non (False).
        :rtype: bool
        """
        return self.front_montant == 1

    def __str__(self) -> str:
        if self.tempo.valid():
            if self.tempo.is_on():
                return f"X{self.name} : {self.state} temporisation : ON  "
            else:
                return f"X{self.name} : {self.state} temporisation : OFF  "
        else:
            return f"X{self.name} : {self.state}"

    def get_name(self) -> int:
        """retourne le nom de l'étape"""
        return self.name

    def get_init(self) -> bool:
        """retourne True si l'étape est une étape initiale"""
        return self.etape_initiale

    def fin_tempo(self) -> bool:
        """retourne si la temporisation de l'étape est terminée"""
        return self.fin_temporisation == 1

    def set_tempo_ms(self, temporisation: int) -> None:
        """modifie la valeur de la temporisation en millisecondes"""
        self.tempo.set_tempo(temporisation)

    def set_tempo_s(self, temporisation: int) -> None:
        """modifie la valeur de la temporisation en secondes"""
        self.tempo.set_tempo(temporisation * 1000)

    def get_tempo(self) -> Temporisation:
        """retourne l'objet Temporisation de l'étape"""
        return self.tempo

    def set_initiale(self) -> None:
        """force à 1 l'étape si celle-ci est une étape initiale"""
        if self.etape_initiale is True:
            self.force(1)


class Grafcet:
    @dispatch()
    def __init__(self):
        """Créer un Grafcet vide"""
        self.etapes: list[Etape] = []
        self.modified = True
        self.figed = False

    @dispatch(list)
    def __init__(self, etapes: list):
        """Créer un Grafcet et ajoute une liste d'étape désignée par leur nom_etape:int au grafcet"""
        self.etapes: list[Etape] = []
        self.modified = True
        self.figed = False
        for e in etapes:
            self.addEtape(e)
        if len(self.etapes) == len(etapes):
            self.etapes[0] = Etape(etapes[0], True)

    @dispatch((int, int),(int, int, int))
    def __init__(self, debut: int, fin: int, pas: int = 1):
        """Créer un Grafcet dont la première etape sera debut et la dernière sera fin.
        les etapes seront espacées de pas.La première etapes sera une étape initiale """
        self.etapes: list[Etape] = []
        self.modified = True
        self.figed = False
        for e in range(debut, fin + 1, pas):
            self.addEtape(e)
        self.etapes[0].etape_initiale = True

    @dispatch(Etape)
    def addEtape(self, e: Etape):
        """ajoute une étape (Etape) au grafcet"""
        self.etapes.append(e)

    @dispatch(int)
    def addEtape(self, nom_etape: int):
        """ajoute une étape désignée par nom_etape avec une temporisation au grafcet"""
        self.etapes.append(Etape(nom_etape))

    @dispatch(int, Temporisation)
    def addEtape(self, nom_etape: int, tempo: Temporisation):
        """ajoute une étape désignée par nom_etape avec une temporisation au grafcet"""
        self.etapes.append(Etape(nom_etape, False, tempo))

    @dispatch(int)
    def addEtapeInit(self, nom_etape: int):
        """ajoute une étape initiale désignée par nom_etape au grafcet"""
        self.etapes.append(Etape(nom_etape, True))

    @dispatch(int, Temporisation)
    def addEtapeInit(self, nom_etape: int, tempo: Temporisation):
        """ajoute une étape initiale désignée par nom_etape avec une temporisation au grafcet"""
        self.etapes.append(Etape(nom_etape, True, tempo))

    def active(self, nom_etape: int, nom_etape_precedente: int, transition: bool)->bool:
        """active l'étape désignée par nom_etape en fonction de
        en fonction de l'état de l'étape précédente et de l'état' d'une transition."""
        e = self.index_by_name(nom_etape)
        ep = self.index_by_name(nom_etape_precedente)
        if self.etapes[e].active(self.etapes[ep], transition)==1:
            self.modified = True
            return True
        return False

    def index_by_name(self, nom_etape: int) -> int:
        """retourne l'index d'une étape désignée par nom_etape dans self.etapes"""
        for i in range(len(self.etapes)):
            if self.etapes[i].get_name() == nom_etape:
                return i
        return -1

    def is_on(self, nom_etape: int) -> bool:
        """retourne True si l'étape designée par nom_etape est ON"""
        return self.etapes[self.index_by_name(nom_etape)].is_on()

    def __str__(self):
        etapes_str = ""
        for e in self.etapes:
            etapes_str += str(e) + "\n"
        return etapes_str

    def init(self, condition: bool = True):
        """initialise les étapes initiales du grafcet"""
        if condition:
            for i in range(len(self.etapes)):
                self.etapes[i].set_initiale()

    def force_zero(self, condition: bool = True) -> None:
        """place les étapes du grafcet à 0"""
        if condition:
            for i in range(len(self.etapes)):
                self.etapes[i].on = False

    def fige(self) -> None:
        """fige le grafcet"""
        self.figed = True

    def defige(self) -> None:
        """défige le grafcet"""
        self.figed = False

    def etape(self, nom_etape: int) -> Etape:
        """retourne l'étape du grafcet désignée par son numéro"""
        return self.etapes[self.index_by_name(nom_etape)]

    def x(self, nom_etape: int) -> bool:
        """retourne l'état de l'étape du grafet désignée par son numéro idem etape"""
        return self.is_on(nom_etape)

    def fin_tempo_x(self, nom_etape: int) -> bool:
        """retourne True si la temporisation de l'étape est terminée"""
        return self.etape(nom_etape).fin_tempo()

    def t_x(self, nom_etape: int) -> bool:
        """retourne True si la temporisation de l'étape est terminée
        idem fin_tempo_x"""
        return self.etape(nom_etape).fin_tempo()

    def fm_x(self, nom_etape: int) -> bool:
        """retourne True sur le front montant de l'étape nom_etape
        et False dans le cas contraire"""
        return self.etape(nom_etape).fin_tempo()

    def x_fm(self, nom_etape: int) -> bool:
        """retourne True sur le front montant de l'étape nom_etape
        et False dans le cas contraire idem fm_x"""
        return self.etape(nom_etape).fin_tempo()

    def tempo_is_on_x(self, nomEtape: int) -> bool:
        """retourne True si la temporisation de l'étape est à ON"""
        return self.etape(nomEtape).get_tempo().is_on()

    def t_x_on(self, nomEtape: int) -> bool:
        """retourne True si la temporisation de l'étape est à ON
        idem tempo_is_on_x"""
        return self.etape(nomEtape).get_tempo().is_on()

    def set_x_tempo_s(self, nom_etape: int, duree_s: int) -> None:
        """
        Définit la durée en secondes d'une étape spécifique du Grafcet.

        Args:
        - nom_etape (int): Le nom de l'étape dont on veut modifier la durée.
        - duree (int): La durée en secondes à affecter à l'étape.

        Returns:
        - None
        """
        self.etapes[self.index_by_name(nom_etape)].set_tempo_s(duree_s)

    def set_x_tempo_ms(self, nom_etape: int, duree_ms: int) -> None:
        """
        Définit la durée en millisecondes d'une étape spécifique du Grafcet.

        Args:
        - nom_etape (int): Le nom de l'étape dont on veut modifier la durée.
        - duree (int): La durée en millisecondes à affecter à l'étape.

        Returns:
        - None
        """
        self.etapes[self.index_by_name(nom_etape)].set_tempo_ms(duree_ms)

    def print_state(self, if_change = True):
        """affiche sur la console l'état du grafcet sous réserve que la variable if_change == True
        et que l'état du grafcet est mofifié"""
        if if_change and self.modified:
            print(self)
            self.modified = False

if __name__ == '__main__':
    g0 = Grafcet(1, 3)
    g0.set_x_tempo_s(1, 3)
    g0.set_x_tempo_s(2, 1)
    g0.set_x_tempo_s(3, 5)
    g0.init()
    nb_tour = 0
    # Etape.trace = True
    t = time()
    while nb_tour < 2:
        g0.print_state()
        g0.active(2, 1, g0.fin_tempo_x(1))
        g0.active(3, 2, g0.fin_tempo_x(2))
        if g0.active(1, 3, g0.fin_tempo_x(3)):
            nb_tour += 1


