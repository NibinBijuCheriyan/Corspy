import streamlit as st
import pandas as pd
import plotly.express as px
from database import SessionLocal, ScrapedItem
from sqlalchemy import func
from datetime import datetime, timedelta

st.set_page_config(page_title="Corporate Spyglass", layout="wide")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

st.title("🕵️ Corporate Spyglass")
st.markdown("### Competitive Intelligence Dashboard")

# Sidebar
st.sidebar.header("Filters")
days_lookback = st.sidebar.slider("Lookback Period (Days)", 1, 90, 30)
min_score = st.sidebar.slider("Min Pivot Score", 0.0, 1.0, 0.5)

# Metrics
db = SessionLocal()
cutoff_date = datetime.now() - timedelta(days=days_lookback)
query = db.query(ScrapedItem).filter(ScrapedItem.date >= cutoff_date)

total_items = query.count()
high_alert_items = query.filter(ScrapedItem.pivot_score >= min_score).count()

col1, col2 = st.columns(2)
col1.metric("Total Items Scanned", total_items)
col2.metric("High Alert Items", high_alert_items)

# Charts
df = pd.read_sql(query.statement, db.bind)
if not df.empty:
    df['date'] = pd.to_datetime(df['date'])
    daily_counts = df.groupby([df['date'].dt.date, 'source']).size().reset_index(name='count')
    fig = px.bar(daily_counts, x='date', y='count', color='source', title="Mentions Over Time")
    st.plotly_chart(fig, use_container_width=True)

    # High Alert Table
    st.subheader("🚨 High Priority Alerts")
    high_alert_df = df[df['pivot_score'] >= min_score].sort_values(by='date', ascending=False)
    
    for index, row in high_alert_df.iterrows():
        with st.expander(f"{row['date'].date()} | {row['source']} | Score: {row['pivot_score']:.2f} - {row['title'][:80]}"):
            st.write(row['content'][:500] + "...")
            st.markdown(f"[Read More]({row['url']})")
else:
    st.info("No data found for the selected period.")

db.close()
