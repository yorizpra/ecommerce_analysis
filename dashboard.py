# dashboard.py

import pandas as pd
import datetime as dt
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Setting up Streamlit
st.title("Proyek Analisis Data: Dataset Pesanan E-Commerce")
st.sidebar.header("Informasi")
st.sidebar.text("Nama: Yoga Rizki Pratama")
st.sidebar.text("Email: yogarizkipratama@gmail.com")
st.sidebar.text("ID Dicoding: yorizpra")

# Load dataset
data = pd.read_csv('orders_dataset.csv')
st.subheader("Dataset")
st.write(data.head())
st.write(f"Jumlah baris dan kolom: {data.shape}")

# Data Wrangling
data.info()
st.subheader("Info Dataset")
st.text("Memeriksa tipe data dari setiap kolom")

# Cleaning Data
for column in ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 
               'order_delivered_customer_date', 'order_estimated_delivery_date']:
    data[column] = pd.to_datetime(data[column])

# Add delivery_duration_days column
data['delivery_duration_days'] = (data['order_delivered_customer_date'] - data['order_purchase_timestamp']).dt.days

# EDA
st.subheader("Distribusi Waktu Pengiriman")
plt.figure(figsize=(10, 6))
sns.histplot(data['delivery_duration_days'].dropna(), bins=20, kde=True)
plt.title('Distribusi Waktu Pengiriman')
plt.xlabel('Hari')
plt.ylabel('Jumlah Pesanan')
st.pyplot(plt)

mean_delivery_time = data['delivery_duration_days'].mean()
st.write(f'Rata-rata waktu pengiriman: {mean_delivery_time:.2f} hari')

# Univariate Analysis
st.subheader("Distribusi Status Pesanan")
plt.figure(figsize=(10, 6))
sns.countplot(data=data, x='order_status')
plt.title('Distribusi Status Pesanan')
plt.xlabel('Status Pesanan')
plt.ylabel('Jumlah Pesanan')
st.pyplot(plt)

# Multivariate Analysis
st.subheader("Waktu Pengiriman Berdasarkan Status Pesanan")
plt.figure(figsize=(10, 6))
sns.boxplot(x='order_status', y='delivery_duration_days', data=data)
plt.title('Waktu Pengiriman Berdasarkan Status Pesanan')
plt.xlabel('Status Pesanan')
plt.ylabel('Durasi Pengiriman (Hari)')
st.pyplot(plt)

# Correlation Analysis
data['order_month'] = data['order_purchase_timestamp'].dt.month
correlation = data[['delivery_duration_days', 'order_month']].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(correlation, annot=True)
plt.title('Korelasi antara Durasi Pengiriman dan Bulan')
st.pyplot(plt)

# RFM Analysis
st.subheader("Analisis RFM")
snapshot_date = data['order_purchase_timestamp'].max() + dt.timedelta(days=1)

# Calculate Recency and Frequency
rf_data = data.groupby('customer_id').agg({
    'order_purchase_timestamp': lambda x: (snapshot_date - x.max()).days,
    'order_id': 'count'
}).reset_index()

# Rename columns
rf_data.columns = ['customer_id', 'Recency', 'Frequency']
st.write(rf_data)

# Insights
st.subheader("Insight")
st.write("""
1. **Identifying Active Customers**: Pelanggan dengan nilai Recency rendah menunjukkan bahwa mereka baru saja melakukan pembelian.
2. **Identifying Loyal Customers**: Pelanggan dengan nilai Frequency tinggi adalah pelanggan yang sering bertransaksi dan bisa dianggap loyal.
3. **Identifying At-Risk Customers**: Pelanggan dengan nilai Recency tinggi menunjukkan bahwa sudah cukup lama sejak mereka melakukan pembelian terakhir.
4. **Segmentation Suggestions**: Loyalists, At-Risk, dan New Customers.
""")

# Conclusion
st.subheader("Kesimpulan")
st.write("""
- **Kesimpulan Pertanyaan 1**: Rata-rata waktu pengiriman adalah sekitar 12 hari.
- **Kesimpulan Pertanyaan 2**: Ada variasi dalam durasi pengiriman berdasarkan hari dan bulan.
- **Kesimpulan Analisis Lanjutan**: RFM Analysis dapat membantu dalam membedakan antara pelanggan yang aktif dan pelanggan yang berisiko.
""")

if __name__ == "__main__":
    st.write("Dashboard siap dijalankan!")
