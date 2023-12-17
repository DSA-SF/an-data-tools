FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV POSTGRES_URI=postgresql://postgres:postgres@postgres:5432/postgres
ENV AN_API_KEY=an_api_key

# Run the Python application
CMD ["python", "src/main.py"]
