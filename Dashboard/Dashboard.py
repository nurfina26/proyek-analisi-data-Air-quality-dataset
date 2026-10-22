import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Beijing Air Quality Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('Dashboard/main_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

st.title("🌫️ Beijing Air Quality Dashboard - Mar 2013 to Feb 2017")
st.markdown("**Nur Fina Mafazah | Q1 Q2 Q3 Analysis | 12 Stations**")

# Sidebar filter
st.sidebar.header("Filter")
stations = st.sidebar.multiselect("Pilih Stasiun", df['station'].unique(), default=df['station'].unique()[:3])
season_filter = st.sidebar.multiselect("Pilih Musim", df['season'].unique(), default=df['season'].unique())

filtered = df[(df['station'].isin(stations)) & (df['season'].isin(season_filter))]

# KPI
col1, col2, col3, col4 = st.columns(4)
col1.metric("Rata-rata PM2.5", f"{filtered['PM2.5'].mean():.2f} µg/m³")
col2.metric("Rata-rata PM10", f"{filtered['PM10'].mean():.2f} µg/m³")
col3.metric("Bulan Terburuk", "Dec 2015 (148.76)")
col4.metric("Stasiun Terburuk", "Dongsi (85.70)")

st.divider()

# Q1
st.subheader("Q1: Tren Bulanan PM2.5 & PM10")
monthly = filtered.groupby(filtered['date'].dt.to_period('M'))[['PM2.5','PM10']].mean()
monthly.index = monthly.index.to_timestamp()
fig1, ax1 = plt.subplots(figsize=(12,4))
ax1.plot(monthly.index, monthly['PM2.5'], label='PM2.5', marker='o')
ax1.plot(monthly.index, monthly['PM10'], label='PM10', marker='o')
ax1.set_ylabel("µg/m³")
ax1.legend()
ax1.grid(True)
st.pyplot(fig1)
st.caption("Insight Q1: Puncak Dec 2015 = 148.76 µg/m³ & Feb 2014 = 144.32 µg/m³ (Winter)")

# Q2 & Q3 side by side
c1, c2 = st.columns(2)

with c1:
    st.subheader("Q2: Pengaruh Cuaca (WSPM -0.27)")
    corr = filtered[['PM2.5','TEMP','WSPM']].corr()
    fig2, ax2 = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax2)
    st.pyplot(fig2)
    st.caption("WSPM -0.27 paling berpengaruh, angin kencang = PM2.5 turun")

with c2:
    st.subheader("Q3: Stasiun & Musim Terburuk")
    station_avg = filtered.groupby('station')['PM2.5'].mean().sort_values(ascending=False)
    fig3, ax3 = plt.subplots()
    station_avg.plot(kind='bar', color='salmon', ax=ax3)
    ax3.set_ylabel("PM2.5")
    plt.xticks(rotation=45)
    st.pyplot(fig3)
    st.caption("Dongsi 85.70 tertinggi, Dingling 61.45 terbersih. Winter 94.90 vs Summer 64.46")

st.divider()
st.subheader("Data Preview (Daily - 17.532 rows)")
st.dataframe(filtered.head(10))

st.success("Kesimpulan: Fokus kebijakan di Dongsi saat Winter Nov-Feb + perkuat koridor angin (WSPM)")