import re, os 
from bs4 import BeautifulSoup

input_dir = "topic_split"
output_dir = "histo_description"

# je crée le dossier histo_description 
os.makedirs(output_dir, exist_ok=True)

# regexp pour matcher l'id qui commence tjrs par la même string mais qui a des chiffres différents ensuite 
pattern = re.compile("^microscopichistologicdescription")


for subdir in os.listdir(input_dir):
    subdir_path = os.path.join(input_dir, subdir)
    output_subdir = os.path.join(output_dir, subdir)

    if os.path.isdir(subdir_path):
        os.makedirs(output_subdir, exist_ok=True)

        for filename in os.listdir(subdir_path):
            if filename.endswith(".html"):
                html_path = os.path.join(subdir_path, filename)
                output_path = os.path.join(output_subdir, filename)
                
                # on ouvre le fichier pour le donner en input a beautifulsoup 
                with open(html_path, "r") as f:
                    html = f.read()


                    # on crée un objet beautifulsoup et on extrait la description histo 
                soup = BeautifulSoup(html, "html.parser")
                histo = soup.find("div", id=pattern)

                if histo: 
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(str(histo))

                    
                    