
import csv
import json

def lire_csv(chemin: str) -> list[dict]:
    with open(chemin, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def sauvegarder_json(data, chemin: str) -> None:
    with open(chemin, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def ecrire_texte(contenu: str, chemin: str) -> None:
    with open(chemin, 'w', encoding='utf-8') as f:
        f.write(contenu)