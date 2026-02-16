from pymotego.broadcast import Broadcast
from datetime import datetime, timedelta
from time import sleep
import random

broadcast = Broadcast()

results = ["correct", "incorrect", "timeout"]
stimulus_types = ["visual", "auditory", "somatosensory"]
participant_groups = ["experimental", "control"]

for i in range(10):
    start_time = datetime.now() - timedelta(seconds=random.randint(1, 60))

    duration = random.randint(1, 5)
    stop_time = start_time + timedelta(seconds=duration)

    result = random.choice(results)

    data = {
        "trial_id": i + 1,
        "participant": {
            "id": f"P{random.randint(100, 999):03d}",
            "age": random.randint(18, 65),
            "group": random.choice(participant_groups),
        },
        "trial_info": {
            "start_time": start_time.isoformat(),
            "stop_time": stop_time.isoformat(),
            "result": result,
            "correct_rate": 1.0 if result == "correct" else 0.0,
        },
        "conditions": {
            "stimulus": {
                "type": random.choice(stimulus_types),
                "intensity": random.randint(50, 100),
                "duration_ms": random.randint(100, 1000),
            },
            "timing": {
                "iti_ms": random.randint(500, 3000),
                "delay_ms": random.randint(100, 500),
                "inter_stimulus_interval_ms": random.randint(200, 1500),
            },
        },
        "measurements": [
            {
                "channel": "EEG",
                "sampling_rate_hz": 500,
                "values": [round(random.uniform(-50, 50), 2) for _ in range(10)],
            },
            {
                "channel": "EMG",
                "sampling_rate_hz": 1000,
                "values": [round(random.uniform(0, 10), 2) for _ in range(5)],
            },
            {
                "channel": "EyeTracking",
                "sampling_rate_hz": 120,
                "values": {
                    "x": [round(random.uniform(0, 1920), 1) for _ in range(8)],
                    "y": [round(random.uniform(0, 1080), 1) for _ in range(8)],
                    "pupil_size": [round(random.uniform(2, 8), 2) for _ in range(8)],
                },
            },
        ],
    }

    future = broadcast.send(data)
    print(f"Sent trial {i + 1}: {future.result()}")

    sleep(duration)
