from pathlib import Path
from tkinter import StringVar, IntVar, DoubleVar

def thisFilePath() -> str :
    return Path(__file__).parents[0]

def jsonPath() -> str:    
    jsonFileName = "recettes.json"
    return Path(Path(thisFilePath()).parents[0], jsonFileName)

if __name__ == "__main__":
    print(jsonPath())