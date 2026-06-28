---
title: SelfText AI
emoji: 🛡️
colorFrom: red
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---

# 🛡️ SelfText-AI

**Advanced adversarial text detection, normalization, and sanitization powered by DistilBERT and TinyLlama.**

SelfText-AI is a high-performance, dual-model machine learning pipeline built to detect and neutralize adversarial text—including invisible characters, homoglyph substitutions, and prompt injection patterns. Deployed natively on Hugging Face Spaces, it combines a fine-tuned DistilBERT classifier for risk-level detection with a PEFT LoRA-adapted TinyLlama model for intelligent text normalization, exposing its capabilities via a Flask REST API and an interactive web interface.

---

## 🚀 Live Deployment

SelfText-AI is actively hosted on Hugging Face Spaces using a Docker runtime environment.
- **Hugging Face Space**: [Chahethsen/SafeText-AI](https://huggingface.co/spaces/Chahethsen/SafeText-AI)
- **Infrastructure**: Python 3.11-slim Base Docker Image
- **Server**: Gunicorn running on port `7860`

---

## ✨ Core Features

| Feature | Description | Architecture |
| :--- | :--- | :--- |
| **🚨 Sensitivity Classification** | Classifies incoming text streams as `LOW`, `MEDIUM`, or `HIGH` risk. | Fine-tuned **DistilBERT** (`Chahethsen/distinctbert-safetext`) |
| **🧹 Intelligent Normalization** | Strips invisible characters, homoglyphs, and adversarial patterns. | LoRA fine-tuned **TinyLlama** (`Chahethsen/tinyllama-safetext-lora`) |
| **🌐 RESTful API** | A programmatic POST endpoint for seamless enterprise integration. | Flask + Gunicorn |
| **🖥️ Interactive UI** | Responsive web interface for real-time visualization and testing. | HTML5 + CSS3 / Jinja2 |
| **🗄️ Persistence Layer** | Scalable, document-based storage for logging and analytics. | **MongoDB** |

---

## 🏗️ Architecture & Model Loading

SafeText-AI has evolved from a local-only implementation to a cloud-native architecture. 

**Dynamic Model Provisioning:**
Model weights are *no longer hosted locally*. Upon initialization, `app.py` dynamically streams the required models directly from the Hugging Face Hub:
1. `Chahethsen/distinctbert-safetext` (Classifier & Tokenizer)
2. `Chahethsen/tinyllama-safetext-lora` (LoRA Adapter & Tokenizer)

**Infrastructure Optimization:**
To accommodate the Hugging Face Spaces free tier limits (16GB System RAM, No GPU), the container is explicitly configured to load the TinyLlama PEFT architecture natively on **standard CPU precision**. This prevents disk thrashing and out-of-memory exceptions while maintaining inference stability.

---

## 🗂️ Project Structure

```text
SelfText-AI/
├── Dockerfile              # Docker runtime configuration (Python 3.11-slim)
├── app.py                  # Flask REST API, Gunicorn entry point & HF Hub integration
├── preprocess.py           # Text sanitization and tokenization pipelines
├── requirements.txt        # Production Python dependencies
├── templates/              # Jinja2 HTML rendering templates
└── static/                 # Front-end CSS & JavaScript assets
```

---

## ⚙️ Local Development Setup

To run the application in a local testing environment, execute the following commands in your terminal:

```bash
# 1. Clone the repository
git clone https://github.com/YourUsername/SelfText-AI.git
cd SelfText-AI

# 2. Create and activate a virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Start the Flask application
python app.py
```

---

## 📡 API Reference

### `POST /api/process`

Analyzes and normalizes a given text payload.

**Request Body:**
```json
{
  "text": "Your adversarial or corrupted string here..."
}
```

**Successful Response:**
```json
{
  "original_text": "Your adversarial or corrupted string here...",
  "normalized_text": "...",
  "processed_text": "...",
  "classifier_input_used": "processed_text",
  "sensitivity_level": "HIGH",
  "confidence": "98.45%",
  "cleaned_text": "Cleaned string ready for downstream consumption.",
  "probabilities": {
    "LOW": 0.005,
    "MEDIUM": 0.010,
    "HIGH": 0.985
  }
}
```
