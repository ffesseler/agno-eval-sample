import os
import json
from langfuse import Langfuse
from dotenv import load_dotenv

load_dotenv()

try:
    langfuse = Langfuse()
    print("Connexion à Langfuse réussie.")
except Exception as e:
    print(f"Erreur lors de l'initialisation de Langfuse. Vérifiez vos clés API. Erreur: {e}")
    exit()


DATASET_NAME = "evaluation-set"
CASES_DIRECTORY = "evaluation_cases"

try:
    if not langfuse.get_dataset(DATASET_NAME):
        langfuse.create_dataset(name=DATASET_NAME)
        print(f"Dataset '{DATASET_NAME}' créé avec succès.")
    else:
        print(f"Dataset '{DATASET_NAME}' trouvé. Aucun nouvel item ne sera ajouté pour éviter les doublons.")
        # print(f"Dataset '{DATASET_NAME}' existe déjà. Il va être vidé et recréé.")
        # langfuse.delete_dataset(DATASET_NAME)
        # langfuse.create_dataset(name=DATASET_NAME)

except Exception as e:
    print(f"Une erreur est survenue lors de la gestion du dataset : {e}")
    try:
        langfuse.create_dataset(name=DATASET_NAME)
        print(f"Dataset '{DATASET_NAME}' créé suite à une erreur de récupération.")
    except Exception as create_e:
        print(f"Impossible de créer le dataset non plus. Erreur: {create_e}")
        exit()


dataset = langfuse.get_dataset(DATASET_NAME)

print(f"Début de l'import des cas depuis le dossier '{CASES_DIRECTORY}'...")

for filename in os.listdir(CASES_DIRECTORY):
    if filename.endswith('.json'):
        file_path = os.path.join(CASES_DIRECTORY, filename)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            input_data = data["input"]
            expected_output_data = data["ground_truth"]

            try:
                langfuse.create_dataset_item(
                    dataset_name=DATASET_NAME,
                    input=input_data,
                    expected_output=expected_output_data,
                    id=data.get("case_id", filename) 
                )
                print(f"  - Cas '{filename}' importé avec succès.")
            except Exception as e:
                if "already exists" in str(e):
                    print(f"  - Cas '{filename}' (ID: {data.get('case_id', '')}) existe déjà. Ignoré.")
                else:
                    print(f"  - Erreur lors de l'import de '{filename}': {e}")


print("\nImportation terminée !")
print(f"Vérifiez le dataset '{DATASET_NAME}' dans votre projet Langfuse.")