# Importation des bibliothèques nécessaires
import argparse
import sys
from pathlib import Path

from src.utils.logger import log_experiment, ActionType
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()


def main():
    """Fonction principale qui coordonne tous les agents"""

    # === ETAPE 1 : LIRE L'ARGUMENT --target_dir ===
    parser = argparse.ArgumentParser(
        description="Refactoring Swarm - Systeme multi-agents"
    )
    parser.add_argument(
        "--target_dir",
        type=str,
        required=True,
        help="Dossier contenant le code Python a analyser"
    )
    args = parser.parse_args()

    # === ETAPE 2 : VERIFIER QUE LE DOSSIER EXISTE ===
    target_directory = Path(args.target_dir)

    if not target_directory.exists():
        print(f"ERREUR : Le dossier {args.target_dir} n'existe pas.")

        log_experiment(
            agent_name="System",
            model_used="N/A",
            action=ActionType.DEBUG,
            details={
                "input_prompt": f"Verification dossier {args.target_dir}",
                "output_response": "Dossier introuvable",
                "error": "Directory not found"
            },
            status="FAILED"
        )

        # Cas critique : dossier absent
        sys.exit(1)

    # === ETAPE 3 : DEMARRAGE DU SYSTEME ===
    print("DEMARRAGE DU REFACTORING SWARM")
    print(f"Dossier cible : {args.target_dir}")
    print("=" * 70)

    log_experiment(
        agent_name="System",
        model_used="N/A",
        action=ActionType.ANALYSIS,
        details={
            "input_prompt": f"Initialisation sur {args.target_dir}",
            "output_response": "Systeme demarre",
            "target_directory": str(target_directory)
        },
        status="SUCCESS"
    )

    try:
        # === PHASE 1 : ANALYSE (AUDITEUR) ===
        print("\nETAPE 1 : ANALYSE PAR L'AUDITEUR")
        print("-" * 70)

        # Simulation temporaire
        audit_result = {
            "files_analyzed": [],
            "issues_found": [],
            "pylint_score_before": 0.0
        }

        print("Agent Auditeur non implemente (simulation)")

        # === PHASE 2 : BOUCLE DE CORRECTION ===
        max_iterations = 10
        iteration = 0
        all_tests_passed = False

        print("\nDEMARRAGE DE LA BOUCLE DE CORRECTION")
        print("=" * 70)

        while iteration < max_iterations and not all_tests_passed:
            iteration += 1

            print("=" * 70)
            print(f"ITERATION {iteration}/{max_iterations}")
            print("=" * 70)

            # --- FIXER ---
            print("Correction par le Fixer...")
            fix_result = {
                "files_modified": [],
                "changes_applied": 0,
                "status": "NOT_IMPLEMENTED"
            }
            print("Agent Fixer non implemente (simulation)")

            # --- JUDGE ---
            print("Tests par le Judge...")
            test_result = {
                "all_passed": False,
                "total_tests": 0,
                "failed_tests": [],
                "error_logs": ""
            }
            print("Agent Judge non implemente (simulation)")

            if test_result.get("all_passed", False):
                all_tests_passed = True
                print("SUCCES : tous les tests sont passes")

                log_experiment(
                    agent_name="System",
                    model_used="N/A",
                    action=ActionType.FIX,
                    details={
                        "iterations_needed": iteration
                    },
                    status="SUCCESS"
                )
                break
            else:
                print("Des problemes persistent, nouvelle tentative...")

        # === PHASE 3 : RAPPORT FINAL ===
        print("\n" + "=" * 70)
        print("RAPPORT FINAL")
        print("=" * 70)
        print(f"Iterations effectuees : {iteration}/{max_iterations}")
        print(f"Statut : {'SUCCES' if all_tests_passed else 'ANALYSE TERMINEE'}")
        print(f"Dossier analyse : {target_directory}")
        print("=" * 70)

        # IMPORTANT POUR LES TESTS :
        # L'execution s'est bien deroulee -> code 0
        sys.exit(0)

    except Exception as e:
        print("ERREUR CRITIQUE")
        print(f"Type : {type(e).__name__}")
        print(f"Message : {str(e)}")

        log_experiment(
            agent_name="System",
            model_used="N/A",
            action=ActionType.DEBUG,
            details={
                "error_type": type(e).__name__,
                "error_message": str(e)
            },
            status="FAILED"
        )

        sys.exit(1)


if __name__ == "__main__":
    main()
