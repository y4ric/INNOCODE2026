from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.car import Cars
from app.repositories.car_repository import CarRepository
from app.schemas.car import CarCreate


class CarService:
    def __init__(self, db: Session):
        self.repository = CarRepository(db)

    def create_car(self, schema: CarCreate) -> Cars:
        new_car = Cars(
            name = schema.name,
            short_description = schema.short_description,
            full_description = schema.full_description,
            url_picture = schema.url_picture,
        )
        return self.repository.create(new_car)

    def get_cars(self) -> list[Cars]:
        return self.repository.get_all()

    def get_car(self, car_id: int) -> Cars:
        car = self.repository.get_by_id(car_id)

        if car is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Car not found",
            )
        car.views_count += 1

        # Делаем коммит. Если в твоем сервисе сессия называется self.db:
        self.repository.db.commit()
        return car

    def update_car(self, car_id: int, schema):
        car = self.repository.get_by_id(car_id)
        if not car:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Машина не найдена")

        # Обновляем поля модели новыми значениями из схемы фронтенда
        car.name = schema.name
        car.short_description = schema.short_description
        car.full_description = schema.full_description
        car.url_picture = schema.url_picture

        # Сохраняем изменения в базу данных
        self.repository.db.commit()
        return {"status": "success", "message": "Данные автомобиля успешно обновлены"}


