import requests
import streamlit as st

from api.client import get_error_message, get_favorites
from auth.state import require_login
from components.item_card import render_item_cards


require_login()
st.header("Избранное")

try:
    response = get_favorites()
except requests.RequestException:
    st.error("Не удалось выполнить запрос к backend.")
    st.stop()

if not response.ok:
    st.error(get_error_message(response))
    st.stop()

items = response.json()     

for item in items:
    render_item_cards(item)