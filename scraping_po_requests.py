import requests
import time 
import random

# 

header_ = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    "Referer": "https://www.pathologyoutlines.com"
    
}



# pages_to_do = [
#     "autopsy", "bladder", "bone", "bonemarrowneoplastic",
#     "bonemarrownonneoplastic", "breast", "cervix", "cns", "cnstumor", "coagulation", "colon",
#     "ear", "esophagus", "eye", "fallopiantubes", "heart", "hematology",
#     "kidney", "kidneytumor", "larynx", "liver", "lung", "lymphnodes", "lymphoma",
#     "mandiblemaxilla", "mediastinum", "muscle", "nasal", "oral", "ovary", "pancreas",
#     "penis", "placenta", "pleura", "prostate", "salivaryglands", "skinmelanocytictumor",
#     "skinnonmelanocytictumor", "skinnontumor", "smallbowel", "softtissue", "stomach",
#     "testis", "thyroid", "uterus", "vulva"
# ]

# pages_restant = ['skintumormelanocytic', 'oralcavity', 'bonemarrow', 'penscrotum', 'cns', 'skintumornonmelanocytic']
pages_restantes = ['cns']

session = requests.Session()
l = []


for page in pages_restantes:
    topic = f'https://www.pathologyoutlines.com/{page}.html'
    superpage = f"https://www.pathologyoutlines.com/superpage/{page}.html"

    print(f"Scraping {topic}")

    r = session.get("https://www.pathologyoutlines.com", headers=header_)
    

    if r.status_code == 200:
        time.sleep(random.uniform(1,3))
        r = session.get(topic, headers=header_)

        if r.status_code == 200:
            time.sleep(random.uniform(3,6))
            r = session.get(superpage, headers=header_)

            if r.status_code == 200:
                with open(f"raw_data_html/{page}.html", "w", encoding="utf-8") as f:
                    f.write(r.text)
            else:
                print(f"superpage erreur {r.status_code} pour {superpage}")
                l.append(page)
        else:
            print(f"Topic page erreur {r.status_code} pour {topic}")
            l.append(page)

    time.sleep(random.uniform(10, 15))

print(f"Nb de pages qui n'ont pas fonctionnées : {len(l)}")
print(l)
