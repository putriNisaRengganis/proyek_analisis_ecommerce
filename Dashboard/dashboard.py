import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Dashboard E-Commerce Dicoding", layout="wide")

sns.set_theme(style="whitegrid")

st.title("📊 Dashboard Analisis E-Commerce (Proyek Akhir)")
st.markdown("---")


@st.cache_data
def load_data():
  df = pd.read_csv("Dashboard/main_data.csv")
  df["order_purchase_timestamp"] = pd.to_datetime(
      df["order_purchase_timestamp"]
  )
  return df


df = load_data()

# ==========================================
# FITUR INTERAKTIF (Filter Rentang Tanggal)
# ==========================================
st.sidebar.header("Filter Interaktif")

min_date = df["order_purchase_timestamp"].min().date()
max_date = df["order_purchase_timestamp"].max().date()

date_range = st.sidebar.date_input(
    label="Rentang Waktu (Filter Visualisasi)",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date,
)

if len(date_range) == 2:
  start_date, end_date = date_range
else:
  start_date = end_date = date_range[0]

# Terapkan filter ke dataframe utama
filtered_df = df[
    (df["order_purchase_timestamp"].dt.date >= start_date)
    & (df["order_purchase_timestamp"].dt.date <= end_date)
]

st.sidebar.markdown("---")
st.sidebar.header("Informasi Proyek")
st.sidebar.write("**Nama:** Putri Nisa Rengganis")
st.sidebar.write("**Dataset:** E-Commerce Public Dataset")

# ==========================================
# PERTANYAAN 1: Kategori Produk (Revenue Tertinggi & Terendah)
# ==========================================
st.header("🛒 Pertanyaan 1: Performa Pendapatan Kategori Produk")
st.write(
    "Menganalisis kategori produk dengan total pendapatan (revenue) tertinggi"
    " dan terendah berdasarkan rentang waktu yang dipilih."
)

if (
    "product_category_name_english" in filtered_df.columns
    and "price" in filtered_df.columns
):
  col1, col2 = st.columns(2)

  cat_rev = (
      filtered_df.groupby("product_category_name_english")["price"]
      .sum()
      .reset_index()
  )

  with col1:
    st.subheader("5 Kategori Revenue Tertinggi")
    top_rev = cat_rev.sort_values(by="price", ascending=False).head(5)
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(
        x="price",
        y="product_category_name_english",
        data=top_rev,
        color="#2b5c8f",
        ax=ax,
    )  # Warna seragam profesional
    ax.set_xlabel("Total Revenue (BRL)")
    ax.set_ylabel("")
    st.pyplot(fig)

  with col2:
    st.subheader("5 Kategori Revenue Terendah")
    bot_rev = cat_rev.sort_values(by="price", ascending=True).head(5)
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(
        x="price",
        y="product_category_name_english",
        data=bot_rev,
        color="#d9534f",
        ax=ax,
    )  # Warna seragam senada untuk nilai terendah
    ax.set_xlabel("Total Revenue (BRL)")
    ax.set_ylabel("")
    st.pyplot(fig)
else:
  st.info(
      "Kolom untuk analisis kategori produk belum terdeteksi di dataset."
  )

st.markdown("---")

# ==========================================
# PERTANYAAN 2: Analisis RFM & Segmentasi Pelanggan
# ==========================================
st.header("👥 Pertanyaan 2: Analisis Segmen Pelanggan (RFM Analysis)")
st.write(
    "Mengidentifikasi performa pelanggan berdasarkan segmentasi RFM (Recency,"
    " Frequency, Monetary) dari data yang telah difilter."
)

if (
    "customer_unique_id" in filtered_df.columns
    and "order_purchase_timestamp" in filtered_df.columns
):
  recent_date = filtered_df["order_purchase_timestamp"].max() + pd.Timedelta(
      days=1
  )

  rfm_df = (
      filtered_df.groupby("customer_unique_id")
      .agg({
          "order_purchase_timestamp": lambda x: (
              recent_date - x.max()
          ).days,
          "order_id": "nunique",
          "price": "sum",
      })
      .reset_index()
  )

  rfm_df.columns = ["customer_unique_id", "recency", "frequency", "monetary"]

  # Scoring RFM
  rfm_df["r_score"] = pd.qcut(
      rfm_df["recency"], 5, labels=[5, 4, 3, 2, 1], duplicates="drop"
  )
  rfm_df["f_score"] = pd.qcut(
      rfm_df["frequency"].rank(method="first"),
      5,
      labels=[1, 2, 3, 4, 5],
      duplicates="drop",
  )
  rfm_df["m_score"] = pd.qcut(
      rfm_df["monetary"], 5, labels=[1, 2, 3, 4, 5], duplicates="drop"
  )

  rfm_df[["r_score", "f_score", "m_score"]] = rfm_df[
      ["r_score", "f_score", "m_score"]
  ].astype(int)


  def segment_customer(row):
    if row["f_score"] >= 4 and row["m_score"] >= 4:
      return "Top Customers"
    elif row["f_score"] >= 3 or row["m_score"] >= 3:
      return "Potential Customers"
    else:
      return "Low-Value / At-Risk Customers"


  rfm_df["customer_segment"] = rfm_df.apply(segment_customer, axis=1)

  # Visualisasi Konsisten dengan Notebook (2 Grafik Berdampingan: Jumlah Pelanggan & Revenue per Segmen)
  col_rfm1, col_rfm2 = st.columns(2)

  with col_rfm1:
    st.subheader("Jumlah Pelanggan per Segmen RFM")
    segment_counts = rfm_df["customer_segment"].value_counts().reset_index()
    segment_counts.columns = ["customer_segment", "count"]

    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(
        x="count",
        y="customer_segment",
        data=segment_counts,
        color="#38a3a5",
        ax=ax,
    )
    ax.set_xlabel("Jumlah Pelanggan")
    ax.set_ylabel("Segmen Pelanggan")
    st.pyplot(fig)

  with col_rfm2:
    st.subheader("Total Kontribusi Revenue per Segmen")
    segment_revenue = (
        rfm_df.groupby("customer_segment")["monetary"].sum().reset_index()
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(
        x="monetary",
        y="customer_segment",
        data=segment_revenue,
        color="#57cc99",
        ax=ax,
    )
    ax.set_xlabel("Total Revenue (BRL)")
    ax.set_ylabel("")
    st.pyplot(fig)

else:
  st.info("Kolom untuk analisis RFM belum lengkap terdeteksi pada dataset.")