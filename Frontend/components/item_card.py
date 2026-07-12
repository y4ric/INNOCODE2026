import requests
import streamlit as st

from api.client import (
    add_favorite,
    delete_item,
    get_error_message,
    remove_favorite,
)
from Frontend.auth.state import is_admin, is_authenticated


def render_favorite_button(item: dict, key_prefix: str) -> None:
    if not is_authenticated():
        st.caption("Войдите, чтобы добавить запись в избранное.")
        return

    item_id = item["id"]
    is_favorite = item.get("is_favorite", False)
    button_text = "Убрать из избранного" if is_favorite else "В избранное"

    if st.button(button_text, key=f"{key_prefix}_favorite_{item_id}"):
        try:
            if is_favorite:
                response = remove_favorite(item_id)
            else:
                response = add_favorite(item_id)
        except requests.RequestException:
            st.error("Не удалось выполнить запрос к backend.")
            return

        if response.ok:
            st.rerun()
        else:
            st.error(get_error_message(response))


def render_admin_actions(item_id: int, key_prefix: str) -> None:
    if not is_admin():
        return

    edit_column, delete_column = st.columns(2)

    if edit_column.button(
        "Редактировать",
        key=f"{key_prefix}_edit_{item_id}",
    ):
        st.session_state["edit_item_id"] = item_id
        st.switch_page("pages/edit_item.py")

    if delete_column.button(
        "Удалить",
        key=f"{key_prefix}_delete_{item_id}",
        type="primary",
    ):
        try:
            response = delete_item(item_id)
        except requests.RequestException:
            st.error("Не удалось выполнить запрос к backend.")
            return

        if response.ok:
            st.success("Запись удалена.")
            st.switch_page("pages/catalog.py")
        else:
            st.error(get_error_message(response))


def render_item_card(item: dict) -> None:
    item_id = item["id"]

    with st.container(border=True):
        if item.get("image_url"):
            st.image(item["image_url"], use_container_width=True)
        else:
            st.info("Изображение не добавлено")

        st.subheader(item["title"])
        st.write(item.get("short_description", ""))

        render_favorite_button(item, key_prefix="card")

        if st.button("Подробнее", key=f"card_details_{item_id}"):
            st.session_state["selected_item_id"] = item_id
            st.switch_page("pages/details.py")

        render_admin_actions(item_id, key_prefix="card")