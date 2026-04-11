<div align="center">

# 🛡️ SafeText AI

**Advanced adversarial text detection, normalization, and sanitization powered by DistilBERT and TinyLlama.**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-REST%20API-000000?style=flat&logo=flask)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![HuggingFace](https://img.shields.io/badge/🤗%20Models-DistilBERT%20%7C%20TinyLlama-FFD21E)](https://huggingface.co/)

</div>

---

## 📌 Overview

SafeText AI is a dual-model machine learning pipeline built to detect and neutralize adversarial text — including invisible characters, homoglyph substitutions, and prompt injection patterns. It combines a fine-tuned **DistilBERT classifier** for risk-level detection with a **LoRA-adapted TinyLlama** model for intelligent text normalization, exposed through both a **Flask REST API** and an interactive **web interface**.

> ⚠️ **Note:** Pre-trained model weights (`distinctbert-safetext` and `tinyllama-safetext-lora`) are not included in this repository due to size constraints. See [Model Setup](#-model-setup) below.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Sensitivity Classification** | DistilBERT-based classifier labels text as `LOW`, `MEDIUM`, or `HIGH` risk |
| 🧹 **Text Normalization** | LoRA fine-tuned TinyLlama removes invisible characters, homoglyphs & adversarial patterns |
| ⚡ **REST API** | Simple POST endpoint for programmatic integration |
| 🌐 **Web Interface** | Responsive UI for real-time testing and visualization |

---

## 🗂️ Project Structure

```
SafeText_App/
├── app.py                  # Flask server entry point & model loading
├── preprocess.py           # Text preprocessing utilities
├── requirements.txt        # Python dependencies
├── models/                 # Fine-tuned model weights (not in source control)
│   ├── distinctbert-safetext/
│   └── tinyllama-safetext-lora/
├── templates/              # Jinja2 HTML templates
└── static/                 # CSS & JavaScript assets
```

---

## ⚙️ Prerequisites

- Python 3.8+
- CUDA-compatible GPU (recommended for inference speed)
- Fine-tuned model weights in the `models/` directory

---

## 🚀 Installation

**1. Clone the repository**
```bash
git clone https://github.com/<your-username>/SafeText_App.git
cd SafeText_App
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add model weights**

Place your fine-tuned models in the `models/` directory:
```
models/
├── distinctbert-safetext/
└── tinyllama-safetext-lora/
```

---

## 🧩 Model Setup

The two models powering SafeText AI:

- **`distinctbert-safetext`** — A DistilBERT model fine-tuned for adversarial text sensitivity classification (`LOW` / `MEDIUM` / `HIGH`).
- **`tinyllama-safetext-lora`** — A TinyLlama 1.1B model fine-tuned with LoRA (PEFT) to normalize and sanitize corrupted or adversarial input text.

If you wish to host model weights publicly, consider uploading them to [Hugging Face Hub](https://huggingface.co/models) and loading them via `from_pretrained()`.

---

## 🖥️ Usage

**Start the Flask development server:**
```bash
python app.py
```
Visit `http://127.0.0.1:5000` in your browser to use the web interface.

---

## 📡 API Reference

### `POST /api/process`

Analyze and normalize a text input.

**Request**
```json
{
  "text": "Your potentially unsafe or adversarial text here..."
}
```

**Response**
```json
{
  "original_text": "...",
  "normalized_text": "...",
  "risk_level": "HIGH",
  "confidence": 0.97
}
```

**Example with cURL:**
```bash
curl -X POST http://127.0.0.1:5000/api/process \
  -H "Content-Type: application/json" \
  -d '{"text": "H\u200bello W\u0041\u0301orld"}'
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Please open an issue first to discuss any significant changes.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).