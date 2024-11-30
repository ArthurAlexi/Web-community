FROM python:3.10-slim

WORKDIR /comunity

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libsqlite3-dev \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . /comunity/

EXPOSE 5000

CMD ["python", "main.py"]
