from fastapi import FastAPI
import random
import logging
import threading
import time
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

from . import models, database, crud, schemas
from .routes.sensors import router as sensors_router
from .routes.auth import router as auth_router
from .routes.users import router as users_router
from .routes.admin import router as admin_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

app = FastAPI(title="Smart Heating System Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://ise-smart-heating-system-frontend.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(admin_router)
app.include_router(sensors_router)

# -------------------------------
# Virtual sensor generator
# -------------------------------
_generator_lock = threading.Lock()
_generator_running = True
_generator_interval_sec = 2.0

def set_generator_running(value: bool):
    global _generator_running
    with _generator_lock:
        _generator_running = value

def set_generator_interval(seconds: float):
    global _generator_interval_sec
    with _generator_lock:
        _generator_interval_sec = max(0.2, float(seconds))

def get_generator_state():
    with _generator_lock:
        return _generator_running, _generator_interval_sec

def generate_virtual_data():
    db = database.SessionLocal()
    try:
        while True:
            running, interval = get_generator_state()
            if running:
                temp = random.uniform(15, 30)
                occupancy = random.choice([0, 1])
                timestamp = datetime.utcnow()

                data = schemas.SensorDataCreate(
                    temperature=temp, occupancy=occupancy, timestamp=timestamp
                )
                crud.create_sensor_data(db, data)

                logging.info(
                    f"{timestamp} | Temperature: {temp:.2f} °C | Occupancy: {occupancy}"
                )

            time.sleep(interval)
    finally:
        db.close()

@app.on_event("startup")
def start_virtual_sensors():
    thread = threading.Thread(target=generate_virtual_data, daemon=True)
    thread.start()