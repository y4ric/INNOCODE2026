import requests
import streamlit as st

from api.client import (
    add_favorite,
    delete_car,
    get_error_message,
    remove_favorite,
)
from auth.state import is_admin, is_authenticated


def render_favorite_button(item: dict, key_prefix: str) -> None:
    if not is_authenticated():
        st.caption("Войдите, чтобы добавить запись в избранное.")
        return

    car_id = item["car_id"]
    is_favorite = item.get("is_favorite", False)
    button_text = "Убрать из избранного" if is_favorite else "В избранное"

    if st.button(button_text, key=f"{key_prefix}_favorite_{car_id}"):
        try:
            if is_favorite:
                response = remove_favorite(car_id)
            else:
                response = add_favorite(car_id)
        except requests.RequestException:
            st.error("Не удалось выполнить запрос к backend.")
            return

        if response.ok:
            # Если мы только что ДОБАВИЛИ в избранное, запускаем шарики
            if not is_favorite:
                st.balloons()

            st.rerun()
        else:
            st.error(get_error_message(response))


def render_admin_actions(car_id: int, key_prefix: str) -> None:
    if not is_admin():
        return

    edit_column, delete_column = st.columns(2)

    if edit_column.button(
        "Редактировать",
        key=f"{key_prefix}_edit_{car_id}",
    ):
        st.session_state["edit_car_id"] = car_id
        st.switch_page("views/edit_car.py")

    if delete_column.button(
        "Удалить",
        key=f"{key_prefix}_delete_{car_id}",
        type="primary",
    ):
        try:
            response = delete_car(car_id)
        except requests.RequestException:
            st.error("Не удалось выполнить запрос к backend.")
            return

        if response.ok:
            st.success("Запись удалена.")
            st.switch_page("views/catalog.py")
        else:
            st.error(get_error_message(response))


def render_item_cards(item: dict) -> None:
    car_id = item["car_id"]

    with st.container(border=True):

        if item.get("url_picture"):
            try:
                st.image(item["url_picture"], use_container_width=True)
            except Exception:
                st.warning("Не удалось загрузить изображение (некорректная ссылка)")
        else:
            st.info("Изображение не добавлено")

        st.subheader(item["name"])
        st.write(item.get("short_description", ""))

        render_favorite_button(item, key_prefix="card")

        if st.button("Подробнее", key=f"card_details_{car_id}"):
            st.session_state["selected_car_id"] = car_id
            st.switch_page("views/details.py")

        render_admin_actions(car_id, key_prefix="card")