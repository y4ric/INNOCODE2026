from app.models.car import Favorites


class FavouriteService:

    def __init__(self, repository):
        self.repository = repository

    # Убедитесь, что вверху файла есть импорт вашей модели избранного, например:
    # from app.models.favourite import Favourite

    def add_favourite(self, schema, user_id):
        # Создаем запись для таблицы избранного, а не саму машину!
        favourite_record = Favorites(  # <-- Используйте вашу модель избранного
            car_id=schema.car_id,
            user_id=user_id
        )

        self.repository.add(favourite_record)
        self.repository.commit()

        return {"status": "success", "message": "Машина успешно добавлена в избранное"}

    def get_favourites(self, user_id: int):

        from app.models.car import Cars

        from app.models.car import Favorites

        records = self.repository.query(Cars).join(
            Favorites, Cars.car_id == Favorites.car_id
        ).filter(Favorites.user_id == user_id).all()

        return records
