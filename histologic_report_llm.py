from ..config.config import load_config, Config
from ollama import Client
import os 


class Histologic_report_writer():
    def __init__(self):
        self.config = load_config(os.path.abspath(...), Config)
        self._ollama_client = Client(host=self._config.ollama.host)
        self._model = self._config.ollama.model


    def report_writer(description_histo: str) -> str: 
        prompt = f"""
    Voici une description histologique sous forme de bullets points concernant une pathologie : 

    {description_histo}

    Transforme ce texte structuré (bullets points) en texte narratif fluide de type compte-rendu médical d'anatomopathologie rédigé en francais en reprenant chaque bullet point. Supprime les références à des articles scientifiques si ils sont mentionnés. Chaque compte-rendu doit refléter uniquement les informations présentes dans le texte source. Rédige un compte-rendu distinct pour chaque variante décrite si besoin. La conclusion de chaque compte-rendu doit être concise et ne reprendre que les informations essentielles et discriminantes. 
    """
        messages = [
            {"role": "system", "content": "Tu es un médecin anatomopatholigiste expert dans la rédaction de compte-rendus médicaux"}
            {"role": "user", "content": prompt}
            ]
        response = response["message"]["content"]
        return response 
    
    def processing_all_files(self, input_dir=..., output_file=...):

        all_report = []

        for subdir in os.listdir(input_dir):
            subdir_path = os.path.join(input_dir, subdir)

            for filename in subdir_path:
                with open(filename, "r") as f:
                    description_histo = f.read()

                medical_report = report_writer(description_histo)
                title = filename.replace(".md", "")
                resume = f"#{title}\n\n{medical_report}\n\n---\n"
                all_report.append(resume)

            print(f"compte-rendu généré pour : {filename}")

        with open(output_file, "w", encoding="utf-8") as f:
            f.writelines(all_report)

        print(f"tous les comptes-rendus sont dans {output_file}")