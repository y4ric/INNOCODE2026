import requests
import streamlit as st

from api.client import get_error_message, get_car
from components.item_card import render_admin_actions, render_favorite_button

car_id = st.session_state.get("selected_car_id")

if not car_id:
    st.warning("Машина не выбрана. Вернитесь в каталог.")
    st.stop()

try:
    response = get_car(car_id)
except requests.RequestException:
    st.error("Не удалось выполнить запрос к backend.")
    st.stop()

if not response.ok:
    st.error(get_error_message(response))
    st.stop()

item = response.json()

st.header(item["name"])

# === БЛОК СТАТИСТИКИ АВТОМОБИЛЯ ===
col_stat1, col_stat2, _ = st.columns([1, 1, 2]) # создаем колонки для красивых метрик
with col_stat1:
    st.metric(label="Просмотры", value=f"👁️ {item.get('views_count', 0)}")
with col_stat2:
    st.metric(label="В избранном", value=f"❤️ {item.get('favorites_count', 0)}")
st.write("") # Небольшой отступ для красоты
# ==================================

if item.get("url_picture"):
    st.image(item["url_picture"], width=500)

st.write(item.get("full_description", ""))

# === ПАСХАЛКА ДЛЯ ЖИГУЛЕЙ (ID 21) ===
if item.get("car_id") == 21:
    st.write("---")  # Отделяем симулятор визуальной чертой
    st.write("### 🛠 Симулятор запуска")

    import random

    # Списки возможных неудачных исходов (состояний)
    warnings = [
        "⚠️ Вжжж-вжжж... Аккумулятор знатно подсел, стартер еле крутит. Попробуй ещё раз.",
        "⚠️ Слышен глухой стук в районе бензонасоса. Кажется, надо подкачать вручную.",
        "⚠️ Чихает, кашляет, но не подхватывает. Похоже, бензин в баке на донышке.",
        "⚠️ Зажигание схватило на полсекунды и тут же заглохло. Недотянул подсос!"
    ]

    errors = [
        "🛑 Пых-пых... Кажется, залило свечи. Нужно выкручивать, сушить или стучать по карбюратору.",
        "🛑 Полная тишина. Похоже, отошёл минусовой провод на массу. Пошевели клемму под капотом.",
        "🛑 Из-под капота раздался странный щелчок, и пошёл лёгкий дымок. Главное, чтобы не проводка!",
        "🛑 Ключ повернулся, но стартер даже не щёлкнул. Михалыч говорит, втягивающее реле умерло."
    ]

    # Сделали ключ кнопки уникальным, добавив ID машины
    if st.button("🔑 Повернуть ключ зажигания (стартер)", key=f"start_zhiga_btn_{item['car_id']}"):
        # Задаем шанс успешного запуска на каждый клик (20%)
        is_lucky = random.random() < 0.20

        if is_lucky:
            st.success("🎉 Ура! Завелась! Из трубы повалил плотный сизый дым, по кузову пошла дикая вибрация. Можно ехать на заварку!")
            st.balloons()
        else:
            # Случайно выбираем, показать предупреждение (желтое) или ошибку (красную)
            if random.choice([True, False]):
                st.warning(random.choice(warnings))
            else:
                st.error(random.choice(errors))

    st.write("---")
# ====================================

render_favorite_button(item, key_prefix="details")
render_admin_actions(item["car_id"], key_prefix="details")
