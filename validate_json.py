# validate_json.py
import json

try:
    with open("logs/experiment_data.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(" JSON valide!")
    print(f"Nombre d'entrées: {len(data)}")
    
    # Afficher la première entrée
    if len(data) > 0:
        print("\n Première entrée:")
        print(json.dumps(data[0], indent=2, ensure_ascii=False))
    
except json.JSONDecodeError as e:
    print(f" ERREUR JSON: {e}")
    print("Corrigez la syntaxe avant de continuer!")
except FileNotFoundError:
    print(" Fichier logs/experiment_data.json introuvable!")