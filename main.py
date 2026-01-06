# Importation des bibliothèques nécessaires
import argparse  # Pour lire les arguments du terminal
import sys       # Pour arrêter le programme
import os        # Pour le système de fichiers
from pathlib import Path  # Pour manipuler les chemins
from src.utils.logger import log_experiment, ActionType  # Pour enregistrer les logs
from dotenv import load_dotenv  # Pour charger les clés API

# Charger les variables d'environnement depuis .env
load_dotenv()

def main():
    """Fonction principale qui coordonne tous les agents"""
    
    # === ÉTAPE 1 : LIRE L'ARGUMENT --target_dir ===
    parser = argparse.ArgumentParser(
        description="Refactoring Swarm - Système multi-agents"
    )
    parser.add_argument(
        "--target_dir",
        type=str,
        required=True,  # Obligatoire
        help="Dossier contenant le code Python à corriger"
    )
    args = parser.parse_args()
    
    # === ÉTAPE 2 : VÉRIFIER QUE LE DOSSIER EXISTE ===
    target_directory = Path(args.target_dir)
    
    if not target_directory.exists():
        # Le dossier n'existe pas → Erreur
        print(f"❌ Erreur : Le dossier {args.target_dir} n'existe pas.")
        
        # Enregistrer l'erreur dans les logs
        log_experiment(
            agent_name="System",
            model_used="N/A",
            action=ActionType.DEBUG,
            details={
                "input_prompt": f"Vérification dossier {args.target_dir}",
                "output_response": f"Dossier introuvable",
                "error": "Directory not found"
            },
            status="FAILED"
        )
        sys.exit(1)  # Arrêter avec code erreur 1
    
    # === ÉTAPE 3 : DÉMARRER LE SYSTÈME ===
    print(f"🚀 DEMARRAGE DU REFACTORING SWARM")
    print(f"   Dossier cible : {args.target_dir}")
    print("=" * 70)
    
    # Enregistrer le démarrage dans les logs
    log_experiment(
        agent_name="System",
        model_used="N/A",
        action=ActionType.ANALYSIS,
        details={
            "input_prompt": f"Initialisation sur {args.target_dir}",
            "output_response": "Système démarré",
            "target_directory": str(target_directory)
        },
        status="SUCCESS"
    )
    
    # === ÉTAPE 4 : ORCHESTRER LES 3 AGENTS ===
    try:
        # --- PHASE 1 : ANALYSER AVEC L'AUDITEUR ---
        print("\n📋 ÉTAPE 1 : ANALYSE PAR L'AUDITEUR")
        print("-" * 70)
        
        # TODO: Décommenter quand l'agent Auditeur sera créé
        # from src.agents.auditor import analyze
        # audit_result = analyze(target_directory)
        
        # Simulation temporaire (à supprimer plus tard)
        audit_result = {
            "files_analyzed": [],
            "issues_found": [],
            "pylint_score_before": 0.0
        }
        print("⚠️  Agent Auditeur non implémenté (TODO Prompt Engineer)")
        
        # --- PHASE 2 : BOUCLE DE CORRECTION (MAX 10 FOIS) ---
        max_iterations = 10  # Maximum 10 essais
        iteration = 0        # Compteur d'essais
        all_tests_passed = False  # Drapeau de succès
        
        print("\n🔄 DÉMARRAGE DE LA BOUCLE DE CORRECTION")
        print(f"   Limite : {max_iterations} itérations")
        print("=" * 70)
        
        # Boucle : Continue tant que tests échouent ET moins de 10 essais
        while iteration < max_iterations and not all_tests_passed:
            iteration += 1  # Incrémenter le compteur
            
            print(f"\n{'='*70}")
            print(f"🔁 ITÉRATION {iteration}/{max_iterations}")
            print(f"{'='*70}")
            
            # --- SOUS-ÉTAPE A : CORRIGER AVEC LE FIXER ---
            print(f"\n🛠️  Correction par le Fixer...")
            
            # TODO: Décommenter quand l'agent Fixer sera créé
            # from src.agents.fixer import fix
            # fix_result = fix(audit_result, target_directory)
            
            # Simulation temporaire
            fix_result = {
                "files_modified": [],
                "changes_applied": 0,
                "status": "NOT_IMPLEMENTED"
            }
            print("⚠️  Agent Fixer non implémenté (TODO Toolsmith)")
            
            # --- SOUS-ÉTAPE B : TESTER AVEC LE JUDGE ---
            print(f"\n✅ Tests par le Judge...")
            
            # TODO: Décommenter quand l'agent Judge sera créé
            # from src.agents.judge import test
            # test_result = test(target_directory)
            
            # Simulation temporaire
            test_result = {
                "all_passed": False,  # Si True → Mission accomplie !
                "total_tests": 0,
                "failed_tests": [],
                "error_logs": ""
            }
            print("⚠️  Agent Judge non implémenté (TODO Toolsmith)")
            
            # --- SOUS-ÉTAPE C : DÉCIDER QUOI FAIRE ---
            if test_result.get("all_passed", False):
                # ✅ SUCCÈS : Tous les tests passent !
                all_tests_passed = True
                print(f"\n🎉 SUCCÈS en {iteration} itération(s) !")
                
                # Enregistrer le succès
                log_experiment(
                    agent_name="System",
                    model_used="N/A",
                    action=ActionType.FIX,
                    details={
                        "input_prompt": "Vérification finale",
                        "output_response": f"Succès en {iteration} itérations",
                        "iterations_needed": iteration
                    },
                    status="SUCCESS"
                )
                break  # Sortir de la boucle immédiatement
            else:
                # ⚠️ ÉCHEC : Certains tests ont échoué
                failed_count = len(test_result.get("failed_tests", []))
                print(f"\n⚠️  {failed_count} test(s) échoué(s)")
                
                if iteration >= max_iterations:
                    # On a atteint la limite de 10 essais
                    print(f"\n❌ LIMITE ATTEINTE ({max_iterations} itérations)")
                    
                    # Enregistrer l'échec
                    log_experiment(
                        agent_name="System",
                        model_used="N/A",
                        action=ActionType.DEBUG,
                        details={
                            "input_prompt": "Fin de boucle",
                            "output_response": "Limite d'itérations atteinte",
                            "failed_tests": test_result.get("failed_tests", [])
                        },
                        status="FAILED"
                    )
                else:
                    # On continue, nouvelle tentative
                    print(f"   → Nouvelle tentative...")
        
        # --- PHASE 3 : AFFICHER LE RAPPORT FINAL ---
        print("\n" + "=" * 70)
        print("📊 RAPPORT FINAL")
        print("=" * 70)
        print(f"✓ Itérations : {iteration}/{max_iterations}")
        print(f"✓ Statut : {'SUCCÈS ✅' if all_tests_passed else 'ÉCHEC ❌'}")
        print(f"✓ Dossier : {target_directory}")
        print("=" * 70)
        
        # Sortir avec le bon code
        if all_tests_passed:
            print("\n✅ MISSION_COMPLETE")
            sys.exit(0)  # Code 0 = Succès
        else:
            print("\n❌ MISSION_INCOMPLETE")
            sys.exit(1)  # Code 1 = Échec
    
    # === GESTION DES ERREURS CRITIQUES ===
    except Exception as e:
        # Si une erreur survient n'importe où
        print(f"\n💥 ERREUR CRITIQUE : {type(e).__name__}")
        print(f"   Message : {str(e)}")
        
        # Enregistrer l'erreur
        log_experiment(
            agent_name="System",
            model_used="N/A",
            action=ActionType.DEBUG,
            details={
                "input_prompt": "Exécution système",
                "output_response": f"Erreur : {str(e)}",
                "error_type": type(e).__name__
            },
            status="FAILED"
        )
        
        sys.exit(1)  # Sortir avec erreur


# Point d'entrée : Lance main() si le fichier est exécuté directement
if __name__ == "__main__":
    main()