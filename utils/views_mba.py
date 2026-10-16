"""Views module for Market Basket Analysis page."""

import streamlit as st
from utils.helpers import mi, section_header, status_banner
from utils.market_basket import run_market_basket_analysis
from utils.viz import (
    plot_top_rules,
    plot_rules_network,
    plot_rules_heatmap,
)


def render_market_basket_page(is_dark):
    """Render Market Basket Analysis page with FP-Growth and association graph."""
    section_header(
        "shopping_basket",
        "Market Basket Analysis (FP-Growth)",
        "Penemuan pola kombinasi produk yang kerap dibeli bersamaan dalam satu struk transaksi"
    )

    if "df_clean" not in st.session_state:
        status_banner("Silakan muat dataset terlebih dahulu di halaman Data Explorer.", ok=False)
        return

    df_clean = st.session_state["df_clean"]

    st.markdown("##### Parameter Aturan Asosiasi")
    c1, c2, c3 = st.columns(3)

    with c1:
        min_support = st.slider(
            "Minimum Support",
            min_value=0.005,
            max_value=0.08,
            value=0.02,
            step=0.005,
            format="%.3f",
            help="Ambang batas persentase transaksi yang memuat kombinasi produk."
        )
    with c2:
        min_lift = st.slider(
            "Minimum Lift",
            min_value=1.0,
            max_value=8.0,
            value=1.5,
            step=0.5,
            help="Lift > 1 mengindikasikan korelasi positif yang lebih kuat dibanding kebetulan."
        )
    with c3:
        max_trans = st.slider(
            "Ukuran Sampel Transaksi",
            min_value=5000,
            max_value=80000,
            value=30000,
            step=5000,
            help="Jumlah transaksi yang diolah untuk menjaga efisiensi memori dan waktu komputasi."
        )

    run_btn = st.button("Mulai Analisis Keranjang", use_container_width=True)

    prog_bar = st.progress(0)
    prog_label = st.empty()

    def update_p(pct, msg):
        prog_bar.progress(int(pct))
        prog_label.markdown(
            f"<div style='font-size:0.85rem; color:var(--text-sec); margin-top:4px;'>"
            f"{mi('hourglass_top', 16)} <strong>{pct}%</strong> — {msg}</div>",
            unsafe_allow_html=True
        )

    if run_btn:
        try:
            update_p(0, "Mempersiapkan data transaksi...")
            frequent_items, rules = run_market_basket_analysis(
                df_clean,
                min_support=min_support,
                min_lift=min_lift,
                max_transactions=max_trans,
                progress_callback=update_p
            )
            st.session_state["mba_items"] = frequent_items
            st.session_state["mba_rules"] = rules

            if rules.empty:
                status_banner("Tidak ditemukan aturan yang memenuhi kriteria. Coba turunkan nilai Minimum Support atau Lift.", ok=False)
            else:
                status_banner(f"Analisis berhasil! Ditemukan {len(rules)} aturan asosiasi bernilai.", ok=True)
        except Exception as e:
            st.error(f"Terjadi kendala saat analisis: {e}")

    # Display results if already computed
    if "mba_rules" in st.session_state and not st.session_state["mba_rules"].empty:
        rules = st.session_state["mba_rules"]

        tab1, tab2, tab3, tab4 = st.tabs([
            "Daftar Aturan Asosiasi",
            "Top 15 Rekomendasi (Lift)",
            "Grafik Jejaring Produk",
            "Matriks Heatmap"
        ])

        with tab1:
            st.markdown(
                f"<p style='color:var(--text-sec); font-size:0.88rem;'>"
                f"{mi('lightbulb', 16)} <em>Jika pelanggan membeli produk Antecedents, kemungkinan besar juga membeli Consequents</em></p>",
                unsafe_allow_html=True
            )
            table_show = rules[["antecedents", "consequents", "support", "confidence", "lift"]].copy()
            table_show.columns = [
                "Beli Produk Ini (Antecedents)",
                "Rekomendasikan Produk (Consequents)",
                "Support",
                "Confidence",
                "Lift"
            ]
            table_show["Support"] = table_show["Support"].round(4)
            table_show["Confidence"] = table_show["Confidence"].round(4)
            table_show["Lift"] = table_show["Lift"].round(2)
            st.dataframe(table_show, use_container_width=True, hide_index=True, height=450)

        with tab2:
            st.plotly_chart(plot_top_rules(rules, is_dark), use_container_width=True)

        with tab3:
            net_col, _ = st.columns([1, 2])
            with net_col:
                top_k = st.slider("Jumlah Aturan Ditampilkan", min_value=5, max_value=40, value=15)
            st.plotly_chart(plot_rules_network(rules, is_dark, top_n=top_k), use_container_width=True)

        with tab4:
            st.plotly_chart(plot_rules_heatmap(rules, is_dark), use_container_width=True)
