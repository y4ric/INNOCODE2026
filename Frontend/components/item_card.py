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

    # Жестко проверяем: если префикс равен "favorite",
    # значит, карточка принудительно отрисовывается на странице Избранного!
    is_favorite = item.get("is_favorite", False) or key_prefix == "favorite"
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
            # Шарики полетят, только если мы нажимали кнопку добавления
            if button_text == "В избранное":
                st.balloons()
                import time
                time.sleep(1.5)
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


# 1. ИСПРАВЛЕНО: добавили аргумент key_prefix со значением по умолчанию "card"
# 1. ИСПРАВЛЕНО: добавили аргумент key_prefix со значением по умолчанию "card"
def render_item_cards(item: dict, key_prefix: str = "card") -> None:
    car_id = item["car_id"]

    with st.container(border=True):

        if item.get("url_picture"):
            try:
                st.image(item["url_picture"], use_container_width=True)
            except Exception:
                st.warning("Не удалось загрузить изображение (некорректная ссылка)")
        else:
            st.info("Изображение не добавлено")

        # === ВСТАВЛЯЕМ СЧЁТЧИКИ ПРОСМОТРОВ И ЛАЙКОВ В КАТАЛОГ ===
        views = item.get("views_count", 0)
        favs = item.get("favorites_count", 0)

        st.markdown(
            f"""
            <div style="display: flex; gap: 15px; margin-top: 5px; margin-bottom: 5px; font-size: 0.9rem; opacity: 0.8;">
                <span>👁️ {views} просмотров</span>
                <span>❤️ {favs} в избранном</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        # =======================================================

        # 1. Фиксированная высота для заголовка (ровно 60 пикселей, под 2 строки)
        st.markdown(
            f"<div style='height: 60px; overflow: hidden;'><h3 style='margin:0; padding:0; font-size:1.3rem; font-weight:600;'>{item['name']}</h3></div>",
            unsafe_allow_html=True
        )

        # 2. Фиксированная высота для краткого описания (ровно 75 пикселей, под 3 строки)
        desc_text = item.get("short_description", "")
        st.markdown(
            f"<div style='height: 75px; overflow: hidden; font-size:0.95rem; color:#31333F; line-height:1.4;'>{desc_text}</div>",
            unsafe_allow_html=True
        )

 

        # 2. ИСПРАВЛЕНО: передаем переменную key_prefix вместо "card"
        render_favorite_button(item, key_prefix=key_prefix)

        if st.button("Подробнее", key=f"card_details_{car_id}"):
            st.session_state["selected_car_id"] = car_id
            st.switch_page("views/details.py")

        # 3. ИСПРАВЛЕНО: передаем переменную key_prefix вместо "card"
        render_admin_actions(car_id, key_prefix=key_prefix)
