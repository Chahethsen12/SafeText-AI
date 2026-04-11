# SafeText AI

SafeText AI is an advanced machine learning API and web interface designed for text normalization and sanitization. It uses a combination of DistinctBERT for sensitivity classification and a PEFT fine-tuned TinyLlama model to normalize and clean corrupted text dynamically.

## Features
- **Sensitivity Classification**: Uses DistinctBERT to classify text risk levels (LOW, MEDIUM, HIGH).
- **Text Normalization**: Utilizes a LoRA fine-tuned TinyLlama model to remove invisible characters, homoglyphs, and adversarial patterns.
- **Flask REST API**: Exposes inference capabilities through a straightforward API endpoint.
- **Web Interface**: Includes a responsive web interface for easy accessibility and testing.

## Prerequisites

- Python 3.8+
- The `models` directory containing the appropriately fine-tuned models (`distinctbert-safetext` and `tinyllama-safetext-lora`). *Note: Models are not included in the source control due to size constraints.*

## Installation

1. Clone the repository:
   ```bash
   git clone <your-github-repo-url>
   cd SafeText_App
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Navigate your browser to `http://127.0.0.1:5000` to interact with the web interface.

## API Endpoint
You can also interact programmatically via the `/api/process` POST endpoint. Provide a JSON payload with a `text` key.

```json
{
  "text": "Your potentially unsafe text here..."
}
```

## Structure
- `app.py`: Main Flask server entrypoint and model loading.
- `preprocess.py`: Helper functions for text preparation.
- `templates/`: HTML interface templates.
- `static/`: Supporting JS/CSS files.
- `requirements.txt`: Python package requirements.
