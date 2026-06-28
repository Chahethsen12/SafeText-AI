FROM python:3.11-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1

COPY . /app

# Upgrade pip, explicitly point to PyTorch CPU wheel index, then install the rest
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 7860
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app", "--timeout", "300"]