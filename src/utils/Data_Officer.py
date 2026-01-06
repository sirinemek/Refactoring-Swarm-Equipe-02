"""
Responsable Qualité & Data (Data Officer)
Rôle : Garantir la traçabilité et la qualité des logs du projet
"""

import json
from pathlib import Path
from collections import Counter

# Import depuis le même dossier
from .logger import log_experiment, ActionType


class DataOfficer:
    """
    Data Officer - Responsable de la qualité des données
    
    Missions :
    - Valider la conformité des logs
    - Générer des rapports de télémétrie
    - Créer les datasets de test internes
    - Assurer que tous les agents logguent correctement
    """
    
    def __init__(self):
        self.log_file = Path("logs/experiment_data.json")
    
    def validate_logs(self, verbose=True):
        """
        Valide la conformité du fichier experiment_data.json
        
        Returns:
            bool: True si conforme, False sinon
        """
        if verbose:
            print(" Validation des logs...")
            print("="*70)
        
        # Vérifier l'existence
        if not self.log_file.exists():
            print(" CRITIQUE: Fichier logs/experiment_data.json introuvable!")
            return False
        
        # Charger le JSON
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        except json.JSONDecodeError as e:
            print(f" CRITIQUE: JSON invalide - {e}")
            return False
        
        if not isinstance(logs, list):
            print(" CRITIQUE: Le JSON doit être un tableau []")
            return False
        
        if len(logs) == 0:
            print("  ATTENTION: Aucune entrée dans les logs")
            return False
        
        if verbose:
            print(f" JSON valide - {len(logs)} entrées\n")
        
        # Validation détaillée
        errors = []
        warnings = []
        
        required_fields = ["id", "timestamp", "agent_name", "model_used", "action", "details", "status"]
        valid_actions = ["ANALYSIS", "FIX", "DEBUG", "GENERATION"]
        
        for i, log in enumerate(logs):
            # Champs obligatoires
            for field in required_fields:
                if field not in log:
                    # Vérifier l'ancien format
                    if field == "agent_name" and "agent" in log:
                        errors.append(f"Entrée {i}: Utilise 'agent' au lieu de 'agent_name'")
                    elif field == "model_used" and "model" in log:
                        errors.append(f"Entrée {i}: Utilise 'model' au lieu de 'model_used'")
                    else:
                        errors.append(f"Entrée {i}: Champ '{field}' manquant")
            
            # Vérifier details
            if "details" in log:
                if not isinstance(log["details"], dict):
                    errors.append(f"Entrée {i}: 'details' doit être un objet {{}}")
                else:
                    if "input_prompt" not in log["details"]:
                        errors.append(f"Entrée {i}: 'input_prompt' manquant dans details")
                    if "output_response" not in log["details"]:
                        errors.append(f"Entrée {i}: 'output_response' manquant dans details")
            
            # Vérifier action
            if "action" in log and log["action"] not in valid_actions:
                warnings.append(f"Entrée {i}: Action '{log['action']}' non standard")
        
        # Affichage
        if errors:
            print(f" {len(errors)} ERREURS CRITIQUES:")
            for error in errors[:10]:
                print(f"  • {error}")
            return False
        
        if warnings and verbose:
            print(f"  {len(warnings)} avertissements:")
            for warning in warnings[:5]:
                print(f"  • {warning}")
        
        if verbose:
            print(" Tous les logs sont conformes!")
        
        return True
    
    def generate_report(self):
        """Génère un rapport statistique sur les logs"""
        
        with open(self.log_file, 'r', encoding='utf-8') as f:
            logs = json.load(f)
        
        print("\n" + "="*70)
        print(" RAPPORT DE TÉLÉMÉTRIE")
        print("="*70)
        
        print(f"\n Total d'entrées: {len(logs)}")
        
        # Par agent (gérer les deux formats)
        agents = Counter([log.get("agent_name") or log.get("agent", "Unknown") for log in logs])
        print("\n Par Agent:")
        for agent, count in sorted(agents.items()):
            print(f"  • {agent}: {count} actions")
        
        # Par action
        actions = Counter([log.get("action", "Unknown") for log in logs])
        print("\n🔧 Par Type d'Action:")
        for action, count in sorted(actions.items()):
            print(f"  • {action}: {count}")
        
        # Par statut
        statuses = Counter([log.get("status", "Unknown") for log in logs])
        print("\n Par Statut:")
        for status, count in statuses.items():
            emoji = "" if status == "SUCCESS" else ""
            print(f"  {emoji} {status}: {count}")
        
        # Taux de succès
        total = len(logs)
        success = statuses.get("SUCCESS", 0)
        rate = (success / total * 100) if total > 0 else 0
        print(f"\n Taux de succès global: {rate:.1f}%")
        
        print("="*70)
    
    def check_team_logging(self):
        """Vérifie que tous les membres de l'équipe logguent"""
        
        with open(self.log_file, 'r', encoding='utf-8') as f:
            logs = json.load(f)
        
        expected_agents = ["Auditor_Agent", "Fixer_Agent", "Judge_Agent", "Orchestrator"]
        found_agents = set(log.get("agent_name") or log.get("agent", "") for log in logs)
        
        print("\n Vérification du logging par rôle:")
        print("="*70)
        
        for agent in expected_agents:
            if agent in found_agents:
                count = len([l for l in logs if (l.get("agent_name") or l.get("agent")) == agent])
                print(f"   {agent}: {count} entrées")
            else:
                print(f"  {agent}: AUCUNE entrée (non loggué!)")
        
        print("="*70)


def main():
    """Point d'entrée principal"""
    officer = DataOfficer()
    
    print("🎓 Data Officer - Validation du Projet")
    print("="*70 + "\n")
    
    # Validation
    is_valid = officer.validate_logs()
    
    if is_valid:
        # Rapport
        officer.generate_report()
        
        # Vérification équipe
        officer.check_team_logging()
        
        print("\n Validation complète réussie!")
        return 0
    else:
        print("\n Validation échouée - Corrigez les erreurs!")
        return 1


if __name__ == "__main__":
    exit(main())