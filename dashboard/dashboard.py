import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Baca dataset dan konversi tipe waktu
df = pd.read_csv('../data/orders_dataset.csv')
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
df['order_approved_at'] = pd.to_datetime(df['order_approved_at'])
df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'])
df['order_delivered_carrier_date'] = pd.to_datetime(df['order_delivered_carrier_date'])
df['order_estimated_delivery_date'] = pd.to_datetime(df['order_estimated_delivery_date'])

# **Tambahkan kolom 'delivery_duration_days'**
df['delivery_duration_days'] = (
    df['order_delivered_customer_date'] - df['order_delivered_carrier_date']
).dt.days

# Sidebar filter
st.sidebar.header('Filter by Status')
status_filter = st.sidebar.selectbox('Select Order Status', df['order_status'].unique())

# Filter data berdasarkan status
filtered_data = df[df['order_status'] == status_filter]

# Tampilkan data yang difilter
st.write(f"Orders with status: {status_filter}")
st.dataframe(filtered_data)

# Visualisasi: Durasi Pengiriman
st.header('Delivery Duration Distribution')
fig, ax = plt.subplots()

# **Pastikan kolom 'delivery_duration_days' ada dalam data yang difilter**
if 'delivery_duration_days' in filtered_data.columns:
    sns.histplot(filtered_data['delivery_duration_days'].dropna(), bins=20, kde=True, ax=ax)
    st.pyplot(fig)
else:
    st.write("No delivery duration data available for this status.")