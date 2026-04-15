import streamlit as st
import plotly.express as px
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.ema_api import fetch_epar_approvals, get_approvals_by_therapeutic_area

def show():
    st.header("🧬 EMA Drug Approvals Timeline")
    st.markdown("Approvals by therapeutic area over time, sourced from the EMA EPAR database.")

    with st.spinner("Fetching EMA approval data... (this may take 20–30 seconds)"):
        df_raw, error = fetch_epar_approvals()

    if error:
        st.error(f"Could not load EMA data: {error}")
        st.info("The EMA server may be temporarily unavailable. Try again in a few minutes.")
        return

    df, error = get_approvals_by_therapeutic_area(df_raw)

    if error:
        st.error(f"Data processing error: {error}")
        return

    st.sidebar.subheader("Filters")

    all_areas = sorted(df["therapeutic_area"].unique())
    selected_areas = st.sidebar.multiselect(
        "Therapeutic Areas",
        options=all_areas,
        default=all_areas[:10]
    )

    min_year = int(df["year"].min())
    max_year = int(df["year"].max())
    year_range = st.sidebar.slider(
        "Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(2010, max_year)
    )

    filtered = df[
        (df["therapeutic_area"].isin(selected_areas)) &
        (df["year"] >= year_range[0]) &
        (df["year"] <= year_range[1])
    ]

    if filtered.empty:
        st.warning("No data for the selected filters.")
        return

    fig = px.bar(
        filtered,
        x="year",
        y="approvals",
        color="therapeutic_area",
        title="EMA Drug Approvals by Therapeutic Area",
        labels={"year": "Year", "approvals": "Number of Approvals", "therapeutic_area": "Therapeutic Area"},
        barmode="stack"
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend_title="Therapeutic Area",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Summary Table")
    pivot = filtered.pivot_table(
        index="therapeutic_area",
        columns="year",
        values="approvals",
        fill_value=0
    )
    st.dataframe(pivot, use_container_width=True)