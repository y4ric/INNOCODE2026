from app.models.car import Cars


class FavouriteService:

    def __init__(self, repository):
        self.repository = repository

    def add_favourite(self, car_id: int) -> Cars:
        favourite_car = Cars(
            car_id=car_id
        )
        self.repository.add(favourite_car)
        return {"status": "success", "message": "Ваша машина успешно добавлена в избранное"}
