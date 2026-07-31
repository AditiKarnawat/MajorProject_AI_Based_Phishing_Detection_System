import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from app.core.config import settings

def generate_synthetic_phishing_dataset(n_samples: int = 1500) -> pd.DataFrame:
    """
    Generate a realistic synthetic training dataset for URL phishing detection with natural feature overlap and noise.
    Features:
    [url_length, domain_length, dot_count, hyphen_count, at_count, question_count, equals_count, slash_count,
     digit_ratio, has_ip, is_https, is_suspicious_tld, subdomain_count, domain_entropy, keyword_count, is_shortener]
    """
    np.random.seed(42)
    half = n_samples // 2

    # 1. Legitimate URLs (Label = 0) with realistic variance & overlap
    legit_url_length = np.clip(np.random.normal(32, 14, half), 10, 120).astype(int)
    legit_domain_length = np.clip(np.random.normal(12, 5, half), 4, 35).astype(int)
    legit_dot_count = np.random.choice([1, 2, 3], half, p=[0.65, 0.28, 0.07])
    legit_hyphen_count = np.random.choice([0, 1, 2], half, p=[0.75, 0.20, 0.05])
    legit_at_count = np.random.choice([0, 1], half, p=[0.98, 0.02])
    legit_question_count = np.random.choice([0, 1, 2], half, p=[0.85, 0.12, 0.03])
    legit_equals_count = np.random.choice([0, 1, 2], half, p=[0.85, 0.12, 0.03])
    legit_slash_count = np.clip(np.random.poisson(2.2, half), 1, 8)
    legit_digit_ratio = np.clip(np.random.exponential(0.04, half), 0.0, 0.25)
    legit_has_ip = np.random.choice([0, 1], half, p=[0.98, 0.02])
    legit_is_https = np.random.choice([1, 0], half, p=[0.88, 0.12])
    legit_is_suspicious_tld = np.random.choice([0, 1], half, p=[0.95, 0.05])
    legit_subdomain_count = np.random.choice([0, 1, 2], half, p=[0.75, 0.20, 0.05])
    legit_domain_entropy = np.clip(np.random.normal(3.1, 0.5, half), 1.5, 4.5)
    legit_keyword_count = np.random.choice([0, 1, 2], half, p=[0.90, 0.08, 0.02])
    legit_is_shortener = np.random.choice([0, 1], half, p=[0.96, 0.04])

    df_legit = pd.DataFrame({
        "url_length": legit_url_length,
        "domain_length": legit_domain_length,
        "dot_count": legit_dot_count,
        "hyphen_count": legit_hyphen_count,
        "at_count": legit_at_count,
        "question_count": legit_question_count,
        "equals_count": legit_equals_count,
        "slash_count": legit_slash_count,
        "digit_ratio": legit_digit_ratio,
        "has_ip": legit_has_ip,
        "is_https": legit_is_https,
        "is_suspicious_tld": legit_is_suspicious_tld,
        "subdomain_count": legit_subdomain_count,
        "domain_entropy": legit_domain_entropy,
        "keyword_count": legit_keyword_count,
        "is_shortener": legit_is_shortener,
        "label": 0
    })

    # 2. Phishing URLs (Label = 1) with realistic variance & overlap
    phish_url_length = np.clip(np.random.normal(68, 25, half), 20, 180).astype(int)
    phish_domain_length = np.clip(np.random.normal(20, 7, half), 8, 45).astype(int)
    phish_dot_count = np.random.choice([1, 2, 3, 4, 5], half, p=[0.10, 0.35, 0.30, 0.18, 0.07])
    phish_hyphen_count = np.random.choice([0, 1, 2, 3, 4], half, p=[0.15, 0.40, 0.28, 0.12, 0.05])
    phish_at_count = np.random.choice([0, 1, 2], half, p=[0.70, 0.24, 0.06])
    phish_question_count = np.random.choice([0, 1, 2, 3], half, p=[0.40, 0.35, 0.18, 0.07])
    phish_equals_count = np.random.choice([0, 1, 2, 3, 4], half, p=[0.35, 0.35, 0.18, 0.08, 0.04])
    phish_slash_count = np.clip(np.random.poisson(4.5, half), 1, 12)
    phish_digit_ratio = np.clip(np.random.normal(0.14, 0.08, half), 0.0, 0.45)
    phish_has_ip = np.random.choice([0, 1], half, p=[0.82, 0.18])
    phish_is_https = np.random.choice([1, 0], half, p=[0.55, 0.45])
    phish_is_suspicious_tld = np.random.choice([0, 1], half, p=[0.45, 0.55])
    phish_subdomain_count = np.random.choice([0, 1, 2, 3], half, p=[0.20, 0.45, 0.25, 0.10])
    phish_domain_entropy = np.clip(np.random.normal(4.1, 0.5, half), 2.0, 5.2)
    phish_keyword_count = np.random.choice([0, 1, 2, 3], half, p=[0.25, 0.45, 0.22, 0.08])
    phish_is_shortener = np.random.choice([0, 1], half, p=[0.75, 0.25])

    df_phish = pd.DataFrame({
        "url_length": phish_url_length,
        "domain_length": phish_domain_length,
        "dot_count": phish_dot_count,
        "hyphen_count": phish_hyphen_count,
        "at_count": phish_at_count,
        "question_count": phish_question_count,
        "equals_count": phish_equals_count,
        "slash_count": phish_slash_count,
        "digit_ratio": phish_digit_ratio,
        "has_ip": phish_has_ip,
        "is_https": phish_is_https,
        "is_suspicious_tld": phish_is_suspicious_tld,
        "subdomain_count": phish_subdomain_count,
        "domain_entropy": phish_domain_entropy,
        "keyword_count": phish_keyword_count,
        "is_shortener": phish_is_shortener,
        "label": 1
    })

    df = pd.concat([df_legit, df_phish], ignore_index=True)
    # Add subtle real-world noise (3% label noise)
    noise_idx = np.random.choice(df.index, size=int(0.03 * len(df)), replace=False)
    df.loc[noise_idx, "label"] = 1 - df.loc[noise_idx, "label"]

    return df.sample(frac=1.0, random_state=42).reset_index(drop=True)


