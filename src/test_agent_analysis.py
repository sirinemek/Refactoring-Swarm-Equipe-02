# test_agent_analysis.py
from pathlib import Path
from utils.The_Toolsmith import run_pylint  # ton module contenant la fonction run_pylint


def test_first_agent_analyzes_file():
    """
    Test simple du Premier Agent :
    - Analyse un fichier Python "mal fait"
    - Vérifie que pylint retourne un score et des erreurs
    """

    # 🔹 1️⃣ Chemin vers le dossier sandbox contenant les fichiers Python à analyser
    sandbox_dir = Path("sandbox")

    # 🔹 2️⃣ Lancer l'analyse
    result = run_pylint(sandbox_dir)

    # 🔹 3️⃣ Vérifier que la sortie contient les clés attendues
    assert "score" in result, "Clé 'score' manquante dans le résultat"
    assert "raw_output" in result, "Clé 'raw_output' manquante dans le résultat"
    assert "errors" in result, "Clé 'errors' manquante dans le résultat"

    # 🔹 4️⃣ Le score doit être compris entre 0 et 10
    assert 0.0 <= result["score"] <= 10.0, f"Score invalide : {result['score']}"

    # 🔹 5️⃣ Il doit y avoir au moins une erreur détectée
    assert len(result["errors"]) > 0, "Aucune erreur détectée : ajoute un fichier Python 'mal fait' dans sandbox/"

    # 🔹 6️⃣ Affichage des résultats pour debug
    print("\n=== Score pylint ===")
    print(result["score"])
    print("\n=== Erreurs détectées ===")
    for err in result["errors"]:
        print(f"{err['file']}:{err['line']}:{err['column']} {err['code']} {err['message']} ({err['symbol']})")
