from fastapi import FastAPI

from patient_name_extractor import API_VERSION
from patient_name_extractor.extractor.interfaces import Document, Patient
from patient_name_extractor.extractor.predict import extract_patient_info

app = FastAPI()


@app.get("/liveness")
def home():
    """
    Basic call to get the liveness of the service
    """
    return {"health_check": "OK", "api_version": API_VERSION}


@app.post("/extract_name", response_model=Patient | None)
def extract_name(payload: Document):
    """
    Main function to return the detected patient info from the API call
    """
    patient_info = extract_patient_info(document=payload)

    if patient_info is None:
        return None
    return patient_info.model_dump(mode="json")
