# Proyek Analisis Data: E-Commerce Public Dataset

Proyek ini bertujuan untuk menganalisis E-Commerce Public Dataset guna menjawab pertanyaan bisnis terkait performa pendapatan kategori produk serta segmentasi pelanggan menggunakan analisis RFM.

## Struktur Direktori
- `dashboard/`: Berisi skrip dashboard Streamlit (`dashboard.py`) dan data utama (`main_data.csv`).
- `data/`: Berisi dataset mentah yang digunakan.
- `notebook.ipynb`: Jupyter Notebook yang berisi seluruh tahapan analisis dari gathering hingga visualization.
- `requirements.txt`: Daftar pustaka (library) Python yang dibutuhkan.
- `url.txt`: Tautan menuju dashboard yang telah di-deploy.

## Cara Menjalankan Dashboard (Lokal)
1.**Membuat Virtual Environment :**
   ```bash
   conda create --name main-ds python=3.9
   conda activate main-dsgit 
   ```
2. Pastikan Anda telah menginstal pustaka yang diperlukan dengan menjalankan:
    
   pip install -r requirements.txt

3. Jika sudah melakukan install pustaka maka lanjut melakukan streamlit:

   python -m streamlit run Dashboard/dashboard.py

4. Setelah melakukan streamlit maka akan muncul link url untuk membuka dashboard lokal.