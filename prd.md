# Product Requirements Document (PRD): Sistem Cerdas E-Commerce (Customer Segmentation & Market Basket Analysis)

## 1. Ringkasan Eksekutif

Sistem ini adalah aplikasi desktop/lokal berbasis web yang dirancang untuk menganalisis dataset transaksi retail (500.000+ baris). Aplikasi ini memiliki dua fitur utama: **Customer Segmentation** untuk mengelompokkan pelanggan berdasarkan perilaku belanja, dan **Market Basket Analysis (MBA)** untuk menemukan pola pembelian barang secara bersamaan. Sistem dirancang seringan mungkin, 100% gratis (open-source), dan dijalankan secara lokal untuk keperluan tugas akademik.

## 2. Tujuan Produk

* **Analitik Tepat Guna:** Mengubah raw data Excel/CSV menjadi insight bisnis visual.
* **Performa Ringan:** Mampu memproses 500 ribu baris data di laptop standar tanpa memerlukan spesifikasi server tinggi atau layanan cloud berbayar.
* **GUI Intuitif:** Menyediakan antarmuka interaktif yang mudah digunakan tanpa perlu mengetik kode (no-code interface bagi pengguna akhir).

## 3. Spesifikasi Teknologi (Gratis & Ringan)

Pendekatan terbaik untuk tugas ini adalah menggunakan **Python** dengan framework **Streamlit**, karena sangat ringan, tidak berbayar, dan memiliki GUI yang modern.

* **Bahasa Pemrograman:** Python 3.10+
* **Framework GUI:** Streamlit (Membangun UI interaktif secara lokal di browser).
* **Data Processing:** Pandas (untuk manipulasi data) & Numpy. Disarankan file Excel dikonversi ke CSV agar proses unggah dan pembacaan jauh lebih ringan.
* **Machine Learning (Segmentation):** Scikit-learn (K-Means Clustering) dipadukan dengan pemodelan RFM (Recency, Frequency, Monetary).
* **Market Basket Analysis:** `mlxtend` (menggunakan algoritma **FP-Growth** yang terbukti jauh lebih cepat dan ringan dibanding Apriori untuk data 500k+ baris).
* **Visualisasi:** Plotly (untuk grafik interaktif) & Seaborn/Matplotlib.

---

## 4. Kebutuhan Fungsional (Fitur Sistem)

### A. Modul Input & Preprocessing Data

* **Upload Data:** Fitur drag-and-drop untuk mengunggah file data.
* **Data Cleaning Otomatis:**
* Menghapus baris dengan `CustomerID` kosong (null).
* Menghapus transaksi yang dibatalkan (biasanya `InvoiceNo` diawali huruf 'C' atau `Quantity` negatif).
* Standarisasi format `InvoiceDate` menjadi tipe *datetime*.


* **Caching Data:** Sistem menyimpan data di memori lokal sementara (*caching*) agar pengguna tidak perlu menunggu proses unggah saat berpindah halaman/fitur.

### B. Modul Customer Segmentation (RFM + K-Means)

* **Perhitungan RFM Otomatis:**
* *Recency:* Berapa hari sejak transaksi terakhir pelanggan.
* *Frequency:* Berapa kali pelanggan berbelanja.
* *Monetary:* Total uang yang dihabiskan (`Quantity` * `UnitPrice`).


* **Pemodelan K-Means Clustering:** Mengelompokkan pelanggan berdasarkan nilai RFM ke dalam *cluster* (misal: Pelanggan Setia, Berisiko Hilang, Pelanggan Baru).
* **Kontrol GUI:** Slider untuk menentukan jumlah *cluster* (K) secara dinamis.
* **Visualisasi:** 3D Scatter Plot (Recency vs Frequency vs Monetary) dan Bar Chart persentase pelanggan per segmen.

### C. Modul Market Basket Analysis (FP-Growth)

* **Pemrosesan Transaksi:** Mengelompokkan `Description` produk berdasarkan `InvoiceNo`.
* **Kontrol Parameter GUI:**
* Slider untuk *Minimum Support* (misal: 0.01 atau 1%).
* Slider untuk *Minimum Lift* (mengukur kekuatan asosiasi).


* **Tabel Aturan Asosiasi (Association Rules):** Menampilkan tabel yang berisi *Antecedents* (jika beli barang A) dan *Consequents* (maka beli barang B), lengkap dengan nilai *Confidence* dan *Lift*.
* **Visualisasi Jaringan:** Network Graph sederhana atau Heatmap untuk menunjukkan hubungan antar produk yang sering dibeli bersamaan.

---

## 5. Kebutuhan Non-Fungsional

* **Local Host:** Sistem berjalan di `localhost:8501` dan tidak mengirim data ke internet.
* **Waktu Pemrosesan:** Menggunakan algoritma FP-Growth dan memori *caching*, analisis harus selesai dalam waktu kurang dari 30 detik untuk dataset 500k baris.
* **Resource:** Penggunaan RAM ditargetkan di bawah 2GB saat melakukan *training* model.

## 6. Desain Arsitektur Antarmuka (UI/UX)

Sistem akan memiliki **Sidebar Navigasi** dengan 4 menu utama:

1. **Beranda:** Pengantar dan ringkasan dataset.
2. **Data Explorer:** Tempat upload file, melihat cuplikan tabel data mentah, dan statistik deskriptif awal.
3. **Customer Segmentation:** Halaman berisi slider K-Means, tabel metrik RFM, dan grafik sebaran pelanggan.
4. **Market Basket Analysis:** Halaman berisi kontrol parameter Support/Confidence, tabel rekomendasi bundel produk, dan grafik asosiasi.

## 7. Metrik Keberhasilan (Untuk Tugas)

1. Sistem berhasil berjalan di laptop lokal tanpa error.
2. File dataset 500.000 baris berhasil dimuat dan dibersihkan.
3. Sistem mampu menghasilkan minimal 3 segmen pelanggan yang masuk akal secara bisnis.
4. Sistem berhasil memunculkan aturan asosiasi (misal: "Pelanggan yang membeli *Jumbo Bag Red Retrosport* juga membeli *Jumbo Bag Pink Polkadot*").