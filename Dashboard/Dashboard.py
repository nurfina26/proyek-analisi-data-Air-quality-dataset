import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob

st.set_page_config(page_title="Beijing Air Quality", layout="wide")
st.title("Beijing Air Quality Dashboard 2013-2017")

@st.cache_data
def load_data():
    files = glob.glob("data/PRSA_Data_20130301-20170228/*.csv")
    if not files:
        files = glob.glob("PRSA_Data_20130301-20170228/*.csv")
    if not files:
        files = glob.glob("data/*.csv")
    df_list = [pd.read_csv(f) for f in files]
    df = pd.concat(df_list, ignore_index=True)
    def get_season(m):
        if m in [3,4,5]: return "Spring"
        elif m in [6,7,8]: return "Summer"
        elif m in [9,10,11]: return "Fall"
        else: return "Winter"
    df['season'] = df['month'].apply(get_season)
    return df

df = load_data()
df_clean = df.dropna(subset=['PM2.5','TEMP','DEWP','WSPM','PRES','CO','NO2','O3'])

# Q1
st.header("Q1: Tren Bulanan PM2.5 & PM10")
monthly = df.groupby(['year','month'])[['PM2.5','PM10']].mean().reset_index()
monthly['date'] = pd.to_datetime(monthly[['year','month']].assign(day=1))
fig, ax = plt.subplots(figsize=(10,4))
ax.plot(monthly['date'], monthly['PM2.5'], label='PM2.5')
ax.plot(monthly['date'], monthly['PM10'], label='PM10')
ax.legend()
st.pyplot(fig)

# Q2 FIX: 4 variabel wajib
st.header("Q2: Pengaruh TEMP, DEWP, WSPM, PRES terhadap PM2.5")
corr_q2 = df_clean[['PM2.5','TEMP','DEWP','WSPM','PRES']].corr()
fig2, ax2 = plt.subplots()
sns.heatmap(corr_q2, annot=True, cmap='coolwarm', ax=ax2)
st.pyplot(fig2)

st.subheader("Korelasi Polutan CO, NO2, O3")
corr_pol = df_clean[['PM2.5','CO','NO2','O3']].corr()
fig_pol, ax_pol = plt.subplots()
sns.heatmap(corr_pol, annot=True, cmap='coolwarm', ax=ax_pol)
st.pyplot(fig_pol)

# Q3 FIX: Stasiun + Musim
st.header("Q3: Stasiun & Musim Terburuk")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Per Stasiun")
    station_avg = df.groupby('station')['PM2.5'].mean().sort_values(ascending=False)
    fig3, ax3 = plt.subplots(figsize=(8,5))
    station_avg.plot(kind='bar', ax=ax3)
    st.pyplot(fig3)
with col2:
    st.subheader("Per Musim")
    season_avg = df.groupby('season')['PM2.5'].mean().reindex(["Spring","Summer","Fall","Winter"])
    fig4, ax4 = plt.subplots()
    season_avg.plot(kind='bar', ax=ax4, color=['green','orange','brown','blue'])
    st.pyplot(fig4)