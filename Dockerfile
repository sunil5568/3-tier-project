FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN mkdir -p data

EXPOSE 5000

CMD ["python", "app.py"]