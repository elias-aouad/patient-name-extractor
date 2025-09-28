# Patient Name Extractor

A FastAPI-based service that extracts patient names and gender information from medical documents using OCR data.


## API Endpoints

### Health Check

- `GET /liveness`

- Returns service health status and API version.

- **CLI** : `curl -X GET 'http://0.0.0.0:8080/liveness'`

- **Expected output** : 
```json
{"health_check":"OK","api_version":"v0.1.0"}
```

### Extract Patient Name

- `POST /extract_name`

- Extracts patient information from a document.

- **CLI** (example) :

```
curl -X POST \
  'http://0.0.0.0:8080/extract_name' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d @example.json
```


- **Expected response:**
```json
{"gender": "male", "first_name": "Jean", "last_name": "Dupont"}
```

## Installation

### Prerequisites
- Python 3.12+
- `uv` package manager

### Setup
1. Clone the repository:
```bash
git clone <repository-url>
cd patient-name-extractor
```

2. Create virtual environment and install dependencies:
```bash
make env
```

## Usage

### Running the Service

- Option 1:
```bash
make run
```


- Option 2: if you prefer the containerized version :
```bash
docker build . -t patient-extractor
docker run -p 8080:8080 patient-extractor
```

- In both ways, the service will be available at `http://localhost:8080`



### API Documentation
Once running, visit `http://localhost:8080/docs` for interactive API documentation.

### Testing
```bash
make test
```

### Code Quality
```bash
# Lint code
make lint

# Fix linting issues
make lint-fix

# Format code
make format
```

## Ideas for future work

For now, the service will only match the patient name based on a regex pattern based on a list of hot words that we selected (such as `Monsieur`ro `Madame` etc...).

But :

1. What if the list of hot words is incomplete ?
2. Or what if the reconstructed text was not perfect - and hence introduced a misalignment in the text ? And hence what if the word we catched was not a name ?


To answer each of these questions seperately :

1. We can awlays complete it : each time we do not catch a patient name within a document, we can suppose that the prefix in this document was not part of our hotword list. We can extract it using a LLM, and if a prefix is indeed extracted, we append it to the list of hot words that we defined (hard-coded for now, could be seperated from the code as a SQL database)

2. For sanity check, we can use a database of public first names / last names, and each time our regex matched a first and last name, we then try to match it with our databse of first / last names. If no match at all, we can log them in a seperate service to validate / infirm these detected names - in which case we either deny these names, or we update our existing database with new names.
