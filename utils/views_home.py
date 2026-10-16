"""Views module for Beranda (Home) and Tentang (About) pages."""

import streamlit as st
from utils.helpers import mi, section_header, status_banner


def render_home_page():
    """Render modern minimalist Home page."""
    st.markdown(
        f"""
        <div class="card" style="padding: 32px 28px; margin-bottom: 24px; text-align: center;">
            <div style="margin-bottom: 12px;">{mi('analytics', 44)}</div>
            <h1 style="font-size: 1.85rem; font-weight: 700; margin: 0 0 8px 0; color: var(--text);">
                Sistem Cerdas Analisis Transaksi E-Commerce
            </h1>
            <p style="color: var(--text-sec); font-size: 0.95rem; max-width: 720px; margin: 0 auto; line-height: 1.6;">
                Platform analisis data terpadu untuk segmentasi pelanggan berbasis RFM & K-Means
                serta penemuan pola belanja bersamaan (Market Basket Analysis) dengan FP-Growth.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
            <div class="card">
                <h4>{mi('groups', 20)} Segmentasi Pelanggan (RFM + K-Means)</h4>
                <p>
                    Mengelompokkan basis pelanggan secara objektif berdasarkan tiga dimensi utama:
                    <strong>Recency</strong> (kebaruan transaksi), <strong>Frequency</strong> (frekuensi belanja),
                    dan <strong>Monetary</strong> (total pengeluaran). Diperkuat dengan algoritma
                    <strong>K-Means Clustering</strong> untuk menghasilkan kelompok pelanggan yang dapat ditindaklanjuti secara komersial.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="card">
                <h4>{mi('tune', 20)} Fleksibilitas Parameter</h4>
                <p>
                    Sesuaikan jumlah klaster (K) secara interaktif, amati kurva inersia metode Elbow,
                    serta sesuaikan ambang batas <em>Support</em>, <em>Confidence</em>, dan <em>Lift</em>
                    sesuai skala bisnis dan karakteristik katalog produk Anda.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="card">
                <h4>{mi('shopping_basket', 20)} Market Basket Analysis (FP-Growth)</h4>
                <p>
                    Menemukan aturan keterkaitan produk yang kerap dibeli bersamaan dalam satu struk transaksi.
                    Menggunakan algoritma <strong>FP-Growth</strong> yang efisien dari segi komputasi
                    dan memori untuk katalog bertransaksi masif tanpa eksplosi kandidat pasangan.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="card">
                <h4>{mi('speed', 20)} Kinerja Ringan & Lokal</h4>
                <p>
                    Dijalankan penuh di lingkungan lokal (<em>localhost</em>) tanpa mengirim data transaksi ke luar.
                    Dilengkapi dengan pemantauan tahapan persentase proses dan pembersihan data otomatis.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    section_header("explore", "Alur Kerja Analisis Cepat", "Panduan langkah mudah untuk memulai eksplorasi data")
    step_cols = st.columns(4)
    steps = [
        ("upload_file", "1. Muat Dataset", "Unggah berkas CSV/XLSX atau gunakan berkas contoh OnlineRetail.xlsx bawaan."),
        ("table_chart", "2. Eksplorasi Data", "Periksa statistik deskriptif dan validasi pembersihan data transaksi."),
        ("scatter_plot", "3. Klaster Pelanggan", "Eksplorasi visualisasi 3D RFM dan segmentasi perilaku berbelanja."),
        ("hub", "4. Aturan Asosiasi", "Temukan rekomendasi bundling produk melalui aturan asosiasi dan grafik relasi."),
    ]
    for col, (icon, title, desc) in zip(step_cols, steps):
        with col:
            st.markdown(
                f"""
                <div class="process-step" style="min-height: 140px;">
                    <h4>{mi(icon, 18)} {title}</h4>
                    <p>{desc}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_about_page():
    """Render About page detailing the end-to-end data pipeline and feature mechanics."""
    section_header("info", "Tentang Sistem & Alur Pemrosesan Data", "Dokumentasi komprehensif alur komputasi dari data mentah hingga wawasan bisnis")

    st.markdown(
        f"""
        <div class="card">
            <h4>{mi('schema', 20)} Ringkasan Alur Kerja Data (End-to-End Pipeline)</h4>
            <p>
                Aplikasi ini dirancang untuk mengolah data transaksi retail mentah tanpa campur tangan teknis manual.
                Setiap tahapan komputasi diverifikasi secara bertahap dan dilengkapi indikator persentase loading.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    t1, t2, t3, t4 = st.tabs([
        "Tahap 1: Ekstraksi & Pembersihan",
        "Tahap 2: Segmentasi RFM & K-Means",
        "Tahap 3: Market Basket (FP-Growth)",
        "Spesifikasi Teknis & Kinerja",
    ])

    with t1:
        st.markdown(
            f"""
            <div class="process-step">
                <h4>{mi('filter_alt', 18)} 1. Sanitasi Kolom & Struktur</h4>
                <p>Nama kolom dibersihkan dari spasi (whitespace) di awal dan akhir agar pemanggilan atribut konsisten.</p>
            </div>
            <div class="process-step">
                <h4>{mi('person_remove', 18)} 2. Penyaringan CustomerID Kosong</h4>
                <p>Data transaksi tanpa ID pelanggan dihapus karena analisis RFM mensyaratkan identitas pembeli yang dapat dilacak secara unik.</p>
            </div>
            <div class="process-step">
                <h4>{mi('cancel', 18)} 3. Eliminasi Transaksi Pembatalan</h4>
                <p>Transaksi pembatalan/retur (nomor InvoiceNo diawali kode 'C' atau memiliki nilai Quantity ≤ 0) disaring dari kumpulan data penjualan bersih.</p>
            </div>
            <div class="process-step">
                <h4>{mi('payments', 18)} 4. Validasi UnitPrice & Kalkulasi Omset</h4>
                <p>Memastikan harga satuan produk bernilai positif (> 0), kemudian menghitung nilai omset transaksi per baris: <code>TotalPrice = Quantity × UnitPrice</code>.</p>
            </div>
            <div class="process-step">
                <h4>{mi('calendar_month', 18)} 5. Standarisasi Tipe Data Waktu</h4>
                <p>Kolom <code>InvoiceDate</code> diparsing ke format ISO datetime, dan entri tanggal invalid dieliminasi guna menjaga keabsahan perhitungan hari.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with t2:
        st.markdown(
            f"""
            <div class="process-step">
                <h4>{mi('calculate', 18)} 1. Rekayasa Fitur RFM</h4>
                <p>
                    • <strong>Recency (R)</strong>: Jumlah hari selisih antara tanggal transaksi terakhir pelanggan dengan batas waktu observasi (snapshot date = max date + 1 hari).<br>
                    • <strong>Frequency (F)</strong>: Jumlah transaksi unik (InvoiceNo) yang dilakukan oleh pelanggan.<br>
                    • <strong>Monetary (M)</strong>: Total pembelanjaan moneter (akumulasi TotalPrice) selama periode pencatatan.
                </p>
            </div>
            <div class="process-step">
                <h4>{mi('tune', 18)} 2. Normalisasi & Penanganan Outlier</h4>
                <p>
                    Outlier ekstrim di atas persentil ke-99 dipotong agar tidak membiaskan titik pusat klaster.
                    Ketiga fitur kemudian distandarisasi menggunakan <code>StandardScaler</code> (mean=0, variance=1)
                    agar dimensi moneter dengan skala ribuan tidak mendominasi dimensi frekuensi yang berskala puluhan.
                </p>
            </div>
            <div class="process-step">
                <h4>{mi('scatter_plot', 18)} 3. Klastering K-Means & Penamaan Segmen</h4>
                <p>
                    Model mengoptimasi posisi centroid melalui 300 iterasi konvergensi.
                    Klaster yang terbentuk kemudian diurutkan berdasarkan rata-rata pembelanjaan dan diberikan label bisnis deskriptif
                    (seperti Pelanggan Premium, Pelanggan Setia, Berisiko Pindah, dsb.).
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with t3:
        st.markdown(
            f"""
            <div class="process-step">
                <h4>{mi('table_rows', 18)} 1. Transformasi Matriks Keranjang Belanja</h4>
                <p>
                    Data transaksi dikelompokkan berdasarkan nomor faktur (<code>InvoiceNo</code>) dan deskripsi produk (<code>Description</code>).
                    Selanjutnya ditransformasikan menjadi matriks boolean satu-panas (One-Hot Encoded Basket) yang merepresentasikan kehadiran produk dalam transaksi.
                </p>
            </div>
            <div class="process-step">
                <h4>{mi('account_tree', 18)} 2. Ekstraksi Itemset dengan Pohon FP-Growth</h4>
                <p>
                    Berbeda dengan Apriori yang berulang kali memindai database secara penuh, FP-Growth membangun struktur pohon FP (Frequent Pattern Tree) ringkas
                    yang memproses kombinasi barang secara langsung dengan ambang batas <em>Minimum Support</em>.
                </p>
            </div>
            <div class="process-step">
                <h4>{mi('insights', 18)} 3. Penentuan Aturan Asosiasi (Support, Confidence, Lift)</h4>
                <p>
                    • <strong>Support</strong>: Probabilitas munculnya itemset dalam seluruh keranjang transaksi.<br>
                    • <strong>Confidence</strong>: Peluang bersyarat barang B terbeli jika barang A dibeli.<br>
                    • <strong>Lift</strong>: Rasio keterikatan nyata terhadap kebetulan acak. Nilai Lift > 1 menandakan asosiasi positif yang kuat antar produk.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with t4:
        st.markdown(
            f"""
            <div class="card">
                <h4>{mi('memory', 18)} Parameter & Batasan Kinerja</h4>
                <p>
                    • <strong>Kecepatan Respons</strong>: Ditargetkan &lt; 30 detik untuk dataset retail skala 500.000 baris.<br>
                    • <strong>Penggunaan Memori</strong>: Tetap terjaga &lt; 2 GB RAM dengan strategi sampling cerdas dan caching state Streamlit.<br>
                    • <strong>Privasi Data</strong>: 100% diproses di localhost tanpa integrasi API eksternal pihak ketiga.<br>
                    • <strong>Arsitektur Kode</strong>: Mengikuti prinsip Clean Code modular dengan pemisahan visualisasi, pemrosesan data, dan tata kelola state.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
