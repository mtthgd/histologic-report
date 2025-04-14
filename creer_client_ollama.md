# Structure minimale pour utiliser Ollama dans un projet : 

Un client Ollama est un objet qui permet d'envoyer un msg à un LLM et de récupérer la réponse. On télécharge un model sur son PC que l'on fait tourner localement (ex: http://localhost:11434), et le client sert à lui parler via un script python 

## Ce qu'il faut : 
- un **fichier de config YAML** avec le nom du model et l'adresse du serveur ollama :
```
ollama:
    host: "https://localhost:11434"
    model: "llama3"
```
- Une **classe python**: 

    - un constructeur __init__ qui lit le fichier config : 
        - *lire le fichier config*
            self._config = load_config(os.path.abspath("chemin/vers/config.yaml"), Config)
        - *recupere le nom du model*(à partir du fichier config)
            self._model = self._config.ollama.model 
        - *crée le client ollama* (connexion avec le serveur)
            self._ollama_client = Client(host=self._config.ollama.host)

        Etant donné qu'on recupere les infos d'un .YAML on pourrait également écrire :
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        self.host = config["ollama"]["host"]
        self.model = config["ollama"]["model"]
        self.Client = Client(host=self.host)

Rq : le fait de stocker le nom du model dans self._model permet de l'utiliser dans des méthodes plutôt que d'avoir redemander au fichier config à chaque fois
    
    - différentes méthodes pour appeler le modèle avec des prompts 
        - Exemple :
            ```python
            def generer_text(self, prompt: str) -> str:
                messages = [{"role":"user", "content": prompt }]
                response = self._ollama_client.chat(self.model, messages=messages)
                return response["message"]["content"]
            ```

Rq : 
- la variable messages permet de preparer notre input au format "chat"
- la variable response envoie notre message au model 
    - self._ollama_client.chat(...) => "hé j'ai une question pour le modèle, voici ce que je veux lui dire"  
    - la réponse de .chat(...) est un dictionnaire :
    {
        "message": {
            "role" : "assistant",
            "content" : "Voici la réponse du modèle"
        }
    }

    => donc pour récupérer la réponse générée par le modèle on fait response["message"]["content"]

### "role": 

Indique le rôle de celui qui parle dans la conversation, en général il y a 3 principaux rôles : 
- *"system"* : permet de définir le contexte ou la personnalité du modèle 
    - Ex : "tu es un expert en anatomopathologie"
-*"user"*: toi, l'utilisateur qui pose une question 
-*"assistant"*: le modèle LLM qui répond 