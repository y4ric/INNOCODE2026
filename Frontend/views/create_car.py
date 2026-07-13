import requests
import streamlit as st

from api.client import create_car, get_error_message
from auth.state import require_admin


require_admin()
st.header("Новая запись")

with st.form("create_item_form"):
    title = st.text_input("Название")
    short_description = st.text_area("Краткое описание")
    description = st.text_area("Полное описание")
    image_url = st.text_input("Ссылка на изображение")
    submitted = st.form_submit_button("Создать")

if submitted:
    if not title.strip():
        st.error("Укажите название.")
        st.stop()

    payload = {
        "name": title.strip(),
        "short_description": short_description.strip(),
        "full_description": description.strip(),
        "url_picture": image_url.strip() or None,
    }

    try:
        response = create_car(payload)
    except requests.RequestException:
        st.error("Не удалось выполнить запрос к backend.")
        st.stop()

    if response.status_code in (200, 201):
        created_item = response.json()
        st.session_state["selected_item_id"] = created_item["id"]
        st.switch_page("views/details.py")
    else:
        st.error(get_error_message(response))