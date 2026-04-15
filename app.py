import streamlit as st

st.set_page_config(
    page_title="OpenPharma | EMA Intelligence Dashboard",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

from _pages import approvals, adverse, shortages

st.sidebar.image("https://www.ema.europa.eu/themes/custom/ema/images/ema-logo.svg", width=120)
st.sidebar.title("OpenPharma")
st.sidebar.markdown("*EMA Regulatory Intelligence*")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    options=[
        "EMA Approval Timeline",
        "Adverse Event Frequency",
        "Drug Shortage Alerts"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("Built by [Lippershey](https://lippershey.co)")
st.sidebar.markdown("Data: EMA EPAR | EudraVigilance | EMA Shortages")

if page == "EMA Approval Timeline":
    approvals.show()
elif page == "Adverse Event Frequency":
    adverse.show()
elif page == "Drug Shortage Alerts":
    shortages.show()
