"""Views module for Data Explorer and Customer Segmentation pages."""

import pandas as pd
import streamlit as st
from utils.helpers import mi, section_header, status_banner
from utils.data_processing import (
    check_sample_exists,
    load_file_with_progress,
    load_sample_with_progress,
    clean_data_with_progress,
)
from utils.segmentation import (
    compute_rfm_with_progress,
    compute_elbow_with_progress,
    run_kmeans_clustering,
)
from utils.viz import (
    plot_elbow,
    plot_3d_clusters,
    plot_segment_distribution,
    plot_segment_pie,
    plot_rfm_comparison,
)


def render_explorer_page():
    """Render Data Explorer page with progress reporting and dual data sourcing."""
    section_header(
        "table_chart",
        "Eksplorasi Data & Pembersihan",
        "Unggah dataset transaksi atau gunakan berkas contoh bawaan"
    )

    sample_ready = check_sample_exists()
    col_source, col_btn = st.columns([2, 1])

    with col_source:
        source_opt = st.radio(
            "Pilih Sumber Dataset:",
            ["Unggah Berkas Baru (CSV / XLSX)", "Gunakan Berkas Contoh (OnlineRetail.xlsx)"],
            horizontal=True
        )

    progress_bar = st.progress(0)
    status_label = st.empty()

    def update_progress(pct, msg):
        progress_bar.progress(int(pct))
        status_label.markdown(
            f"<div style='font-size:0.85rem; color:var(--text-sec); margin-top:4px;'>"
            f"{mi('hourglass_top', 16)} <strong>{pct}%</strong> — {msg}</div>",
            unsafe_allow_html=True
        )

    if source_opt == "Gunakan Berkas Contoh (OnlineRetail.xlsx)":
        if not sample_ready:
            st.error("Berkas contoh 'OnlineRetail.xlsx' tidak ditemukan di direktori root.")
        else:
            with col_btn:
                st.write("")
                st.write("")
                load_sample_btn = st.button("Muat Berkas Contoh", use_container_width=True)

            if load_sample_btn:
                try:
                    df_raw = load_sample_with_progress(update_progress)
                    st.session_state["df_raw"] = df_raw
                    update_progress(0, "Mulai pembersihan data otomatis...")
                    df_clean = clean_data_with_progress(df_raw, update_progress)
                    st.session_state["df_clean"] = df_clean
                    st.session_state.pop("rfm_data", None)
                    st.session_state.pop("rfm_clusters", None)
                    st.session_state.pop("mba_rules", None)
                    status_banner(
                        f"Berkas contoh berhasil dimuat dan dibersihkan! {len(df_clean):,} baris siap dianalisis.",
                        ok=True
                    )
                except Exception as e:
                    st.error(f"Gagal memuat berkas contoh: {e}")

    else:
        uploaded_file = st.file_uploader(
            "Pilih berkas transaksi CSV atau Excel",
            type=["csv", "xlsx", "xls"],
            help="Mendukung format CSV (latin-1) dan berkas Excel Workbook."
        )
        if uploaded_file is not None:
            if "last_uploaded_name" not in st.session_state or st.session_state["last_uploaded_name"] != uploaded_file.name:
                try:
                    df_raw = load_file_with_progress(uploaded_file, update_progress)
                    st.session_state["df_raw"] = df_raw
                    st.session_state["last_uploaded_name"] = uploaded_file.name
                    update_progress(0, "Memulai sanitasi data transaksi...")
                    df_clean = clean_data_with_progress(df_raw, update_progress)
                    st.session_state["df_clean"] = df_clean
                    st.session_state.pop("rfm_data", None)
                    st.session_state.pop("rfm_clusters", None)
                    st.session_state.pop("mba_rules", None)
                    status_banner(
                        f"Dataset {uploaded_file.name} berhasil diproses ({len(df_clean):,} baris valid).",
                        ok=True
                    )
                except Exception as e:
                    st.error(f"Gagal memproses berkas: {e}")

    # Display dataset details if available
    if "df_clean" in st.session_state:
        df_raw = st.session_state.get("df_raw", st.session_state["df_clean"])
        df_clean = st.session_state["df_clean"]
        removed_count = len(df_raw) - len(df_clean)
        removed_pct = (removed_count / len(df_raw) * 100) if len(df_raw) > 0 else 0

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Baris Mentah", f"{len(df_raw):,}")
        m2.metric("Baris Bersih", f"{len(df_clean):,}")
        m3.metric("Baris Dieliminasi", f"{removed_count:,}", f"-{removed_pct:.1f}%")
        n_cust = df_clean["CustomerID"].nunique() if "CustomerID" in df_clean.columns else 0
        m4.metric("Jumlah Pelanggan Unik", f"{n_cust:,}")

        m5, m6, m7, m8 = st.columns(4)
        n_prod = df_clean["Description"].nunique() if "Description" in df_clean.columns else 0
        m5.metric("Katalog Produk Unik", f"{n_prod:,}")
        n_inv = df_clean["InvoiceNo"].nunique() if "InvoiceNo" in df_clean.columns else 0
        m6.metric("Total Struk / Faktur", f"{n_inv:,}")
        if "InvoiceDate" in df_clean.columns:
            days = (df_clean["InvoiceDate"].max() - df_clean["InvoiceDate"].min()).days
            m7.metric("Rentang Periode", f"{days} Hari")
        else:
            m7.metric("Rentang Periode", "-")
        if "TotalPrice" in df_clean.columns:
            rev = df_clean["TotalPrice"].sum()
            m8.metric("Akumulasi Omset", f"£{rev:,.0f}")
        else:
            m8.metric("Akumulasi Omset", "-")

        t1, t2, t3 = st.tabs(["Struktur Kolom", "Cuplikan Data Bersih", "Statistik Deskriptif"])
        with t1:
            col_info = pd.DataFrame({
                "Nama Kolom": df_clean.columns,
                "Tipe Data": [str(df_clean[c].dtype) for c in df_clean.columns],
                "Valid Count": [df_clean[c].notna().sum() for c in df_clean.columns],
                "Null Count": [df_clean[c].isna().sum() for c in df_clean.columns],
                "Contoh Nilai": [str(df_clean[c].iloc[0]) if len(df_clean) > 0 else "-" for c in df_clean.columns]
            })
            st.dataframe(col_info, use_container_width=True, hide_index=True)
        with t2:
            st.dataframe(df_clean.head(100), use_container_width=True, height=450)
        with t3:
            st.dataframe(df_clean.describe(), use_container_width=True)
    else:
        st.markdown(
            f"""
            <div class="card" style="text-align: center; padding: 48px 24px; margin-top: 24px;">
                <div style="margin-bottom: 8px;">{mi('folder_open', 42)}</div>
                <h3 style="color: var(--text); font-size: 1.15rem; margin-bottom: 6px;">Belum Ada Dataset yang Dimuat</h3>
                <p style="color: var(--text-sec); font-size: 0.88rem; max-width: 480px; margin: 0 auto;">
                    Gunakan salah satu opsi di atas untuk mengunggah berkas transaksi baru atau menggunakan berkas contoh lokal OnlineRetail.xlsx.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_segmentation_page(is_dark):
    """Render Customer Segmentation page with progress and theme reactivity."""
    section_header(
        "groups",
        "Segmentasi Pelanggan (RFM + K-Means)",
        "Pengelompokan pelanggan berdasarkan kebaruan, frekuensi, dan nilai transaksi"
    )

    if "df_clean" not in st.session_state:
        status_banner("Silakan muat dataset terlebih dahulu di halaman Data Explorer.", ok=False)
        return

    df_clean = st.session_state["df_clean"]
    pbar = st.progress(0)
    plabel = st.empty()

    def update_p(pct, msg):
        pbar.progress(int(pct))
        plabel.markdown(
            f"<div style='font-size:0.85rem; color:var(--text-sec); margin-top:4px;'>"
            f"{mi('hourglass_top', 16)} <strong>{pct}%</strong> — {msg}</div>",
            unsafe_allow_html=True
        )

    # Compute or retrieve RFM
    if "rfm_data" not in st.session_state:
        rfm = compute_rfm_with_progress(df_clean, update_p)
        st.session_state["rfm_data"] = rfm
    else:
        rfm = st.session_state["rfm_data"]

    status_banner(f"Metrik RFM aktif untuk {len(rfm):,} pelanggan unik.", ok=True)

    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown("##### Parameter Klastering")
        n_clusters = st.slider("Jumlah Segmen (K)", min_value=2, max_value=8, value=4)
        show_elbow = st.checkbox("Analisis Metode Elbow", value=False)
        recluster_btn = st.button("Jalankan Klastering Ulang", use_container_width=True)

    with c2:
        if show_elbow:
            st.markdown("##### Evaluasi Nilai K Optimal (Metode Elbow)")
            k_range, inertias = compute_elbow_with_progress(rfm, max_k=8, progress_callback=update_p)
            st.plotly_chart(plot_elbow(k_range, inertias, is_dark), use_container_width=True)

    # Run clustering if not present or changed
    if recluster_btn or "rfm_clusters" not in st.session_state or st.session_state.get("last_k") != n_clusters:
        update_p(0, "Memulai algoritma K-Means...")
        rfm_res, _, _, _ = run_kmeans_clustering(rfm, n_clusters, update_p)
        st.session_state["rfm_clusters"] = rfm_res
        st.session_state["last_k"] = n_clusters

    rfm_result = st.session_state["rfm_clusters"]

    tab1, tab2, tab3, tab4 = st.tabs([
        "Visualisasi 3D RFM",
        "Distribusi Segmen",
        "Profil Rata-rata RFM",
        "Tabel Data Pelanggan"
    ])

    with tab1:
        st.plotly_chart(plot_3d_clusters(rfm_result, is_dark), use_container_width=True)

    with tab2:
        seg_counts = rfm_result["Segment"].value_counts().reset_index()
        seg_counts.columns = ["Segment", "Count"]
        seg_counts["Percentage"] = (seg_counts["Count"] / seg_counts["Count"].sum() * 100).round(1)

        bcol, pcol = st.columns([3, 2])
        with bcol:
            st.plotly_chart(plot_segment_distribution(seg_counts, is_dark), use_container_width=True)
        with pcol:
            st.plotly_chart(plot_segment_pie(seg_counts, is_dark), use_container_width=True)

    with tab3:
        means = rfm_result.groupby("Segment")[["Recency", "Frequency", "Monetary"]].mean().reset_index()
        st.plotly_chart(plot_rfm_comparison(means, is_dark), use_container_width=True)

    with tab4:
        summary_table = rfm_result.groupby("Segment").agg({
            "Recency": "mean",
            "Frequency": "mean",
            "Monetary": "mean",
            "CustomerID": "count"
        }).round(1).reset_index()
        summary_table.columns = ["Segmen", "Rata-rata Recency (Hari)", "Rata-rata Frequency", "Rata-rata Monetary (£)", "Jumlah Pelanggan"]
        st.dataframe(summary_table, use_container_width=True, hide_index=True)
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        st.dataframe(rfm_result[["CustomerID", "Recency", "Frequency", "Monetary", "Segment"]].head(250), use_container_width=True, height=400)
