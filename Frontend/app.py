import streamlit as st
import sys
from pathlib import Path
from auth.state import is_admin

st.set_page_config(
    page_title="CarLibrary",
    page_icon="🏎️",
    layout="wide",
)

# === КОД ДЛЯ ТУМБЛЕРА ТЕМЫ И КНОПКИ "МНЕ ПОВЕЗЁТ!" ===
with st.sidebar:
    st.write("### 🛠 Настройки сайта")
    # Переключатель темы (с уникальным key)
    dark_mode = st.toggle("🌙 Темная тема сайта", key="main_theme_toggle")

    st.write("---")  # Визуальная линия-разделитель в меню

    # Кнопка "Мне повезёт!" (с уникальным key)
    if st.button("🎲 Мне повезёт!", use_container_width=True, key="sidebar_lucky_btn"):
        try:
            import random
            from api.client import get_cars

            response = get_cars()
            if response.ok:
                all_cars = response.json()
                if all_cars:
                    # Выбираем случайную машину из списка
                    random_car = random.choice(all_cars)

                    # Записываем её ID в сессию
                    st.session_state["selected_car_id"] = random_car["car_id"]

                    # Мгновенно переключаем пользователя на страницу "Подробнее"
                    st.switch_page("views/details.py")
                else:
                    st.sidebar.error("В базе пока нет машин.")
            else:
                st.sidebar.error("Ошибка при получении машин.")
        except Exception:
            st.sidebar.error("Бэкенд недоступен.")

# Определяем цвета в зависимости от положения тумблера
if dark_mode:
    bg_color = "#121212"  # Тёмный фон сайта
    card_bg = "#1e1e1e"  # Тёмный фон карточек
    text_color = "#ffffff"  # Белый текст карточек
    border_color = "#333333"  # Тёмные рамки
    sidebar_bg = "#1a1a1a"  # Тёмный фон сайдбара
    sidebar_text = "#e0e0e0"  # Светлый текст в сайдбаре
    button_bg = "#2d2d2d"  # Тёмный фон кнопок в карточках
    button_border = "#444444"  # Рамка кнопок
else:
    bg_color = "#f8f9fa"  # Светлый фон сайта
    card_bg = "#ffffff"  # Белый фон карточек
    text_color = "#000000"  # Чёрный текст карточек
    border_color = "#e0e0e0"  # Светлые рамки
    sidebar_bg = "#f0f2f6"  # Стандартный светлый сайдбар Streamlit
    sidebar_text = "#31333F"  # Стандартный тёмный текст Streamlit
    button_bg = "#ffffff"  # Светлый фон кнопок
    button_border = "#d3d3d3"  # Светлая рамка кнопок

st.markdown(f"""
    <style>
    /* Меняем фон главной страницы */
    .stApp {{
        background-color: {bg_color} !important;
    }}

    /* Красим панель навигации (сайдбар) */
    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
    }}

    /* Красим весь текст, ссылки и заголовки внутри сайдбара */
    section[data-testid="stSidebar"] *, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] label {{
        color: {sidebar_text} !important;
    }}

    /* Красим заголовки и тексты ТОЛЬКО внутри колонок-карточек */
    div[data-testid="stColumn"] h1, 
    div[data-testid="stColumn"] h2, 
    div[data-testid="stColumn"] h3, 
    div[data-testid="stColumn"] p, 
    div[data-testid="stColumn"] span, 
    div[data-testid="stColumn"] label,
    div[data-testid="stColumn"] div {{
        color: {text_color} !important;
    }}

    /* Стилизуем сами контейнеры карточек */
    div[data-testid="stColumn"] {{
        background-color: {card_bg} !important;
        border: 1px solid {border_color} !important;
        padding: 15px;
        border-radius: 10px;
    }}

    /* СТИЛИЗАЦИЯ КНОПОК: Возвращаем видимость тексту на кнопках */
    div[data-testid="stColumn"] button {{
        background-color: {button_bg} !important;
        border: 1px solid {button_border} !important;
        color: {text_color} !important;
        transition: background-color 0.2s ease, transform 0.1s ease;
    }}

    /* Эффект при наведении на кнопку для красоты */
    div[data-testid="stColumn"] button:hover {{
        background-color: #ff4b4b !important;
        color: #ffffff !important;
        border-color: #ff4b4b !important;
    }}
    </style>
""", unsafe_allow_html=True)

# ============================================

views = {
    "Каталог": [
        st.Page(
            "views/catalog.py",
            title="Каталог",
            icon=":material/store:",
            url_path="catalog",
            default=True,
        ),
        st.Page(
            "views/details.py",
            title="Подробнее",
            icon=":material/article:",
            url_path="details",
        ),
    ],
    "Пользователь": [
        st.Page(
            "views/favorites.py",
            title="Избранное",
            icon=":material/favorite:",
            url_path="favorites",
        ),
        st.Page(
            "views/profile.py",
            title="Профиль",
            icon=":material/person:",
            url_path="profile",
        ),
        # === ДОБАВИЛ СЮДА ДЛЯ ОБЫЧНЫХ ПОЛЬЗОВАТЕЛЕЙ (ИГРА ДОЛЖНА БЫТЬ ДОСТУПНА ВСЕМ) ===
        st.Page(
            "views/quiz.py",
            title="Мини-игра: Угадай авто",
            icon=":material/sports_esports:",
            url_path="quiz",
        ),
    ],
    "Авторизация": [
        st.Page(
            "views/login.py",
            title="Вход",
            icon=":material/login:",
            url_path="login",
        ),
        st.Page(
            "views/registration.py",
            title="Регистрация",
            icon=":material/person_add:",
            url_path="registration",
        ),
    ],
}

if is_admin():
    views["Администратор"] = [
        st.Page(
            "views/create_car.py",
            title="Создать запись",
            icon=":material/add:",
            url_path="create-item",
        ),
        st.Page(
            "views/edit_car.py",
            title="Редактировать запись",
            icon=":material/edit:",
            url_path="edit-item",
        ),
    ]

nav = st.navigation(views, expanded=True, position="sidebar")
nav.run()
