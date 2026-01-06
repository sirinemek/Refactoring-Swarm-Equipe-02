#!/usr/bin/env python3
"""Script de validation du fichier experiment_data.json"""

import json
from pathlib import Path
from collections import Counter

LOG_FILE = Path("logs/experiment_data.json")

REQUIRED_FIELDS = ["id", "timestamp", "agent_name", "model_used", "action", "details", "status"]
REQUIRED_DETAIL_FIELDS = ["input_prompt", "output_response"]
VALID_ACTIONS = ["ANALYSIS", "FIX", "DEBUG", "GENERATION"]
VALID_STATUSES = ["SUCCESS", "FAILURE"]

print("Validation du fichier experiment_data.json")
print("="*70)

# Charger le fichier
with open(LOG_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f" JSON valide - {len(data)} entrées\n")

errors = []
warnings = []
stats = {"by_agent": {}, "by_action": {}, "by_status": {}}

# Valider chaque entrée
for i, entry in enumerate(data):
    # Champs de premier niveau
    for field in REQUIRED_FIELDS:
        if field not in entry:
            errors.append(f" Entrée {i}: Champ '{field}' manquant")
    
    # Vérifier agent_name
    if "agent_name" in entry:
        agent = entry["agent_name"]
        if "," in str(agent):
            errors.append(f" Entrée {i}: 'agent_name' contient une virgule - UN SEUL agent par entrée!")
        stats["by_agent"][agent] = stats["by_agent"].get(agent, 0) + 1
    
    # Vérifier action
    if "action" in entry:
        action = entry["action"]
        if action not in VALID_ACTIONS:
            warnings.append(f"  Entrée {i}: Action '{action}' non standard")
        stats["by_action"][action] = stats["by_action"].get(action, 0) + 1
    
    # Vérifier status
    if "status" in entry:
        status = entry["status"]
        if status not in VALID_STATUSES:
            warnings.append(f"  Entrée {i}: Status '{status}' devrait être SUCCESS ou FAILURE")
        stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
    
    # Vérifier details
    if "details" in entry:
        if not isinstance(entry["details"], dict):
            errors.append(f" Entrée {i}: 'details' doit être un objet {{}}")
        else:
            for field in REQUIRED_DETAIL_FIELDS:
                if field not in entry["details"]:
                    errors.append(f" Entrée {i}: '{field}' manquant dans details")
                elif not entry["details"][field] or not str(entry["details"][field]).strip():
                    errors.append(f" Entrée {i}: '{field}' est vide")

# Afficher les résultats
print("\n" + "="*70)
print(" RAPPORT")
print("="*70)

if stats["by_agent"]:
    print("\n Par Agent:")
    for agent, count in stats["by_agent"].items():
        print(f"  • {agent}: {count} actions")

if stats["by_action"]:
    print("\n Par Action:")
    for action, count in stats["by_action"].items():
        print(f"  • {action}: {count}")

if stats["by_status"]:
    print("\n Par Statut:")
    for status, count in stats["by_status"].items():
        emoji = "" if status == "SUCCESS" else ""
        print(f"  {emoji} {status}: {count}")

if warnings:
    print(f"\n AVERTISSEMENTS ({len(warnings)}):")
    for warning in warnings[:5]:
        print(f"  {warning}")

if errors:
    print(f"\n ERREURS CRITIQUES ({len(errors)}):")
    for error in errors[:10]:
        print(f"  {error}")
    print("\n CES ERREURS DOIVENT ÊTRE CORRIGÉES!")
else:
    print("\n AUCUNE ERREUR CRITIQUE - Validation réussie!")

print("\n" + "="*70)