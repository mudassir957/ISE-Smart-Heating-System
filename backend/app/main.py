from fastapi import FastAPI
import random
import logging
import threading
import time
from datetime import datetime

from fastapi.middleware.cors import CORSMiddleware

from . import models, database, crud, schemas
from app.routes.sensors import router as sensors_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

app = FastAPI(title="Smart Heating System Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # adjust if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DB tables (IMPORTANT: uses database.Base now)
models.Base.metadata.create_all(bind=database.engine)

# Register routers
app.include_router(sensors_router)


# -------------------------------
# Virtual sensor generator
# -------------------------------
def generate_virtual_data():
    db = database.SessionLocal()
    try:
        while True:
            temp = random.uniform(15, 30)
            occupancy = random.choice([0, 1])
            timestamp = datetime.utcnow()

            data = schemas.SensorDataCreate(
                temperature=temp,
                occupancy=occupancy,
                timestamp=timestamp,
            )

            crud.create_sensor_data(db, data)

            logging.info(
                f"{timestamp} | Temperature: {temp:.2f} °C | Occupancy: {occupancy}"
            )

            time.sleep(2)
    finally:
        db.close()


@app.on_event("startup")
def start_virtual_sensors():
    thread = threading.Thread(target=generate_virtual_data, daemon=True)
    thread.start()
