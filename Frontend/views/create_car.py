import requests
import streamlit as st

from api.client import create_car, get_error_message
from auth.state import require_admin


require_admin()
st.header("Новая запись")

with st.form("create_item_form"):
    name = st.text_input("Название")
    short_description = st.text_area("Краткое описание")
    full_description = st.text_area("Полное описание")
    url_picture = st.text_input("Ссылка на изображение")
    submitted = st.form_submit_button("Создать")

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
        response = create_car(payload)
    except requests.RequestException:
        st.error("Не удалось выполнить запрос к backend.")
        st.stop()

    if response.status_code in (200, 201):
        created_car = response.json()
        st.session_state["selected_car_id"] = created_car["car_id"]
        st.switch_page("views/details.py")
    else:
        st.error(get_error_message(response))