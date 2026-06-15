FROM python:3.12.4-slim

WORKDIR /app
COPY . /app

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir torch==2.9.1 torchaudio==2.9.1

RUN pip install --no-cache-dir -r requirements.txt --no-deps

CMD ["sh", "-c", "python -m app.main && python -m app.bot"]
