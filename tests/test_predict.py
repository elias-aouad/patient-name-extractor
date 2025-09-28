import json
import pytest
from patient_name_extractor.extractor.predict import extract_patient_info
from patient_name_extractor.extractor.interfaces import (
    Document,
    Page,
    Word,
    BoundingBox,
)


def create_document_from_text(text: str) -> Document:
    words = []
    for i, word_text in enumerate(text.split()):
        word = Word(
            text=word_text,
            bbox=BoundingBox(
                x_min=i * 0.1,
                x_max=i * 0.1 + 0.05,
                y_min=0.1,
                y_max=0.15,
            ),
        )
        words.append(word)
    page = Page(words=words)
    return Document(pages=[page], original_page_count=1, needs_ocr_case="no_ocr")


@pytest.mark.parametrize(
    "text,expected_first,expected_last,expected_gender",
    [
        ("Monsieur Jean Dupont", "Jean", "Dupont", "male"),
        ("Mr Pierre Martin", "Pierre", "Martin", "male"),
        ("M. Jacques Bernard", "Jacques", "Bernard", "male"),
        ("Madame Marie Dubois", "Marie", "Dubois", "female"),
        ("Mme Sophie Laurent", "Sophie", "Laurent", "female"),
        ("Mademoiselle Claire Moreau", "Claire", "Moreau", "female"),
        ("Mlle Anne Petit", "Anne", "Petit", "female"),
        ("monsieur jean dupont", "Jean", "Dupont", "male"),
        ("Monsieur François André", "François", "André", "male"),
        ("Le patient Monsieur Jean Dupont est arrivé", "Jean", "Dupont", "male"),
        ("  Monsieur   Jean   Dupont  ", "Jean", "Dupont", "male"),
    ],
)
def test_extract_valid_patients(text, expected_first, expected_last, expected_gender):
    document = create_document_from_text(text)
    result = extract_patient_info(document)

    assert result is not None
    assert result.first_name == expected_first
    assert result.last_name == expected_last
    assert result.gender == expected_gender


@pytest.mark.parametrize(
    "text",
    [
        "This is just some random text",
        "Résultats des tests sanguins",
    ],
)
def test_extract_invalid_cases(text):
    document = create_document_from_text(text)
    result = extract_patient_info(document)
    assert result is None


def test_extract_patient_info_from_example_document():
    with open("example.json", "r") as f:
        json_document = json.load(f)
    document = Document.model_validate(json_document)
    result = extract_patient_info(document)
    assert result is not None
    assert result.first_name == "Jean"
    assert result.last_name == "Dupont"
    assert result.gender == "male"
