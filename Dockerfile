FROM python:3.10-slim AS builder

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# UPDATED CLEANUP: We no longer delete the 'tests' directories
RUN find /opt/venv -type d -name "__pycache__" -exec rm -r {} + \
    && rm -rf /root/.cache

FROM python:3.10-slim

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv

COPY offline_analyzer.py .
COPY models/ ./models/
COPY nltk_data/ ./nltk_data/

ENV PATH="/opt/venv/bin:$PATH"

ENTRYPOINT ["python", "offline_analyzer.py"]
CMD ["--help"]