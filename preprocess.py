import re
import unicodedata

STOPWORDS = {
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves",
    "you", "your", "yours", "yourself", "yourselves",
    "he", "him", "his", "himself", "she", "her", "hers",
    "it", "its", "itself", "they", "them", "their", "theirs",
    "this", "that", "these", "those", "am", "is", "are", "was",
    "were", "be", "been", "being", "have", "has", "had", "do",
    "does", "did", "a", "an", "the", "and", "but", "if", "or",
    "because", "as", "until", "while", "of", "at", "by", "for",
    "with", "about", "against", "between", "into", "through",
    "during", "before", "after", "above", "below", "to", "from",
    "up", "down", "in", "out", "on", "off", "over", "under",
    "again", "further", "then", "once", "here", "there", "when",
    "where", "why", "how", "all", "any", "both", "each", "few",
    "more", "most", "other", "some", "such", "only", "own",
    "same", "so", "than", "too", "very", "can", "will", "just",
    "now"
}

KEEP_WORDS = {
    "not", "no", "nor", "never",
    "click", "login", "secure", "alert", "free", "gift", "claim",
    "paypal", "bank", "password", "verify", "urgent", "winner",
    "money", "bitcoin", "wallet"
}

def normalize_unicode(text):
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def tokenize_basic(text):
    return re.findall(r"\b\w+\b", text, flags=re.UNICODE)

def selective_stopword_removal(text):
    tokens = tokenize_basic(text)
    kept_tokens = []

    for token in tokens:
        token_lower = token.lower()
        if token_lower in KEEP_WORDS:
            kept_tokens.append(token)
        elif token_lower not in STOPWORDS:
            kept_tokens.append(token)

    return " ".join(kept_tokens)

def preprocess_for_classifier(text, remove_stopwords=True):
    normalized = normalize_unicode(text)

    if remove_stopwords:
        processed = selective_stopword_removal(normalized)
    else:
        processed = normalized

    return {
        "raw_text": text,
        "normalized_text": normalized,
        "processed_text": processed
    }
