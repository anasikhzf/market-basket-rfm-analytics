"""Market Basket Analysis using FP-Growth and Association Rules."""

import time
import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules


def run_market_basket_analysis(df_clean, min_support=0.02, min_lift=1.5, max_transactions=30000, progress_callback=None):
    """Execute FP-Growth market basket mining with step-by-step progress tracking."""
    if progress_callback:
        progress_callback(15, f"Sampling data ({min(len(df_clean), max_transactions):,} transaksi) (15%)...")
        time.sleep(0.04)

    if len(df_clean) > max_transactions:
        df_sample = df_clean.sample(n=max_transactions, random_state=42)
    else:
        df_sample = df_clean.copy()

    if progress_callback:
        progress_callback(40, "Menyusun matriks one-hot transaksi barang (40%)...")
        time.sleep(0.04)

    basket = (
        df_sample.groupby(["InvoiceNo", "Description"])["Quantity"]
        .sum()
        .unstack()
        .fillna(0)
    )
    basket = (basket > 0).astype(bool)

    # Filter out empty or whitespace-only product names
    valid_cols = [c for c in basket.columns if str(c).strip() != ""]
    basket = basket[valid_cols]

    if progress_callback:
        progress_callback(70, f"Mencari frequent itemset (min_support={min_support:.3f}) via FP-Growth (70%)...")

    frequent_items = fpgrowth(basket, min_support=min_support, use_colnames=True)

    if frequent_items.empty:
        if progress_callback:
            progress_callback(100, "Selesai: Tidak ada itemset yang memenuhi ambang batas support (100%).")
        return pd.DataFrame(), pd.DataFrame()

    if progress_callback:
        progress_callback(90, f"Membangkitkan aturan asosiasi (min_lift={min_lift:.1f}) (90%)...")
        time.sleep(0.04)

    rules = association_rules(frequent_items, metric="lift", min_threshold=min_lift)

    if not rules.empty:
        rules["antecedents"] = rules["antecedents"].apply(lambda s: ", ".join(list(s)))
        rules["consequents"] = rules["consequents"].apply(lambda s: ", ".join(list(s)))
        rules = rules.sort_values("lift", ascending=False).reset_index(drop=True)

    if progress_callback:
        progress_callback(100, f"Analisis selesai! {len(rules)} aturan asosiasi ditemukan (100%).")
        time.sleep(0.04)

    return frequent_items, rules
