import requests
import streamlit as st

from api.client import get_error_message, get_car, update_car
from auth.state import require_admin

from views.create_car import full_description

require_admin()
st.header("Редактирование записи")

car_id = st.session_state.get("edit_car_id")

if car_id is None:
    st.info("Сначала выберите запись для редактирования.")
    st.stop()

try:
    item_response = get_car(car_id)
except requests.RequestException:
    st.error("Не удалось получить запись с backend.")
    st.stop()

if not item_response.ok:
    st.error(get_error_message(item_response))
    st.stop()

item = item_response.json()
st.toast('Данные успешно загружены!', icon='🎉')  # Всплывающее уведомление в углу

with st.form(f"edit_item_form_{car_id}"):
    name = st.text_input("Название", value=item["name"])
    short_description = st.text_area(
        "Краткое описание",
        value=item.get("short_description", ""),
    )
    full_description = st.text_area(
        "Полное описание",
        value=item.get("full_description", ""),
    )
    url_picture = st.text_input(
        "Ссылка на изображение",
        value=item.get("url_picture") or "",
    )
    submitted = st.form_submit_button("Сохранить")

if submitted:
    if not name.strip():
        st.error("Укажите название.")
        st.stop()

    payload = {
        "name": name.strip(),
        "short_description": short_description.strip(),
        "full_description": full_description.strip(),
        "url_picture": url_picture.strip() or None,
    }

    try:
        response = update_car(car_id, payload)
    except requests.RequestException:
        st.error("Не удалось выполнить запрос к backend.")
        st.stop()

    if response.ok:
        st.session_state["selected_car_id"] = car_id
        st.switch_page("views/details.py")
    else:
        st.error(get_error_message(response))