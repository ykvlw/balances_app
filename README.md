# Balances APP

## To start the app:
1. Create a `.env` file with the following variables:
    - `MONGO_URI=` 


2. Run the following command:
             
       docker-compose up

## Endpoints:
      
- http://127.0.0.1:8000/docs  - Swagger UI  
- http://127.0.0.1:8000/redoc - Docs UI

## To run the tests:

        docker-compose run --rm  app pytest tests.py -v