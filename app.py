import os
import sys
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Ensure project root is on sys.path so backend imports work on macOS/Streamlit
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from backend.analysis import load_dataset, preprocess, detect_anomalies

# -------------------------
# Page
# -------------------------
st.set_page_config(page_title="UNSW-NB15 • Early Anomaly Dashboard", layout="wide")
st.title("UNSW-NB15 • Early Anomaly Detection Dashboard")
st.caption("Interaktivna vizuelna analiza ranih anomalija (prag: mean + k·std)")

DATA_PATH = os.path.join("data", "UNSW_NB15_training-set.csv")
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------
# Load
# -------------------------
if not os.path.exists(DATA_PATH):
    st.error(f"Dataset nije pronađen: {DATA_PATH}")
    st.info("Provjeri da li je fajl u folderu data/ unutar projekta.")
    st.stop()

df_raw = load_dataset(DATA_PATH)
df_num = preprocess(df_raw)

# -------------------------
# Sidebar
# -------------------------
st.sidebar.header("Kontrole")
numeric_cols = list(df_num.columns)

preferred = [c for c in ["dur", "sbytes", "dbytes", "spkts", "dpkts", "pkts"] if c in numeric_cols]
default_metric = preferred[0] if preferred else numeric_cols[0]

metric = st.sidebar.selectbox("Izaberi metriku", options=numeric_cols, index=numeric_cols.index(default_metric))
k = st.sidebar.slider("Osjetljivost (k)", 1.0, 5.0, 2.5, 0.1)

# -------------------------
# Detect
# -------------------------
res = detect_anomalies(df_num, metric, k=k)

anomaly_count = int(res["anomaly"].sum())
total = int(len(res))
anom_pct = (anomaly_count / total * 100) if total else 0.0

mean = float(res["mean"].iloc[0])
std = float(res["std"].iloc[0])
threshold = float(res["threshold"].iloc[0])

# -------------------------
# KPIs
# -------------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Mean", f"{mean:.3f}")
c2.metric("Std", f"{std:.3f}")
c3.metric("Threshold", f"{threshold:.3f}")
c4.metric("Anomalije", f"{anomaly_count} ({anom_pct:.2f}%)")

if anomaly_count > 0:
    st.error("⚠️ Detektovane rane anomalije za izabranu metriku i k.")
else:
    st.success("✅ Nema detektovanih anomalija za izabranu metriku i k.")

# -------------------------
# Main plots
# -------------------------
st.subheader(f"Vizuelizacija metrike: {metric}")

y = res["metric_value"].values
anom_idx = np.where(res["anomaly"].values)[0]

fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(y, label="Vrijednost")
ax1.axhline(threshold, color="red", linestyle="--", label=f"Threshold = {threshold:.3f}")
if len(anom_idx) > 0:
    ax1.scatter(anom_idx, y[anom_idx], s=10, color="red", label="Anomalije")
ax1.set_xlabel("Uzorci")
ax1.set_ylabel(metric)
ax1.legend()
st.pyplot(fig1)

fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.hist(y, bins=60)
ax2.axvline(threshold, color="red", linestyle="--")
ax2.set_xlabel(metric)
ax2.set_ylabel("Frekvencija")
ax2.set_title("Distribucija vrijednosti (histogram) + prag")
st.pyplot(fig2)

# -------------------------
# Table + filters
# -------------------------
st.divider()
st.subheader("Pregled anomalija (Top N)")

show_mode = st.radio("Prikaz", ["Svi uzorci", "Samo anomalije", "Samo normalni"], horizontal=True)

view_df = df_raw.copy()
view_df["_metric"] = pd.to_numeric(df_raw[metric], errors="coerce")
view_df["_anomaly"] = res["anomaly"].values
view_df["_severity"] = res["severity"].values

if show_mode == "Samo anomalije":
    view_df = view_df[view_df["_anomaly"] == True]
elif show_mode == "Samo normalni":
    view_df = view_df[view_df["_anomaly"] == False]

if view_df.empty:
    if show_mode == "Samo anomalije":
        st.info("ℹ️ Za izabranu metriku i k nema detektovanih anomalija.")
    elif show_mode == "Samo normalni":
        st.info("ℹ️ Svi prikazani uzorci pripadaju normalnom ponašanju.")
    else:
        st.info("ℹ️ Nema podataka za prikaz sa trenutnim postavkama.")
else:
    top_n = st.slider("Koliko redova prikazati", 10, 200, 50, 10)
    view_sorted = view_df.sort_values(by="_severity", ascending=False).head(top_n)

    preferred_cols = [
        "srcip", "dstip", "sport", "dport", "proto", "service", "state",
        "dur", "sbytes", "dbytes", "spkts", "dpkts", "sttl", "dttl",
        "label", "attack_cat"
    ]
    cols_to_show = [c for c in preferred_cols if c in view_sorted.columns]
    if not cols_to_show:
        cols_to_show = list(view_sorted.columns)

    st.dataframe(view_sorted[cols_to_show], use_container_width=True)

# -------------------------
# Download + export
# -------------------------
st.divider()
st.subheader("Eksport (CSV/PNG) za IEEE članak")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# CSV anomalies
anom_only = df_raw.copy()
anom_only["metric"] = metric
anom_only["k"] = k
anom_only["threshold"] = threshold
anom_only["anomaly"] = res["anomaly"].values
anom_only["severity"] = res["severity"].values
anom_only = anom_only[anom_only["anomaly"] == True].sort_values(by="severity", ascending=False)

if len(anom_only) == 0:
    st.info("ℹ️ Nema anomalija za izabranu metriku i k — CSV export se ne prikazuje.")
else:
    csv_bytes = anom_only.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Preuzmi anomalije (CSV)",
        data=csv_bytes,
        file_name=f"unsw_nb15_anomalies_{metric}_k{k:.1f}.csv",
        mime="text/csv",
    )

# Save figures to outputs for paper
png1 = os.path.join(OUTPUT_DIR, f"figure_metric_{metric}_k{k:.1f}_{timestamp}.png")
png2 = os.path.join(OUTPUT_DIR, f"figure_hist_{metric}_k{k:.1f}_{timestamp}.png")
fig1.savefig(png1, dpi=200, bbox_inches="tight")
fig2.savefig(png2, dpi=200, bbox_inches="tight")
st.success(f"PNG exportovan u: {png1} i {png2}")
