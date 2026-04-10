import requests
import streamlit as st

from services.api_client import get_api_base_url, get_calculation, get_calculations, get_categories, solve_calculation


st.set_page_config(page_title="Hand Calculation App", page_icon="🧮", layout="centered")
st.title("🧮 Hand Calculation App")
st.caption("Frontend: Streamlit | Backend: FastAPI")

api_url = get_api_base_url()
st.write(f"Backend URL: `{api_url}`")

try:
    categories = get_categories()
except requests.RequestException as exc:
    st.error(f"Could not connect to the API. Error: {exc}")
    st.stop()

selected_category = st.selectbox("Select calculation type", categories)

calculations = get_calculations(selected_category)
calc_name_to_id = {item["name"]: item["id"] for item in calculations}
selected_calc_name = st.selectbox("Select related calculation", list(calc_name_to_id.keys()))
selected_calc_id = calc_name_to_id[selected_calc_name]

calc_meta = get_calculation(selected_calc_id)

st.subheader(calc_meta["name"])
st.write(calc_meta.get("description", ""))

values: dict[str, float] = {}
with st.form("calculation_form"):
    for field in calc_meta["inputs"]:
        values[field["key"]] = st.number_input(
            label=f"{field['label']} ({field.get('unit', '-')})",
            value=float(field.get("default", 0.0)),
            step=1.0,
            format="%.6f",
        )
    submitted = st.form_submit_button("Solve")

if submitted:
    try:
        result = solve_calculation(selected_calc_id, values)
        st.success("Calculation completed.")
        st.subheader("Outputs")
        for key, value in result["outputs"].items():
            st.write(f"**{key}** = {value}")
    except requests.RequestException as exc:
        st.error(f"Failed to solve calculation. Error: {exc}")
