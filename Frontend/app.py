import streamlit as st

from auth.state import is_admin


st.set_page_config(
    page_title="Каталог",
    page_icon="📚",
    layout="wide",
)

views = {
    "Каталог": [
        st.Page(
            "Frontend/views/catalog.py",
            title="Каталог",
            icon=":material/store:",
            url_path="catalog",
            default=True,
        ),
        st.Page(
            "Frontend/views/details.py",
            title="Подробнее",
            icon=":material/article:",
            url_path="details",
        ),
    ],
    "Пользователь": [
        st.Page(
            "Frontend/views/favorites.py",
            title="Избранное",
            icon=":material/favorite:",
            url_path="favorites",
        ),
        st.Page(
            "Frontend/views/profile.py",
            title="Профиль",
            icon=":material/person:",
            url_path="profile",
        ),
    ],
    "Авторизация": [
        st.Page(
            "Frontend/views/login.py",
            title="Вход",
            icon=":material/login:",
            url_path="login",
        ),
        st.Page(
            "Frontend/views/registration.py",
            title="Регистрация",
            icon=":material/person_add:",
            url_path="registration",
        ),
    ],
}

if is_admin():
    pages["Администратор"] = [
        st.Page(
            "Frontend/views/create_car.py",
            title="Создать запись",
            icon=":material/add:",
            url_path="create-item",
        ),
        st.Page(
            "Frontend/views/edit_car.py",
            title="Редактировать запись",
            icon=":material/edit:",
            url_path="edit-item",
        ),
    ]

navigation = st.navigation(pages)
navigation.run()