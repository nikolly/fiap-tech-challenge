# Embrapa API

This is the documentation for the Embrapa project API, which includes endpoints for processing production data, import/export and more.

## Índice

- [Embrapa API](#embrapa-api)
  - [Índice](#índice)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Docs](#docs)
  - [API Client](#api-client)
  - [Tests](#tests)
  - [Authentication](#authentication)
    - [Obtaining Token JWT](#obtaining-token-jwt)
  - [Api Routes](#api-routes)
    - [Production](#production)
    - [Sales](#sales)
    - [Processing](#processing)
    - [Exportação](#exportação)
    - [Importação](#importação)

## Installation

1. Clone the repository: `git clone https://github.com/your-username/fiap-tech-challenge.git`
2. Navigate to the project directory: `cd fiap-tech-challenge`
3. Run in terminal `python -m venv venv`
4. Start the virtual environment `source venv/bin/activate`  # Linux/Mac
                                 `venv\Scripts\activate`  # Windows
5. Install the dependencies: `pip install -r requirements.txt`

## Usage

1. Start the application: `./run.sh`
2. Open your browser and go to `http://localhost:8000/embrapa/production`

## Docs

1. Open your browser and go to `http://localhost:8000/docs` to find the API documentation in OpenAPI

## API Client

1. In the api_client folder there are some examples of requests prepared that you can use for interacting with the APIs.
2. The platform chosen to prepare these requests was [Bruno](https://github.com/usebruno/bruno), you can import the requests from the file api_client_bruno.json to it.
3. The project also contains a file that you can import in postman, its name is api_client_postman.json.

## Tests

We have tests prepared for the login API.
To run the tests you can run in the terminal `pytest`.

## Authentication

The authentication is based in JWT. Use the login enndpoint to obtain a token and add it inside the header `Authorization` as `Bearer <token>` in all the other requests.

### Obtaining Token JWT

Example of request to obtain the token:

`curl --request POST \
  --url http://127.0.0.1:8000/api/login/ \
  --data '{
  "username": "fiap",
  "password": "fakehashedpassword"
}'`

## Api Routes

Response example:

`{
  "items": [
    {
      "id": "1",
      "name": "VINHO DE MESA",
      "data": [
        {
          "year": 1970,
          "value": 217208604
        },
        {
          "year": 1971,
          "value": 154264651
        }
      ]
    }
  ]
}`

### Production

`POST /api/embrapa/production`
Process production data.

### Sales

`POST /api/embrapa/sales`
Process sales data.

### Processing

`POST /api/embrapa/processing/vinifera`
Process vinifera data.

`POST /api/embrapa/processing/americanAndHybrid`
Process American and Hybrid data.

`POST /api/embrapa/processing/tableGrapes`
Process table grapes data.

`POST /api/embrapa/processing/noClassification`
Process no classification data.

### Exportação

`POST /api/embrapa/exportation/tableGrapes`
Process table grapes data of exportation.

`POST /api/embrapa/exportation/sparklingWines`
Process sparkling wines data of exportation.

`POST /api/embrapa/exportation/freshGrapes`
Process fresh grapes data of exportation.

`POST /api/embrapa/exportation/grapeJuice`
Process grape juice data of exportation.

### Importação

`POST /api/embrapa/importation/tableGrapes`
Process table grapes data of importation.

`POST /api/embrapa/importation/sparklingWines`
Process sparkling wines data of importation.

`POST /api/embrapa/importation/freshGrapes`
Process fresh grapes data of importation.

`POST /api/embrapa/importation/raisins`
Process raisins data of importation.

`POST /api/embrapa/importation/grapeJuice`
Process grape juice data of importation.
