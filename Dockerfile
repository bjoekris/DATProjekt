FROM python:3.10-slim

WORKDIR /Converter

COPY Converter/ /Converter/

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    libmagic1 && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "ConverterAPI:app", "--host", "0.0.0.0", "--port", "8000"]
