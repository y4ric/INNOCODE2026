import streamlit as st
import requests
import random
from api.client import get_cars

st.header("🎮 Мини-игра: Угадай автомобиль")
st.write("Сайт покажет тебе краткое описание машины, а ты должен угадать её название!")

# 1. Загружаем данные с бэкенда FastAPI
try:
    response = get_cars()
    if not response.ok:
        st.error("Не удалось загрузить машины для игры.")
        st.stop()
    cars = response.json()
except requests.RequestException:
    st.error("Backend недоступен.")
    st.stop()

# Если в базе меньше 3 машин, играть не получится (не из чего делать варианты ответов)
if len(cars) < 3:
    st.info("Добавьте хотя бы 3 машины в базу данных, чтобы запустить игру!")
    st.stop()

# 2. Инициализируем состояние игры в st.session_state, чтобы данные не сбрасывались при кликах
if "quiz_car" not in st.session_state:
    st.session_state.quiz_car = None
    st.session_state.quiz_options = []
    st.session_state.game_answered = False


# Функция для генерации нового раунда
def generate_new_round():
    # Загаданная машина
    secret_car = random.choice(cars)

    # Собираем варианты ответов (загаданная + 2 случайные другие)
    other_cars = [c for c in cars if c["car_id"] != secret_car["car_id"]]
    wrong_options = random.sample(other_cars, 2)

    options = [secret_car["name"]] + [c["name"] for c in wrong_options]
    random.shuffle(options)  # перемешиваем, чтобы правильный ответ не был всегда первым

    # Сохраняем в сессию
    st.session_state.quiz_car = secret_car
    st.session_state.quiz_options = options
    st.session_state.game_answered = False


# Если игра только открылась, генерируем первый раунд
if st.session_state.quiz_car is None:
    generate_new_round()

# 3. Отрисовываем интерфейс игры
secret_car = st.session_state.quiz_car
options = st.session_state.quiz_options

# Показываем описание (помним, что картинку и имя скрываем!)
st.info(f"**Загадка:** {secret_car.get('short_description', 'Описание отсутствует')}")

# Форма для ответа
with st.form("quiz_form"):
    st.write("Выберите правильный вариант:")
    user_choice = st.radio("Варианты:", options, label_visibility="collapsed")
    submit = st.form_submit_button("Проверить ответ 🚀")

    if submit:
        st.session_state.game_answered = True
        if user_choice == secret_car["name"]:
            st.success(f"🎉 Абсолютно верно! Это {secret_car['name']}!")
            st.balloons()
        else:
            st.error(f"❌ Неверно. На самом деле это была: **{secret_car['name']}**")

# Кнопка для перехода к следующему вопросу (появляется только после ответа)
if st.session_state.game_answered:
    if st.button("Следующий автомобиль ➡️"):
        generate_new_round()
        st.rerun()
