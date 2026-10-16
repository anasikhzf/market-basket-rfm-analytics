"""Customer segmentation engine using RFM Analysis and K-Means Clustering."""

import time
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


def compute_rfm_with_progress(df_clean, progress_callback=None):
    """Compute Recency, Frequency, Monetary (RFM) with step progress."""
    if progress_callback:
        progress_callback(20, "Menghitung tanggal acuan transaksi terbaru (20%)...")
        time.sleep(0.04)

    snapshot_date = df_clean["InvoiceDate"].max() + pd.Timedelta(days=1)

    if progress_callback:
        progress_callback(50, "Melakukan agregasi RFM per CustomerID (50%)...")
        time.sleep(0.04)

    rfm = df_clean.groupby("CustomerID").agg({
        "InvoiceDate": lambda x: (snapshot_date - x.max()).days,
        "InvoiceNo": "nunique",
        "TotalPrice": "sum"
    }).reset_index()

    rfm.columns = ["CustomerID", "Recency", "Frequency", "Monetary"]

    if progress_callback:
        progress_callback(80, "Pembersihan outlier ekstrim (persentil ke-99) (80%)...")
        time.sleep(0.04)

    for col in ["Recency", "Frequency", "Monetary"]:
        q99 = rfm[col].quantile(0.99)
        rfm = rfm[rfm[col] <= q99]

    if progress_callback:
        progress_callback(100, f"Selesai! RFM siap untuk {len(rfm):,} pelanggan (100%).")
        time.sleep(0.04)

    return rfm.reset_index(drop=True)


def compute_elbow_with_progress(rfm, max_k=10, progress_callback=None):
    """Compute inertia across a range of K values with precise progress reporting."""
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm[["Recency", "Frequency", "Monetary"]])

    inertias = []
    k_range = list(range(2, max_k + 1))
    total_steps = len(k_range)

    for idx, k in enumerate(k_range):
        pct = int(10 + (idx / total_steps) * 85)
        if progress_callback:
            progress_callback(pct, f"Menghitung Elbow K-Means: Evaluasi K={k}/{max_k} ({pct}%)...")
        km = KMeans(n_clusters=k, random_state=42, n_init=10, max_iter=300)
        km.fit(rfm_scaled)
        inertias.append(km.inertia_)

    if progress_callback:
        progress_callback(100, "Perhitungan inertia Elbow method selesai (100%).")

    return k_range, inertias


def run_kmeans_clustering(rfm, n_clusters, progress_callback=None):
    """Run K-Means clustering and assign descriptive business segments."""
    if progress_callback:
        progress_callback(25, f"Standarisasi fitur RFM (StandardScaler) (25%)...")
        time.sleep(0.04)

    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm[["Recency", "Frequency", "Monetary"]])

    if progress_callback:
        progress_callback(60, f"Melatih model K-Means dengan K={n_clusters} cluster (60%)...")
        time.sleep(0.05)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10, max_iter=300)
    rfm_result = rfm.copy()
    rfm_result["Cluster"] = kmeans.fit_predict(rfm_scaled)

    if progress_callback:
        progress_callback(85, "Memetakan label segmen bisnis berdasarkan profil RFM (85%)...")
        time.sleep(0.04)

    cluster_summary = rfm_result.groupby("Cluster").agg({
        "Recency": "mean",
        "Frequency": "mean",
        "Monetary": "mean"
    }).reset_index()

    # Sort descending by Monetary to map meaningful labels
    cluster_summary = cluster_summary.sort_values("Monetary", ascending=False).reset_index(drop=True)

    segment_titles = [
        "Pelanggan Premium",
        "Pelanggan Setia",
        "Pelanggan Potensial",
        "Pelanggan Reguler",
        "Pelanggan Baru",
        "Berisiko Pindah",
        "Pelanggan Pasif",
        "Pelanggan Dorman",
    ]

    labels = {}
    for i, row in cluster_summary.iterrows():
        cid = row["Cluster"]
        labels[cid] = segment_titles[i] if i < len(segment_titles) else f"Segmen {cid}"

    rfm_result["Segment"] = rfm_result["Cluster"].map(labels)

    if progress_callback:
        progress_callback(100, f"Clustering selesai! {n_clusters} segmen teridentifikasi (100%).")
        time.sleep(0.04)

    return rfm_result, kmeans, scaler, rfm_scaled