def train_and_benchmark_models() -> Dict[str, Any]:
    """
    Train Random Forest, XGBoost, and Logistic Regression models.
    Select and save the best performing model.
    """
    df = generate_synthetic_phishing_dataset(1500)
    
    feature_cols = [
        "url_length", "domain_length", "dot_count", "hyphen_count", "at_count",
        "question_count", "equals_count", "slash_count", "digit_ratio", "has_ip",
        "is_https", "is_suspicious_tld", "subdomain_count", "domain_entropy",
        "keyword_count", "is_shortener"
    ]
    
    X = df[feature_cols]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    models = {
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42),
        "XGBoost": XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, eval_metric="logloss"),
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42)
    }

    results = {}
    best_model_name = None
    best_f1 = -1.0
    best_model_obj = None

    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        
        acc = accuracy_score(y_test, preds)
        prec = precision_score(y_test, preds)
        rec = recall_score(y_test, preds)
        f1 = f1_score(y_test, preds)

        results[name] = {
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1_score": round(float(f1), 4)
        }

    # Determine active model (prefer Random Forest / Tree ensembles if within 2% margin of top linear model)
    top_f1 = max(r["f1_score"] for r in results.values())
    rf_f1 = results["Random Forest"]["f1_score"]

    if (top_f1 - rf_f1) <= 0.02:
        best_model_name = "Random Forest"
        best_model_obj = models["Random Forest"]
        best_f1 = rf_f1
    else:
        best_model_name = max(results.keys(), key=lambda k: results[k]["f1_score"])
        best_model_obj = models[best_model_name]
        best_f1 = results[best_model_name]["f1_score"]

    # Save model artifact
    os.makedirs(settings.MODEL_DIR, exist_ok=True)
    model_path = os.path.join(settings.MODEL_DIR, "best_phishing_model.joblib")
    meta_path = os.path.join(settings.MODEL_DIR, "model_metadata.joblib")

    meta = {
        "active_model": best_model_name,
        "feature_names": feature_cols,
        "benchmark_results": results,
        "f1_score": best_f1
    }

    joblib.dump(best_model_obj, model_path)
    joblib.dump(meta, meta_path)

    return {
        "status": "success",
        "selected_model": best_model_name,
        "metrics": results[best_model_name],
        "all_models_benchmark": results,
        "saved_path": model_path
    }


def load_active_model() -> Tuple[Any, Dict[str, Any]]:
    """
    Load the saved model and metadata, or trigger training if missing.
    """
    model_path = os.path.join(settings.MODEL_DIR, "best_phishing_model.joblib")
    meta_path = os.path.join(settings.MODEL_DIR, "model_metadata.joblib")

    if not os.path.exists(model_path) or not os.path.exists(meta_path):
        train_and_benchmark_models()

    model = joblib.load(model_path)
    meta = joblib.load(meta_path)
    return model, meta
