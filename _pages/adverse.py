import streamlit as st
import plotly.express as px
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.ema_api import fetch_adverse_events

def show():
    st.header("⚠️ Adverse Event Frequency by Drug")
    st.markdown("Search EudraVigilance for adverse event reports on any EMA-approved medicine.")

    drug_name = st.text_input("Enter a medicine name", placeholder="e.g. ibuprofen, atorvastatin, pembrolizumab")

    if not drug_name:
        st.info("Enter a medicine name above to search adverse event reports.")
        return

    with st.spinner(f"Searching EudraVigilance for '{drug_name}'..."):
        data, error = fetch_adverse_events(drug_name)

    if error:
        st.error(f"Could not retrieve data: {error}")
        st.markdown("You can also search directly at [EudraVigilance](https://www.adrreports.eu/en/search.html)")
        return

    if not data:
        st.warning(f"No adverse event records found for '{drug_name}'.")
        return

    st.success(f"Results for: **{drug_name}**")

    if isinstance(data, list) and len(data) > 0:
        import pandas as pd
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
    elif isinstance(data, dict):
        import pandas as pd
        df = pd.DataFrame([data])
        st.dataframe(df, use_container_width=True)
    else:
        st.json(data)

    st.markdown("---")
    st.markdown(
        f"[View full report on EudraVigilance](https://www.adrreports.eu/en/search.html#) "
        f"— search for **{drug_name}** for detailed SOC breakdowns."
    )
