import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import time

st.set_page_config(layout='wide', page_title='Mottu - Dashboard')

engine = create_engine('sqlite:///./detections.db', connect_args={"check_same_thread": False})

st.title('Mottu - Live Detections Dashboard')

col1, col2 = st.columns([2,1])

with col1:
    if st.button('Refresh now'):
        st.experimental_rerun()

    @st.cache_data(ttl=2)
    def load_recent(n=200):
        try:
            df = pd.read_sql(f'SELECT id, timestamp, payload FROM detections ORDER BY id DESC LIMIT {n}', engine)
            return df
        except Exception as e:
            st.error("Error reading DB: " + str(e))
            return pd.DataFrame()

    df = load_recent(200)

    st.subheader('Recent detections (most recent first)')
    if df.empty:
        st.info('No detections yet. Run detector and backend.')
    else:
        # show summary fields to be more readable
        df_display = df.copy()
        df_display['time'] = pd.to_datetime(df_display['timestamp'], unit='s')
        df_display['n_detections'] = df_display['payload'].apply(lambda p: len(p.get('detections', [])) if isinstance(p, dict) else 0)
        st.dataframe(df_display[['id','time','n_detections']].set_index('id'))

with col2:
    st.subheader('Stats')
    if not df.empty:
        times = pd.to_datetime(df['timestamp'], unit='s')
        counts = times.dt.floor('T').value_counts().sort_index()
        st.line_chart(counts)
        st.write("Total persisted detections rows:", len(df))
    else:
        st.write("Waiting for data...")

st.markdown("---")
st.write("Tip: to collect metrics, check the detector console (FPS) and measurement of latency by comparing the detection timestamp with persistence time stored in DB.")
