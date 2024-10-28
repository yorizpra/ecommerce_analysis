import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Baca dataset dan konversi tipe waktu
try:
    df = pd.read_csv('../data/orders_dataset.csv')
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    df['order_approved_at'] = pd.to_datetime(df['order_approved_at'])
    df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'])
    df['order_delivered_carrier_date'] = pd.to_datetime(df['order_delivered_carrier_date'])
    df['order_estimated_delivery_date'] = pd.to_datetime(df['order_estimated_delivery_date'])

    # Tambahkan kolom 'delivery_duration_days'
    df['delivery_duration_days'] = (
        df['order_delivered_customer_date'] - df['order_delivered_carrier_date']
    ).dt.days
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Sidebar filter
st.sidebar.header('Filter by Order Status')
status_options = df['order_status'].unique()
status_filter = st.sidebar.selectbox('Select Order Status', status_options)

# Filter data berdasarkan status
filtered_data = df[df['order_status'] == status_filter]

# Tampilkan data yang difilter
st.write(f"Orders with status: **{status_filter}**")
st.write(f"Total orders displayed: {len(filtered_data)}")
st.dataframe(filtered_data)

# Visualisasi: Distribusi Durasi Pengiriman
st.header('Delivery Duration Distribution')

fig, ax = plt.subplots()
if 'delivery_duration_days' in filtered_data.columns and not filtered_data['delivery_duration_days'].isnull().all():
    sns.histplot(filtered_data['delivery_duration_days'].dropna(), bins=20, kde=True, ax=ax)
    ax.set_xlabel('Delivery Duration (days)')
    ax.set_ylabel('Frequency')
    ax.set_title(f'Distribution of Delivery Duration for Orders with Status: {status_filter}')
    st.pyplot(fig)
else:
    st.write("No delivery duration data available for this status.")
