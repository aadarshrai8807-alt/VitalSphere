# seed.py
from db import init_db, get_session
import crud
from models import Ward, WardMetric
import random, time

init_db()

# Create sample wards if none exist
wards = crud.list_wards()
if len(wards) == 0:
    demo_coords = [
        ("Ward 1", 28.7041, 77.1025),
        ("Ward 2", 28.7100, 77.1200),
        ("Ward 3", 28.6900, 77.0900),
        ("Ward 4", 28.7000, 77.1300),
        ("Ward 5", 28.7300, 77.1100)
    ]
    for name, lat, lon in demo_coords:
        w = crud.create_ward(name, lat, lon)
        # create a few metric snapshots
        for _ in range(1):
            aqi = random.randint(40,230)
            green = random.randint(5,60)
            temp = random.uniform(24,40)
            hosp = random.randint(0,150)
            reports_count = random.randint(0,50)
            crud.add_metric(w.id, aqi, green, temp, hosp, reports_count)

# Create some reports
for i in range(20):
    ward_id = random.randint(1,5)
    cat = random.choice(["air","waste","water","green"])
    desc = f"Sample {cat} issue #{i}"
    crud.add_report(ward_id, cat, desc, reporter=f"user{i}")

print("Seed completed.")