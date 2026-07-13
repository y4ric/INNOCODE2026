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
    def create(self, car: Cars) -> Cars:
        new_car = Cars(car_id=car.id)
        self.db.add(new_car)
    
