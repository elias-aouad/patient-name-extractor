import re

from patient_name_extractor.extractor.document_utils import (
    reconstruct_text_from_document,
)
from patient_name_extractor.extractor.interfaces import Document, Patient

MALE_PATIENT = ["monsieur", "m.", "mr", "m "]
FEMALE_PATIENT = ["madame", "mademoiselle", "mme", "mlle"]
REGEX_PATTERN = r"\b(?:{})\s+([A-ZÉÈÊÀÂÇÔÛÎ][a-zéèêàâçôûî]+)\s+([A-ZÉÈÊÀÂÇÔÛÎ][a-zA-ZÉÈÊÀÂÇÔÛÎ\-]+)\b"


def extract_patient_info(document: Document) -> Patient | None:
    text = reconstruct_text_from_document(document=document).lower()

    # Build regex patterns dynamically
    male_pattern = REGEX_PATTERN.format("|".join(MALE_PATIENT))
    female_pattern = REGEX_PATTERN.format("|".join(FEMALE_PATIENT))

    match = re.search(male_pattern, text, flags=re.IGNORECASE)
    if match:
        # then we know it's a male patient
        first, last = match.groups()
        return Patient(
            first_name=first.capitalize(), last_name=last.capitalize(), gender="male"
        )

    match = re.search(female_pattern, text, flags=re.IGNORECASE)
    if match:
        first, last = match.groups()
        return Patient(
            first_name=first.capitalize(), last_name=last.capitalize(), gender="female"
        )

    return None
