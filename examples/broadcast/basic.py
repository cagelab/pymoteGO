from pymotego.broadcast import Broadcast
from datetime import datetime, timedelta
from time import sleep
import random

broadcast = Broadcast()

results = ["correct", "incorrect", "timeout"]

for i in range(10):
    start_time = datetime.now() - timedelta(seconds=random.randint(1, 60))

    duration = random.randint(1, 5)
    stop_time = start_time + timedelta(seconds=duration)

    result = random.choice(results)

    correct_rate = 1.0 if result == "correct" else 0.0

    data = {
        "trial_id": i + 1,
        "participant_id": f"P{random.randint(1, 50):03d}",
        "age": random.randint(18, 65),
        "gender": random.choice(["M", "F", "Other"]),
        "group": random.choice(["experimental", "control"]),
        "trial_type": random.choice(["practice", "experimental"]),
        "block_number": random.randint(1, 5),
        "session_id": f"S{random.randint(1, 3):02d}",
        "trial_start_time": start_time.isoformat(),
        "trial_stop_time": stop_time.isoformat(),
        "result": result,
        "correct_rate": correct_rate,
        "stimulus_type": random.choice(["visual", "auditory", "somatosensory"]),
        "stimulus_name": f"stim_{random.randint(1, 10)}",
        "stimulus_duration_ms": random.randint(100, 1000),
        "response_key": random.choice(["A", "B", "C", "D"]),
        "reaction_time_ms": random.randint(200, 1500),
        "confidence": random.randint(1, 10),
        "experimenter_id": "E001",
        "device_id": "DEV001",
        "lab_location": "lab_1",
    }

    future = broadcast.send(data)
    print(future.result())

    sleep(duration)
