import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import matplotlib.dates as mdates

sns.set(style='dark')

# Load data dari file CSV
orders_reviews = pd.read_csv('orders_reviews_items_df.csv')
orders_sellers = pd.read_csv('orders_products_sellers_df.csv')

# Mengubah format kolom tanggal menjadi tipe datetime agar bisa digunakan untuk filter
orders_sellers['order_purchase_timestamp'] = pd.to_datetime(orders_sellers['order_purchase_timestamp'])

# Menampilkan sidebar untuk filter data
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/3/3a/Placeholder_view_vector.svg", width=150)
st.sidebar.title("Filter E-Commerce")

# Filter berdasarkan rentang tanggal yang dipilih oleh pengguna
date_range = st.sidebar.date_input("Pilih Rentang Tanggal", [])
if date_range:
    start_date, end_date = date_range if len(date_range) == 2 else (date_range[0], date_range[0])
    filtered_orders = orders_sellers[(orders_sellers['order_purchase_timestamp'] >= pd.Timestamp(start_date)) &
                                     (orders_sellers['order_purchase_timestamp'] <= pd.Timestamp(end_date))]
else:
    filtered_orders = orders_sellers

# Menampilkan judul dashboard
st.title("📊 Dashboard E-Commerce")

# Menampilkan total pesanan dan total pendapatan
total_orders = filtered_orders.shape[0]
total_revenue = filtered_orders['price'].sum()
st.metric("Total Pesanan", total_orders)
st.metric("Total Pendapatan", f"AUD {total_revenue:,.2f}")

# Grafik jumlah pesanan harian
st.subheader("Pesanan Harian")
daily_orders = filtered_orders.groupby(filtered_orders['order_purchase_timestamp'].dt.date).size()
fig, ax = plt.subplots(figsize=(12, 6))
daily_orders.plot(kind='line', ax=ax, color='blue', linewidth=2)

# Format tanggal pada sumbu x
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=30))  # Menampilkan label setiap 30 hari
plt.xticks(rotation=45)  # Memutar label tanggal agar tidak bertumpuk

ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Pesanan")
ax.grid(True, linestyle='--', alpha=0.7)  # Menambahkan grid dengan garis putus-putus
st.pyplot(fig)

# Analisis kepuasan pelanggan berdasarkan review
st.subheader("Kepuasan Pelanggan")
avg_review_score = orders_reviews['review_score'].mean()
st.metric("Rata-rata Skor Review", round(avg_review_score, 2))
fig, ax = plt.subplots()
sns.histplot(orders_reviews['review_score'], bins=5, kde=True, ax=ax, color='orange')
ax.set_xlabel("Skor Review")
ax.set_ylabel("Jumlah")
st.pyplot(fig)

# Analisis performa seller berdasarkan jumlah pesanan dan pendapatan
st.subheader("Performa Seller")
seller_performance = filtered_orders.groupby('seller_id').agg({'order_id': 'count', 'price': 'sum'}).reset_index()
seller_performance.columns = ['ID Seller', 'Total Pesanan', 'Total Pendapatan']

# Mengambil 5 seller dengan performa terbaik dan terburuk
top_sellers = seller_performance.nlargest(5, 'Total Pendapatan')
bottom_sellers = seller_performance.nsmallest(5, 'Total Pendapatan')

# Menampilkan grafik performa seller terbaik
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=top_sellers, x='Total Pesanan', y='ID Seller', palette='Blues_r', ax=ax)
ax.set_xlabel("Total Pesanan")
ax.set_ylabel("ID Seller")
ax.set_title("5 Seller dengan Pendapatan Tertinggi")
st.pyplot(fig)

# Menampilkan grafik performa seller terburuk
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=bottom_sellers, x='Total Pesanan', y='ID Seller', palette='Reds_r', ax=ax)
ax.set_xlabel("Total Pesanan")
ax.set_ylabel("ID Seller")
ax.set_title("5 Seller dengan Pendapatan Terendah")
st.pyplot(fig)
