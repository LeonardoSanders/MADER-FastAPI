import re


def normalize_text(text: str):
    text_normalized = ' '.join(text.split()).strip().lower()
    text_cleaned = re.sub(r'[^a-zA-A\s]', '', text_normalized)

    return text_cleaned
