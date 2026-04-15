import requests
import pandas as pd

EMA_BASE = "https://www.ema.europa.eu"

def fetch_epar_approvals():
    url = f"{EMA_BASE}/en/documents/report/medicines-output-medicines-report_en.xlsx"
    try:
        response = requests.get(url, timeout=60, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        df = pd.read_excel(pd.io.common.BytesIO(response.content), sheet_name=0, engine="openpyxl", header=8)
        df.columns = [str(c).strip() for c in df.columns]
        df = df.loc[:, ~df.columns.str.startswith("Unnamed")]
        return df, None
    except Exception as e:
        return None, str(e)

def get_approvals_by_therapeutic_area(df):
    name_col = "Name of medicine"
    ta_col = "Therapeutic area (MeSH)"
    date_col = "Marketing authorisation date"
    for col in [name_col, ta_col, date_col]:
        if col not in df.columns:
            return None, f"Missing column: '{col}'. Available: {list(df.columns)}"
    df = df[[name_col, ta_col, date_col]].dropna()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df["year"] = df[date_col].dt.year
    df = df[df["year"] >= 2000]
    summary = df.groupby([ta_col, "year"]).size().reset_index(name="approvals").rename(columns={ta_col: "therapeutic_area"})
    return summary, None

def fetch_adverse_events(medicine_name: str):
    try:
        response = requests.get(
            f"https://www.adrreports.eu/services/esearch?medicine={requests.utils.quote(medicine_name)}",
            timeout=15, headers={"Accept": "application/json"}
        )
        response.raise_for_status()
        return response.json(), None
    except Exception as e:
        return None, str(e)

def fetch_drug_shortages():
    url = f"{EMA_BASE}/en/documents/report/medicines-output-shortages-report_en.xlsx"
    try:
        response = requests.get(url, timeout=60, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        df = pd.read_excel(pd.io.common.BytesIO(response.content), sheet_name=0, engine="openpyxl", header=8)
        df.columns = [str(c).strip() for c in df.columns]
        df = df.loc[:, ~df.columns.str.startswith("Unnamed")]
        return df, None
    except Exception as e:
        return None, str(e)

def get_shortages_by_country(df):
    country_col = next((c for c in df.columns if "country" in c.lower()), None)
    status_col = next((c for c in df.columns if "status" in c.lower()), None)
    if not country_col:
        return None, f"Could not find country column. Available: {list(df.columns)}"
    active = df[df[status_col].str.lower().str.contains("ongoing|active", na=False)] if status_col else df
    summary = active.groupby(country_col).size().reset_index(name="shortage_count").rename(columns={country_col: "country"}).sort_values("shortage_count", ascending=False)
    return summary, None