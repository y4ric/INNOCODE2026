import requests
import streamlit as st

from api.client import get_error_message, get_cars
from auth.state import is_admin
from components.item_card import render_item_cards



st.header("Каталог")

if is_admin():
    if st.button("Создать запись"):
        st.switch_page("views/create_car.py")

try:
    response = get_cars()
except requests.RequestException:
    st.error("Backend недоступен. Проверьте запуск FastAPI.")
    st.stop()

if not response.ok:
    st.error(get_error_message(response))
    st.stop()

items = response.json()

if not items:
    st.info("В каталоге пока нет записей.")
    st.stop()

columns = st.columns(3)

for index, item in enumerate(items):
    with columns[index % 3]:
        render_item_cards(item)