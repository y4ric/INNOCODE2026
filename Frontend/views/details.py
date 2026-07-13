import requests
import streamlit as st

from api.client import get_error_message, get_car
from components.item_card import render_admin_actions, render_favorite_button


car_id = st.session_state.get("selected_car_id")


if not car_id:
    st.warning("Машина не выбрана. Вернитесь в каталог.")
    st.stop()

try:
    response = get_car(car_id)
except requests.RequestException:
    st.error("Не удалось выполнить запрос к backend.")
    st.stop()

if not response.ok:
    st.error(get_error_message(response))
    st.stop()

item = response.json()

st.header(item["name"])

if item.get("url_picture"):
    st.image(item["url_picture"] , width=500)


st.write(item.get("description", ""))
render_favorite_button(item, key_prefix="details")
render_admin_actions(item["car_id"], key_prefix="details")