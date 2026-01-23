from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.crud.user import create_user, get_user_by_email
from app.schemas.user import UserCreate
from typing import List
from app.schemas.bus_schedule import BusScheduleCreate
from app.crud.bus_schedule import create_bus_schedule, list_bus_schedules

def seed_schedules(db: Session):
    if list_bus_schedules(db):
        print("Bus schedules already exist")
        return

    schedules_a = [
        {"trip_number": 1, "bus_type": "A", "departure_terminal": "07h10", "departure_campus": "07h25"},
        {"trip_number": 3, "bus_type": "A", "departure_terminal": "08h30", "departure_campus": "08h45"},
        {"trip_number": 5, "bus_type": "A", "departure_terminal": "10h00", "departure_campus": "10h15"},
    ]
    
    schedules_b = [
        {"trip_number": 2, "bus_type": "B", "departure_terminal": "07h15", "departure_campus": "07h30"},
        {"trip_number": 4, "bus_type": "B", "departure_terminal": "09h00", "departure_campus": "09h15"},
        {"trip_number": 6, "bus_type": "B", "departure_terminal": "11h00", "departure_campus": "11h15"},
    ]

    for data in schedules_a + schedules_b:
        create_bus_schedule(db, BusScheduleCreate(**data))
    
    print("Bus schedules created")

def seed_db():
    db: Session = SessionLocal()
    try:
        # Create Carla (Admin)
        if not get_user_by_email(db, "carlaevelyn@alu.ufc.br"):
            carla = UserCreate(
                name="Carla Evelyn",
                email="carlaevelyn@alu.ufc.br",
                password="senha123",
                papel="admin",
                curso="Engenharia de Software",
                bio="Estudante da UFC de Quixadá. Apaixonada por tecnologia.",
                avatar_url="https://i.pravatar.cc/150?img=1"
            )
            create_user(db, carla)
            print("Carla created")
        else:
            print("Carla already exists")

        # Create Maria (User)
        if not get_user_by_email(db, "maria.barros@alu.ufc.br"):
            maria = UserCreate(
                name="Maria Barros",
                email="maria.barros@alu.ufc.br",
                password="since2023",
                papel="user",
                curso="Design Digital",
                bio="Designer em formação.",
                avatar_url="https://i.pravatar.cc/150?img=2"
            )
            create_user(db, maria)
            print("Maria created")
        else:
            print("Maria already exists")
            
        seed_schedules(db)
            
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
