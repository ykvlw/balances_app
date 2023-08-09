FROM python:3.11.4-slim-buster

WORKDIR /app
COPY . /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]