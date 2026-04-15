import streamlit as st
import plotly.express as px
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.ema_api import fetch_drug_shortages, get_shortages_by_country

def show():
    st.header("🚨 Drug Shortage Alerts by Country")
    st.markdown("Active medicine shortages across EU member states, sourced from the EMA shortage database.")

    with st.spinner("Fetching EMA shortage data..."):
        df_raw, error = fetch_drug_shortages()

    if error:
        st.error(f"Could not load shortage data: {error}")
        st.info("Try again in a few minutes or visit the EMA shortage page directly.")
        st.markdown("[EMA Medicine Shortages](https://www.ema.europa.eu/en/human-regulatory-overview/post-authorisation/availability-medicines/shortages-medicines)")
        return

    st.success(f"Loaded {len(df_raw)} shortage records from EMA.")

    summary, error = get_shortages_by_country(df_raw)

    if error:
        st.error(f"Data processing error: {error}")
        st.write("Raw columns available:", list(df_raw.columns))
        return

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            summary.head(20),
            x="shortage_count",
            y="country",
            orientation="h",
            title="Top 20 Countries by Active Shortages",
            labels={"shortage_count": "Number of Shortages", "country": "Country"},
            color="shortage_count",
            color_continuous_scale="Reds"
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=500,
            yaxis={"categoryorder": "total ascending"}
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Shortage Count by Country")
        st.dataframe(summary, use_container_width=True, height=500)

    st.subheader("Full Shortage Records")
    st.dataframe(df_raw, use_container_width=True)
