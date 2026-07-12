import streamlit as st


with st.container(border=True, horizontal_alignment="center", vertical_alignment="center"):
    st.title("Книжка")
    st.badge("❤️ Избранное", color="red")
    st.image("https://i.pinimg.com/736x/00/ea/10/00ea1065350cf8865afa2d803c9d1614.jpg")
    if st.button("Подробнее"):
        st.switch_page("pages/book1.py")


st.write("Кошка снаружи")
st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRggmpieE5NR7wYmvRst59UvRj3n-yE0ffdXpj7MArKHg&s")
