from bs4 import BeautifulSoup
from pathlib import Path
import re
import json


TOPIC_SPLIT_DIR = Path("topic_split")
OUTPUT_DIR = Path("qcm_bank/question.json")
OUTPUT_DIR.parent.mkdir(parents=True, exist_ok=True)




def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def extract_question_number(title: str):
    match = re.search(r"#(\d+)", title)
    return int(match.group(1)) if match else None


def parse_topic_page(html_path: Path) -> dict:

    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")


    organ = html_path.parent.name
    topic_tag = soup.find("div", class_="topic_divider_title")
    topic = clean_text(topic_tag.get_text()) if topic_tag else html_path.stem

    data = {
        "organ": organ,
        "topic": topic,
        "source_file": str(html_path),
        "questions": []
    }

    blocks = soup.find_all("div", class_="block_section")

    current_question = None

    for block in blocks:
        title_tag = block.find("div", class_="topicheading_title")
        body_tag = block.find("div", class_="block_body")

        if not title_tag or not body_tag:
            continue

        title = clean_text(title_tag.get_text())


        if title.lower().startswith("board review style question"):
            q_number = extract_question_number(title)

            # --- IMAGES ---
            images = []
            for img in body_tag.find_all("img"):
                src = img.get("src")
                if src:
                    images.append(src)

            # --- ANSWERS ---
            answers = []
            ol = body_tag.find("ol")

            if ol:
                for i, li in enumerate(ol.find_all("li"), start=1):
                    answers.append({
                        "label": chr(64 + i),  # A, B, C...
                        "text": clean_text(li.get_text(" ", strip=True)),
                        "is_correct": False
                    })
                ol.extract()  # important → pour ne pas polluer le texte

            # --- QUESTION TEXT ---
            question_text = clean_text(body_tag.get_text(" ", strip=True))

            current_question = {
                "question_number": q_number,
                "question_text": question_text,
                "images": images,
                "answers": answers,
                "explanation": ""
            }

 
        elif title.lower().startswith("board review style answer") and current_question:
            body_text = clean_text(body_tag.get_text(" ", strip=True))

            # --- BONNE RÉPONSE ---
            correct_tag = body_tag.find("b")
            correct_label = None

            if correct_tag:
                correct_label = clean_text(correct_tag.get_text()).replace(".", "").upper()

            for ans in current_question["answers"]:
                if ans["label"] == correct_label:
                    ans["is_correct"] = True

            # --- EXPLANATION ---
            explanation = re.sub(r"^[A-Z]\.?\s*", "", body_text).strip()

            current_question["explanation"] = explanation

            # --- AJOUT ---
            data["questions"].append(current_question)
            current_question = None

    return data

if __name__ == "__main__":
    all_data = []

    for html_file in TOPIC_SPLIT_DIR.rglob("*.html"):
        topic_data = parse_topic_page(html_file)
        all_data.append(topic_data)


    with open(OUTPUT_DIR, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    print(f"Parsed {len(all_data)} topics and saved to {OUTPUT_DIR}")