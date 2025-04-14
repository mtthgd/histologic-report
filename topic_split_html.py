import re
import os 


input_dir = "raw_data_html"
output_base_dir = "topic_split"

# Créer le dossier principal s'il n'existe pas
os.makedirs(output_base_dir, exist_ok=True)


for filename in os.listdir(input_dir):
    if filename.endswith('html'):
        file_path = os.path.join(input_dir, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            data = f.read()

        topic_name = filename.replace(".html", "")
        output_dir = os.path.join(output_base_dir, topic_name)
        os.makedirs(output_dir, exist_ok=True)

        # Ici ce sépare mes données à chaque topic 
        splits = data.split('<div class="topic_divider_title">')[1:] #on split le html sur tout les titre de topic et on enlève l'entête 
        
        # je boucle dans tout les splits à partir des data 
        for idx, split in enumerate(splits):
            match = re.search(r'^(.*?)</div>', split) #je cherche ma regexp dans la chaine de caractère que je lui renseigne donc ici split 
            if match:
                titre = match.group(1).strip() #si il trouve qqc on prend ce qui est a l'intérieur de la balise avec group() et on enlève les espaces inutiles avec strip()
                titre = "".join(c for c in titre if c.isalnum() or c in " _-").strip()

            output_path = os.path.join(output_dir, f"{titre}.html")

            # Reconstituer le bloc HTML
            full_block = f'<div class="topic_divider_title">{split}'

            with open(output_path, "w", encoding="utf-8") as out:
                out.write(full_block)
         
