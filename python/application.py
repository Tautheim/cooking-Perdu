from pathlib import Path
import subprocess
import sys

folder = Path(__file__).parent
venv_path = folder / "pyenv"

print("Vérification de l'environement virtuel...")
if not venv_path.exists():
    print("\tL'environnement n'a pas été trouvé : création en cours...")
    try:
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
        print("\t\tTerminé")
    except subprocess.CalledProcessError as e:
        print(f"\t\tLa création du venv a échoué (code {e.returncode})")
        exit(1)
print("\tVérifiaction terminée")

if sys.platform.startswith("win"):
    python_exec = venv_path / "Scripts" / "pythonw.exe"
    pip_exec = venv_path / "Scripts" / "pip.exe"
else:
    python_exec = venv_path / "bin" / "pythonw"
    pip_exec = venv_path / "bin" / "pip"


req_file = folder / "requirements.txt"
print("Vérification des dépendaces...")
if req_file.exists():
    try:
        subprocess.run([str(pip_exec), "install", "-r", str(req_file)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\tInstallation des dépendances échouée (code {e.returncode})")
        exit(1)
else:
    print("\t⚠️ Aucun requirements.txt trouvé — dépendances non installées.")
print("\tVérifiaction terminée")

print("Démarrage de l'application...")
try:
    subprocess.run([str(python_exec), "editingInterface.py"], check=True, cwd=folder, shell=False)
    print("\tApplication démarée")
except subprocess.CalledProcessError as e:
    print(f"\tErreur à l'exécution (code {e.returncode})")
