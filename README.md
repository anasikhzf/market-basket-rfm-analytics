# Sistem Cerdas Analisis Transaksi E-Commerce
### Customer Segmentation (RFM + K-Means) & Market Basket Analysis (FP-Growth)

Platform analitik berbasis web yang dirancang untuk mengolah data transaksi retail skala besar menjadi wawasan strategis bisnis. Sistem ini menyediakan pembersihan data otomatis, segmentasi pelanggan berdasarkan perilaku belanja (Recency, Frequency, Monetary), serta identifikasi pola pembelian bersamaan (*cross-selling/bundling*) dengan algoritma yang efisien.

---

## 📌 Fitur Utama

1. **Eksplorasi & Pembersihan Data Otomatis (Data Explorer)**
   - Mendukung dua opsi dataset: unggah berkas baru (CSV / Excel) atau gunakan dataset contoh bawaan (`OnlineRetail.xlsx`).
   - Pembersihan otomatis: sanitasi nama kolom, eliminasi `CustomerID` kosong, penghapusan transaksi retur/batal (`InvoiceNo` awalan 'C' & kuantitas negatif), validasi harga, konversi datetime, dan komputasi nilai transaksi (`TotalPrice`).
   - Indikator pemrosesan interaktif dengan persentase numerik spesifik (0% s/d 100%).

2. **Customer Segmentation (RFM + K-Means Clustering)**
   - Rekayasa fitur **RFM**: *Recency* (hari sejak transaksi terakhir), *Frequency* (jumlah transaksi unik), dan *Monetary* (total pembelanjaan).
   - Penanganan outlier ekstrim dan normalisasi data dengan `StandardScaler`.
   - Analisis nilai klaster optimal menggunakan **Metode Elbow** (Inertia plot).
   - Visualisasi interaktif: **3D Scatter Plot RFM**, Bar chart distribusi pelanggan, Pie/Donut chart proporsi segmen, serta tabel perbandingan profil pelanggan.

3. **Market Basket Analysis (FP-Growth & Aturan Asosiasi)**
   - Menggunakan algoritma **FP-Growth** yang jauh lebih cepat dan hemat memori dibanding Apriori konvensional untuk data 500.000+ baris.
   - Kontrol parameter dinamis: slider *Minimum Support*, *Minimum Lift*, dan ukuran sampel transaksi.
   - Visualisasi relasi produk: **Grafik Jejaring Produk (Network Graph)** interaktif, **Heatmap Asosiasi**, dan tabel peringkat aturan asosiasi (*antecedents* & *consequents*).

4. **Desain Minimalis Modern & Pengalihan Tema (Dark/Light Mode)**
   - Antarmuka modern bertema minimalis dengan tipografi **Google Font Inter** dan ikon **Google Material Symbols** (tanpa icon emoji bawaan).
   - Toggle switch **Mode Gelap / Terang** dengan penyesuaian instan pada palet warna dan tema grafik Plotly.
   - Desain responsif di berbagai ukuran layar (desktop, tablet, dan smartphone).

5. **Halaman Dokumentasi Alur Sistem (Tentang Sistem)**
   - Menyajikan dokumentasi menyeluruh mengenai alur kerja *end-to-end* yang dilakukan kode terhadap dataset dari tahap awal hingga akhir beserta rincian teknis setiap fitur.

---

## 🛠️ Teknologi yang Digunakan

