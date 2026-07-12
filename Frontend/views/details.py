import requests
import streamlit as st

from api.client import get_error_message, get_car
from components.item_card import render_admin_actions, render_favorite_button


item_id = st.session_state.get("selected_item_id")

if item_id is None:
    st.info("Сначала выберите запись в каталоге.")
    st.page_link("views/catalog.py", label="Перейти в каталог")
    st.stop()

try:
    response = get_car(item_id)
except requests.RequestException:
    st.error("Не удалось выполнить запрос к backend.")
    st.stop()

if not response.ok:
    st.error(get_error_message(response))
    st.stop()

item = response.json()

st.header(item["title"])

if item.get("image_url"):
    st.image(item["image_url"], width=500)

st.write(item.get("description", ""))
render_favorite_button(item, key_prefix="details")
render_admin_actions(item["id"], key_prefix="details")