import os
import requests
import streamlit as st


def get_api_base_url() -> str:
    return st.secrets.get("API_BASE_URL", os.getenv("API_BASE_URL", "http://localhost:8000"))


def get_categories() -> list[str]:
    response = requests.get(f"{get_api_base_url()}/categories", timeout=30)
    response.raise_for_status()
    return response.json()["categories"]


def get_calculations(category: str) -> list[dict]:
    response = requests.get(f"{get_api_base_url()}/categories/{category}/calculations", timeout=30)
    response.raise_for_status()
    return response.json()["calculations"]


def get_calculation(calc_id: str) -> dict:
    response = requests.get(f"{get_api_base_url()}/calculations/{calc_id}", timeout=30)
    response.raise_for_status()
    return response.json()


def solve_calculation(calc_id: str, values: dict[str, float]) -> dict:
    response = requests.post(
        f"{get_api_base_url()}/calculations/{calc_id}/solve",
        json={"values": values},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
