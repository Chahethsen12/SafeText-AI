# Use Python 3.11 to support your modern torch and numpy versions
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Ensure standard output is not buffered
ENV PYTHONUNBUFFERED=1

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# The application listens on port 7860 (Hugging Face Spaces default)
EXPOSE 7860

# Run gunicorn to serve the Flask app
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app", "--timeout", "300"]