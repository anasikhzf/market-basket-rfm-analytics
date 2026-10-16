"""Data loading and cleaning functions with detailed step-by-step progress tracking."""

import os
import time
import pandas as pd

SAMPLE_PATH = "OnlineRetail.xlsx"


def check_sample_exists():
    """Check whether the sample dataset file is available."""
    return os.path.exists(SAMPLE_PATH)


def load_file_with_progress(file_obj, progress_callback=None):
    """Load data from uploaded file with progress updates.
    
    Args:
        file_obj: Uploaded file object
        progress_callback: Function accepting (percentage: int, message: str)
    """
    if progress_callback:
        progress_callback(10, f"Membaca file '{file_obj.name}'...")
        time.sleep(0.05)

    is_csv = file_obj.name.lower().endswith(".csv")
    if is_csv:
        if progress_callback:
            progress_callback(40, "Mengurai data CSV (encoding latin-1)...")
        df = pd.read_csv(file_obj, encoding="latin-1")
    else:
        if progress_callback:
            progress_callback(30, "Membaca berkas Excel (.xlsx)... Ini membutuhkan beberapa detik...")
        df = pd.read_excel(file_obj, engine="openpyxl")

    if progress_callback:
        progress_callback(100, f"Selesai! Dimuat {len(df):,} baris data.")
        time.sleep(0.05)

    return df


def load_sample_with_progress(progress_callback=None):
    """Load the sample dataset (OnlineRetail.xlsx) with progress updates."""
    if not check_sample_exists():
        raise FileNotFoundError(f"File sample {SAMPLE_PATH} tidak ditemukan.")

    if progress_callback:
        progress_callback(15, f"Membuka file contoh lokal '{SAMPLE_PATH}'...")
        time.sleep(0.05)

    if progress_callback:
        progress_callback(45, "Mengekstrak lembar kerja Excel (engine openpyxl)...")

    df = pd.read_excel(SAMPLE_PATH, engine="openpyxl")

    if progress_callback:
        progress_callback(100, f"Selesai! {len(df):,} baris data berhasil dimuat.")
        time.sleep(0.05)

    return df


def clean_data_with_progress(df, progress_callback=None):
    """Clean raw dataset according to PRD with granular progress steps.

    Cleaning pipeline:
      1. (15%) Trim whitespace pada nama kolom
      2. (35%) Hapus baris dengan CustomerID kosong (null)
      3. (55%) Hapus transaksi dibatalkan (InvoiceNo diawali 'C')
      4. (75%) Hapus Quantity <= 0 dan UnitPrice <= 0
      5. (90%) Konversi InvoiceDate ke datetime & validasi
      6. (100%) Hitung TotalPrice = Quantity * UnitPrice
    """
    out = df.copy()

    if progress_callback:
        progress_callback(15, "Langkah 1/6 (15%): Merapikan nama kolom dataset...")
        time.sleep(0.04)
    out.columns = out.columns.str.strip()

    if progress_callback:
        progress_callback(35, "Langkah 2/6 (35%): Menyaring baris tanpa CustomerID...")
        time.sleep(0.04)
    if "CustomerID" in out.columns:
        out = out.dropna(subset=["CustomerID"])
        out["CustomerID"] = out["CustomerID"].astype(int)

    if progress_callback:
        progress_callback(55, "Langkah 3/6 (55%): Menghapus transaksi pembatalan (InvoiceNo 'C')...")
        time.sleep(0.04)
    if "InvoiceNo" in out.columns:
        out["InvoiceNo"] = out["InvoiceNo"].astype(str)
        out = out[~out["InvoiceNo"].str.startswith("C")]

    if progress_callback:
        progress_callback(75, "Langkah 4/6 (75%): Validasi Quantity > 0 dan UnitPrice > 0...")
        time.sleep(0.04)
    if "Quantity" in out.columns:
        out = out[out["Quantity"] > 0]
    if "UnitPrice" in out.columns:
        out = out[out["UnitPrice"] > 0]

    if progress_callback:
        progress_callback(90, "Langkah 5/6 (90%): Standarisasi tipe data InvoiceDate ke datetime...")
        time.sleep(0.04)
    if "InvoiceDate" in out.columns:
        out["InvoiceDate"] = pd.to_datetime(out["InvoiceDate"], errors="coerce")
        out = out.dropna(subset=["InvoiceDate"])

    if progress_callback:
        progress_callback(100, "Langkah 6/6 (100%): Menghitung TotalPrice per item transaksi...")
        time.sleep(0.04)
    if "Quantity" in out.columns and "UnitPrice" in out.columns:
        out["TotalPrice"] = out["Quantity"] * out["UnitPrice"]

    return out.reset_index(drop=True)
