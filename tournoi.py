from joueur import Joueur
from match import Match
import utils

class Tournoi:
    def __init__(self, nom: str = "Tournoi"):
        self.nom = nom
        self.joueurs: dict[str, Joueur] = {}
        self.matchs: list[Match] = []

    def charger_joueurs(self, chemin_csv: str) -> None:
        
        data = utils.lire_csv(chemin_csv)
        for row in data:
            # on prend la première clé du dict (le nom de la première colonne)
            cle_pseudo = next(iter(row.keys()))
            pseudo = row[cle_pseudo].strip()
            if pseudo and pseudo not in self.joueurs:
                self.joueurs[pseudo] = Joueur(pseudo)

    def charger_matchs(self, chemin_csv: str) -> None:

        data = utils.lire_csv(chemin_csv)
        for row in data:
            cles = list(row.keys())
            p1 = row[cles[0]].strip()
            p2 = row[cles[1]].strip()
            if p1 in self.joueurs and p2 in self.joueurs:
                self.matchs.append(Match(self.joueurs[p1], self.joueurs[p2]))

    def saisir_scores(self) -> None:
        for m in self.matchs:
            print(f"Match : {m.joueur1.pseudo} vs {m.joueur2.pseudo}")
            s1 = int(input(f"Score {m.joueur1.pseudo} : "))
            s2 = int(input(f"Score {m.joueur2.pseudo} : "))
            m.definir_scores(s1, s2)
            gagnant = m.gagnant()
            if gagnant:
                gagnant.enregistrer_victoire()

    def afficher_classement(self) -> None:
        classe = sorted(self.joueurs.values(), key=lambda j: j.victoires, reverse=True)
        print(f"\nClassement final du tournoi '{self.nom}' :")
        for i, j in enumerate(classe, start=1):
            print(f"{i}. {j.pseudo} – {j.victoires} victoires")

    def sauvegarder(self, chemin_json: str) -> None:
        data = {
            'nom': self.nom,
            'joueurs': [
                {'pseudo': j.pseudo, 'victoires': j.victoires}
                for j in self.joueurs.values()
            ],
            'matchs': [
                {
                    'joueur1': m.joueur1.pseudo,
                    'joueur2': m.joueur2.pseudo,
                    'score1': m.score1,
                    'score2': m.score2
                }
                for m in self.matchs
            ]
        }
        utils.sauvegarder_json(data, chemin_json)

    def generer_rapport(self, chemin_txt: str) -> None:
        lignes = [f"--- Rapport de '{self.nom}' ---\n\n"]
        lignes.append("Classement final :\n")
        for i, j in enumerate(sorted(self.joueurs.values(), key=lambda j: j.victoires, reverse=True), 1):
            lignes.append(f"{i}. {j.pseudo} – {j.victoires} victoires\n")
        lignes.append("\nDétails des matchs :\n")
        for m in self.matchs:
            lignes.append(f"{m.joueur1.pseudo} {m.score1} – {m.score2} {m.joueur2.pseudo}\n")
        utils.ecrire_texte(''.join(lignes), chemin_txt)
