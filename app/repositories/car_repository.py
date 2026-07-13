from sqlalchemy.orm import Session
from app.models.car import Cars


class CarRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Cars]:
        return self.db.query(Cars).all()

    def get_by_id(
        self,
        car_id: int,
    ) -> Cars | None:

        return (
            self.db.query(Cars).filter(Cars.car_id == car_id).first()
        )

    def create(self, car) -> Cars:
        new_car = Cars(
            name=car.name,
            short_description=car.short_description,
            full_description=car.full_description,
            url_picture=car.url_picture
        )

        self.db.add(new_car)
        self.db.commit()
        self.db.refresh(new_car)
        return new_car



