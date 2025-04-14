from markitdown import MarkItDown
import os 
from tqdm import tqdm 

md = MarkItDown(enable_plugins=False) # Set to True to enable plugins

#Conversion de tout les topics .html en .md // Changer l'input_dir en fonction des fichiers qu'on veut convertir, initialement j'ai mis topic_split mais après j'ai mis histo_description 
input_dir = "/Users/matthieuguillard/Desktop/CODE/scraping/topic_split"

for subdir in os.listdir(input_dir):
    subdir_path = os.path.join(input_dir, subdir)

    if os.path.isdir(subdir_path):
        for filename in tqdm(os.listdir(subdir_path), desc=subdir):
            if filename.endswith(".html"):
                html_path = os.path.join(subdir_path, filename)

                # Conversion
                result = md.convert(html_path)

                title = filename.replace(".html", "").replace("_", " ").strip()

                # Garde le nom du fichier.html vers le .md 
                md_filename = filename.replace(".html", ".md")
                md_path = os.path.join(subdir_path, md_filename)

                # Écriture du fichier .md
                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(f"# {title}\n\n")
                    f.write(result.text_content)