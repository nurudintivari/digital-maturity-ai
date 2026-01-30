import pandas as pd
import numpy as np

def load_dataset(path: str) -> pd.DataFrame:
    """Load UNSW-NB15 CSV dataset."""
    return pd.read_csv(path)

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """
    Keep numeric columns only (for metric selection),
    fill missing values with 0 for stable statistics.
    """
    numeric_df = df.select_dtypes(include=[np.number]).copy()
    return numeric_df.fillna(0)

def detect_anomalies(df_numeric: pd.DataFrame, metric: str, k: float = 2.5) -> pd.DataFrame:
    """
    Early anomaly indicator (simple, explainable):
        anomaly if x > mean + k * std

    Returns DataFrame with:
      metric_value, mean, std, threshold, anomaly, severity
    where severity = max(0, x - threshold).
    """
    x = pd.to_numeric(df_numeric[metric], errors="coerce").fillna(0)

    mean = float(x.mean())
    std = float(x.std(ddof=1)) if len(x) > 1 else 0.0
    threshold = mean + k * std

    out = pd.DataFrame({
        "metric_value": x,
        "mean": mean,
        "std": std,
        "threshold": threshold,
    })

    out["anomaly"] = out["metric_value"] > threshold
    out["severity"] = (out["metric_value"] - threshold).clip(lower=0)

    return out
