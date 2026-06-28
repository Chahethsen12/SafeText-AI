from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForCausalLM
from peft import PeftModel, PeftConfig
import re
import os

from preprocess import preprocess_for_classifier

app = Flask(__name__)
CORS(app)

# =====================================================================
# 1. LOAD DISTINCTBERT (Sensitivity Classifier)
# =====================================================================
print("Loading DistinctBERT...")
bert_path = "Chahethsen/distinctbert-safetext"
bert_tokenizer = AutoTokenizer.from_pretrained(bert_path)
bert_model = AutoModelForSequenceClassification.from_pretrained(bert_path)

# Force CPU routing safely for Spaces free tier
device = "cpu"
bert_model = bert_model.to(device)
bert_model.eval()

LABELS = ["LOW", "MEDIUM", "HIGH"]

# =====================================================================
# 2. LOAD TINYLLAMA (Text Normalizer)
# =====================================================================
print("Loading TinyLlama Base Model and LoRA Adapters...")
tiny_base_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
lora_path = "Chahethsen/tinyllama-safetext-lora"

llama_tokenizer = AutoTokenizer.from_pretrained(lora_path)

llama_base = AutoModelForCausalLM.from_pretrained(
    tiny_base_id,
    low_cpu_mem_usage=True
)

llama_model = PeftModel.from_pretrained(llama_base, lora_path)
llama_model = llama_model.to(device)
llama_model.eval()

# =====================================================================
# 3. HELPER FUNCTIONS
# =====================================================================
def basic_clean(text):
    return re.sub(r"\s+", " ", text).strip()

def bert_predict_proba(texts):
    if isinstance(texts, str):
        texts = [texts]

    all_probs = []

    for text in texts:
        inputs = bert_tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=256,
            padding=True
        ).to(device)

        with torch.no_grad():
            outputs = bert_model(**inputs)
            probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
            probs = probabilities.cpu().numpy()[0]

        all_probs.append(probs)

    return np.array(all_probs)

def bert_predict_proba_preprocessed(texts):
    if isinstance(texts, str):
        texts = [texts]

    processed_texts = []
    for text in texts:
        prep = preprocess_for_classifier(text, remove_stopwords=True)
        processed_texts.append(prep["processed_text"])

    return bert_predict_proba(processed_texts)

def bert_predict_label(text):
    probs = bert_predict_proba([text])[0]
    prediction_idx = int(np.argmax(probs))
    label = LABELS[prediction_idx]
    confidence = float(probs[prediction_idx] * 100)
    return label, confidence, probs

def choose_higher_risk_result(result_a, result_b):
    risk_order = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}

    label_a, conf_a, probs_a = result_a
    label_b, conf_b, probs_b = result_b

    if risk_order[label_b] > risk_order[label_a]:
        return result_b, "processed_text"
    elif risk_order[label_b] < risk_order[label_a]:
        return result_a, "normalized_text"
    else:
        if conf_b > conf_a:
            return result_b, "processed_text"
        return result_a, "normalized_text"

def normalize_with_llama(raw_text):
    prompt = f"""<|system|>
You are SafeText AI, an expert system for text normalization and sanitization.</s>
<|user|>
Normalize and clean the following corrupted text. Remove any invisible characters, homoglyphs, or adversarial patterns, and output only the clean text.

Corrupted text:
{raw_text}</s>
<|assistant|>
"""

    llama_inputs = llama_tokenizer(prompt, return_tensors="pt").to(device)

    with torch.no_grad():
        generated_ids = llama_model.generate(
            **llama_inputs,
            max_new_tokens=100,
            temperature=0.1,
            pad_token_id=llama_tokenizer.eos_token_id
        )

    full_output = llama_tokenizer.decode(generated_ids[0], skip_special_tokens=False)
    clean_text = full_output.split("<|assistant|>\n")[-1].replace("</s>", "").strip()
    return clean_text

# =====================================================================
# 4. ROUTES
# =====================================================================
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def process_text():
    data = request.json
    raw_text = data.get("text", "")

    if not raw_text:
        return jsonify({"error": "No text provided"}), 400

    prep = preprocess_for_classifier(raw_text, remove_stopwords=True)

    normalized_result = bert_predict_label(prep["normalized_text"])
    processed_result = bert_predict_label(prep["processed_text"])

    (sensitivity, confidence, probs), selected_source = choose_higher_risk_result(
        normalized_result,
        processed_result
    )

    confidence_str = f"{confidence:.2f}%"
    selected_input = prep["processed_text"] if selected_source == "processed_text" else prep["normalized_text"]

    if sensitivity == "LOW":
        clean_text = basic_clean(selected_input)
    else:
        clean_text = normalize_with_llama(selected_input)

    return jsonify({
        "original_text": raw_text,
        "normalized_text": prep["normalized_text"],
        "processed_text": prep["processed_text"],
        "classifier_input_used": selected_source,
        "sensitivity_level": sensitivity,
        "confidence": confidence_str,
        "cleaned_text": clean_text,
        "probabilities": {
            "LOW": float(probs[0]),
            "MEDIUM": float(probs[1]),
            "HIGH": float(probs[2])
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 7860))
    print(f"SafeText AI API is starting on http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