- **Bahasa & Framework Utama:** Python 3.10+, [Streamlit](https://streamlit.io/)
- **Manipulasi & Analisis Data:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Machine Learning (Clustering):** [Scikit-learn](https://scikit-learn.org/) (K-Means, StandardScaler)
- **Data Mining (Association Rules):** [mlxtend](http://rasbt.github.io/mlxtend/) (FP-Growth, Association Rules)
- **Visualisasi Data Interaktif:** [Plotly](https://plotly.com/python/), [NetworkX](https://networkx.org/)
- **Parser File Excel:** [openpyxl](https://openpyxl.readthedocs.io/)
- **Styling & Ikonografi:** Vanilla CSS (CSS Variables, Flexbox, Grid), Google Fonts Inter, Google Material Symbols

---

## 📁 Struktur Direktori Proyek

Proyek ini dibangun dengan prinsip *Clean Code* terstruktur, modular, dan membatasi ukuran berkas maksimal di bawah 500 baris kode:

```text
CustomerSegmentation&MarketBasketAnalysis/
├── .streamlit/
│   └── config.toml             # Konfigurasi server Streamlit
├── utils/
│   ├── __init__.py             # Inisialisasi package utils
│   ├── helpers.py              # Helper Material Icons, section header, banner
│   ├── charts.py               # Konfigurasi tema & palet warna grafik Plotly
│   ├── data_processing.py      # Pemuatan data & pipeline data cleaning (+ progress %)
│   ├── segmentation.py         # Komputasi RFM, Elbow method, & K-Means clustering
│   ├── market_basket.py        # Pipeline FP-Growth & pembentukan aturan asosiasi
│   ├── viz.py                  # Pembangun grafik interaktif 3D, bar, network, & heatmap
│   ├── views_home.py           # Render tampilan Halaman Beranda & Tentang Sistem
│   ├── views_analysis.py       # Render tampilan Data Explorer & Customer Segmentation
│   └── views_mba.py            # Render tampilan Market Basket Analysis
├── OnlineRetail.xlsx           # Dataset contoh transaksi retail
├── app.py                      # Titik masuk utama aplikasi (routing & state management)
├── styles.py                   # Modul CSS dinamis (Light/Dark mode & media queries)
├── requirements.txt            # Daftar pustaka dependensi Python
├── prd.md                      # Dokumen spesifikasi kebutuhan produk
└── README.md                   # Dokumentasi proyek
```

---

## 🚀 Panduan Instalasi & Menjalankan Aplikasi

### 1. Prasyarat Sistem
- Python versi 3.10 atau yang lebih baru terpasang di sistem.
- Git (opsional untuk cloning repositori).

### 2. Kloning atau Buka Direktori Proyek
```bash
cd d:\www\CustomerSegmentation&MarketBasketAnalysis
```

### 3. Buat dan Aktifkan Virtual Environment (Disarankan)
- **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 4. Pasang Dependensi
Pasang seluruh paket yang dibutuhkan melalui `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 5. Jalankan Aplikasi
Jalankan server aplikasi lokal Streamlit:
```bash
streamlit run app.py
```

Setelah perintah dijalankan, antarmuka web akan otomatis terbuka di browser pada alamat:
```
http://localhost:8501
```

---

## 💻 Panduan Penggunaan & Demo Alur Kerja

1. **Halaman Beranda (`Beranda`)**
   - Melihat ringkasan pengenalan platform, penjelasan modul RFM + K-Means, FP-Growth, dan panduan langkah cepat.
2. **Halaman Data Explorer (`Data Explorer`)**
   - Pilih sumber data: klik tombol **"Muat Berkas Contoh"** untuk langsung menggunakan berkas bawaan `OnlineRetail.xlsx` atau unggah berkas transaksi CSV/Excel kustom Anda.
   - Amati progress loading dengan indikator persentase angka (0% - 100%) dan ringkasan metrik statistik data bersih.
3. **Halaman Segmentasi Pelanggan (`Customer Segmentation`)**
   - Tinjau metrik RFM setiap pelanggan.
   - Tentukan jumlah klaster (K) menggunakan slider, periksa kurva Elbow jika diinginkan, lalu amati visualisasi interaktif **3D Scatter Plot** serta distribusi segmen pelanggan (misal: Pelanggan Premium, Pelanggan Setia, Berisiko Pindah, dsb.).
4. **Halaman Market Basket Analysis (`Market Basket Analysis`)**
   - Atur nilai *Minimum Support* (contoh: `0.02`) dan *Minimum Lift* (contoh: `1.5`).
   - Klik **"Mulai Analisis Keranjang"** untuk mengekstrak aturan asosiasi.
   - Eksplorasi tabel rekomendasi bundling produk, bar chart aturan teratas, visualisasi jejaring produk (*Network Graph*), dan matriks *Heatmap*.
5. **Halaman Tentang Sistem (`Tentang Sistem`)**
   - Membaca dokumentasi mendalam tentang mekanisme pembersihan data, logika matematika pembentukan skor RFM, efisiensi algoritma pohon FP-Growth, dan standar keamanan komputasi lokal.
6. **Pengalihan Mode Tema**
   - Klik sakelar **"Mode Gelap"** pada sidebar kiri kapan saja untuk beralih antara tema gelap elegan atau tema terang yang bersih.

---

## 📄 Lisensi & Privasi Data

- Sistem ini berjalan sepenuhnya pada lingkungan lokal (*localhost*), menjamin keamanan dan privasi data transaksi bisnis Anda tanpa dikirim ke server pihak ketiga di internet.
