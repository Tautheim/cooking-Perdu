import typing
import json
from variable import jsonPath

def read_json()->dict:
    with open(jsonPath(),'r') as file :
        data = json.load(file)
    return data

def write_json(data:dict):
    sorted_data = dict(sorted(data.items()))
    with open(jsonPath(), 'w') as file :
        json.dump(sorted_data,file,indent=1)

def search_recipe(name:str)->dict:
    recipes = read_json()
    if name not in recipes.keys() :
        return {}
    else :
        return recipes[name]

if __name__ == "__main__" :
    recettes = {}
    recettes["Mousse au chocolat"] = {"Type":"Dessert", "Temps":{"Préparation":[0,""], "Cuisson":[0,""],  "Repos":[0,""]},\
        "Ingrédients":[(3,"","Blanc d'oeufs"),(20,"g","Sucre"),(125,"g","chocolat"),(2,"","Jaune d'oeuf"),(75,"g","Beurre"),(50,"g","Sucre")],\
            "Préparation":["Faire fondre le chocolat au bain marie","Hors du feu ajouter le beurre jusqu'à obtenir un mélange pommade","Une fois le mélange froid ajouter les jaunes et 50 g de sucre","Battre les blancs en neige et à mi-parcours ajouter le sucre restant","Mélanger délicatement les blancs avec le reste","Mettre au frais"]}
    write_json(recettes)
    recipes = read_json()
    print(recipes)